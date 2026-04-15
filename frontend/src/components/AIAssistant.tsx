import React, { useState, useRef, useEffect } from 'react';
import Container from '@cloudscape-design/components/container';
import Header from '@cloudscape-design/components/header';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Box from '@cloudscape-design/components/box';
import Button from '@cloudscape-design/components/button';
import Textarea from '@cloudscape-design/components/textarea';
import Spinner from '@cloudscape-design/components/spinner';
import Alert from '@cloudscape-design/components/alert';
import { complianceApi } from '../services/complianceApi';
import { useEngagement, FRAMEWORK_LABELS } from '../contexts/EngagementContext';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const QUICK_PROMPTS = [
  'Generate a calendar invite agenda for Meeting 1',
  'Create a facilitation guide for the next meeting',
  'What evidence should I request before Meeting 3?',
  'Draft a pre-meeting document review summary',
  'What are the key risk areas for this engagement?',
  'Generate the full engagement schedule as a customer-facing document',
];

const AIAssistant: React.FC = () => {
  const { activeEngagement, scheduleMeetings, evidenceItems } = useEngagement();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text?: string) => {
    const msg = text || input.trim();
    if (!msg || loading) return;

    const userMsg: ChatMessage = { role: 'user', content: msg, timestamp: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const context: Record<string, unknown> = {};
      if (activeEngagement) {
        context.config = activeEngagement.config;
        context.schedule = scheduleMeetings;
        context.evidence = evidenceItems;
      }
      const result = await complianceApi.aiChat(msg, context);
      const assistantMsg: ChatMessage = { role: 'assistant', content: result.response, timestamp: new Date() };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (e: unknown) {
      const errorMsg = e instanceof Error ? e.message : 'Unknown error';
      const errMsg: ChatMessage = { role: 'assistant', content: `Error: ${errorMsg}. Make sure the Lambda has Bedrock permissions.`, timestamp: new Date() };
      setMessages(prev => [...prev, errMsg]);
    }
    setLoading(false);
  };

  const copyMessage = (idx: number, content: string) => {
    navigator.clipboard.writeText(content);
    setCopied(idx);
    setTimeout(() => setCopied(null), 2000);
  };

  const engLabel = activeEngagement
    ? `${activeEngagement.config.customerName} — ${FRAMEWORK_LABELS[activeEngagement.config.framework]}`
    : 'No engagement selected';

  return (
    <SpaceBetween size="l">
      <Container header={
        <Header variant="h2" description={engLabel}>
          🤖 AI Engagement Assistant
        </Header>
      }>
        <Box variant="small" color="text-body-secondary">
          Powered by Amazon Bedrock (Claude). Ask me to generate calendar agendas, facilitation guides, evidence requests, or engagement advice. I have context about your active engagement, schedule, and evidence status.
        </Box>
      </Container>

      {/* Quick prompts */}
      {messages.length === 0 && (
        <Container header={<Header variant="h3">Quick actions</Header>}>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {QUICK_PROMPTS.map((prompt, idx) => (
              <Button key={idx} onClick={() => sendMessage(prompt)} variant="normal">
                {prompt}
              </Button>
            ))}
          </div>
        </Container>
      )}

      {/* Chat messages */}
      {messages.length > 0 && (
        <div style={{ maxHeight: '500px', overflowY: 'auto', padding: '4px' }}>
          <SpaceBetween size="m">
            {messages.map((msg, idx) => (
              <div key={idx} style={{
                padding: '12px 16px',
                borderRadius: '12px',
                background: msg.role === 'user' ? '#0972d3' : '#f2f3f3',
                color: msg.role === 'user' ? '#fff' : '#16191f',
                marginLeft: msg.role === 'user' ? '60px' : '0',
                marginRight: msg.role === 'assistant' ? '60px' : '0',
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <Box variant="small" color={msg.role === 'user' ? 'inherit' : 'text-body-secondary'}>
                    {msg.role === 'user' ? 'You' : '🤖 AI Assistant'}
                  </Box>
                  {msg.role === 'assistant' && (
                    <Button variant="icon" iconName={copied === idx ? 'check' : 'copy'}
                      onClick={() => copyMessage(idx, msg.content)} />
                  )}
                </div>
                <div style={{ whiteSpace: 'pre-wrap', marginTop: '4px', fontSize: '14px', lineHeight: '1.5' }}>
                  {msg.content}
                </div>
              </div>
            ))}
            {loading && (
              <div style={{ padding: '12px', background: '#f2f3f3', borderRadius: '12px', marginRight: '60px' }}>
                <Spinner /> Thinking...
              </div>
            )}
            <div ref={messagesEndRef} />
          </SpaceBetween>
        </div>
      )}

      {/* Input */}
      <Container>
        <div style={{ display: 'flex', gap: '8px' }}>
          <div style={{ flex: 1 }}>
            <Textarea
              value={input}
              onChange={({ detail }) => setInput(detail.value)}
              placeholder="Ask me to generate a calendar agenda, facilitation guide, or anything else..."
              rows={2}
              onKeyDown={(e: any) => { if (e.detail.key === 'Enter' && !e.detail.shiftKey) { e.preventDefault(); sendMessage(); } }}
            />
          </div>
          <Button variant="primary" onClick={() => sendMessage()} loading={loading} disabled={!input.trim()}>
            Send
          </Button>
        </div>
      </Container>

      <Alert type="info">
        AWS SAS Advisory Notice: AI-generated content is advisory guidance only. All outputs require professional review before use in customer deliverables. Do not input customer PII, production configurations, or credentials.
      </Alert>
    </SpaceBetween>
  );
};

export default AIAssistant;
