import React, { useState, useEffect } from 'react';
import { complianceApi, Control, Question, ControlDetail, Framework } from '../services/complianceApi';
import AppLayout from '@cloudscape-design/components/app-layout';
import Container from '@cloudscape-design/components/container';
import Header from '@cloudscape-design/components/header';
import SpaceBetween from '@cloudscape-design/components/space-between';
import TextFilter from '@cloudscape-design/components/text-filter';
import Select from '@cloudscape-design/components/select';
import ExpandableSection from '@cloudscape-design/components/expandable-section';
import Badge from '@cloudscape-design/components/badge';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import Button from '@cloudscape-design/components/button';
import Textarea from '@cloudscape-design/components/textarea';
import Alert from '@cloudscape-design/components/alert';
import Spinner from '@cloudscape-design/components/spinner';
import Box from '@cloudscape-design/components/box';
import Modal from '@cloudscape-design/components/modal';
import Sidebar from './Sidebar';
import Dashboard from './Dashboard';
import InterviewMode from './InterviewMode';
import AWSImplementationGuide from './AWSImplementationGuide';
import Settings from './Settings';
import ExportPanel from './ExportPanel';
import './ComplianceQuestionnaire.css';

// NIST 800-53 Family Name Mappings
const NIST_FAMILY_NAMES: Record<string, string> = {
  'ac': 'Access Control',
  'at': 'Awareness and Training',
  'au': 'Audit and Accountability',
  'ca': 'Assessment, Authorization, and Monitoring',
  'cm': 'Configuration Management',
  'cp': 'Contingency Planning',
  'ia': 'Identification and Authentication',
  'ir': 'Incident Response',
  'ma': 'Maintenance',
  'mp': 'Media Protection',
  'pe': 'Physical and Environmental Protection',
  'pl': 'Planning',
  'pm': 'Program Management',
  'ps': 'Personnel Security',
  'pt': 'PII Processing and Transparency',
  'ra': 'Risk Assessment',
  'sa': 'System and Services Acquisition',
  'sc': 'System and Communications Protection',
  'si': 'System and Information Integrity',
  'sr': 'Supply Chain Risk Management'
};

// CSF Function Name Mappings
const CSF_FUNCTION_NAMES: Record<string, string> = {
  'gv': 'Govern',
  'id': 'Identify',
  'pr': 'Protect',
  'de': 'Detect',
  'rs': 'Respond',
  'rc': 'Recover'
};

// CMMC Domain Name Mappings
const CMMC_DOMAIN_NAMES: Record<string, string> = {
  'ac': 'Access Control',
  'at': 'Awareness and Training',
  'au': 'Audit and Accountability',
  'cm': 'Configuration Management',
  'ia': 'Identification and Authentication',
  'ir': 'Incident Response',
  'ma': 'Maintenance',
  'mp': 'Media Protection',
  'pe': 'Physical Protection',
  'ps': 'Personnel Security',
  'ra': 'Risk Assessment',
  'ca': 'Security Assessment',
  'sc': 'System and Communications Protection',
  'si': 'System and Information Integrity'
};

// Badge color mapping for NIST 800-53 families (Cloudscape badge colors)
const NIST_FAMILY_BADGE_COLORS: Record<string, 'blue' | 'grey' | 'green' | 'red'> = {
  'ac': 'blue', 'at': 'grey', 'au': 'blue', 'ca': 'green',
  'cm': 'green', 'cp': 'red', 'ia': 'blue', 'ir': 'red',
  'ma': 'grey', 'mp': 'grey', 'pe': 'grey', 'pl': 'green',
  'pm': 'green', 'ps': 'blue', 'pt': 'grey', 'ra': 'green',
  'sa': 'green', 'sc': 'blue', 'si': 'blue', 'sr': 'green'
};

// Badge color mapping for CSF functions (Cloudscape badge colors)
const CSF_FUNCTION_BADGE_COLORS: Record<string, 'blue' | 'grey' | 'green' | 'red'> = {
  'gv': 'grey', 'id': 'blue', 'pr': 'green',
  'de': 'red', 'rs': 'red', 'rc': 'blue'
};

// Badge color mapping for CMMC domains (Cloudscape badge colors)
const CMMC_DOMAIN_BADGE_COLORS: Record<string, 'blue' | 'grey' | 'green' | 'red'> = {
  'ac': 'blue', 'at': 'grey', 'au': 'blue', 'cm': 'green',
  'ia': 'blue', 'ir': 'red', 'ma': 'grey', 'mp': 'grey',
  'pe': 'grey', 'ps': 'blue', 'ra': 'green', 'ca': 'green',
  'sc': 'blue', 'si': 'blue'
};

// Accent hex colors for left-border strips — Cloudscape design token palette
// CSF functions: each gets a unique, distinguishable color
const CSF_FUNCTION_ACCENT_COLORS: Record<string, string> = {
  'gv': '#687078', // Grey — Governance
  'id': '#0073BB', // Teal/Blue — Identify
  'pr': '#037F0C', // Green — Protect
  'de': '#D45B07', // Orange — Detect
  'rs': '#D13212', // Red — Respond
  'rc': '#00838F', // Dark Cyan — Recover
};

// CMMC domain accent colors for left-border strips
const CMMC_DOMAIN_ACCENT_COLORS: Record<string, string> = {
  // Access & Identity — Blue
  'ac': '#0073BB', 'ia': '#0073BB', 'ps': '#0073BB',
  // Monitoring & Audit — Teal
  'au': '#00838F', 'ca': '#00838F', 'si': '#00838F',
  // Protection & Config — Green
  'cm': '#037F0C', 'sc': '#037F0C',
  // Risk — Purple
  'ra': '#6B40B8',
  // Operations — Orange
  'ma': '#D45B07', 'mp': '#D45B07', 'ir': '#D45B07',
  // People & Physical — Grey
  'at': '#687078', 'pe': '#687078',
};

// NIST 800-53 families grouped by domain
const NIST_FAMILY_ACCENT_COLORS: Record<string, string> = {
  // Access & Identity — Blue
  'ac': '#0073BB', 'ia': '#0073BB', 'ps': '#0073BB',
  // Monitoring & Audit — Teal
  'au': '#00838F', 'ca': '#00838F', 'si': '#00838F',
  // Protection & Config — Green
  'cm': '#037F0C', 'cp': '#037F0C', 'sc': '#037F0C', 'sr': '#037F0C',
  // Risk & Planning — Purple
  'ra': '#6B40B8', 'sa': '#6B40B8', 'pl': '#6B40B8', 'pm': '#6B40B8',
  // Operations — Orange
  'ma': '#D45B07', 'mp': '#D45B07', 'pe': '#D45B07', 'ir': '#D45B07',
  // People & Privacy — Grey
  'at': '#687078', 'pt': '#687078',
};

// Question type badge colors
const QUESTION_TYPE_COLORS: Record<string, 'blue' | 'grey' | 'green' | 'red'> = {
  'implementation': 'blue',
  'evidence': 'green',
  'second_line_defense': 'grey',
  'third_line_defense': 'grey',
  'audit_readiness': 'red',
};

const getFamilyFullName = (familyCode: string, framework: string): string => {
  const code = familyCode.toLowerCase();
  if (framework === 'nist-csf') {
    return CSF_FUNCTION_NAMES[code] || familyCode.toUpperCase();
  }
  if (framework === 'cmmc') {
    return CMMC_DOMAIN_NAMES[code] || familyCode.toUpperCase();
  }
  return NIST_FAMILY_NAMES[code] || familyCode.toUpperCase();
};

const getFamilyColor = (familyCode: string, framework: string): 'blue' | 'grey' | 'green' | 'red' => {
  const code = familyCode.toLowerCase();
  if (framework === 'nist-csf') {
    return CSF_FUNCTION_BADGE_COLORS[code] || 'grey';
  }
  if (framework === 'cmmc') {
    return CMMC_DOMAIN_BADGE_COLORS[code] || 'grey';
  }
  return NIST_FAMILY_BADGE_COLORS[code] || 'grey';
};

const getAccentColor = (familyCode: string, framework: string): string => {
  const code = familyCode.toLowerCase();
  if (framework === 'nist-csf') {
    return CSF_FUNCTION_ACCENT_COLORS[code] || '#687078';
  }
  if (framework === 'cmmc') {
    return CMMC_DOMAIN_ACCENT_COLORS[code] || '#687078';
  }
  return NIST_FAMILY_ACCENT_COLORS[code] || '#687078';
};

const getColorEmoji = (familyCode: string, framework: string): string => {
  const accent = getAccentColor(familyCode, framework);
  // Map accent hex to colored circle for dropdown labels
  const emojiMap: Record<string, string> = {
    '#6B40B8': '🟣',
    '#0073BB': '🔵',
    '#037F0C': '🟢',
    '#D45B07': '🟠',
    '#D13212': '🔴',
    '#00838F': '🔵',
    '#687078': '⚪',
  };
  return emojiMap[accent] || '⚪';
};

const getQuestionTypeBadgeColor = (questionType: string): 'blue' | 'grey' | 'green' | 'red' => {
  return QUESTION_TYPE_COLORS[questionType.toLowerCase()] || 'blue';
};

interface ComplianceQuestionnaireProps {
  sessionId?: string;
}

const ComplianceQuestionnaire: React.FC<ComplianceQuestionnaireProps> = ({ sessionId: initialSessionId }) => {
  const [controls, setControls] = useState<Control[]>([]);
  const [selectedControl, setSelectedControl] = useState<ControlDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedControl, setExpandedControl] = useState<string | null>(null);
  const [responses, setResponses] = useState<Record<string, string>>({});
  const [selectedFamily, setSelectedFamily] = useState<string>('all');
  const [selectedResponsibility, setSelectedResponsibility] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeView, setActiveView] = useState<string>('questionnaire');
  const [allQuestions, setAllQuestions] = useState<Record<string, Question[]>>({});
  const [interviewControl, setInterviewControl] = useState<ControlDetail | null>(null);
  const [sessionId, setSessionId] = useState<string | undefined>(initialSessionId);
  const [showExportModal, setShowExportModal] = useState(false);
  const [selectedFramework, setSelectedFramework] = useState<string>('nist-800-53');
  const [frameworks, setFrameworks] = useState<Framework[]>([]);
  const [frameworkLabel, setFrameworkLabel] = useState<string>('NIST 800-53 Rev 5 Moderate Baseline');

  useEffect(() => {
    loadFrameworks();
  }, []);

  useEffect(() => {
    setSelectedFamily('all');
    setSelectedResponsibility('all');
    setSearchQuery('');
    setExpandedControl(null);
    setSelectedControl(null);
    setAllQuestions({});
    loadControls();
  }, [selectedFramework]);

  useEffect(() => {
    loadControls();
  }, [selectedFamily]);

  const loadFrameworks = async () => {
    try {
      const data = await complianceApi.getFrameworks();
      setFrameworks(data.frameworks);
    } catch (err) {
      console.error('Failed to load frameworks:', err);
    }
  };

  const loadControls = async () => {
    try {
      setLoading(true);
      const family = selectedFamily === 'all' ? undefined : selectedFamily;
      const data = await complianceApi.getControls(family, selectedFramework);
      setControls(data.controls);
      if (data.framework_label) {
        setFrameworkLabel(data.framework_label);
      }
      setError(null);
    } catch (err) {
      setError('Failed to load controls. Please ensure the API server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadControlDetail = async (controlId: string) => {
    try {
      const detail = await complianceApi.getControl(controlId, selectedFramework);
      setSelectedControl(detail);
      setExpandedControl(controlId);
      setAllQuestions(prev => ({
        ...prev,
        [controlId]: detail.questions
      }));
    } catch (err) {
      setError(`Failed to load control ${controlId}`);
      console.error(err);
    }
  };

  const handleResponseChange = (questionId: string, value: string) => {
    setResponses(prev => ({ ...prev, [questionId]: value }));
  };

  const saveResponse = async (questionId: string) => {
    if (!sessionId) return;
    try {
      await complianceApi.recordResponse(sessionId, {
        question_id: questionId,
        answer: responses[questionId] || '',
      });
    } catch (err) {
      console.error('Failed to save response:', err);
    }
  };

  const families = Array.from(new Set(controls.map(c => c.family))).sort();

  const filteredControls = controls.filter(control => {
    const matchesFamily = selectedFamily === 'all' || control.family === selectedFamily;
    const matchesSearch = searchQuery === '' ||
      control.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      control.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      control.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesResponsibility = selectedResponsibility === 'all' || control.aws_responsibility === selectedResponsibility;
    return matchesFamily && matchesSearch && matchesResponsibility;
  });

  const totalQuestions = Object.values(allQuestions).flat().length;
  const answeredQuestions = Object.keys(responses).length;
  const isCSF = selectedFramework === 'nist-csf';

  if (loading) {
    return (
      <div style={{ display: 'flex', height: '100vh' }}>
        <Sidebar activeView={activeView} onViewChange={setActiveView} controlCount={0} completionRate={0} />
        <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <SpaceBetween size="m" direction="vertical" alignItems="center">
            <Spinner size="large" />
            <Box variant="p" color="text-body-secondary">Loading controls</Box>
          </SpaceBetween>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ display: 'flex', height: '100vh' }}>
        <Sidebar activeView={activeView} onViewChange={setActiveView} controlCount={0} completionRate={0} />
        <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}>
          <Alert type="error" header="Connection error">
            {error}
          </Alert>
        </div>
      </div>
    );
  }

  return (
    <>
      <AppLayout
        navigation={
          <Sidebar
            activeView={activeView}
            onViewChange={setActiveView}
            controlCount={controls.length}
            completionRate={totalQuestions > 0 ? Math.round((answeredQuestions / totalQuestions) * 100) : 0}
          />
        }
        navigationOpen={true}
        navigationWidth={280}
        maxContentWidth={Number.MAX_VALUE}
        content={
          <SpaceBetween size="l">
            {/* Header section */}
            <Container>
              <SpaceBetween size="m">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <Header
                    variant="h1"
                    description={`${filteredControls.length} ${filteredControls.length === controls.length ? (isCSF ? 'subcategories' : 'controls') : `of ${controls.length} ${isCSF ? 'subcategories' : 'controls'}`}`}
                  >
                    {frameworkLabel}
                  </Header>

                  <SpaceBetween size="xs" direction="horizontal">
                    <Select
                      selectedOption={
                        frameworks.find(f => f.id === selectedFramework)
                          ? { label: frameworks.find(f => f.id === selectedFramework)!.label, value: selectedFramework }
                          : { label: 'NIST 800-53 Rev 5 Moderate Baseline', value: 'nist-800-53' }
                      }
                      onChange={({ detail }) => setSelectedFramework(detail.selectedOption.value || 'nist-800-53')}
                      options={frameworks.map(f => ({ label: f.label, value: f.id }))}
                      placeholder="Choose framework"
                    />
                    <Button
                      variant="primary"
                      iconName="download"
                      onClick={() => setShowExportModal(true)}
                    >
                      Export responses
                    </Button>
                  </SpaceBetween>
                </div>

                <SpaceBetween size="xs" direction="horizontal">
                  {selectedResponsibility !== 'all' && (
                    <Badge color={
                      selectedResponsibility === 'aws' ? 'red' :
                      selectedResponsibility === 'shared' ? 'green' : 'blue'
                    }>
                      {selectedResponsibility === 'aws' ? 'AWS only' :
                       selectedResponsibility === 'shared' ? 'Shared' : 'Customer only'}
                    </Badge>
                  )}
                  {selectedFamily !== 'all' && (
                    <Badge color={getFamilyColor(selectedFamily, selectedFramework)}>
                      {selectedFamily.toUpperCase()} - {getFamilyFullName(selectedFamily, selectedFramework)}
                    </Badge>
                  )}
                </SpaceBetween>
              </SpaceBetween>
            </Container>

            {/* Filters */}
            <div style={{ background: '#FAFAFA', borderRadius: '8px', padding: '2px' }}>
            <Container>
              <SpaceBetween size="m" direction="horizontal">
                <div style={{ flex: 1 }}>
                  <TextFilter
                    filteringText={searchQuery}
                    filteringPlaceholder={isCSF ? 'Find subcategories' : 'Find controls'}
                    onChange={({ detail }) => setSearchQuery(detail.filteringText)}
                    countText={`${filteredControls.length} ${filteredControls.length === 1 ? 'match' : 'matches'}`}
                  />
                </div>

                <Select
                  selectedOption={
                    selectedFamily === 'all'
                      ? { label: isCSF ? 'All functions' : 'All families', value: 'all' }
                      : { label: `${getColorEmoji(selectedFamily, selectedFramework)} ${selectedFamily.toUpperCase()} - ${getFamilyFullName(selectedFamily, selectedFramework)}`, value: selectedFamily }
                  }
                  onChange={({ detail }) => setSelectedFamily(detail.selectedOption.value || 'all')}
                  options={[
                    { label: isCSF ? 'All functions' : 'All families', value: 'all' },
                    ...families.map(family => ({
                      label: `${getColorEmoji(family, selectedFramework)} ${family.toUpperCase()} - ${getFamilyFullName(family, selectedFramework)}`,
                      value: family
                    }))
                  ]}
                  placeholder={isCSF ? 'Choose function' : 'Choose family'}
                />

                {(
                  <Select
                    selectedOption={
                      selectedResponsibility === 'all'
                        ? { label: 'All responsibilities', value: 'all' }
                        : selectedResponsibility === 'aws'
                        ? { label: '🔴 AWS only', value: 'aws' }
                        : selectedResponsibility === 'shared'
                        ? { label: '🟢 Shared', value: 'shared' }
                        : { label: '🔵 Customer only', value: 'customer' }
                    }
                    onChange={({ detail }) => setSelectedResponsibility(detail.selectedOption.value || 'all')}
                    options={[
                      { label: 'All responsibilities', value: 'all' },
                      { label: '🔴 AWS only', value: 'aws' },
                      { label: '🟢 Shared', value: 'shared' },
                      { label: '🔵 Customer only', value: 'customer' }
                    ]}
                    placeholder="Choose responsibility"
                  />
                )}
              </SpaceBetween>
            </Container>
            </div>

            {/* Content views */}
            {activeView === 'dashboard' && (
              <Dashboard
                totalControls={controls.length}
                answeredQuestions={answeredQuestions}
                totalQuestions={totalQuestions}
              />
            )}

            {activeView === 'settings' && (
              <Settings
                sessionId={sessionId}
                onSessionChange={setSessionId}
              />
            )}

            {activeView === 'questionnaire' && (
              <SpaceBetween size="m">
                {filteredControls.map(control => {
                  const controlQuestions = allQuestions[control.id] || [];
                  const answeredCount = controlQuestions.filter(q => responses[q.id]).length;
                  const isComplete = answeredCount === controlQuestions.length && controlQuestions.length > 0;
                  const accentColor = getAccentColor(control.family, selectedFramework);

                  return (
                    <div
                      key={control.id}
                      style={{
                        borderLeft: `4px solid ${accentColor}`,
                        borderRadius: '4px',
                      }}
                    >
                    <ExpandableSection
                      variant="container"
                      headerText={
                        <SpaceBetween size="xs" direction="horizontal">
                          <StatusIndicator type={isComplete ? 'success' : 'pending'}>
                            {control.id.toUpperCase()}
                          </StatusIndicator>
                          <Badge color={getFamilyColor(control.family, selectedFramework)}>
                            {isCSF
                              ? `${control.family.toUpperCase()} - ${getFamilyFullName(control.family, selectedFramework)}`
                              : control.family.toUpperCase()
                            }
                          </Badge>
                          {isCSF && control.category_name && (
                            <Badge color="grey">{control.category_name}</Badge>
                          )}
                          {controlQuestions.length > 0 && (
                            <Badge color="blue">
                              {answeredCount}/{controlQuestions.length} answered
                            </Badge>
                          )}
                          {control.aws_responsibility && (
                            <>
                              <span style={{ color: '#687078', margin: '0 4px' }}>—</span>
                              <span style={{ color: '#687078', fontSize: '12px' }}>Ownership:</span>
                              <Badge color={
                                control.aws_responsibility === 'aws' ? 'red'
                                : control.aws_responsibility === 'shared' ? 'green'
                                : 'blue'
                              }>
                                {control.aws_responsibility === 'aws' ? 'AWS only'
                                : control.aws_responsibility === 'shared' ? 'Shared'
                                : 'Customer only'}
                              </Badge>
                            </>
                          )}
                        </SpaceBetween>
                      }
                      headerDescription={control.title}
                      expanded={expandedControl === control.id}
                      onChange={({ detail }) => {
                        if (detail.expanded) {
                          loadControlDetail(control.id);
                        } else {
                          setExpandedControl(null);
                          setSelectedControl(null);
                        }
                      }}
                    >
                      {selectedControl && expandedControl === control.id && (
                        <SpaceBetween size="l">
                          {control.title !== control.description && (
                            <Box variant="p">{control.description}</Box>
                          )}

                          {controlQuestions.length > 0 && (
                            <Button
                              variant="primary"
                              onClick={async () => {
                                const detail = await complianceApi.getControl(control.id, selectedFramework);
                                setInterviewControl(detail);
                              }}
                            >
                              Start interview
                            </Button>
                          )}

                          {/* Organizational Requirements (non-AWS controls) */}
                          {selectedControl.organizational_requirements && selectedControl.organizational_requirements.length > 0 && (
                            <Container
                              header={
                                <Header
                                  variant="h3"
                                  description="Policies, processes, and governance controls needed alongside AWS technical controls"
                                  counter={`(${selectedControl.organizational_requirements.length})`}
                                >
                                  Organizational requirements
                                </Header>
                              }
                            >
                              <SpaceBetween size="m">
                                {selectedControl.organizational_requirements.map((req, idx) => {
                                  const meta = selectedControl.organizational_category_metadata?.[req.category];
                                  const badgeColor: 'blue' | 'grey' | 'green' | 'red' =
                                    req.category === 'POLICY' ? 'blue' :
                                    req.category === 'PROCESS' ? 'green' :
                                    req.category === 'GOVERNANCE' ? 'blue' :
                                    req.category === 'TRAINING' ? 'red' :
                                    req.category === 'DOCUMENTATION' ? 'grey' :
                                    'grey';
                                  return (
                                    <div key={idx} style={{ borderLeft: `3px solid ${meta?.color || '#687078'}`, paddingLeft: '12px' }}>
                                      <SpaceBetween size="xxs">
                                        <SpaceBetween size="xs" direction="horizontal">
                                          <Badge color={badgeColor}>{meta?.label || req.category}</Badge>
                                          <Box variant="strong">{req.title}</Box>
                                        </SpaceBetween>
                                        <Box variant="p" color="text-body-secondary">{req.description}</Box>
                                      </SpaceBetween>
                                    </div>
                                  );
                                })}
                              </SpaceBetween>
                            </Container>
                          )}

                          {/* AWS Implementation Guide */}
                          {((selectedControl.aws_controls && selectedControl.aws_controls.length > 0) ||
                            (selectedControl.preventive_controls &&
                              ((selectedControl.preventive_controls.scps && selectedControl.preventive_controls.scps.length > 0) ||
                               (selectedControl.preventive_controls.opa_rules && selectedControl.preventive_controls.opa_rules.length > 0)))) && (
                            <AWSImplementationGuide
                              controlId={selectedControl.control.id}
                              awsControls={selectedControl.aws_controls || []}
                              framework={selectedFramework}
                              preventiveControls={selectedControl.preventive_controls}
                            />
                          )}

                          {/* Framework Relevance */}
                          {selectedControl.framework_relevance && selectedControl.framework_relevance.relevant_frameworks.length > 0 && (
                            <Container header={<Header variant="h3">Relevant compliance frameworks</Header>}>
                              <SpaceBetween size="s">
                                <SpaceBetween size="xs" direction="horizontal">
                                  {selectedControl.framework_relevance.relevant_frameworks.map((framework, idx) => (
                                    <Badge key={idx}>{framework}</Badge>
                                  ))}
                                </SpaceBetween>
                                {selectedControl.framework_relevance.has_specific_mappings && (
                                  <Box variant="small">Specific framework mappings available for this control</Box>
                                )}
                                <Box variant="small" color="text-body-secondary">
                                  {selectedControl.framework_relevance.notes}
                                </Box>
                              </SpaceBetween>
                            </Container>
                          )}

                          {/* AWS Hints (fallback) */}
                          {(!selectedControl.aws_controls || selectedControl.aws_controls.length === 0) &&
                           selectedControl.aws_hints.length > 0 && (
                            <Container header={<Header variant="h3">AWS managed controls</Header>}>
                              <ul>
                                {selectedControl.aws_hints.map((hint, idx) => (
                                  <li key={idx}>{hint}</li>
                                ))}
                              </ul>
                            </Container>
                          )}

                          {/* Questions */}
                          {selectedControl.questions.length > 0 && (
                            <>
                              {/* AWS Guidance - control level, shown once above all questions */}
                              {(() => {
                                const guidance = selectedControl.questions
                                  .map(q => q.aws_service_guidance)
                                  .find(g => g);
                                return guidance ? (
                                  <Alert type="info" header="AWS guidance">
                                    {guidance}
                                  </Alert>
                                ) : null;
                              })()}
                            <Container header={
                              <Header
                                variant="h3"
                                counter={`(${selectedControl.questions.length})`}
                              >
                                Discovery questions
                              </Header>
                            }>
                              <SpaceBetween size="m">
                                {selectedControl.questions.map((question, idx) => {
                                  const isAnswered = !!responses[question.id];
                                  return (
                                    <Container key={question.id}>
                                      <SpaceBetween size="m">
                                        <SpaceBetween size="xs" direction="horizontal">
                                          <Badge>{idx + 1}</Badge>
                                          <Badge color={getQuestionTypeBadgeColor(question.question_type)}>
                                            {question.question_type.replace(/_/g, ' ').toUpperCase()}
                                          </Badge>
                                          {isAnswered && (
                                            <Badge color="green">Answered</Badge>
                                          )}
                                        </SpaceBetween>

                                        <Box variant="p">{question.question_text}</Box>

                                        <Textarea
                                          value={responses[question.id] || ''}
                                          onChange={({ detail }) => handleResponseChange(question.id, detail.value)}
                                          onBlur={() => saveResponse(question.id)}
                                          placeholder="Enter your detailed response here"
                                          rows={6}
                                        />
                                      </SpaceBetween>
                                    </Container>
                                  );
                                })}
                              </SpaceBetween>
                            </Container>
                            </>
                          )}
                        </SpaceBetween>
                      )}
                    </ExpandableSection>
                    </div>
                  );
                })}
              </SpaceBetween>
            )}
          </SpaceBetween>
        }
        toolsHide
      />

      {/* Export Modal */}
      <Modal
        visible={showExportModal}
        onDismiss={() => setShowExportModal(false)}
        header="Export questionnaire"
        size="medium"
      >
        <ExportPanel onClose={() => setShowExportModal(false)} />
      </Modal>

      {/* Interview Mode Modal */}
      {interviewControl && (
        <InterviewMode
          control={interviewControl}
          responses={responses}
          onResponseChange={handleResponseChange}
          onSave={saveResponse}
          onClose={() => setInterviewControl(null)}
          framework={selectedFramework}
        />
      )}
    </>
  );
};

export default ComplianceQuestionnaire;
