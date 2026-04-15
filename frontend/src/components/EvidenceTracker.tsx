import React, { useState } from 'react';
import Container from '@cloudscape-design/components/container';
import Header from '@cloudscape-design/components/header';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Table from '@cloudscape-design/components/table';
import Select from '@cloudscape-design/components/select';
import Badge from '@cloudscape-design/components/badge';
import Button from '@cloudscape-design/components/button';
import Box from '@cloudscape-design/components/box';
import Input from '@cloudscape-design/components/input';
import { useEngagement, FRAMEWORK_LABELS } from '../contexts/EngagementContext';

interface EvidenceItem {
  id: string;
  meeting: string;
  artifact: string;
  controlMapping: string;
  status: string;
  notes: string;
}

const STATUS_OPTIONS = [
  { label: 'NEW REQUEST', value: 'NEW REQUEST' },
  { label: 'RECEIVED / CONFIRM', value: 'RECEIVED / CONFIRM' },
  { label: 'PARTIALLY ADDRESSED', value: 'PARTIALLY ADDRESSED' },
  { label: 'RECEIVED', value: 'RECEIVED' },
  { label: 'FUNDAMENTALLY RECHARACTERIZED', value: 'FUNDAMENTALLY RECHARACTERIZED' },
  { label: 'NOT APPLICABLE', value: 'NOT APPLICABLE' },
];

// Sample evidence items organized by meeting — these would come from the API in production
const SAMPLE_EVIDENCE: Record<string, EvidenceItem[]> = {
  'nist-csf': [
    { id: '1-1', meeting: 'Meeting 1', artifact: 'Enterprise Risk Management (ERM) framework or policy', controlMapping: 'GV.RM-01', status: 'NEW REQUEST', notes: 'Confirm how RCSA is documented and structured' },
    { id: '1-2', meeting: 'Meeting 1', artifact: 'Cybersecurity risk appetite and tolerance statement', controlMapping: 'GV.RM-02', status: 'NEW REQUEST', notes: 'Confirm cloud-specific risk thresholds' },
    { id: '1-3', meeting: 'Meeting 1', artifact: 'Third-party / vendor risk management policy', controlMapping: 'GV.SC-01', status: 'NEW REQUEST', notes: 'Confirm fourth-party breach notification requirements' },
    { id: '1-4', meeting: 'Meeting 1', artifact: 'Vendor inventory or supplier register', controlMapping: 'GV.SC-04', status: 'NEW REQUEST', notes: 'Confirm AWS and ProServe are included' },
    { id: '2-1', meeting: 'Meeting 2', artifact: 'Information Security Policy (board-approved)', controlMapping: 'GV.PO-01', status: 'NEW REQUEST', notes: 'Request formal signed/approved document' },
    { id: '2-2', meeting: 'Meeting 2', artifact: 'Organizational chart showing cybersecurity roles', controlMapping: 'GV.RR-01', status: 'NEW REQUEST', notes: 'Confirm ISO and Steering Committee structure' },
    { id: '2-3', meeting: 'Meeting 2', artifact: 'Cybersecurity roles and responsibilities matrix (RACI)', controlMapping: 'GV.RR-02', status: 'NEW REQUEST', notes: 'Confirm cloud-specific roles are defined' },
    { id: '3-1', meeting: 'Meeting 3', artifact: 'ITSM CMDB export showing AWS assets', controlMapping: 'ID.AM-01', status: 'NEW REQUEST', notes: 'Request current AWS-scoped extract' },
    { id: '3-2', meeting: 'Meeting 3', artifact: 'AWS account inventory (account IDs, regions)', controlMapping: 'ID.AM-01', status: 'NEW REQUEST', notes: 'AWS Organizations structure' },
    { id: '3-3', meeting: 'Meeting 3', artifact: 'Network architecture diagram (AWS topology)', controlMapping: 'ID.AM-03', status: 'NEW REQUEST', notes: 'ProServe-produced or bank-maintained' },
    { id: '4-1', meeting: 'Meeting 4', artifact: 'Vulnerability management policy and procedure', controlMapping: 'ID.RA-01', status: 'NEW REQUEST', notes: 'Confirm SLAs are formally documented' },
    { id: '4-2', meeting: 'Meeting 4', artifact: 'Most recent vulnerability scan results (AWS)', controlMapping: 'ID.RA-01', status: 'NEW REQUEST', notes: 'Request most recent AWS-scoped scan report' },
    { id: '4-3', meeting: 'Meeting 4', artifact: 'AppSec / Secure SDLC roadmap', controlMapping: 'ID.IM-01', status: 'NEW REQUEST', notes: 'Key gap area — request current state and target dates' },
    { id: '5-1', meeting: 'Meeting 5', artifact: 'AWS IAM policy documentation', controlMapping: 'PR.AA-01', status: 'NEW REQUEST', notes: 'Confirm least privilege enforcement' },
    { id: '5-2', meeting: 'Meeting 5', artifact: 'MFA enforcement evidence in AWS', controlMapping: 'PR.AA-03', status: 'NEW REQUEST', notes: 'IAM policy or AWS Config rule evidence' },
    { id: '5-3', meeting: 'Meeting 5', artifact: 'Encryption policy (at rest and in transit)', controlMapping: 'PR.DS-01', status: 'NEW REQUEST', notes: 'Confirm AES-256 and TLS 1.2+' },
    { id: '6-1', meeting: 'Meeting 6', artifact: 'AWS Config rules and conformance pack documentation', controlMapping: 'PR.PS-01', status: 'NEW REQUEST', notes: 'Confirm configuration compliance monitoring' },
    { id: '6-2', meeting: 'Meeting 6', artifact: 'Landing zone guardrails and SCPs', controlMapping: 'PR.PS-01', status: 'NEW REQUEST', notes: 'ProServe-produced or bank-maintained' },
    { id: '7-1', meeting: 'Meeting 7', artifact: 'AWS GuardDuty configuration and findings review', controlMapping: 'DE.CM-09', status: 'NEW REQUEST', notes: 'Confirm GuardDuty enabled across all accounts' },
    { id: '7-2', meeting: 'Meeting 7', artifact: 'Incident declaration criteria and escalation thresholds', controlMapping: 'DE.AE-08', status: 'NEW REQUEST', notes: 'Confirm formal criteria are documented' },
    { id: '8-1', meeting: 'Meeting 8', artifact: 'Incident response plan (current version)', controlMapping: 'RS.MA-01', status: 'NEW REQUEST', notes: 'Confirm AWS-specific procedures included' },
    { id: '8-2', meeting: 'Meeting 8', artifact: 'Incident containment playbooks (AWS-specific)', controlMapping: 'RS.MI-01', status: 'NEW REQUEST', notes: 'EC2 isolation, IAM revocation, S3 lockdown' },
    { id: '8-3', meeting: 'Meeting 8', artifact: 'RTO and RPO documentation (critical systems)', controlMapping: 'RC.RP-01', status: 'NEW REQUEST', notes: 'Confirm replication targets are formally documented' },
  ],
};

const EvidenceTracker: React.FC = () => {
  const { activeEngagement } = useEngagement();
  const framework = activeEngagement!.config.framework;
  const [items, setItems] = useState<EvidenceItem[]>(SAMPLE_EVIDENCE['nist-csf'] || []);
  const [copied, setCopied] = useState(false);

  // Load evidence for the active engagement's framework
  React.useEffect(() => {
    setItems(SAMPLE_EVIDENCE[framework] || SAMPLE_EVIDENCE['nist-csf'] || []);
  }, [framework]);

  const updateStatus = (id: string, newStatus: string) => {
    setItems(prev => prev.map(item => item.id === id ? { ...item, status: newStatus } : item));
  };

  const updateNotes = (id: string, newNotes: string) => {
    setItems(prev => prev.map(item => item.id === id ? { ...item, notes: newNotes } : item));
  };

  const stats = {
    total: items.length,
    received: items.filter(i => i.status === 'RECEIVED' || i.status === 'FUNDAMENTALLY RECHARACTERIZED').length,
    partial: items.filter(i => i.status === 'PARTIALLY ADDRESSED' || i.status === 'RECEIVED / CONFIRM').length,
    outstanding: items.filter(i => i.status === 'NEW REQUEST').length,
  };

  const copyReport = () => {
    let report = `Evidence Request Tracker\n${'='.repeat(40)}\n\n`;
    report += `Framework: ${framework}\n`;
    report += `Total: ${stats.total} | Received: ${stats.received} | Partial: ${stats.partial} | Outstanding: ${stats.outstanding}\n\n`;
    const meetings = [...new Set(items.map(i => i.meeting))];
    meetings.forEach(mtg => {
      report += `--- ${mtg} ---\n`;
      items.filter(i => i.meeting === mtg).forEach((item, idx) => {
        report += `${idx + 1}. ${item.artifact}\n`;
        report += `   Control: ${item.controlMapping} | Status: ${item.status}\n`;
        if (item.notes) report += `   Notes: ${item.notes}\n`;
        report += `\n`;
      });
    });
    navigator.clipboard.writeText(report);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <SpaceBetween size="l">
      <Container header={
        <Header variant="h2" description={`${activeEngagement!.config.customerName} — ${FRAMEWORK_LABELS[framework]} — Track evidence artifacts across your engagement`}
          actions={<Button iconName={copied ? 'check' : 'copy'} onClick={copyReport}>{copied ? 'Copied' : 'Copy tracker'}</Button>}
        >
          Evidence Request Tracker
        </Header>
      }>
        <SpaceBetween size="s" direction="horizontal">
          <div style={{ textAlign: 'center', padding: '8px 16px', background: '#f2f3f3', borderRadius: '8px' }}>
            <Box variant="h1" fontSize="display-l">{stats.total}</Box>
            <Box variant="small">Total</Box>
          </div>
          <div style={{ textAlign: 'center', padding: '8px 16px', background: '#f2fcf3', borderRadius: '8px' }}>
            <Box variant="h1" fontSize="display-l" color="text-status-success">{stats.received}</Box>
            <Box variant="small">Received</Box>
          </div>
          <div style={{ textAlign: 'center', padding: '8px 16px', background: '#fef6f0', borderRadius: '8px' }}>
            <Box variant="h1" fontSize="display-l" color="text-status-warning">{stats.partial}</Box>
            <Box variant="small">Partial</Box>
          </div>
          <div style={{ textAlign: 'center', padding: '8px 16px', background: '#fdf3f1', borderRadius: '8px' }}>
            <Box variant="h1" fontSize="display-l" color="text-status-error">{stats.outstanding}</Box>
            <Box variant="small">Outstanding</Box>
          </div>
        </SpaceBetween>
      </Container>

      <Table
        columnDefinitions={[
          { id: 'meeting', header: 'Meeting', cell: (item: EvidenceItem) => <Badge color="blue">{item.meeting}</Badge>, width: 110 },
          { id: 'artifact', header: 'Artifact', cell: (item: EvidenceItem) => <Box variant="strong">{item.artifact}</Box> },
          { id: 'control', header: 'Control', cell: (item: EvidenceItem) => <Box variant="code" fontSize="body-s">{item.controlMapping}</Box>, width: 100 },
          { id: 'status', header: 'Status', cell: (item: EvidenceItem) => {
            return (
              <Select
                selectedOption={{ label: item.status, value: item.status }}
                onChange={({ detail }) => updateStatus(item.id, detail.selectedOption.value || item.status)}
                options={STATUS_OPTIONS}
                expandToViewport
              />
            );
          }, width: 220 },
          { id: 'notes', header: 'Notes', cell: (item: EvidenceItem) => (
            <Input value={item.notes} onChange={({ detail }) => updateNotes(item.id, detail.value)} placeholder="Add notes..." />
          )},
        ]}
        items={items}
        variant="embedded"
        header={<Header variant="h3">Evidence artifacts by meeting</Header>}
      />
    </SpaceBetween>
  );
};

export default EvidenceTracker;
