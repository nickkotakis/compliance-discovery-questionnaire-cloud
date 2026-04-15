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

interface EngagementConfig {
  customerName: string;
  framework: string;
  scope: string;
  regulator: string;
  engagementWeeks: number;
  meetingFrequency: string;
  maxMeetingDuration: number;
}

// =========================================================================
// Control group definitions with complexity scoring
// =========================================================================
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
  // Calculate total minutes needed
  const groupMinutes = groups.map(g => ({
    ...g,
    totalMinutes: g.controlCount * g.minutesPerControl,
  }));
  const totalNeeded = groupMinutes.reduce((sum, g) => sum + g.totalMinutes, 0);
  const totalAvailable = availableSlots * maxDuration;

  // Compression factor if we need to fit into fewer slots
  const compressionFactor = totalNeeded > totalAvailable ? totalAvailable / totalNeeded : 1;

  const meetings: Meeting[] = [];
  let currentMeeting: { groups: typeof groupMinutes; totalMin: number } = { groups: [], totalMin: 0 };
  let meetingNum = 1;

  const flushMeeting = () => {
    if (currentMeeting.groups.length === 0) return;
    const grps = currentMeeting.groups;
    const duration = Math.min(Math.ceil(currentMeeting.totalMin / 5) * 5, maxDuration); // round to 5min
    const needsProserve = grps.some(g => g.proserve);
    const allAttendees = new Set<string>();
    grps.forEach(g => g.attendees.forEach(a => allAttendees.add(a)));
    allAttendees.add('AWS SAS Advisor (facilitator)');

    const agendaItems: AgendaItem[] = [];
    grps.forEach(g => {
      const adjustedMin = Math.round(g.totalMinutes * compressionFactor);
      const perTopic = Math.max(5, Math.round(adjustedMin / g.agendaTopics.length));
      g.agendaTopics.forEach(topic => {
        agendaItems.push({ topic, controls: g.controls.join(', '), minutes: perTopic });
      });
    });

    // Adjust agenda times to fit duration
    const agendaTotal = agendaItems.reduce((s, a) => s + a.minutes, 0);
    if (agendaTotal > duration) {
      const scale = duration / agendaTotal;
      agendaItems.forEach(a => { a.minutes = Math.max(5, Math.round(a.minutes * scale)); });
    }

    const srmNotes = grps.filter(g => g.srmInherited?.length).flatMap(g => g.srmInherited || []);
    if (srmNotes.length > 0) {
      agendaItems.push({ topic: `SRM Note: ${srmNotes.join('; ')}`, controls: '', minutes: 0 });
    }

    meetings.push({
      id: `mtg${meetingNum}`,
      topic: grps.map(g => g.topic).join(' & '),
      functions: grps.map(g => g.functions).join(' / '),
      controls: grps.map(g => g.controls.join(', ')).join('; '),
      duration,
      proserve: needsProserve ? 'Yes' : 'No',
      attendees: Array.from(allAttendees),
      agendaItems,
    });
    meetingNum++;
    currentMeeting = { groups: [], totalMin: 0 };
  };

  for (const group of groupMinutes) {
    const adjustedMin = Math.round(group.totalMinutes * compressionFactor);

    // If this group alone exceeds max duration, it gets its own meeting
    if (adjustedMin > maxDuration) {
      flushMeeting();
      currentMeeting.groups.push(group);
      currentMeeting.totalMin = adjustedMin;
      flushMeeting();
      continue;
    }

    // If adding this group would exceed max duration, flush and start new
    if (currentMeeting.totalMin + adjustedMin > maxDuration) {
      flushMeeting();
    }

    currentMeeting.groups.push(group);
    currentMeeting.totalMin += adjustedMin;
  }
  flushMeeting();

  return meetings;
}

// =========================================================================
// Persistence
// =========================================================================
const STORAGE_KEY = 'sas-engagements';
interface SavedEngagement { id: string; config: EngagementConfig; savedAt: string; }
const loadSaved = (): SavedEngagement[] => { try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch { return []; } };
const persistSaved = (e: SavedEngagement[]) => localStorage.setItem(STORAGE_KEY, JSON.stringify(e));

const FRAMEWORK_LABELS: Record<string, string> = { 'nist-csf': 'NIST CSF 2.0', 'nist-800-53': 'NIST 800-53 Rev 5', 'cmmc': 'CMMC Level 2' };

// =========================================================================
// Component
// =========================================================================
const EngagementSchedule: React.FC = () => {
  const [savedList, setSavedList] = useState<SavedEngagement[]>(loadSaved());
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [config, setConfig] = useState<EngagementConfig>({
    customerName: '', framework: 'nist-csf', scope: 'AWS Environment Only',
    regulator: '', engagementWeeks: 10, meetingFrequency: 'weekly', maxMeetingDuration: 75,
  });
  const [generated, setGenerated] = useState(false);
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [copied, setCopied] = useState(false);
  const [saved, setSaved] = useState(false);
  const [scheduleWarning, setScheduleWarning] = useState('');

  const doGenerate = () => {
    const groups = FRAMEWORK_GROUPS[config.framework] || [];
    const slotsPerWeek = config.meetingFrequency === 'weekly' ? 1 : 0.5;
    // Reserve 1 slot for kickoff, leave rest for interviews
    const interviewSlots = Math.floor(config.engagementWeeks * slotsPerWeek) - 1;
    const totalNeeded = groups.reduce((s, g) => s + g.controlCount * g.minutesPerControl, 0);
    const totalAvailable = interviewSlots * config.maxMeetingDuration;

    if (totalNeeded > totalAvailable * 1.3) {
      setScheduleWarning(`This schedule is compressed. ${totalNeeded} minutes of discussion time needed but only ${totalAvailable} minutes available across ${interviewSlots} interview slots. Consider increasing engagement duration or meeting length.`);
    } else if (totalNeeded < totalAvailable * 0.6) {
      setScheduleWarning(`This schedule has ample time. ${totalNeeded} minutes needed across ${totalAvailable} available. Meetings will include buffer time for deeper discussion.`);
    } else {
      setScheduleWarning('');
    }

    const mtgs = generateMeetings(groups, config.maxMeetingDuration, interviewSlots);
    setMeetings(mtgs);
    setGenerated(true);
  };

  const handleSave = () => {
    if (!config.customerName.trim()) return;
    const id = selectedId || `eng-${Date.now()}`;
    const updated = savedList.filter(e => e.id !== id);
    updated.push({ id, config: { ...config }, savedAt: new Date().toISOString() });
    persistSaved(updated);
    setSavedList(updated);
    setSelectedId(id);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const handleLoad = (id: string) => {
    const eng = savedList.find(e => e.id === id);
    if (eng) { setConfig(eng.config); setSelectedId(eng.id); doGenerate(); setGenerated(true); }
  };

  const handleDelete = (id: string) => {
    const updated = savedList.filter(e => e.id !== id);
    persistSaved(updated); setSavedList(updated);
    if (selectedId === id) { setSelectedId(null); setGenerated(false); }
  };

  const handleNew = () => {
    setSelectedId(null);
    setConfig({ customerName: '', framework: 'nist-csf', scope: 'AWS Environment Only', regulator: '', engagementWeeks: 10, meetingFrequency: 'weekly', maxMeetingDuration: 75 });
    setGenerated(false); setMeetings([]);
  };

  const generateReport = () => {
    let r = `${config.customerName || '[Customer Name]'}\n`;
    r += `${FRAMEWORK_LABELS[config.framework]} Stakeholder Interview Schedule\n\n`;
    r += `AWS Security Assurance Services (AWS SAS) - Advisory Engagement\n`;
    r += `Scope: ${config.scope}${config.regulator ? ` | Regulator: ${config.regulator}` : ''}\n`;
    r += `Duration: ${config.engagementWeeks} weeks | Cadence: ${config.meetingFrequency} | Max meeting: ${config.maxMeetingDuration} min\n\n`;
    r += `AWS SAS Advisory Notice: This schedule is advisory guidance only.\n\n`;
    r += `SRM Scoping Note: Scoped to ${config.scope}. AWS responsible for security of the cloud; customer responsible for security in the cloud.\n\n`;
    r += `--- SCHEDULE (${meetings.length} interviews + kickoff + buffer + close-out) ---\n\n`;
    r += `Kickoff: Engagement Overview & Scope Confirmation (90 min)\n\n`;
    meetings.forEach((m, i) => {
      r += `Meeting ${i + 1}: ${m.topic}\n`;
      r += `  Functions: ${m.functions} | Duration: ${m.duration} min | ProServe: ${m.proserve}\n`;
      r += `  Attendees: ${m.attendees.join(', ')}\n`;
      r += `  Agenda:\n`;
      m.agendaItems.forEach(a => { r += `    ${a.minutes} min — ${a.topic}\n`; });
      r += `\n`;
    });
    r += `Buffer: Evidence Collection & CPR Drafting (3+ weeks)\n`;
    r += `Session 1: Draft CPR Walkthrough (90 min)\n`;
    r += `Session 2: Recommendations Review & Close-Out (90 min)\n`;
    return r;
  };

  const copyReport = () => { navigator.clipboard.writeText(generateReport()); setCopied(true); setTimeout(() => setCopied(false), 2000); };

  const totalControlMinutes = (FRAMEWORK_GROUPS[config.framework] || []).reduce((s, g) => s + g.controlCount * g.minutesPerControl, 0);
  const totalControls = (FRAMEWORK_GROUPS[config.framework] || []).reduce((s, g) => s + g.controlCount, 0);

  return (
    <SpaceBetween size="l">
      {savedList.length > 0 && (
        <Container header={<Header variant="h3" description="Select a saved engagement or create a new one" actions={<Button onClick={handleNew} iconName="add-plus">New engagement</Button>}>Saved engagements</Header>}>
          <SpaceBetween size="s">
            {savedList.map(eng => (
              <div key={eng.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 14px', borderRadius: '8px', cursor: 'pointer', border: selectedId === eng.id ? '2px solid #0972d3' : '1px solid #e9ebed', background: selectedId === eng.id ? '#f2f8fd' : '#fff' }} onClick={() => handleLoad(eng.id)}>
                <SpaceBetween size="xxs">
                  <Box variant="strong">{eng.config.customerName}</Box>
                  <SpaceBetween size="xxs" direction="horizontal">
                    <Badge color="blue">{FRAMEWORK_LABELS[eng.config.framework]}</Badge>
                    <Box variant="small" color="text-body-secondary">{eng.config.engagementWeeks} weeks | {eng.config.maxMeetingDuration} min meetings</Box>
                  </SpaceBetween>
                </SpaceBetween>
                <Button variant="icon" iconName="remove" onClick={(e) => { e.stopPropagation(); handleDelete(eng.id); }} />
              </div>
            ))}
          </SpaceBetween>
        </Container>
      )}

      <Container header={<Header variant="h2" description="Configure engagement parameters — the schedule adapts to your timeline and framework complexity">Engagement Schedule Builder</Header>}>
        <SpaceBetween size="m">
          <ColumnLayout columns={2}>
            <FormField label="Customer name">
              <Input value={config.customerName} onChange={({ detail }) => setConfig({ ...config, customerName: detail.value })} placeholder="e.g., Acme Financial Corp" />
            </FormField>
            <FormField label="Compliance framework">
              <Select selectedOption={{ label: FRAMEWORK_LABELS[config.framework], value: config.framework }} onChange={({ detail }) => setConfig({ ...config, framework: detail.selectedOption.value || 'nist-csf' })} options={Object.entries(FRAMEWORK_LABELS).map(([v, l]) => ({ label: l, value: v }))} />
            </FormField>
            <FormField label="Engagement scope">
              <Input value={config.scope} onChange={({ detail }) => setConfig({ ...config, scope: detail.value })} placeholder="e.g., AWS Environment Only" />
            </FormField>
            <FormField label="Primary regulator (optional)">
              <Input value={config.regulator} onChange={({ detail }) => setConfig({ ...config, regulator: detail.value })} placeholder="e.g., OCC, FFIEC, DoD" />
            </FormField>
          </ColumnLayout>
          <ColumnLayout columns={3}>
            <FormField label="Interview weeks" description={`${totalControls} controls, ~${totalControlMinutes} min discussion time`}>
              <Select selectedOption={{ label: `${config.engagementWeeks} weeks`, value: String(config.engagementWeeks) }} onChange={({ detail }) => setConfig({ ...config, engagementWeeks: parseInt(detail.selectedOption.value || '10') })} options={[4,6,8,10,12,14,16].map(w => ({ label: `${w} weeks`, value: String(w) }))} />
            </FormField>
            <FormField label="Meeting frequency">
              <Select selectedOption={{ label: config.meetingFrequency === 'weekly' ? 'Weekly (1/week)' : 'Bi-weekly (1/2 weeks)', value: config.meetingFrequency }} onChange={({ detail }) => setConfig({ ...config, meetingFrequency: detail.selectedOption.value || 'weekly' })} options={[{ label: 'Weekly (1/week)', value: 'weekly' }, { label: 'Bi-weekly (1/2 weeks)', value: 'biweekly' }]} />
            </FormField>
            <FormField label="Max meeting duration">
              <Select selectedOption={{ label: `${config.maxMeetingDuration} minutes`, value: String(config.maxMeetingDuration) }} onChange={({ detail }) => setConfig({ ...config, maxMeetingDuration: parseInt(detail.selectedOption.value || '75') })} options={[{ label: '60 minutes', value: '60' }, { label: '75 minutes', value: '75' }, { label: '90 minutes', value: '90' }]} />
            </FormField>
          </ColumnLayout>
          <SpaceBetween size="xs" direction="horizontal">
            <Button variant="primary" onClick={() => { doGenerate(); handleSave(); }}>Generate schedule</Button>
            <Button onClick={handleSave} iconName={saved ? 'check' : 'upload'} disabled={!config.customerName.trim()}>{saved ? 'Saved' : 'Save engagement'}</Button>
            {generated && <Button iconName={copied ? 'check' : 'copy'} onClick={copyReport}>{copied ? 'Copied' : 'Copy full report'}</Button>}
          </SpaceBetween>
        </SpaceBetween>
      </Container>

      {generated && meetings.length > 0 && (
        <>
          {scheduleWarning && <Alert type={scheduleWarning.includes('compressed') ? 'warning' : 'info'}>{scheduleWarning}</Alert>}

          <Alert type="info">AWS SAS Advisory Notice: This schedule is advisory guidance only. Legal counsel should be consulted for regulatory interpretation.</Alert>

          <Container header={<Header variant="h3">Shared Responsibility Model (SRM) Scoping Note</Header>}>
            <Box>This engagement is scoped to <Box variant="strong" display="inline">{config.scope}</Box>. AWS is responsible for security of the cloud. {config.customerName || 'The customer'} is responsible for security in the cloud.</Box>
          </Container>

          <Container header={<Header variant="h2" description={`Kickoff + ${meetings.length} interview sessions + buffer + 2 close-out sessions`}>{config.customerName || '[Customer]'} — {FRAMEWORK_LABELS[config.framework]} Interview Schedule</Header>}>
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
                      <Box key={i} variant="small">
                        <Badge color="grey">{a.minutes} min</Badge>{' '}{a.topic}
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
