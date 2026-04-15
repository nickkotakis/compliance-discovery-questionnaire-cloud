import React, { useState } from 'react';
import Container from '@cloudscape-design/components/container';
import Header from '@cloudscape-design/components/header';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Button from '@cloudscape-design/components/button';
import Box from '@cloudscape-design/components/box';
import Badge from '@cloudscape-design/components/badge';
import Table from '@cloudscape-design/components/table';
import ColumnLayout from '@cloudscape-design/components/column-layout';
import Alert from '@cloudscape-design/components/alert';
import ExpandableSection from '@cloudscape-design/components/expandable-section';

// =========================================================================
// Types
// =========================================================================
interface AgendaItem {
  topic: string;
  controls: string;
  minutes: number;
}

interface Meeting {
  id: string;
  topic: string;
  functions: string;
  controls: string;
  duration: number;
  proserve: string;
  attendees: string[];
  agendaItems: AgendaItem[];
}

interface ControlGroup {
  id: string;
  topic: string;
  functions: string;
  controls: string[];
  controlCount: number;
  minutesPerControl: number;  // complexity-based
  proserve: boolean;
  attendees: string[];
  agendaTopics: string[];
  srmInherited?: string[];  // controls excluded due to SRM
}

// Complexity: HIGH=12min, MEDIUM=8min, LOW=5min per control
const CSF_CONTROL_GROUPS: ControlGroup[] = [
  { id: 'gv-oc', topic: 'Organizational Context', functions: 'GOVERN (GV)', controls: ['GV.OC-01','GV.OC-02','GV.OC-03','GV.OC-04','GV.OC-05'], controlCount: 5, minutesPerControl: 8, proserve: false, attendees: ['CISO / ISO', 'CRO', 'Compliance Officer'], agendaTopics: ['Mission-to-risk alignment', 'Stakeholder expectations', 'Regulatory obligations', 'Critical services', 'External dependencies'] },
  { id: 'gv-rm', topic: 'Risk Management Strategy', functions: 'GOVERN (GV)', controls: ['GV.RM-01','GV.RM-02','GV.RM-03','GV.RM-04','GV.RM-05','GV.RM-06','GV.RM-07'], controlCount: 7, minutesPerControl: 8, proserve: false, attendees: ['CRO', 'CISO / ISO', 'IT Risk Manager'], agendaTopics: ['Risk management objectives', 'Risk appetite and tolerance', 'ERM integration', 'Risk response strategy', 'Risk communication', 'Risk scoring methodology'] },
  { id: 'gv-sc', topic: 'Supply Chain Risk Management', functions: 'GOVERN (GV)', controls: ['GV.SC-01','GV.SC-02','GV.SC-03','GV.SC-04','GV.SC-05','GV.SC-06','GV.SC-07','GV.SC-08','GV.SC-09','GV.SC-10'], controlCount: 10, minutesPerControl: 5, proserve: false, attendees: ['Third-Party Risk Manager', 'Procurement Lead', 'CISO / ISO'], agendaTopics: ['C-SCRM program', 'Supplier roles and responsibilities', 'Supplier prioritization', 'Contract requirements', 'Supplier monitoring', 'Supplier incident planning'] },
  { id: 'gv-rr', topic: 'Roles, Responsibilities & Policy', functions: 'GOVERN (GV)', controls: ['GV.RR-01','GV.RR-02','GV.RR-03','GV.RR-04','GV.PO-01','GV.PO-02'], controlCount: 6, minutesPerControl: 8, proserve: false, attendees: ['CISO / ISO', 'CCO', 'HR Director', 'Internal Audit Director'], agendaTopics: ['Leadership accountability', 'Roles and responsibilities', 'Resource allocation', 'Cybersecurity in HR', 'Policy management and review'] },
  { id: 'id-am', topic: 'Asset Management', functions: 'IDENTIFY (ID)', controls: ['ID.AM-01','ID.AM-02','ID.AM-03','ID.AM-04','ID.AM-05','ID.AM-07','ID.AM-08'], controlCount: 7, minutesPerControl: 10, proserve: true, attendees: ['IT Director', 'Cloud Architecture Lead (ProServe)', 'Data Governance Officer', 'IT Asset Manager'], agendaTopics: ['Hardware/software inventory in AWS', 'Network diagrams and data flows', 'Supplier service inventories', 'Asset classification and criticality', 'Data inventories', 'Asset lifecycle management'] },
  { id: 'id-ra', topic: 'Risk Assessment', functions: 'IDENTIFY (ID)', controls: ['ID.RA-01','ID.RA-02','ID.RA-03','ID.RA-04','ID.RA-05','ID.RA-06','ID.RA-07','ID.RA-08','ID.RA-09','ID.RA-10'], controlCount: 10, minutesPerControl: 8, proserve: false, attendees: ['CISO / ISO', 'IT Risk Manager', 'Vulnerability Management Lead', 'AppSec Lead'], agendaTopics: ['Vulnerability identification', 'Threat intelligence', 'Threat identification', 'Impact/likelihood assessment', 'Risk response planning', 'Vulnerability disclosure', 'Software authenticity'] },
  { id: 'id-im', topic: 'Improvement', functions: 'IDENTIFY (ID)', controls: ['ID.IM-01','ID.IM-02','ID.IM-03','ID.IM-04'], controlCount: 4, minutesPerControl: 12, proserve: false, attendees: ['CISO / ISO', 'AppSec Lead', 'Internal Audit Rep'], agendaTopics: ['Improvements from evaluations', 'Improvements from security tests (Secure SDLC gap)', 'Operational process improvements', 'IRP maintenance'] },
  { id: 'pr-aa', topic: 'Identity, Authentication & Access Control', functions: 'PROTECT (PR)', controls: ['PR.AA-01','PR.AA-02','PR.AA-03','PR.AA-04','PR.AA-05'], controlCount: 5, minutesPerControl: 12, proserve: true, attendees: ['CISO / ISO', 'IAM Lead', 'Cloud Architect (ProServe)'], agendaTopics: ['Identity and credential management', 'Authentication controls and MFA', 'Access permissions and least privilege', 'Separation of duties'], srmInherited: ['PR.AA-06 (Physical Access) — AWS inherited'] },
  { id: 'pr-at', topic: 'Awareness & Training', functions: 'PROTECT (PR)', controls: ['PR.AT-01','PR.AT-02'], controlCount: 2, minutesPerControl: 8, proserve: false, attendees: ['Security Awareness Coordinator', 'CISO / ISO'], agendaTopics: ['General security awareness training', 'Role-based specialized training'] },
  { id: 'pr-ds', topic: 'Data Security', functions: 'PROTECT (PR)', controls: ['PR.DS-01','PR.DS-02','PR.DS-10','PR.DS-11'], controlCount: 4, minutesPerControl: 10, proserve: true, attendees: ['Data Security Lead', 'Cloud Architect (ProServe)', 'CISO / ISO'], agendaTopics: ['Data-at-rest protection (KMS)', 'Data-in-transit protection (TLS)', 'Data-in-use protection', 'Backup controls and integrity'] },
  { id: 'pr-ps', topic: 'Platform Security', functions: 'PROTECT (PR)', controls: ['PR.PS-01','PR.PS-02','PR.PS-04','PR.PS-05','PR.PS-06'], controlCount: 5, minutesPerControl: 10, proserve: true, attendees: ['IT Director', 'Cloud Architecture Lead (ProServe)', 'DevSecOps Lead'], agendaTopics: ['Configuration management', 'Patch management', 'Log generation', 'Unauthorized software prevention', 'Secure SDLC'], srmInherited: ['PR.PS-03 (Hardware Maintenance) — AWS inherited'] },
  { id: 'pr-ir', topic: 'Infrastructure Resilience', functions: 'PROTECT (PR)', controls: ['PR.IR-01','PR.IR-03','PR.IR-04'], controlCount: 3, minutesPerControl: 12, proserve: true, attendees: ['Network Security Engineer', 'BC/DR Manager', 'Cloud Architecture Lead (ProServe)'], agendaTopics: ['Network protection and segmentation', 'Resilience mechanisms (Multi-AZ, Auto Scaling)', 'Capacity management'], srmInherited: ['PR.IR-02 (Environmental Threats) — AWS inherited'] },
  { id: 'de-ae', topic: 'Adverse Event Analysis', functions: 'DETECT (DE)', controls: ['DE.AE-02','DE.AE-03','DE.AE-04','DE.AE-06','DE.AE-07','DE.AE-08'], controlCount: 6, minutesPerControl: 10, proserve: true, attendees: ['CISO / ISO', 'SOC Manager', 'Threat Intelligence Analyst', 'Cloud Security Engineer (ProServe)'], agendaTopics: ['Event analysis and correlation', 'Impact and scope estimation', 'Information sharing and routing', 'Threat intelligence integration', 'Incident declaration criteria'] },
  { id: 'de-cm', topic: 'Continuous Monitoring', functions: 'DETECT (DE)', controls: ['DE.CM-01','DE.CM-03','DE.CM-06','DE.CM-09'], controlCount: 4, minutesPerControl: 10, proserve: true, attendees: ['SOC Manager', 'Network Security Engineer', 'Cloud Security Engineer (ProServe)'], agendaTopics: ['Network monitoring', 'Personnel activity monitoring', 'External service provider monitoring', 'Runtime and computing monitoring'], srmInherited: ['DE.CM-02 (Physical Monitoring) — AWS inherited'] },
  { id: 'rs', topic: 'Incident Response', functions: 'RESPOND (RS)', controls: ['RS.MA-01','RS.MA-02','RS.MA-03','RS.MA-04','RS.MA-05','RS.AN-03','RS.AN-06','RS.AN-07','RS.AN-08','RS.CO-02','RS.CO-03','RS.MI-01','RS.MI-02'], controlCount: 13, minutesPerControl: 5, proserve: false, attendees: ['CISO / ISO', 'IR Manager', 'Legal Counsel', 'Communications Officer'], agendaTopics: ['IR plan execution', 'Incident triage and categorization', 'Escalation criteria', 'Incident analysis and forensics', 'Regulatory notification', 'Containment and eradication'] },
  { id: 'rc', topic: 'Recovery', functions: 'RECOVER (RC)', controls: ['RC.RP-01','RC.RP-02','RC.RP-03','RC.RP-04','RC.RP-05','RC.RP-06','RC.CO-03','RC.CO-04'], controlCount: 8, minutesPerControl: 5, proserve: false, attendees: ['BC/DR Manager', 'CISO / ISO', 'Compliance Officer'], agendaTopics: ['Recovery plan execution', 'Recovery prioritization', 'Backup integrity verification', 'Post-recovery validation', 'Recovery communications'] },
];

const NIST_800_53_CONTROL_GROUPS: ControlGroup[] = [
  { id: 'ac', topic: 'Access Control', functions: 'AC', controls: ['AC-1 through AC-22'], controlCount: 22, minutesPerControl: 5, proserve: true, attendees: ['CISO', 'IAM Lead', 'Cloud Architect (ProServe)'], agendaTopics: ['Access control policy', 'Account management', 'Least privilege', 'Separation of duties', 'Remote access', 'Wireless and mobile'] },
  { id: 'ia', topic: 'Identification & Authentication', functions: 'IA', controls: ['IA-1 through IA-12'], controlCount: 12, minutesPerControl: 6, proserve: true, attendees: ['CISO', 'IAM Lead', 'Cloud Architect (ProServe)'], agendaTopics: ['Authentication policy', 'MFA enforcement', 'Credential management', 'Device authentication', 'External user auth'] },
  { id: 'au', topic: 'Audit & Accountability', functions: 'AU', controls: ['AU-1 through AU-12'], controlCount: 12, minutesPerControl: 6, proserve: true, attendees: ['CISO', 'IT Director', 'Cloud Architect (ProServe)'], agendaTopics: ['Audit logging policy', 'Log retention', 'Log protection', 'Log review', 'Time synchronization'] },
  { id: 'cm', topic: 'Configuration Management', functions: 'CM', controls: ['CM-1 through CM-12'], controlCount: 12, minutesPerControl: 6, proserve: true, attendees: ['CISO', 'IT Director', 'Cloud Architect (ProServe)'], agendaTopics: ['Configuration baselines', 'Change management', 'Security settings', 'Software restrictions', 'Information location'] },
  { id: 'sc', topic: 'System & Communications Protection', functions: 'SC', controls: ['SC-1 through SC-39'], controlCount: 18, minutesPerControl: 5, proserve: true, attendees: ['CISO', 'Network Security Engineer', 'Cloud Architect (ProServe)'], agendaTopics: ['Boundary protection', 'Encryption at rest and in transit', 'Key management', 'FIPS cryptography', 'Network segmentation'] },
  { id: 'si', topic: 'System & Information Integrity', functions: 'SI', controls: ['SI-1 through SI-16'], controlCount: 14, minutesPerControl: 5, proserve: true, attendees: ['CISO', 'SOC Manager', 'Cloud Architect (ProServe)'], agendaTopics: ['Flaw remediation', 'Malware protection', 'System monitoring', 'Security alerts', 'Input validation'] },
  { id: 'ra', topic: 'Risk Assessment', functions: 'RA', controls: ['RA-1 through RA-9'], controlCount: 7, minutesPerControl: 8, proserve: false, attendees: ['CISO', 'IT Risk Manager', 'Vulnerability Management Lead'], agendaTopics: ['Risk assessment methodology', 'Vulnerability scanning', 'Vulnerability remediation', 'Criticality analysis'] },
  { id: 'pl', topic: 'Planning', functions: 'PL', controls: ['PL-1 through PL-11'], controlCount: 7, minutesPerControl: 5, proserve: false, attendees: ['CISO', 'IT Risk Manager'], agendaTopics: ['System security plan', 'Rules of behavior', 'Security architecture', 'Baseline selection'] },
  { id: 'ir', topic: 'Incident Response', functions: 'IR', controls: ['IR-1 through IR-8'], controlCount: 8, minutesPerControl: 8, proserve: false, attendees: ['CISO', 'IR Manager', 'Legal Counsel'], agendaTopics: ['IR plan and testing', 'Incident handling', 'Incident reporting', 'IR assistance'] },
  { id: 'cp', topic: 'Contingency Planning', functions: 'CP', controls: ['CP-1 through CP-10'], controlCount: 10, minutesPerControl: 6, proserve: false, attendees: ['BC/DR Manager', 'CISO'], agendaTopics: ['Contingency plan and testing', 'Backup and recovery', 'Alternate sites', 'Telecommunications'] },
  { id: 'at', topic: 'Awareness & Training', functions: 'AT', controls: ['AT-1 through AT-4'], controlCount: 4, minutesPerControl: 5, proserve: false, attendees: ['Training Coordinator', 'CISO'], agendaTopics: ['Security awareness program', 'Role-based training', 'Training records'] },
  { id: 'ps', topic: 'Personnel Security', functions: 'PS', controls: ['PS-1 through PS-9'], controlCount: 9, minutesPerControl: 4, proserve: false, attendees: ['HR Director', 'CISO'], agendaTopics: ['Personnel screening', 'Termination/transfer', 'Access agreements', 'Sanctions'] },
  { id: 'sr', topic: 'Supply Chain Risk Management', functions: 'SR', controls: ['SR-1 through SR-12'], controlCount: 10, minutesPerControl: 5, proserve: false, attendees: ['Procurement Lead', 'CISO'], agendaTopics: ['Supply chain policy', 'Supplier assessments', 'Component authenticity'] },
  { id: 'sa', topic: 'System & Services Acquisition', functions: 'SA', controls: ['SA-1 through SA-22'], controlCount: 12, minutesPerControl: 5, proserve: false, attendees: ['CISO', 'Development Lead'], agendaTopics: ['Acquisition security', 'Secure SDLC', 'Developer testing', 'External services'] },
  { id: 'ma', topic: 'Maintenance', functions: 'MA', controls: ['MA-1 through MA-6'], controlCount: 6, minutesPerControl: 4, proserve: false, attendees: ['IT Director'], agendaTopics: ['Maintenance procedures', 'Remote maintenance', 'Maintenance tools'] },
  { id: 'mp', topic: 'Media Protection', functions: 'MP', controls: ['MP-1 through MP-8'], controlCount: 8, minutesPerControl: 4, proserve: false, attendees: ['IT Director', 'CISO'], agendaTopics: ['Media protection', 'Media sanitization', 'Removable media'] },
  { id: 'pe', topic: 'Physical & Environmental Protection', functions: 'PE', controls: ['PE-1 through PE-17'], controlCount: 3, minutesPerControl: 5, proserve: false, attendees: ['Facilities Manager'], agendaTopics: ['Physical security (SRM scoping)', 'Remote work security'], srmInherited: ['Most PE controls — AWS inherited per SRM'] },
  { id: 'pm', topic: 'Program Management', functions: 'PM', controls: ['PM-1 through PM-16'], controlCount: 16, minutesPerControl: 4, proserve: false, attendees: ['CISO', 'CRO', 'Compliance Officer'], agendaTopics: ['Security program plan', 'Risk management strategy', 'Authorization process', 'Insider threat program'] },
];

const CMMC_CONTROL_GROUPS: ControlGroup[] = [
  { id: 'ac', topic: 'Access Control', functions: 'AC Domain', controls: ['AC.L2-3.1.1 through AC.L2-3.1.22'], controlCount: 22, minutesPerControl: 5, proserve: true, attendees: ['CISO', 'IAM Lead', 'Cloud Architect (ProServe)'], agendaTopics: ['Authorized access and least privilege', 'CUI flow control', 'Remote access and wireless', 'Mobile device and portable storage', 'Public information controls'] },
  { id: 'au', topic: 'Audit & Accountability', functions: 'AU Domain', controls: ['AU.L2-3.3.1 through AU.L2-3.3.9'], controlCount: 9, minutesPerControl: 7, proserve: true, attendees: ['CISO', 'IT Director', 'Cloud Architect (ProServe)'], agendaTopics: ['Audit logging and retention', 'Individual accountability', 'Log correlation', 'Log protection'] },
  { id: 'cm', topic: 'Configuration Management', functions: 'CM Domain', controls: ['CM.L2-3.4.1 through CM.L2-3.4.9'], controlCount: 9, minutesPerControl: 7, proserve: true, attendees: ['CISO', 'IT Director', 'Cloud Architect (ProServe)'], agendaTopics: ['Configuration baselines', 'Change management', 'Least functionality', 'Software authorization'] },
  { id: 'ia', topic: 'Identification & Authentication', functions: 'IA Domain', controls: ['IA.L2-3.5.1 through IA.L2-3.5.11'], controlCount: 11, minutesPerControl: 6, proserve: true, attendees: ['CISO', 'IAM Lead', 'Cloud Architect (ProServe)'], agendaTopics: ['User identification', 'MFA enforcement', 'Password policy', 'Credential protection'] },
  { id: 'sc', topic: 'System & Communications Protection', functions: 'SC Domain', controls: ['SC.L2-3.13.1 through SC.L2-3.13.16'], controlCount: 16, minutesPerControl: 5, proserve: true, attendees: ['CISO', 'Network Security Engineer', 'Cloud Architect (ProServe)'], agendaTopics: ['Boundary protection', 'Encryption at rest and in transit', 'FIPS cryptography', 'Network segmentation', 'Key management'] },
  { id: 'si', topic: 'System & Information Integrity', functions: 'SI Domain', controls: ['SI.L2-3.14.1 through SI.L2-3.14.7'], controlCount: 7, minutesPerControl: 8, proserve: false, attendees: ['CISO', 'IT Director'], agendaTopics: ['Flaw remediation', 'Malware protection', 'System monitoring', 'Security alerts'] },
  { id: 'ir', topic: 'Incident Response', functions: 'IR Domain', controls: ['IR.L2-3.6.1 through IR.L2-3.6.3'], controlCount: 3, minutesPerControl: 12, proserve: false, attendees: ['CISO', 'IR Manager'], agendaTopics: ['IR capability', 'Incident tracking and reporting', 'IR testing'] },
  { id: 'ra', topic: 'Risk Assessment', functions: 'RA Domain', controls: ['RA.L2-3.11.1 through RA.L2-3.11.3'], controlCount: 3, minutesPerControl: 10, proserve: false, attendees: ['CISO', 'IT Risk Manager'], agendaTopics: ['Risk assessment process', 'Vulnerability scanning', 'Vulnerability remediation'] },
  { id: 'ca', topic: 'Security Assessment', functions: 'CA Domain', controls: ['CA.L2-3.12.1 through CA.L2-3.12.4'], controlCount: 4, minutesPerControl: 10, proserve: false, attendees: ['CISO', 'IT Risk Manager'], agendaTopics: ['Control assessment', 'POA&M', 'Continuous monitoring', 'SSP maintenance'] },
  { id: 'at', topic: 'Awareness & Training', functions: 'AT Domain', controls: ['AT.L2-3.2.1 through AT.L2-3.2.3'], controlCount: 3, minutesPerControl: 8, proserve: false, attendees: ['CISO', 'Training Coordinator'], agendaTopics: ['Security awareness', 'Role-based training', 'Insider threat training'] },
  { id: 'ma', topic: 'Maintenance', functions: 'MA Domain', controls: ['MA.L2-3.7.1 through MA.L2-3.7.6'], controlCount: 6, minutesPerControl: 5, proserve: false, attendees: ['IT Director'], agendaTopics: ['Maintenance procedures', 'Remote maintenance', 'Maintenance tools'] },
  { id: 'mp', topic: 'Media Protection', functions: 'MP Domain', controls: ['MP.L2-3.8.1 through MP.L2-3.8.9'], controlCount: 9, minutesPerControl: 4, proserve: false, attendees: ['IT Director', 'CISO'], agendaTopics: ['Media protection and marking', 'Media sanitization', 'Removable media', 'Backup CUI protection'] },
  { id: 'pe', topic: 'Physical Protection', functions: 'PE Domain', controls: ['PE.L2-3.10.1 through PE.L2-3.10.6'], controlCount: 6, minutesPerControl: 4, proserve: false, attendees: ['Facilities Manager', 'CISO'], agendaTopics: ['Physical access (SRM scoping)', 'Visitor management', 'Alternate work sites'], srmInherited: ['PE.L2-3.10.1 through PE.L2-3.10.5 — AWS inherited per SRM'] },
  { id: 'ps', topic: 'Personnel Security', functions: 'PS Domain', controls: ['PS.L2-3.9.1 through PS.L2-3.9.2'], controlCount: 2, minutesPerControl: 8, proserve: false, attendees: ['HR Director', 'CISO'], agendaTopics: ['Personnel screening', 'Termination/transfer procedures'] },
];

const FRAMEWORK_GROUPS: Record<string, ControlGroup[]> = {
  'nist-csf': CSF_CONTROL_GROUPS,
  'nist-800-53': NIST_800_53_CONTROL_GROUPS,
  'cmmc': CMMC_CONTROL_GROUPS,
};

// =========================================================================
// Schedule generation algorithm
// =========================================================================
function generateMeetings(groups: ControlGroup[], maxDuration: number, availableSlots: number): Meeting[] {
  // Calculate total minutes needed and apply compression to fit available time
  const totalNeeded = groups.reduce((s, g) => s + g.controlCount * g.minutesPerControl, 0);
  const totalAvailable = availableSlots * maxDuration;
  const compressionFactor = Math.min(1, totalAvailable / totalNeeded);

  // Build weighted groups
  const weightedGroups = groups.map(g => ({
    ...g,
    adjustedMinutes: Math.max(10, Math.round(g.controlCount * g.minutesPerControl * compressionFactor)),
  }));

  // Bin-pack groups into exactly availableSlots meetings (or fewer)
  const bins: { groups: typeof weightedGroups; totalMin: number }[] = [];

  for (const group of weightedGroups) {
    // Try to fit into an existing bin
    let placed = false;
    for (const bin of bins) {
      if (bin.totalMin + group.adjustedMinutes <= maxDuration) {
        bin.groups.push(group);
        bin.totalMin += group.adjustedMinutes;
        placed = true;
        break;
      }
    }
    if (!placed) {
      bins.push({ groups: [group], totalMin: group.adjustedMinutes });
    }
  }

  // If we have more bins than slots, merge the two smallest bins repeatedly
  while (bins.length > availableSlots && bins.length > 1) {
    bins.sort((a, b) => a.totalMin - b.totalMin);
    const smallest = bins.shift()!;
    const secondSmallest = bins.shift()!;
    bins.push({
      groups: [...smallest.groups, ...secondSmallest.groups],
      totalMin: smallest.totalMin + secondSmallest.totalMin,
    });
  }

  // Convert bins to Meeting objects
  const meetings: Meeting[] = bins.map((bin, idx) => {
    const grps = bin.groups;
    const duration = Math.min(Math.ceil(bin.totalMin / 5) * 5, Math.max(maxDuration, bin.totalMin));
    const needsProserve = grps.some(g => g.proserve);
    const allAttendees = new Set<string>();
    grps.forEach(g => g.attendees.forEach(a => allAttendees.add(a)));
    allAttendees.add('AWS SAS Advisor (facilitator)');

    const agendaItems: AgendaItem[] = [];
    grps.forEach(g => {
      const perTopic = Math.max(5, Math.round(g.adjustedMinutes / g.agendaTopics.length));
      g.agendaTopics.forEach(topic => {
        agendaItems.push({ topic, controls: g.controls.join(', '), minutes: perTopic });
      });
    });

    // Scale agenda to fit duration
    const agendaTotal = agendaItems.reduce((s, a) => s + a.minutes, 0);
    if (agendaTotal > duration && agendaTotal > 0) {
      const scale = duration / agendaTotal;
      agendaItems.forEach(a => { a.minutes = Math.max(5, Math.round(a.minutes * scale)); });
    }

    const srmNotes = grps.filter(g => g.srmInherited?.length).flatMap(g => g.srmInherited || []);
    if (srmNotes.length > 0) {
      agendaItems.push({ topic: `SRM Note: ${srmNotes.join('; ')}`, controls: '', minutes: 0 });
    }

    return {
      id: `mtg${idx + 1}`,
      topic: grps.map(g => g.topic).join(' & '),
      functions: grps.map(g => g.functions).join(' / '),
      controls: grps.map(g => g.controls.join(', ')).join('; '),
      duration,
      proserve: needsProserve ? 'Yes' : 'No',
      attendees: Array.from(allAttendees),
      agendaItems,
    };
  });

  return meetings;
}

// =========================================================================
// Component — reads from shared EngagementContext
// =========================================================================
import { useEngagement, FRAMEWORK_LABELS } from '../contexts/EngagementContext';

const EngagementSchedule: React.FC = () => {
  const { activeEngagement, setScheduleMeetings, scheduleMeetings: savedMeetings } = useEngagement();
  const [meetings, setMeetings] = useState<Meeting[]>(savedMeetings as Meeting[]);
  const [generated, setGenerated] = useState(savedMeetings.length > 0);
  const [copied, setCopied] = useState(false);
  const [scheduleWarning, setScheduleWarning] = useState('');

  const config = activeEngagement!.config;

  const doGenerate = () => {
    const groups = FRAMEWORK_GROUPS[config.framework] || [];
    const slotsPerWeek = config.meetingFrequency === 'weekly' ? 1 : 0.5;
    const interviewSlots = Math.floor(config.engagementWeeks * slotsPerWeek) - 1;
    const totalNeeded = groups.reduce((s, g) => s + g.controlCount * g.minutesPerControl, 0);
    const totalAvailable = interviewSlots * config.maxMeetingDuration;

    if (totalNeeded > totalAvailable * 1.3) {
      setScheduleWarning(`Schedule is compressed: ${totalNeeded} min needed but only ${totalAvailable} min available across ${interviewSlots} slots. Consider increasing duration or meeting length.`);
    } else if (totalNeeded < totalAvailable * 0.6) {
      setScheduleWarning(`Schedule has ample time: ${totalNeeded} min needed across ${totalAvailable} available. Meetings will include buffer for deeper discussion.`);
    } else { setScheduleWarning(''); }

    const mtgs = generateMeetings(groups, config.maxMeetingDuration, interviewSlots);
    setMeetings(mtgs);
    setScheduleMeetings(mtgs);  // persist to context
    setGenerated(true);
  };

  // Auto-generate on mount if no saved schedule
  React.useEffect(() => { if (savedMeetings.length === 0) doGenerate(); }, []);

  const generateReport = () => {
    let r = `${config.customerName}\n${FRAMEWORK_LABELS[config.framework]} Stakeholder Interview Schedule\n\n`;
    r += `AWS SAS Advisory Engagement | Scope: ${config.scope}${config.regulator ? ` | Regulator: ${config.regulator}` : ''}\n`;
    r += `Duration: ${config.engagementWeeks} weeks | Cadence: ${config.meetingFrequency} | Max meeting: ${config.maxMeetingDuration} min\n\n`;
    r += `AWS SAS Advisory Notice: This schedule is advisory guidance only.\n\n`;
    r += `SRM Scoping Note: Scoped to ${config.scope}.\n\n`;
    r += `--- SCHEDULE (${meetings.length} interviews + kickoff + buffer + close-out) ---\n\n`;
    meetings.forEach((m, i) => {
      r += `Meeting ${i + 1}: ${m.topic}\n  ${m.functions} | ${m.duration} min | ProServe: ${m.proserve}\n  Attendees: ${m.attendees.join(', ')}\n`;
      m.agendaItems.forEach(a => { r += `    ${a.minutes} min — ${a.topic}\n`; });
      r += `\n`;
    });
    r += `Buffer: Evidence Collection & CPR Drafting (3+ weeks)\nSession 1: Draft CPR Walkthrough (90 min)\nSession 2: Close-Out (90 min)\n`;
    return r;
  };

  const copyReport = () => { navigator.clipboard.writeText(generateReport()); setCopied(true); setTimeout(() => setCopied(false), 2000); };

  const totalControls = (FRAMEWORK_GROUPS[config.framework] || []).reduce((s, g) => s + g.controlCount, 0);

  return (
    <SpaceBetween size="l">
      <Container header={<Header variant="h2" description={`${config.customerName} — ${FRAMEWORK_LABELS[config.framework]} — ${config.engagementWeeks} weeks — ${totalControls} controls`} actions={
        <SpaceBetween size="xs" direction="horizontal">
          <Button onClick={doGenerate}>Regenerate</Button>
          <Button iconName={copied ? 'check' : 'copy'} onClick={copyReport}>{copied ? 'Copied' : 'Copy report'}</Button>
        </SpaceBetween>
      }>Engagement Schedule</Header>}>
        <Box variant="small" color="text-body-secondary">Schedule generated based on control complexity scoring. Adjust engagement parameters from the engagement setup page.</Box>
      </Container>

      {scheduleWarning && <Alert type={scheduleWarning.includes('compressed') ? 'warning' : 'info'}>{scheduleWarning}</Alert>}

      <Alert type="info">AWS SAS Advisory Notice: This schedule is advisory guidance only. Legal counsel should be consulted for regulatory interpretation.</Alert>

      <Container header={<Header variant="h3">Shared Responsibility Model (SRM) Scoping Note</Header>}>
        <Box>This engagement is scoped to <Box variant="strong" display="inline">{config.scope}</Box>. AWS is responsible for security of the cloud. {config.customerName} is responsible for security in the cloud.</Box>
      </Container>

      {generated && meetings.length > 0 && (
        <>
          <Container header={<Header variant="h2" description={`Kickoff + ${meetings.length} interviews + buffer + 2 close-out`}>{config.customerName} — Interview Schedule</Header>}>
            <Table
              columnDefinitions={[
                { id: 'meeting', header: 'Meeting', cell: (m: Meeting) => <Box variant="strong">Meeting {meetings.indexOf(m) + 1}</Box>, width: 100 },
                { id: 'topic', header: 'Topic', cell: (m: Meeting) => m.topic },
                { id: 'functions', header: 'Function(s)', cell: (m: Meeting) => <Badge color="blue">{m.functions}</Badge> },
                { id: 'duration', header: 'Duration', cell: (m: Meeting) => `${m.duration} min` },
                { id: 'proserve', header: 'ProServe', cell: (m: Meeting) => <Badge color={m.proserve === 'Yes' ? 'green' : 'grey'}>{m.proserve}</Badge> },
              ]}
              items={meetings}
              variant="embedded"
            />
          </Container>

          {meetings.map((m, idx) => (
            <ExpandableSection key={m.id} variant="container"
              headerText={`Meeting ${idx + 1} — ${m.topic}`}
              headerDescription={`${m.functions} | ${m.duration} min | ProServe: ${m.proserve}`}
            >
              <SpaceBetween size="m">
                <ColumnLayout columns={2}>
                  <div>
                    <Box variant="awsui-key-label">Controls covered</Box>
                    <Box variant="small">{m.controls}</Box>
                  </div>
                  <div>
                    <Box variant="awsui-key-label">Recommended attendees</Box>
                    <SpaceBetween size="xxs">
                      {m.attendees.map((a, i) => <Box key={i} variant="small">• {a}</Box>)}
                    </SpaceBetween>
                  </div>
                </ColumnLayout>
                <div>
                  <Box variant="awsui-key-label">Agenda (timed)</Box>
                  <SpaceBetween size="xxs">
                    {m.agendaItems.map((a, i) => (
                      <Box key={i} variant="small"><Badge color="grey">{a.minutes} min</Badge>{' '}{a.topic}</Box>
                    ))}
                  </SpaceBetween>
                </div>
              </SpaceBetween>
            </ExpandableSection>
          ))}

          <Container header={<Header variant="h3">Close-Out Sessions</Header>}>
            <SpaceBetween size="s">
              <Box><Box variant="strong" display="inline">Buffer Period</Box> — Evidence Collection & CPR Drafting (3+ weeks)</Box>
              <Box><Box variant="strong" display="inline">Session 1</Box> — Draft CPR Walkthrough & Findings Review (90 min)</Box>
              <Box><Box variant="strong" display="inline">Session 2</Box> — Recommendations Review & Close-Out (90 min)</Box>
            </SpaceBetween>
          </Container>
        </>
      )}
    </SpaceBetween>
  );
};

export default EngagementSchedule;
