"""AI Assistant for SAS Engagement PM using Amazon Bedrock (Claude).

Provides a conversational interface for consultants to generate
calendar agendas, facilitation guides, and get engagement advice.
"""

import json
import boto3
import os

# Use Claude 3.5 Haiku for speed and cost
MODEL_ID = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'
REGION = os.environ.get('AWS_REGION', 'us-east-1')

SYSTEM_PROMPT = """You are an AI assistant for AWS Security Assurance Services (AWS SAS) compliance engagement project management. You help SAS consultants manage their customer engagements by generating professional artifacts.

Your capabilities:
1. Generate natural-language calendar invite agendas for stakeholder interview meetings
2. Generate facilitation guides with opening questions, follow-ups, red flags, and CPR templates
3. Provide engagement management advice
4. Help draft pre-meeting document review summaries
5. Generate evidence request lists

Key principles:
- All outputs are ADVISORY ONLY — never provide legal advice
- Use professional, customer-facing language suitable for calendar invites and meeting agendas
- Reference specific NIST CSF 2.0, NIST 800-53, or CMMC control IDs where relevant
- Include priming questions that help the customer prepare for the discussion
- Follow the AWS Shared Responsibility Model — note inherited controls
- Keep calendar agendas concise but informative — they should be paste-ready for Outlook/Google Calendar
- For facilitation guides, include: opening questions, follow-up probes, what to listen for, red flags, and CPR documentation templates

When generating calendar agendas:
- Use this format for each agenda item:
  [Topic Title] — [Control IDs]:
  [Natural language description with 1-2 priming questions]
- Group related controls together under descriptive topic titles
- Include time allocations
- End with "Wrap-up & Action Items"

When generating facilitation guides:
- Include pre-meeting checklist
- Include document review summary template (Strengths / Areas Requiring Validation / Gaps)
- For each control: opening question, follow-ups, what to listen for, red flags, CPR notes
- Include wrap-up and next steps

AWS SAS Advisory Notice: All outputs are advisory guidance only. This does not constitute a formal audit, assessment, or compliance certification. Legal counsel should be consulted for regulatory interpretation."""


def invoke_assistant(user_message: str, engagement_context: dict) -> str:
    """Invoke the Bedrock AI assistant with engagement context.

    Args:
        user_message: The consultant's message/request
        engagement_context: Dict with engagement config, schedule, evidence status

    Returns:
        AI assistant response text
    """
    try:
        client = boto3.client('bedrock-runtime', region_name=REGION)
    except Exception as e:
        return f"Error connecting to Bedrock: {str(e)}"

    # Build context from engagement data
    context_parts = []
    if engagement_context.get('config'):
        cfg = engagement_context['config']
        context_parts.append(f"Active Engagement: {cfg.get('customerName', 'Unknown')} | Framework: {cfg.get('framework', 'Unknown')} | Scope: {cfg.get('scope', 'Unknown')} | Duration: {cfg.get('engagementWeeks', '?')} weeks | Meeting frequency: {cfg.get('meetingFrequency', 'weekly')} | Max meeting duration: {cfg.get('maxMeetingDuration', 75)} min")

    if engagement_context.get('schedule'):
        schedule = engagement_context['schedule']
        context_parts.append(f"Generated Schedule: {len(schedule)} meetings")
        for i, mtg in enumerate(schedule):
            context_parts.append(f"  Meeting {i+1}: {mtg.get('topic', '')} | Controls: {mtg.get('controls', '')} | {mtg.get('duration', '')} min | ProServe: {mtg.get('proserve', 'No')}")

    if engagement_context.get('evidence'):
        evidence = engagement_context['evidence']
        received = len([e for e in evidence if e.get('status') in ('RECEIVED', 'RECEIVED / CONFIRM', 'FUNDAMENTALLY RECHARACTERIZED')])
        outstanding = len([e for e in evidence if e.get('status') in ('NEW REQUEST', 'PARTIALLY ADDRESSED')])
        context_parts.append(f"Evidence Status: {received} received, {outstanding} outstanding out of {len(evidence)} total")

    context_str = "\n".join(context_parts) if context_parts else "No active engagement context."

    messages = [
        {
            "role": "user",
            "content": f"[ENGAGEMENT CONTEXT]\n{context_str}\n\n[CONSULTANT REQUEST]\n{user_message}"
        }
    ]

    try:
        response = client.invoke_model(
            modelId=MODEL_ID,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "system": SYSTEM_PROMPT,
                "messages": messages,
            })
        )
        result = json.loads(response['body'].read())
        return result.get('content', [{}])[0].get('text', 'No response generated.')
    except Exception as e:
        return f"Error invoking Bedrock: {str(e)}"
