import React, { useState } from 'react';
import { ControlDetail } from '../services/complianceApi';
import Modal from '@cloudscape-design/components/modal';
import Box from '@cloudscape-design/components/box';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Button from '@cloudscape-design/components/button';
import Badge from '@cloudscape-design/components/badge';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import ProgressBar from '@cloudscape-design/components/progress-bar';
import Container from '@cloudscape-design/components/container';
import Header from '@cloudscape-design/components/header';
import Textarea from '@cloudscape-design/components/textarea';
import Alert from '@cloudscape-design/components/alert';
import AWSImplementationGuide from './AWSImplementationGuide';

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

const getFamilyFullName = (familyCode: string): string => {
  return FAMILY_NAMES[familyCode.toLowerCase()] || familyCode.toUpperCase();
};

interface InterviewModeProps {
  control: ControlDetail;
  responses: Record<string, string>;
  onResponseChange: (questionId: string, value: string) => void;
  onSave: (questionId: string) => void;
  onClose: () => void;
  framework?: string;
}

const InterviewMode: React.FC<InterviewModeProps> = ({
  control,
  responses,
  onResponseChange,
  onSave,
  onClose,
  framework = 'nist-800-53'
}) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const questions = control.questions || [];
  
  // Safety check - close if no questions
  if (questions.length === 0) {
    return (
      <Modal
        visible={true}
        onDismiss={onClose}
        header="No questions available"
        footer={
          <Box float="right">
            <Button variant="primary" onClick={onClose}>
              Close
            </Button>
          </Box>
        }
      >
        <Box variant="p">This control does not have any questions generated yet.</Box>
      </Modal>
    );
  }
  
  const currentQuestion = questions[currentQuestionIndex];
  const answeredCount = questions.filter(q => responses[q.id]).length;
  const progress = Math.round((answeredCount / questions.length) * 100);

  const goToNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const goToPrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const isAnswered = !!responses[currentQuestion.id];

  return (
    <Modal
      visible={true}
      onDismiss={onClose}
      size="max"
      header={
        <SpaceBetween size="m">
          <SpaceBetween size="xs" direction="horizontal">
            <Box variant="h2">{control.control.id.toUpperCase()}</Box>
            <Badge>{control.control.family.toUpperCase()} - {getFamilyFullName(control.control.family)}</Badge>
          </SpaceBetween>
          <Box variant="p">{control.control.title}</Box>
          <ProgressBar
            value={progress}
            label={`Progress: ${answeredCount}/${questions.length} questions`}
            description={`${progress}% complete`}
          />
        </SpaceBetween>
      }
      footer={
        <Box float="right">
          <SpaceBetween direction="horizontal" size="xs">
            <Button
              onClick={goToPrevious}
              disabled={currentQuestionIndex === 0}
            >
              Previous
            </Button>
            <Box variant="span" color="text-body-secondary">
              Question {currentQuestionIndex + 1} of {questions.length}
            </Box>
            <Button
              onClick={goToNext}
              disabled={currentQuestionIndex === questions.length - 1}
            >
              Next
            </Button>
          </SpaceBetween>
        </Box>
      }
    >
      <SpaceBetween size="l">
        {/* Question Number and Type */}
        <Container>
          <SpaceBetween size="s">
            <SpaceBetween size="xs" direction="horizontal">
              <Badge color="blue">Question {currentQuestionIndex + 1}</Badge>
              <Badge>{currentQuestion.question_type.replace(/_/g, ' ').toUpperCase()}</Badge>
              {isAnswered && (
                <StatusIndicator type="success">Answered</StatusIndicator>
              )}
            </SpaceBetween>
            <Box variant="small" color="text-body-secondary">
              Question {currentQuestionIndex + 1} of {questions.length}
            </Box>
          </SpaceBetween>
        </Container>

        {/* Question Text */}
        <Container>
          <Box variant="h3" fontSize="heading-l" padding={{ vertical: 's' }}>
            {currentQuestion.question_text}
          </Box>
        </Container>

        {/* AWS Guidance - Only show if no detailed AWS Implementation Guide */}
        {currentQuestion.aws_service_guidance && 
         (!control.aws_controls || control.aws_controls.length === 0) && (
          <Alert type="info" header="AWS implementation guidance">
            {currentQuestion.aws_service_guidance}
          </Alert>
        )}

        {/* AWS Responsibility Indicator */}
        {control.aws_applicability && control.aws_applicability.responsibility && (
          <Container>
            <SpaceBetween size="xs" direction="horizontal">
              <Box variant="small">AWS Responsibility:</Box>
              <Badge color={
                control.aws_applicability.responsibility === 'aws' ? 'red' :
                control.aws_applicability.responsibility === 'shared' ? 'green' : 'blue'
              }>
                {control.aws_applicability.responsibility === 'aws' && 'AWS Only'}
                {control.aws_applicability.responsibility === 'shared' && 'Shared'}
                {control.aws_applicability.responsibility === 'customer' && 'Customer Only'}
              </Badge>
              
              {/* Evidence link for AWS-only controls */}
              {control.aws_applicability.responsibility === 'aws' && (
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
          </Container>
        )}

        {/* Framework Relevance */}
        {control.framework_relevance && control.framework_relevance.relevant_frameworks.length > 0 && (
          <Container header={<Header variant="h3">Relevant compliance frameworks</Header>}>
            <SpaceBetween size="s">
              <SpaceBetween size="xs" direction="horizontal">
                {control.framework_relevance.relevant_frameworks.map((framework, idx) => (
                  <Badge key={idx}>{framework}</Badge>
                ))}
              </SpaceBetween>
              {control.framework_relevance.has_specific_mappings && (
                <Box variant="small">✓ Specific framework mappings available for this control</Box>
              )}
              <Box variant="small" color="text-body-secondary">
                {control.framework_relevance.notes}
              </Box>
            </SpaceBetween>
          </Container>
        )}

        {/* AWS Implementation Guide */}
        {((control.aws_controls && control.aws_controls.length > 0) ||
          (control.preventive_controls &&
            ((control.preventive_controls.scps && control.preventive_controls.scps.length > 0) ||
             (control.preventive_controls.opa_rules && control.preventive_controls.opa_rules.length > 0)))) && (
          <AWSImplementationGuide
            controlId={control.control.id}
            awsControls={control.aws_controls || []}
            framework={framework}
            preventiveControls={control.preventive_controls}
          />
        )}

        {/* AWS Hints (fallback if no detailed controls) */}
        {(!control.aws_controls || control.aws_controls.length === 0) && control.aws_hints.length > 0 && (
          <Container header={<Header variant="h3">AWS managed controls</Header>}>
            <ul>
              {control.aws_hints.map((hint, idx) => (
                <li key={idx}>{hint}</li>
              ))}
            </ul>
          </Container>
        )}

        {/* Response Area */}
        <Container header={<Header variant="h3">Client response</Header>}>
          <Textarea
            value={responses[currentQuestion.id] || ''}
            onChange={({ detail }) => onResponseChange(currentQuestion.id, detail.value)}
            onBlur={() => onSave(currentQuestion.id)}
            placeholder="Document the client's response here..."
            rows={8}
          />
        </Container>
      </SpaceBetween>
    </Modal>
  );
};

export default InterviewMode;
