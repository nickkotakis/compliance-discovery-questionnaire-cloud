import React from 'react';
import Container from '@cloudscape-design/components/container';
import Header from '@cloudscape-design/components/header';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Box from '@cloudscape-design/components/box';
import ProgressBar from '@cloudscape-design/components/progress-bar';
import ColumnLayout from '@cloudscape-design/components/column-layout';

interface DashboardProps {
  totalControls: number;
  answeredQuestions: number;
  totalQuestions: number;
}

const Dashboard: React.FC<DashboardProps> = ({ 
  totalControls, 
  answeredQuestions, 
  totalQuestions 
}) => {
  const completionRate = totalQuestions > 0 
    ? Math.round((answeredQuestions / totalQuestions) * 100) 
    : 0;

  return (
    <SpaceBetween size="l">
      <Header variant="h1" description="Track your compliance assessment progress">
        Assessment overview
      </Header>

      <ColumnLayout columns={4} variant="text-grid">
        <div>
          <Box variant="awsui-key-label">Total controls</Box>
          <Box variant="h1" fontSize="display-l" fontWeight="bold">
            {totalControls}
          </Box>
          <Box variant="small" color="text-body-secondary">
            NIST 800-53 Rev 5
          </Box>
        </div>

        <div>
          <Box variant="awsui-key-label">Questions answered</Box>
          <Box variant="h1" fontSize="display-l" fontWeight="bold">
            {answeredQuestions}/{totalQuestions}
          </Box>
          <Box variant="small" color="text-body-secondary">
            Total responses
          </Box>
        </div>

        <div>
          <Box variant="awsui-key-label">Completion rate</Box>
          <Box variant="h1" fontSize="display-l" fontWeight="bold">
            {completionRate}%
          </Box>
          <Box variant="small" color="text-body-secondary">
            Overall progress
          </Box>
        </div>

        <div>
          <Box variant="awsui-key-label">Pending review</Box>
          <Box variant="h1" fontSize="display-l" fontWeight="bold">
            {totalQuestions - answeredQuestions}
          </Box>
          <Box variant="small" color="text-body-secondary">
            Remaining questions
          </Box>
        </div>
      </ColumnLayout>

      <Container
        header={
          <Header
            variant="h2"
            description={`${answeredQuestions} of ${totalQuestions} questions completed`}
          >
            Overall progress
          </Header>
        }
      >
        <ProgressBar
          value={completionRate}
          label="Assessment completion"
          description={`${completionRate}% complete`}
          resultText={`${answeredQuestions} of ${totalQuestions} questions`}
        />
      </Container>
    </SpaceBetween>
  );
};

export default Dashboard;
