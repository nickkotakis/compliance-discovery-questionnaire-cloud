import React, { useState } from 'react';
import Container from '@cloudscape-design/components/container';
import Header from '@cloudscape-design/components/header';
import SpaceBetween from '@cloudscape-design/components/space-between';
import FormField from '@cloudscape-design/components/form-field';
import Input from '@cloudscape-design/components/input';
import Select from '@cloudscape-design/components/select';
import Button from '@cloudscape-design/components/button';
import Box from '@cloudscape-design/components/box';
import Badge from '@cloudscape-design/components/badge';
import Table from '@cloudscape-design/components/table';
import ColumnLayout from '@cloudscape-design/components/column-layout';
import Alert from '@cloudscape-design/components/alert';
import ExpandableSection from '@cloudscape-design/components/expandable-section';

interface Meeting {
  id: string;
  topic: string;
  functions: string;
  controls: string;
  duration: string;
  proserve: string;
  attendees: string[];
  agendaItems: string[];
}

interface EngagementConfig {
  customerName: string;
  framework: string;
  scope: string;
  regulator: string;
  startDate: string;
  cadence: string;
}

const FRAMEWORK_MEETINGS: Record<string, Meeting[]> = {
  'nist-csf': [
    {
      id: 'kickoff', topic: 'Kickoff & Organizational Governance Context',
      functions: 'GOVERN (GV)', controls: 'GV.OC-01 through GV.OC-05',
      duration: '90 min', proserve: 'Optional',
      attendees: ['CISO / ISO', 'CRO', 'Compliance Officer', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Engagement overview and scope confirmation', 'Shared Responsibility Model scoping', 'Pre-engagement control context review', 'Organizational context and mission alignment', 'Stakeholder identification and expectations']
    },
    {
      id: 'mtg1', topic: 'Risk Management Strategy & Cybersecurity Supply Chain',
      functions: 'GOVERN (GV)', controls: 'GV.RM-01 through GV.RM-07; GV.SC-01 through GV.SC-10',
      duration: '75 min', proserve: 'No',
      attendees: ['CRO', 'CISO / ISO', 'Third-Party Risk Manager', 'Procurement Lead', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Risk management objectives and stakeholder agreement', 'Risk appetite and tolerance statements', 'ERM integration', 'Risk scoring methodology', 'Supply chain risk management program', 'Supplier identification and contracts', 'Supplier incident planning']
    },
    {
      id: 'mtg2', topic: 'Roles, Responsibilities, Policy & Oversight',
      functions: 'GOVERN (GV)', controls: 'GV.RR-01 through GV.RR-04; GV.PO-01/02; GV.OV-01 through GV.OV-03',
      duration: '60 min', proserve: 'No',
      attendees: ['CISO / ISO', 'CCO', 'HR Director', 'Internal Audit Director', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Leadership accountability', 'Roles and responsibilities', 'Resource allocation', 'Cybersecurity in HR practices', 'Policy management', 'Oversight of risk management performance']
    },
    {
      id: 'mtg3', topic: 'Asset Management',
      functions: 'IDENTIFY (ID)', controls: 'ID.AM-01 through ID.AM-08',
      duration: '75 min', proserve: 'Yes',
      attendees: ['IT Director', 'Cloud Architecture Lead (ProServe)', 'Data Governance Officer', 'IT Asset Manager', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Hardware and software asset inventory in AWS', 'Network communication and data flow diagrams', 'Supplier service inventories', 'Asset classification and criticality', 'Data inventories and metadata', 'Asset lifecycle management']
    },
    {
      id: 'mtg4', topic: 'Risk Assessment & Improvement',
      functions: 'IDENTIFY (ID)', controls: 'ID.RA-01 through ID.RA-10; ID.IM-01 through ID.IM-04',
      duration: '90 min', proserve: 'No',
      attendees: ['CISO / ISO', 'IT Risk Manager', 'Vulnerability Management Lead', 'AppSec Lead', 'Internal Audit Rep', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Vulnerability identification and validation', 'Cyber threat intelligence sources', 'Internal and external threat identification', 'Impact and likelihood assessment', 'Risk response planning and change management', 'Secure SDLC gap assessment', 'Operational process improvements']
    },
    {
      id: 'mtg5', topic: 'Identity, Access Control, Awareness & Data Security',
      functions: 'PROTECT (PR)', controls: 'PR.AA-01 through PR.AA-05; PR.AT-01/02; PR.DS-01/02/10/11',
      duration: '75 min', proserve: 'Yes',
      attendees: ['CISO / ISO', 'IAM Lead', 'Security Awareness Coordinator', 'Data Security Lead', 'Cloud Architect (ProServe)', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Identity and credential management', 'Authentication controls and MFA', 'Access permissions and least privilege', 'Security awareness and training', 'Data-at-rest and in-transit protection', 'Backup controls and data integrity']
    },
    {
      id: 'mtg6', topic: 'Platform Security & Infrastructure Resilience',
      functions: 'PROTECT (PR)', controls: 'PR.PS-01/02/04/05/06; PR.IR-01/03/04',
      duration: '75 min', proserve: 'Yes',
      attendees: ['IT Director', 'Cloud Architecture Lead (ProServe)', 'DevSecOps Lead', 'Network Security Engineer', 'BC/DR Manager', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Configuration management practices', 'Software maintenance and patch management', 'Log generation and availability', 'Unauthorized software prevention', 'Secure SDLC (gap area revisit)', 'Network protection and resilience']
    },
    {
      id: 'mtg7', topic: 'Continuous Monitoring & Adverse Event Analysis',
      functions: 'DETECT (DE)', controls: 'DE.AE-02 through DE.AE-08; DE.CM-01/03/06/09',
      duration: '75 min', proserve: 'Yes',
      attendees: ['CISO / ISO', 'SOC Manager', 'Threat Intelligence Analyst', 'Network Security Engineer', 'Cloud Security Engineer (ProServe)', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Adverse event analysis and correlation', 'Impact and scope estimation', 'Information sharing and routing', 'Threat intelligence integration', 'Incident declaration criteria', 'Network and runtime monitoring', 'External service provider monitoring']
    },
    {
      id: 'mtg8', topic: 'Incident Response, Recovery & Communications',
      functions: 'RESPOND (RS) / RECOVER (RC)', controls: 'RS.MA-01 through RS.MA-05; RS.AN-03/06-08; RS.CO-02/03; RS.MI-01/02; RC.RP-01 through RC.RP-06; RC.CO-03/04',
      duration: '75 min', proserve: 'No',
      attendees: ['CISO / ISO', 'IR Manager', 'BC/DR Manager', 'Legal Counsel', 'Communications Officer', 'Compliance Officer', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Incident response plan execution', 'Incident triage and categorization', 'Escalation and recovery criteria', 'Incident analysis and forensics', 'Regulatory notification procedures', 'Containment and eradication', 'Recovery plan execution and validation', 'Post-incident review and communications']
    },
  ],
  'nist-800-53': [
    {
      id: 'kickoff', topic: 'Kickoff & Governance Context',
      functions: 'Program Management (PM)', controls: 'PM-1 through PM-16',
      duration: '90 min', proserve: 'Optional',
      attendees: ['CISO', 'CRO', 'Compliance Officer', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Engagement overview and scope', 'Shared Responsibility Model scoping', 'Pre-engagement control context', 'Security program overview']
    },
    {
      id: 'mtg1', topic: 'Access Control & Identification',
      functions: 'AC / IA', controls: 'AC-1 through AC-22; IA-1 through IA-12',
      duration: '90 min', proserve: 'Yes',
      attendees: ['CISO', 'IAM Lead', 'Cloud Architect (ProServe)', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Access control policy and account management', 'Least privilege and separation of duties', 'Remote access and wireless controls', 'Identification and authentication', 'MFA and credential management']
    },
    {
      id: 'mtg2', topic: 'Audit, Accountability & Configuration Management',
      functions: 'AU / CM', controls: 'AU-1 through AU-12; CM-1 through CM-12',
      duration: '90 min', proserve: 'Yes',
      attendees: ['CISO', 'IT Director', 'Cloud Architect (ProServe)', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Audit logging and retention', 'Log protection and review', 'Configuration baselines and change management', 'Security configuration enforcement', 'Software restrictions']
    },
    {
      id: 'mtg3', topic: 'Risk Assessment & Planning',
      functions: 'RA / PL', controls: 'RA-1 through RA-9; PL-1 through PL-11',
      duration: '75 min', proserve: 'No',
      attendees: ['CISO', 'IT Risk Manager', 'Vulnerability Management Lead', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Risk assessment methodology', 'Vulnerability scanning and remediation', 'System security plan', 'Security architecture']
    },
    {
      id: 'mtg4', topic: 'System & Communications Protection',
      functions: 'SC / SI', controls: 'SC-1 through SC-39; SI-1 through SI-16',
      duration: '90 min', proserve: 'Yes',
      attendees: ['CISO', 'Network Security Engineer', 'Cloud Architect (ProServe)', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Boundary protection and network security', 'Encryption at rest and in transit', 'Key management', 'Flaw remediation and patching', 'Malware protection', 'System monitoring']
    },
    {
      id: 'mtg5', topic: 'Incident Response & Contingency Planning',
      functions: 'IR / CP', controls: 'IR-1 through IR-8; CP-1 through CP-10',
      duration: '75 min', proserve: 'No',
      attendees: ['CISO', 'IR Manager', 'BC/DR Manager', 'Legal Counsel', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Incident response plan and testing', 'Incident handling and reporting', 'Contingency planning and testing', 'Backup and recovery', 'Alternate processing sites']
    },
    {
      id: 'mtg6', topic: 'Personnel, Training, Awareness & Supply Chain',
      functions: 'PS / AT / SR / SA', controls: 'PS-1 through PS-9; AT-1 through AT-4; SR-1 through SR-12; SA-1 through SA-22',
      duration: '75 min', proserve: 'No',
      attendees: ['CISO', 'HR Director', 'Training Coordinator', 'Procurement Lead', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Personnel security and screening', 'Security awareness and training', 'Supply chain risk management', 'System acquisition security']
    },
    {
      id: 'mtg7', topic: 'Maintenance, Media Protection & Physical Security',
      functions: 'MA / MP / PE', controls: 'MA-1 through MA-6; MP-1 through MP-8; PE-1 through PE-17',
      duration: '60 min', proserve: 'No',
      attendees: ['IT Director', 'Facilities Manager', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['System maintenance procedures', 'Media protection and sanitization', 'Physical security (SRM scoping)', 'Remote work security']
    },
  ],
  'cmmc': [
    {
      id: 'kickoff', topic: 'Kickoff & CUI Scope Definition',
      functions: 'All Domains', controls: 'CUI boundary definition',
      duration: '90 min', proserve: 'Optional',
      attendees: ['CISO', 'CUI Program Manager', 'IT Director', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Engagement overview and CMMC Level 2 scope', 'CUI boundary definition', 'Shared Responsibility Model scoping', 'Pre-engagement control context review']
    },
    {
      id: 'mtg1', topic: 'Access Control',
      functions: 'AC Domain', controls: 'AC.L2-3.1.1 through AC.L2-3.1.22',
      duration: '90 min', proserve: 'Yes',
      attendees: ['CISO', 'IAM Lead', 'Cloud Architect (ProServe)', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Authorized access and least privilege', 'CUI flow control', 'Remote access and wireless', 'Mobile device and portable storage', 'Public information controls']
    },
    {
      id: 'mtg2', topic: 'Audit, Configuration & Identification',
      functions: 'AU / CM / IA Domains', controls: 'AU.L2-3.3.1 through AU.L2-3.3.9; CM.L2-3.4.1 through CM.L2-3.4.9; IA.L2-3.5.1 through IA.L2-3.5.11',
      duration: '90 min', proserve: 'Yes',
      attendees: ['CISO', 'IT Director', 'Cloud Architect (ProServe)', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Audit logging and accountability', 'Configuration baselines and change management', 'Identification and authentication', 'MFA and credential management']
    },
    {
      id: 'mtg3', topic: 'System Protection & Communications',
      functions: 'SC Domain', controls: 'SC.L2-3.13.1 through SC.L2-3.13.16',
      duration: '75 min', proserve: 'Yes',
      attendees: ['CISO', 'Network Security Engineer', 'Cloud Architect (ProServe)', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Boundary protection', 'Encryption at rest and in transit', 'FIPS cryptography', 'Network segmentation', 'Key management']
    },
    {
      id: 'mtg4', topic: 'Incident Response, Risk & Security Assessment',
      functions: 'IR / RA / CA Domains', controls: 'IR.L2-3.6.1 through IR.L2-3.6.3; RA.L2-3.11.1 through RA.L2-3.11.3; CA.L2-3.12.1 through CA.L2-3.12.4',
      duration: '75 min', proserve: 'No',
      attendees: ['CISO', 'IR Manager', 'IT Risk Manager', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Incident response capability and testing', 'Risk assessment and vulnerability management', 'Security control assessment', 'POA&M and SSP maintenance']
    },
    {
      id: 'mtg5', topic: 'Integrity, Awareness, Maintenance & Media',
      functions: 'SI / AT / MA / MP Domains', controls: 'SI.L2-3.14.1 through SI.L2-3.14.7; AT.L2-3.2.1 through AT.L2-3.2.3; MA.L2-3.7.1 through MA.L2-3.7.6; MP.L2-3.8.1 through MP.L2-3.8.9',
      duration: '75 min', proserve: 'No',
      attendees: ['CISO', 'IT Director', 'Training Coordinator', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['System integrity and malware protection', 'Security awareness and insider threat training', 'System maintenance procedures', 'Media protection and CUI marking']
    },
    {
      id: 'mtg6', topic: 'Personnel & Physical Security',
      functions: 'PS / PE Domains', controls: 'PS.L2-3.9.1 through PS.L2-3.9.2; PE.L2-3.10.1 through PE.L2-3.10.6',
      duration: '60 min', proserve: 'No',
      attendees: ['CISO', 'HR Director', 'Facilities Manager', 'AWS SAS Advisor (facilitator)'],
      agendaItems: ['Personnel screening and termination', 'Physical access controls (SRM scoping)', 'Alternate work site safeguards']
    },
  ],
};

const EngagementSchedule: React.FC = () => {
  const [config, setConfig] = useState<EngagementConfig>({
    customerName: '',
    framework: 'nist-csf',
    scope: 'AWS Environment Only',
    regulator: '',
    startDate: '',
    cadence: 'weekly',
  });
  const [generated, setGenerated] = useState(false);
  const [copied, setCopied] = useState(false);

  const meetings = FRAMEWORK_MEETINGS[config.framework] || [];

  const frameworkLabel: Record<string, string> = {
    'nist-csf': 'NIST CSF 2.0',
    'nist-800-53': 'NIST 800-53 Rev 5',
    'cmmc': 'CMMC Level 2',
  };

  const generateReport = () => {
    let report = `${config.customerName || '[Customer Name]'}\n`;
    report += `${frameworkLabel[config.framework]} Stakeholder Interview Schedule & Artifact Request List\n\n`;
    report += `AWS Security Assurance Services (AWS SAS) - Advisory Engagement\n`;
    report += `Scope: ${config.scope}\n`;
    if (config.regulator) report += `Primary Regulator: ${config.regulator}\n`;
    report += `Prepared by: AWS SAS Compliance Advisor\n\n`;
    report += `AWS SAS Advisory Notice: The following schedule and agendas are provided as advisory guidance only. This does not constitute a formal audit, assessment, or compliance certification. Legal counsel should be consulted for regulatory interpretation.\n\n`;
    report += `---\n\nShared Responsibility Model (SRM) Scoping Note\n\n`;
    report += `This engagement is scoped to ${config.scope}. In accordance with the AWS Shared Responsibility Model, AWS is responsible for the security of the cloud (physical infrastructure, hardware, hypervisor, global network, and data center environmental controls). The customer is responsible for security in the cloud (operating systems, applications, data, identity, access management, and configurations within their AWS accounts).\n\n`;
    report += `---\n\nEngagement Schedule Overview\n\n`;
    meetings.forEach((m, idx) => {
      report += `${m.id === 'kickoff' ? 'Kickoff' : `Meeting ${idx}`}: ${m.topic}\n`;
      report += `  Function(s): ${m.functions}\n`;
      report += `  Controls: ${m.controls}\n`;
      report += `  Duration: ${m.duration} | ProServe: ${m.proserve}\n`;
      report += `  Attendees: ${m.attendees.join(', ')}\n`;
      report += `  Agenda:\n`;
      m.agendaItems.forEach(a => { report += `    - ${a}\n`; });
      report += `\n`;
    });
    report += `Buffer: Evidence Collection & CPR Drafting (3+ weeks)\n`;
    report += `Session 1: Draft CPR Walkthrough & Findings Review (90 min)\n`;
    report += `Session 2: Recommendations Review & Engagement Close-Out (90 min)\n`;
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
        <Header variant="h2" description="Configure your engagement parameters to generate a structured interview schedule">
          Engagement Schedule Builder
        </Header>
      }>
        <ColumnLayout columns={2}>
          <FormField label="Customer name">
            <Input value={config.customerName} onChange={({ detail }) => setConfig({ ...config, customerName: detail.value })} placeholder="e.g., Acme Financial Corp" />
          </FormField>
          <FormField label="Compliance framework">
            <Select
              selectedOption={{ label: frameworkLabel[config.framework], value: config.framework }}
              onChange={({ detail }) => setConfig({ ...config, framework: detail.selectedOption.value || 'nist-csf' })}
              options={[
                { label: 'NIST CSF 2.0', value: 'nist-csf' },
                { label: 'NIST 800-53 Rev 5', value: 'nist-800-53' },
                { label: 'CMMC Level 2', value: 'cmmc' },
              ]}
            />
          </FormField>
          <FormField label="Engagement scope">
            <Input value={config.scope} onChange={({ detail }) => setConfig({ ...config, scope: detail.value })} placeholder="e.g., AWS Environment Only" />
          </FormField>
          <FormField label="Primary regulator (optional)">
            <Input value={config.regulator} onChange={({ detail }) => setConfig({ ...config, regulator: detail.value })} placeholder="e.g., OCC, FFIEC, DoD" />
          </FormField>
        </ColumnLayout>
        <Box margin={{ top: 'm' }}>
          <SpaceBetween size="xs" direction="horizontal">
            <Button variant="primary" onClick={() => setGenerated(true)}>Generate schedule</Button>
            {generated && <Button iconName={copied ? 'check' : 'copy'} onClick={copyReport}>{copied ? 'Copied' : 'Copy full report'}</Button>}
          </SpaceBetween>
        </Box>
      </Container>

      {generated && (
        <>
          <Alert type="info">
            AWS SAS Advisory Notice: This schedule is provided as advisory guidance only. This does not constitute a formal audit, assessment, or compliance certification. Legal counsel should be consulted for regulatory interpretation.
          </Alert>

          <Container header={<Header variant="h3">Shared Responsibility Model (SRM) Scoping Note</Header>}>
            <Box>This engagement is scoped to <Box variant="strong" display="inline">{config.scope}</Box>. In accordance with the AWS Shared Responsibility Model, AWS is responsible for the security of the cloud. {config.customerName || 'The customer'} is responsible for security in the cloud.</Box>
          </Container>

          <Container header={
            <Header variant="h2" description={`${meetings.length} interview sessions + buffer + close-out`}>
              {config.customerName || '[Customer]'} — {frameworkLabel[config.framework]} Interview Schedule
            </Header>
          }>
            <Table
              columnDefinitions={[
                { id: 'meeting', header: 'Meeting', cell: (m: Meeting) => <Box variant="strong">{m.id === 'kickoff' ? 'Kickoff' : m.id.replace('mtg', 'Meeting ')}</Box>, width: 100 },
                { id: 'topic', header: 'Topic', cell: (m: Meeting) => m.topic },
                { id: 'functions', header: 'Function(s)', cell: (m: Meeting) => <Badge color="blue">{m.functions}</Badge> },
                { id: 'duration', header: 'Duration', cell: (m: Meeting) => m.duration },
                { id: 'proserve', header: 'ProServe', cell: (m: Meeting) => <Badge color={m.proserve === 'Yes' ? 'green' : 'grey'}>{m.proserve}</Badge> },
              ]}
              items={meetings}
              variant="embedded"
            />
          </Container>

          {meetings.map((m) => (
            <ExpandableSection key={m.id} variant="container"
              headerText={`${m.id === 'kickoff' ? 'Kickoff' : m.id.replace('mtg', 'Meeting ')} — ${m.topic}`}
              headerDescription={`${m.functions} | ${m.duration} | ProServe: ${m.proserve}`}
            >
              <SpaceBetween size="m">
                <ColumnLayout columns={2}>
                  <div>
                    <Box variant="awsui-key-label">Controls covered</Box>
                    <Box>{m.controls}</Box>
                  </div>
                  <div>
                    <Box variant="awsui-key-label">Recommended attendees</Box>
                    <SpaceBetween size="xxs">
                      {m.attendees.map((a, i) => <Box key={i} variant="small">• {a}</Box>)}
                    </SpaceBetween>
                  </div>
                </ColumnLayout>
                <div>
                  <Box variant="awsui-key-label">Agenda</Box>
                  <SpaceBetween size="xxs">
                    {m.agendaItems.map((a, i) => (
                      <Box key={i} variant="small">
                        <Box variant="strong" display="inline">{(i + 1) * Math.round(parseInt(m.duration) / m.agendaItems.length)} min</Box> — {a}
                      </Box>
                    ))}
                  </SpaceBetween>
                </div>
              </SpaceBetween>
            </ExpandableSection>
          ))}

          <Container header={<Header variant="h3">Close-Out Sessions</Header>}>
            <SpaceBetween size="s">
              <Box><Box variant="strong" display="inline">Buffer Period</Box> — Evidence Collection & CPR Drafting (3+ weeks after final interview)</Box>
              <Box><Box variant="strong" display="inline">Session 1</Box> — Draft CPR Walkthrough & Findings Review (90 min)</Box>
              <Box><Box variant="strong" display="inline">Session 2</Box> — Recommendations Review & Engagement Close-Out (90 min)</Box>
            </SpaceBetween>
          </Container>
        </>
      )}
    </SpaceBetween>
  );
};

export default EngagementSchedule;
