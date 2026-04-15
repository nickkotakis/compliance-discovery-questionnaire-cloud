import React, { useState, useEffect } from 'react';
import Container from '@cloudscape-design/components/container';
import Header from '@cloudscape-design/components/header';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Box from '@cloudscape-design/components/box';
import Button from '@cloudscape-design/components/button';
import Badge from '@cloudscape-design/components/badge';
import ExpandableSection from '@cloudscape-design/components/expandable-section';
import ColumnLayout from '@cloudscape-design/components/column-layout';
import Select from '@cloudscape-design/components/select';
import Alert from '@cloudscape-design/components/alert';
import FormField from '@cloudscape-design/components/form-field';
import { complianceApi, Control, Question } from '../services/complianceApi';
import { useEngagement, FRAMEWORK_LABELS } from '../contexts/EngagementContext';

interface ControlGuideData {
  control: Control;
  questions: Question[];
}

const FacilitationGuide: React.FC = () => {
  const { activeEngagement, scheduleMeetings, evidenceItems } = useEngagement();
  const framework = activeEngagement!.config.framework;
  const customerName = activeEngagement!.config.customerName;

  const [selectedMeetingId, setSelectedMeetingId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [guideData, setGuideData] = useState<ControlGuideData[]>([]);
  const [copied, setCopied] = useState(false);

  const selectedMeeting = scheduleMeetings.find(m => m.id === selectedMeetingId);

  // Get evidence statuses for controls in this meeting
  const getEvidenceForControl = (controlId: string) => {
    return evidenceItems.filter(e =>
      e.controlMapping.toUpperCase() === controlId.toUpperCase() ||
      e.controlMapping.toUpperCase().startsWith(controlId.toUpperCase())
    );
  };

  const receivedEvidence = evidenceItems.filter(e =>
    e.status === 'RECEIVED' || e.status === 'RECEIVED / CONFIRM' || e.status === 'FUNDAMENTALLY RECHARACTERIZED'
  );
  const outstandingEvidence = evidenceItems.filter(e =>
    e.status === 'NEW REQUEST' || e.status === 'PARTIALLY ADDRESSED'
  );

  // When meeting is selected, extract control IDs and fetch data
  useEffect(() => {
    if (!selectedMeeting) { setGuideData([]); return; }
    const loadControls = async () => {
      setLoading(true);
      // Parse control IDs from the meeting's controls string
      const controlStr = selectedMeeting.controls;
      // Controls are comma/semicolon separated, may be ranges like "GV.RM-01, GV.RM-02"
      const ids = controlStr.split(/[;,]/).map(s => s.trim()).filter(Boolean);
      const data: ControlGuideData[] = [];
      for (const id of ids) {
        try {
          const detail = await complianceApi.getControl(id, framework);
          if (detail) data.push({ control: detail.control, questions: detail.questions });
        } catch (e) { /* skip controls that don't resolve */ }
      }
      setGuideData(data);
      setLoading(false);
    };
    loadControls();
  }, [selectedMeetingId]);

  const generateReport = () => {
    if (!selectedMeeting) return '';
    const mtgLabel = `Meeting ${scheduleMeetings.indexOf(selectedMeeting) + 1}`;
    let r = `${mtgLabel} Facilitator Question Guide\n`;
    r += `${selectedMeeting.topic}\n`;
    r += `${customerName} | ${FRAMEWORK_LABELS[framework]} Advisory\n`;
    r += `${selectedMeeting.duration} min | ProServe: ${selectedMeeting.proserve}\n\n`;
    r += `AWS SAS ADVISORY NOTICE: This guide is advisory guidance only.\n\n`;
    r += `${'='.repeat(50)}\nPRE-MEETING CHECKLIST\n${'='.repeat(50)}\n`;
    r += `[ ] Evidence received and reviewed\n[ ] Attendees confirmed\n[ ] Prior meeting notes reviewed\n[ ] CPR documentation templates prepared\n\n`;

    // Evidence status
    const mtgEvidence = evidenceItems.filter(e => e.meeting === mtgLabel || e.meeting === `Meeting ${scheduleMeetings.indexOf(selectedMeeting) + 1}`);
    if (mtgEvidence.length > 0) {
      r += `${'='.repeat(50)}\nEVIDENCE STATUS\n${'='.repeat(50)}\n`;
      mtgEvidence.forEach(e => { r += `[${e.status}] ${e.artifact}\n  Notes: ${e.notes}\n\n`; });
    }

    r += `${'='.repeat(50)}\nDOCUMENT REVIEW SUMMARY\n${'='.repeat(50)}\n`;
    r += `STRENGTHS:\n- [Document observations]\n\nAREAS REQUIRING VALIDATION:\n- [Document observations]\n\nGAPS IDENTIFIED:\n- [Document observations]\n\n`;

    guideData.forEach(({ control, questions }) => {
      r += `${'='.repeat(50)}\n${control.id.toUpperCase()}: ${control.title}\n${'='.repeat(50)}\n`;
      r += `${control.description}\n\n`;
      const implQs = questions.filter(q => q.question_type === 'implementation');
      const evidenceQs = questions.filter(q => q.question_type === 'evidence');
      if (implQs.length > 0) {
        r += `OPENING QUESTION:\n"${implQs[0].question_text}"\n\n`;
        if (implQs.length > 1) { r += `FOLLOW-UP QUESTIONS:\n`; implQs.slice(1).forEach((q, i) => { r += `${i + 1}. "${q.question_text}"\n`; }); r += `\n`; }
      }
      r += `WHAT TO LISTEN FOR:\n- Specific AWS services mentioned\n- Documented procedures (not ad hoc)\n- AWS environment coverage\n- Defined ownership and review cadence\n\n`;
      r += `RED FLAGS:\n- Control on paper but not implemented\n- AWS not covered\n- No ownership or review cadence\n- Manual-only without automation\n\n`;
      if (evidenceQs.length > 0) r += `EVIDENCE REQUEST:\n${evidenceQs[0].question_text}\n\n`;
      r += `CPR NOTES:\nOwner: [Record]\nStatus: [IN PLACE / PARTIAL / NOT IN PLACE]\n`;
      r += `[IF IN PLACE]: "${control.id} established with [evidence]."\n`;
      r += `[IF PARTIAL]: "${control.id} exists but [gap]."\n`;
      r += `[IF NOT IN PLACE]: "Gap: [statement]. Recommend: (1)...; (2)...; (3)..."\n\n`;
    });
    r += `${'='.repeat(50)}\nWRAP-UP\n${'='.repeat(50)}\n`;
    r += `1. "Any concerns not discussed?"\n2. "Additional artifacts to provide?"\n3. "Next meeting preview"\n`;
    return r;
  };

  const copyReport = () => { navigator.clipboard.writeText(generateReport()); setCopied(true); setTimeout(() => setCopied(false), 2000); };

  const meetingOptions = scheduleMeetings.map((m, idx) => ({
    label: `Meeting ${idx + 1} — ${m.topic}`,
    value: m.id,
    description: `${m.functions} | ${m.duration} min`,
  }));

  return (
    <SpaceBetween size="l">
      <Container header={<Header variant="h2" description={`${customerName} — ${FRAMEWORK_LABELS[framework]}`}>Facilitation Guide Generator</Header>}>
        <SpaceBetween size="m">
          {scheduleMeetings.length === 0 ? (
            <Alert type="warning">No schedule generated yet. Go to Engagement Schedule to generate a schedule first.</Alert>
          ) : (
            <FormField label="Select meeting" description="Controls and evidence will be loaded automatically from the schedule and evidence tracker">
              <Select
                selectedOption={selectedMeetingId ? meetingOptions.find(o => o.value === selectedMeetingId) || null : null}
                onChange={({ detail }) => setSelectedMeetingId(detail.selectedOption.value || null)}
                options={meetingOptions}
                placeholder="Choose a meeting..."
              />
            </FormField>
          )}
          {selectedMeeting && guideData.length > 0 && (
            <Button iconName={copied ? 'check' : 'copy'} onClick={copyReport}>{copied ? 'Copied' : 'Copy full guide'}</Button>
          )}
        </SpaceBetween>
      </Container>

      {loading && <Alert type="info">Loading control data...</Alert>}

      {selectedMeeting && !loading && guideData.length > 0 && (
        <>
          <Alert type="info">AWS SAS Advisory Notice: This guide is advisory guidance only. Legal counsel should be consulted for regulatory interpretation.</Alert>

          <Container header={<Header variant="h3">Pre-Meeting Checklist</Header>}>
            <SpaceBetween size="xs">
              <Box>☐ Evidence received and reviewed</Box>
              <Box>☐ Attendees confirmed: {selectedMeeting.attendees.join(', ')}</Box>
              <Box>☐ Prior meeting notes reviewed</Box>
              <Box>☐ CPR documentation templates prepared</Box>
            </SpaceBetween>
          </Container>

          {/* Evidence status from tracker */}
          {evidenceItems.length > 0 && (
            <Container header={<Header variant="h3">Evidence Status (from Evidence Tracker)</Header>}>
              <ColumnLayout columns={2}>
                <div style={{ borderLeft: '4px solid #037f0c', paddingLeft: '12px' }}>
                  <Box variant="awsui-key-label">Received ({receivedEvidence.length})</Box>
                  <SpaceBetween size="xxs">
                    {receivedEvidence.slice(0, 5).map(e => (
                      <Box key={e.id} variant="small">✅ {e.artifact}</Box>
                    ))}
                    {receivedEvidence.length > 5 && <Box variant="small" color="text-body-secondary">...and {receivedEvidence.length - 5} more</Box>}
                  </SpaceBetween>
                </div>
                <div style={{ borderLeft: '4px solid #d13212', paddingLeft: '12px' }}>
                  <Box variant="awsui-key-label">Outstanding ({outstandingEvidence.length})</Box>
                  <SpaceBetween size="xxs">
                    {outstandingEvidence.slice(0, 5).map(e => (
                      <Box key={e.id} variant="small">⚠️ {e.artifact} — {e.status}</Box>
                    ))}
                    {outstandingEvidence.length > 5 && <Box variant="small" color="text-body-secondary">...and {outstandingEvidence.length - 5} more</Box>}
                  </SpaceBetween>
                </div>
              </ColumnLayout>
            </Container>
          )}

          <Container header={<Header variant="h3">Pre-Meeting Document Review Summary</Header>}>
            <ColumnLayout columns={3}>
              <div style={{ borderLeft: '4px solid #037f0c', paddingLeft: '12px' }}>
                <Box variant="awsui-key-label">Strengths</Box>
                <Box variant="small" color="text-body-secondary">What is working well</Box>
              </div>
              <div style={{ borderLeft: '4px solid #d45b07', paddingLeft: '12px' }}>
                <Box variant="awsui-key-label">Areas requiring validation</Box>
                <Box variant="small" color="text-body-secondary">What needs probing</Box>
              </div>
              <div style={{ borderLeft: '4px solid #d13212', paddingLeft: '12px' }}>
                <Box variant="awsui-key-label">Gaps identified</Box>
                <Box variant="small" color="text-body-secondary">What is missing</Box>
              </div>
            </ColumnLayout>
          </Container>

          {guideData.map(({ control, questions }) => {
            const implQs = questions.filter(q => q.question_type === 'implementation');
            const evidenceQs = questions.filter(q => q.question_type === 'evidence');
            const controlEvidence = getEvidenceForControl(control.id);
            return (
              <ExpandableSection key={control.id} variant="container"
                headerText={`${control.id.toUpperCase()}: ${control.title}`}
                defaultExpanded
              >
                <SpaceBetween size="m">
                  <Box variant="small" color="text-body-secondary">{control.description}</Box>

                  {controlEvidence.length > 0 && (
                    <div style={{ background: '#f2f8fd', padding: '8px 12px', borderRadius: '6px' }}>
                      <Box variant="awsui-key-label">Evidence status for this control</Box>
                      {controlEvidence.map(e => (
                        <Box key={e.id} variant="small">
                          <Badge color={e.status === 'RECEIVED' || e.status === 'FUNDAMENTALLY RECHARACTERIZED' ? 'green' : e.status === 'NEW REQUEST' ? 'grey' : 'blue'}>{e.status}</Badge>
                          {' '}{e.artifact}{e.notes ? ` — ${e.notes}` : ''}
                        </Box>
                      ))}
                    </div>
                  )}

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
                        {implQs.slice(1).map((q, i) => <Box key={i} variant="small">{i + 1}. "{q.question_text}"</Box>)}
                      </SpaceBetween>
                    </div>
                  )}
                  <ColumnLayout columns={2}>
                    <div style={{ borderLeft: '4px solid #037f0c', paddingLeft: '12px' }}>
                      <Box variant="awsui-key-label">What to listen for</Box>
                      <SpaceBetween size="xxs">
                        <Box variant="small">• Specific AWS services and configurations</Box>
                        <Box variant="small">• Documented procedures (not ad hoc)</Box>
                        <Box variant="small">• AWS environment coverage</Box>
                        <Box variant="small">• Defined ownership and review cadence</Box>
                      </SpaceBetween>
                    </div>
                    <div style={{ borderLeft: '4px solid #d13212', paddingLeft: '12px' }}>
                      <Box variant="awsui-key-label">Red flags</Box>
                      <SpaceBetween size="xxs">
                        <Box variant="small">• Control on paper but not implemented</Box>
                        <Box variant="small">• AWS not explicitly covered</Box>
                        <Box variant="small">• No ownership or review cadence</Box>
                        <Box variant="small">• Manual-only without automation</Box>
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
                      <Box variant="small" color="text-status-success">[IF IN PLACE]: "{control.id} established with [evidence]. AWS confirmed via [services]."</Box>
                      <Box variant="small" color="text-status-info">[IF PARTIAL]: "{control.id} exists but [gap]. AWS implementation [describe]."</Box>
                      <Box variant="small" color="text-status-error">[IF NOT IN PLACE]: "Gap: [statement]. Recommend: (1)...; (2)...; (3)..."</Box>
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

      {selectedMeeting && !loading && guideData.length === 0 && (
        <Alert type="warning">No control data could be loaded for this meeting's controls. The controls listed in the schedule may use range notation (e.g., "GV.RM-01 through GV.RM-07") which requires individual control IDs to resolve.</Alert>
      )}
    </SpaceBetween>
  );
};

export default FacilitationGuide;
