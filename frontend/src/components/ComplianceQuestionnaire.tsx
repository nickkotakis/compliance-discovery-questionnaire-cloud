import React, { useState, useEffect } from 'react';
import { complianceApi, Control, Question, ControlDetail } from '../services/complianceApi';
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
const FAMILY_NAMES: Record<string, string> = {
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

// Color mapping for control families
const FAMILY_COLORS: Record<string, 'blue' | 'grey' | 'green' | 'red'> = {
  'ac': 'blue',      // Access Control
  'at': 'grey',      // Awareness and Training
  'au': 'blue',      // Audit and Accountability
  'ca': 'green',     // Assessment, Authorization, and Monitoring
  'cm': 'blue',      // Configuration Management
  'cp': 'red',       // Contingency Planning
  'ia': 'blue',      // Identification and Authentication
  'ir': 'red',       // Incident Response
  'ma': 'grey',      // Maintenance
  'mp': 'grey',      // Media Protection
  'pe': 'grey',      // Physical and Environmental Protection
  'pl': 'green',     // Planning
  'pm': 'green',     // Program Management
  'ps': 'grey',      // Personnel Security
  'pt': 'blue',      // PII Processing and Transparency
  'ra': 'green',     // Risk Assessment
  'sa': 'green',     // System and Services Acquisition
  'sc': 'blue',      // System and Communications Protection
  'si': 'blue',      // System and Information Integrity
  'sr': 'green'      // Supply Chain Risk Management
};

const getFamilyFullName = (familyCode: string): string => {
  return FAMILY_NAMES[familyCode.toLowerCase()] || familyCode.toUpperCase();
};

const getFamilyColor = (familyCode: string): 'blue' | 'grey' | 'green' | 'red' => {
  return FAMILY_COLORS[familyCode.toLowerCase()] || 'grey';
};

const getColorEmoji = (familyCode: string): string => {
  const color = getFamilyColor(familyCode);
  switch (color) {
    case 'blue': return '🔵';
    case 'green': return '🟢';
    case 'red': return '🔴';
    case 'grey': return '⚪';
    default: return '⚪';
  }
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

  useEffect(() => {
    loadControls();
  }, [selectedFamily]);

  const loadControls = async () => {
    try {
      setLoading(true);
      const family = selectedFamily === 'all' ? undefined : selectedFamily;
      const data = await complianceApi.getControls(family);
      setControls(data.controls);
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
      const detail = await complianceApi.getControl(controlId);
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
    setResponses(prev => ({
      ...prev,
      [questionId]: value
    }));
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

  if (loading) {
    return (
      <div style={{ display: 'flex', height: '100vh' }}>
        <Sidebar activeView={activeView} onViewChange={setActiveView} controlCount={0} completionRate={0} />
        <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <SpaceBetween size="m" direction="vertical" alignItems="center">
            <Spinner size="large" />
            <Box variant="p" color="text-body-secondary">Loading controls...</Box>
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
            {/* Header Section */}
            <Container>
              <SpaceBetween size="m">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <Header
                    variant="h1"
                    description={`Comprehensive compliance assessment questionnaire • ${filteredControls.length} ${filteredControls.length === controls.length ? 'controls' : `of ${controls.length} controls`}`}
                  >
                    NIST 800-53 Rev 5 Moderate Baseline
                  </Header>
                  
                  <Button
                    variant="primary"
                    iconName="download"
                    onClick={() => setShowExportModal(true)}
                  >
                    Export responses
                  </Button>
                </div>
                
                <SpaceBetween size="xs" direction="horizontal">
                  {selectedResponsibility !== 'all' && (
                    <Badge color={
                      selectedResponsibility === 'aws' ? 'red' : 
                      selectedResponsibility === 'shared' ? 'green' : 'blue'
                    }>
                      {selectedResponsibility === 'aws' ? 'AWS Only' : 
                       selectedResponsibility === 'shared' ? 'Shared' : 'Customer Only'}
                    </Badge>
                  )}
                  
                  {selectedFamily !== 'all' && (
                    <Badge color={getFamilyColor(selectedFamily)}>
                      {selectedFamily.toUpperCase()} - {getFamilyFullName(selectedFamily)}
                    </Badge>
                  )}
                </SpaceBetween>
              </SpaceBetween>
            </Container>

            {/* Filters */}
            <Container>
              <SpaceBetween size="m" direction="horizontal">
                <div style={{ flex: 1 }}>
                  <TextFilter
                    filteringText={searchQuery}
                    filteringPlaceholder="Find controls"
                    onChange={({ detail }) => setSearchQuery(detail.filteringText)}
                    countText={`${filteredControls.length} ${filteredControls.length === 1 ? 'match' : 'matches'}`}
                  />
                </div>
                
                <Select
                  selectedOption={
                    selectedFamily === 'all' 
                      ? { label: 'All families', value: 'all' }
                      : { label: `${getColorEmoji(selectedFamily)} ${selectedFamily.toUpperCase()} - ${getFamilyFullName(selectedFamily)}`, value: selectedFamily }
                  }
                  onChange={({ detail }) => setSelectedFamily(detail.selectedOption.value || 'all')}
                  options={[
                    { label: 'All families', value: 'all' },
                    ...families.map(family => ({
                      label: `${getColorEmoji(family)} ${family.toUpperCase()} - ${getFamilyFullName(family)}`,
                      value: family
                    }))
                  ]}
                  placeholder="Choose family"
                />
                
                <Select
                  selectedOption={
                    selectedResponsibility === 'all'
                      ? { label: 'All responsibilities', value: 'all' }
                      : selectedResponsibility === 'aws'
                      ? { label: '🔴 AWS Only', value: 'aws' }
                      : selectedResponsibility === 'shared'
                      ? { label: '🟢 Shared', value: 'shared' }
                      : { label: '🔵 Customer Only', value: 'customer' }
                  }
                  onChange={({ detail }) => setSelectedResponsibility(detail.selectedOption.value || 'all')}
                  options={[
                    { label: 'All responsibilities', value: 'all' },
                    { label: '🔴 AWS Only', value: 'aws' },
                    { label: '🟢 Shared', value: 'shared' },
                    { label: '🔵 Customer Only', value: 'customer' }
                  ]}
                  placeholder="Choose responsibility"
                />
              </SpaceBetween>
            </Container>

            {/* Content Views */}
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
                  
                  return (
                    <ExpandableSection
                      key={control.id}
                      variant="container"
                      headerText={
                        <SpaceBetween size="xs" direction="horizontal">
                          <StatusIndicator type={isComplete ? 'success' : 'pending'}>
                            {control.id.toUpperCase()}
                          </StatusIndicator>
                          <Badge color={getFamilyColor(control.family)}>
                            {control.family.toUpperCase()}
                          </Badge>
                          {controlQuestions.length > 0 && (
                            <Badge color="blue">
                              {answeredCount}/{controlQuestions.length} answered
                            </Badge>
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
                          <Box variant="p">{control.description}</Box>
                          
                          {controlQuestions.length > 0 && (
                            <Button
                              variant="primary"
                              onClick={async () => {
                                const detail = await complianceApi.getControl(control.id);
                                setInterviewControl(detail);
                              }}
                            >
                              Start interview
                            </Button>
                          )}

                          {/* AWS Implementation Guide */}
                          {selectedControl.aws_controls && selectedControl.aws_controls.length > 0 && (
                            <AWSImplementationGuide
                              controlId={selectedControl.control.id}
                              awsControls={selectedControl.aws_controls}
                            />
                          )}

                          {/* AWS Responsibility */}
                          {selectedControl.aws_applicability && selectedControl.aws_applicability.responsibility && (
                            <SpaceBetween size="xs" direction="horizontal">
                              <Box variant="small">AWS Responsibility:</Box>
                              <Badge color={
                                selectedControl.aws_applicability.responsibility === 'aws' ? 'red' :
                                selectedControl.aws_applicability.responsibility === 'shared' ? 'green' : 'blue'
                              }>
                                {selectedControl.aws_applicability.responsibility === 'aws' && 'AWS Only'}
                                {selectedControl.aws_applicability.responsibility === 'shared' && 'Shared'}
                                {selectedControl.aws_applicability.responsibility === 'customer' && 'Customer Only'}
                              </Badge>
                              
                              {selectedControl.aws_applicability.responsibility === 'aws' && (
                                <Button
                                  variant="primary"
                                  iconName="external"
                                  href="https://console.aws.amazon.com/artifact/"
                                  target="_blank"
                                >
                                  Get evidence from AWS Artifact
                                </Button>
                              )}
                            </SpaceBetween>
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
                                  <Box variant="small">✓ Specific framework mappings available for this control</Box>
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
                                          <Badge color="blue">
                                            {question.question_type.replace(/_/g, ' ').toUpperCase()}
                                          </Badge>
                                          {isAnswered && (
                                            <Badge color="green">Answered</Badge>
                                          )}
                                        </SpaceBetween>
                                        
                                        <Box variant="p">{question.question_text}</Box>
                                        
                                        {question.aws_service_guidance && (
                                          <Alert type="info" header="AWS guidance">
                                            {question.aws_service_guidance}
                                          </Alert>
                                        )}

                                        <Textarea
                                          value={responses[question.id] || ''}
                                          onChange={({ detail }) => handleResponseChange(question.id, detail.value)}
                                          onBlur={() => saveResponse(question.id)}
                                          placeholder="Enter your detailed response here..."
                                          rows={6}
                                        />
                                      </SpaceBetween>
                                    </Container>
                                  );
                                })}
                              </SpaceBetween>
                            </Container>
                          )}
                        </SpaceBetween>
                      )}
                    </ExpandableSection>
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
        />
      )}
    </>
  );
};

export default ComplianceQuestionnaire;
