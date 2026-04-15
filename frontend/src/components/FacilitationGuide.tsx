import React, { useState } from 'react';
import Container from '@cloudscape-design/components/container';
import Header from '@cloudscape-design/components/header';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Box from '@cloudscape-design/components/box';
import Button from '@cloudscape-design/components/button';
import Badge from '@cloudscape-design/components/badge';
import ExpandableSection from '@cloudscape-design/components/expandable-section';
import ColumnLayout from '@cloudscape-design/components/column-layout';
import Input from '@cloudscape-design/components/input';
import Alert from '@cloudscape-design/components/alert';
import { complianceApi, Control, Question } from '../services/complianceApi';
import { useEngagement, FRAMEWORK_LABELS } from '../contexts/EngagementContext';

interface ControlGuideData {
  control: Control;
  questions: Question[];
}

const FacilitationGuide: React.FC = () => {
  const { activeEngagement } = useEngagement();
  const framework = activeEngagement!.config.framework;
  const customerName = activeEngagement!.config.customerName;
  const [meetingName, setMeetingName] = useState('');
  const [controlIds, setControlIds] = useState('');
  const [loading, setLoading] = useState(false);
  const [guideData, setGuideData] = useState<ControlGuideData[]>([]);
  const [copied, setCopied] = useState(false);
  const [generated, setGenerated] = useState(false);

  const generateGuide = async () => {
    setLoading(true);
    const ids = controlIds.split(',').map(id => id.trim()).filter(Boolean);
    const data: ControlGuideData[] = [];
    for (const id of ids) {
      try {
        const detail = await complianceApi.getControl(id, framework);
        if (detail) {
          data.push({
            control: detail.control,
            questions: detail.questions,
          });
        }
      } catch (e) {
        console.warn(`Could not load control ${id}`, e);
      }
    }
    setGuideData(data);
    setGenerated(true);
    setLoading(false);
  };

  const generateReport = () => {
    let report = `${meetingName || 'Meeting'} Facilitator Question Guide\n`;
    report += `${customerName || '[Customer Name]'} | ${framework === 'nist-csf' ? 'NIST CSF 2.0' : framework === 'nist-800-53' ? 'NIST 800-53 Rev 5' : 'CMMC Level 2'} Advisory\n\n`;
    report += `AWS SAS ADVISORY NOTICE: This guide is provided as advisory guidance only. This does not constitute a formal audit, assessment, or compliance certification. Legal counsel should be consulted for regulatory interpretation.\n\n`;
    report += `${'='.repeat(60)}\nPRE-MEETING CHECKLIST\n${'='.repeat(60)}\n\n`;
    report += `[ ] Evidence received and reviewed\n[ ] Attendees confirmed\n[ ] Prior meeting notes reviewed\n[ ] CPR documentation templates prepared\n\n`;
    report += `${'='.repeat(60)}\nPRE-MEETING DOCUMENT REVIEW SUMMARY\n${'='.repeat(60)}\n\n`;
    report += `STRENGTHS (what is working well):\n- [Document observations here]\n\n`;
    report += `AREAS REQUIRING VALIDATION (what needs probing):\n- [Document observations here]\n\n`;
    report += `GAPS IDENTIFIED (what is missing):\n- [Document observations here]\n\n`;

    guideData.forEach(({ control, questions }) => {
      report += `${'='.repeat(60)}\n${control.id.toUpperCase()}: ${control.title}\n${'='.repeat(60)}\n\n`;
      report += `Control Description: ${control.description}\n\n`;

      const implQs = questions.filter(q => q.question_type === 'implementation');
      const evidenceQs = questions.filter(q => q.question_type === 'evidence');

      if (implQs.length > 0) {
        report += `OPENING QUESTION:\n"${implQs[0].question_text}"\n\n`;
        if (implQs.length > 1) {
          report += `FOLLOW-UP QUESTIONS:\n`;
          implQs.slice(1).forEach((q, i) => { report += `${i + 1}. "${q.question_text}"\n`; });
          report += `\n`;
        }
      }

      report += `WHAT TO LISTEN FOR:\n`;
      report += `- Specific AWS services and configurations mentioned\n`;
      report += `- Evidence of documented procedures (not just ad hoc practices)\n`;
      report += `- Coverage of AWS environment (not just on-premises)\n`;
      report += `- Defined ownership and review cadence\n\n`;

      report += `RED FLAGS:\n`;
      report += `- Control exists on paper but not implemented\n`;
      report += `- AWS environment not explicitly covered\n`;
      report += `- No defined ownership or review cadence\n`;
      report += `- Reliance on manual processes without automation\n\n`;

      if (evidenceQs.length > 0) {
        report += `EVIDENCE REQUEST:\n${evidenceQs[0].question_text}\n\n`;
      }

      report += `CPR DOCUMENTATION NOTES:\n`;
      report += `Control Owner: [Record from response]\n`;
      report += `Status: [IN PLACE / PARTIAL / NOT IN PLACE]\n\n`;
      report += `[IF IN PLACE]: "${control.id} is established with [specific evidence]. AWS implementation confirmed via [services/configurations]."\n\n`;
      report += `[IF PARTIAL]: "${control.id} exists at framework level but [specific gap]. AWS-specific implementation [describe gap]."\n\n`;
      report += `[IF NOT IN PLACE]: "Gap: [specific gap statement]. Recommend: (1) [recommendation 1]; (2) [recommendation 2]; (3) [recommendation 3]."\n\n`;
    });

    report += `${'='.repeat(60)}\nWRAP-UP & NEXT STEPS\n${'='.repeat(60)}\n\n`;
    report += `1. "Are there any concerns we haven't discussed today?"\n`;
    report += `2. "Are there additional artifacts you can provide before we finalize observations?"\n`;
    report += `3. "For the next meeting, we'll need [preview next meeting topics]. Any areas to flag in advance?"\n`;
    return report;
  };

  const copyReport = () => {
    navigator.clipboard.writeText(generateReport());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <SpaceBetween size="l">
      <Container header={
        <Header variant="h2" description={`${customerName} — ${FRAMEWORK_LABELS[framework]} — Generate structured interview guides`}>
          Facilitation Guide Generator
        </Header>
      }>
        <SpaceBetween size="m">
          <ColumnLayout columns={2}>
            <FormField label="Meeting name">
              <Input value={meetingName} onChange={({ detail }) => setMeetingName(detail.value)} placeholder="e.g., Meeting 4 — Risk Assessment" />
            </FormField>
            <FormField label="Control IDs (comma-separated)" description={`Enter ${FRAMEWORK_LABELS[framework]} control IDs`}>
              <Input value={controlIds} onChange={({ detail }) => setControlIds(detail.value)} placeholder="e.g., GV.RM-01, GV.RM-02, GV.SC-01" />
            </FormField>
          </ColumnLayout>
          <SpaceBetween size="xs" direction="horizontal">
            <Button variant="primary" onClick={generateGuide} loading={loading}>Generate guide</Button>
            {generated && <Button iconName={copied ? 'check' : 'copy'} onClick={copyReport}>{copied ? 'Copied' : 'Copy full guide'}</Button>}
          </SpaceBetween>
        </SpaceBetween>
      </Container>

      {generated && guideData.length > 0 && (
        <>
          <Alert type="info">
            AWS SAS Advisory Notice: This guide is provided as advisory guidance only. Legal counsel should be consulted for regulatory interpretation.
          </Alert>

          <Container header={<Header variant="h3">Pre-Meeting Checklist</Header>}>
            <SpaceBetween size="xs">
              <Box>☐ Evidence received and reviewed</Box>
              <Box>☐ Attendees confirmed</Box>
              <Box>☐ Prior meeting notes reviewed</Box>
              <Box>☐ CPR documentation templates prepared</Box>
            </SpaceBetween>
          </Container>

          <Container header={<Header variant="h3">Pre-Meeting Document Review Summary</Header>}>
            <ColumnLayout columns={3}>
              <div style={{ borderLeft: '4px solid #037f0c', paddingLeft: '12px' }}>
                <Box variant="awsui-key-label">Strengths</Box>
                <Box variant="small" color="text-body-secondary">What is working well — document observations here</Box>
              </div>
              <div style={{ borderLeft: '4px solid #d45b07', paddingLeft: '12px' }}>
                <Box variant="awsui-key-label">Areas requiring validation</Box>
                <Box variant="small" color="text-body-secondary">What needs probing during the interview</Box>
              </div>
              <div style={{ borderLeft: '4px solid #d13212', paddingLeft: '12px' }}>
                <Box variant="awsui-key-label">Gaps identified</Box>
                <Box variant="small" color="text-body-secondary">What is missing or not yet addressed</Box>
              </div>
            </ColumnLayout>
          </Container>

          {guideData.map(({ control, questions }) => {
            const implQs = questions.filter(q => q.question_type === 'implementation');
            const evidenceQs = questions.filter(q => q.question_type === 'evidence');
            return (
              <ExpandableSection key={control.id} variant="container"
                headerText={`${control.id.toUpperCase()}: ${control.title}`}
                defaultExpanded
              >
                <SpaceBetween size="m">
                  <Box variant="small" color="text-body-secondary">{control.description}</Box>

                  {implQs.length > 0 && (
                    <div style={{ borderLeft: '4px solid #0972d3', paddingLeft: '12px' }}>
                      <Box variant="awsui-key-label">Opening question</Box>
                      <Box>"{implQs[0].question_text}"</Box>
                    </div>
                  )}

                  {implQs.length > 1 && (
                    <div>
                      <Box variant="awsui-key-label">Follow-up questions</Box>
                      <SpaceBetween size="xxs">
                        {implQs.slice(1).map((q, i) => (
                          <Box key={i} variant="small">{i + 1}. "{q.question_text}"</Box>
                        ))}
                      </SpaceBetween>
                    </div>
                  )}

                  <ColumnLayout columns={2}>
                    <div style={{ borderLeft: '4px solid #037f0c', paddingLeft: '12px' }}>
                      <Box variant="awsui-key-label">What to listen for</Box>
                      <SpaceBetween size="xxs">
                        <Box variant="small">• Specific AWS services and configurations mentioned</Box>
                        <Box variant="small">• Evidence of documented procedures</Box>
                        <Box variant="small">• Coverage of AWS environment (not just on-prem)</Box>
                        <Box variant="small">• Defined ownership and review cadence</Box>
                      </SpaceBetween>
                    </div>
                    <div style={{ borderLeft: '4px solid #d13212', paddingLeft: '12px' }}>
                      <Box variant="awsui-key-label">Red flags</Box>
                      <SpaceBetween size="xxs">
                        <Box variant="small">• Control exists on paper but not implemented</Box>
                        <Box variant="small">• AWS environment not explicitly covered</Box>
                        <Box variant="small">• No defined ownership or review cadence</Box>
                        <Box variant="small">• Reliance on manual processes without automation</Box>
                      </SpaceBetween>
                    </div>
                  </ColumnLayout>

                  {evidenceQs.length > 0 && (
                    <div style={{ borderLeft: '4px solid #d97706', paddingLeft: '12px' }}>
                      <Box variant="awsui-key-label">Evidence request</Box>
                      <Box variant="small">{evidenceQs[0].question_text}</Box>
                    </div>
                  )}

                  <div style={{ background: '#fafafa', padding: '12px', borderRadius: '8px' }}>
                    <Box variant="awsui-key-label">CPR documentation notes</Box>
                    <SpaceBetween size="xs">
                      <Box variant="small">Control Owner: [Record from response]</Box>
                      <Box variant="small">Status: <Badge color="green">IN PLACE</Badge> / <Badge color="blue">PARTIAL</Badge> / <Badge color="red">NOT IN PLACE</Badge></Box>
                      <Box variant="small" color="text-status-success">[IF IN PLACE]: "{control.id} is established with [specific evidence]. AWS implementation confirmed via [services/configurations]."</Box>
                      <Box variant="small" color="text-status-info">[IF PARTIAL]: "{control.id} exists at framework level but [specific gap]. AWS-specific implementation [describe gap]."</Box>
                      <Box variant="small" color="text-status-error">[IF NOT IN PLACE]: "Gap: [specific gap statement]. Recommend: (1) [rec 1]; (2) [rec 2]; (3) [rec 3]."</Box>
                    </SpaceBetween>
                  </div>
                </SpaceBetween>
              </ExpandableSection>
            );
          })}

          <Container header={<Header variant="h3">Wrap-Up & Next Steps</Header>}>
            <SpaceBetween size="xs">
              <Box>1. "Are there any concerns we haven't discussed today?"</Box>
              <Box>2. "Are there additional artifacts you can provide before we finalize observations?"</Box>
              <Box>3. "For the next meeting, we'll need [preview topics]. Any areas to flag in advance?"</Box>
            </SpaceBetween>
          </Container>
        </>
      )}
    </SpaceBetween>
  );
};

// Need FormField import
import FormField from '@cloudscape-design/components/form-field';

export default FacilitationGuide;
