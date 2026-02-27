import React, { useState } from 'react';
import AppLayout from '@cloudscape-design/components/app-layout';
import TopNavigation from '@cloudscape-design/components/top-navigation';
import Button from '@cloudscape-design/components/button';
import Modal from '@cloudscape-design/components/modal';
import Box from '@cloudscape-design/components/box';
import SpaceBetween from '@cloudscape-design/components/space-between';
import FormField from '@cloudscape-design/components/form-field';
import Input from '@cloudscape-design/components/input';
import Alert from '@cloudscape-design/components/alert';
import ComplianceQuestionnaire from '../components/ComplianceQuestionnaire';
import { complianceApi } from '../services/complianceApi';

const Compliance: React.FC = () => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [showNewSessionForm, setShowNewSessionForm] = useState(false);
  const [customerName, setCustomerName] = useState('');
  const [analystName, setAnalystName] = useState('');

  const handleCreateSession = async () => {
    try {
      const session = await complianceApi.createSession({
        customer_name: customerName,
        analyst_name: analystName,
        frameworks: ['NIST 800-53', 'AWS'],
      });
      setSessionId(session.id);
      setShowNewSessionForm(false);
      setCustomerName('');
      setAnalystName('');
    } catch (err) {
      console.error('Failed to create session:', err);
      alert('Failed to create session. Please ensure the API server is running.');
    }
  };

  const handleExportTemplate = async () => {
    try {
      const template = await complianceApi.exportTemplate('json');
      const blob = new Blob([JSON.stringify(template, null, 2)], {
        type: 'application/json',
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `compliance-questionnaire-${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Failed to export template:', err);
      alert('Failed to export template. Please ensure the API server is running.');
    }
  };

  return (
    <>
      <TopNavigation
        identity={{
          href: '#',
          title: 'Compliance Discovery',
          logo: {
            src: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiByeD0iOCIgZmlsbD0iIzIzMkYzRSIvPgo8cGF0aCBkPSJNMjAgMTBMMjggMjBMMjAgMzBMMTIgMjBMMjAgMTBaIiBmaWxsPSIjRkY5OTAwIi8+Cjwvc3ZnPgo=',
            alt: 'Compliance Discovery'
          }
        }}
        utilities={[
          {
            type: 'button',
            text: 'Export Template',
            onClick: handleExportTemplate
          },
          {
            type: 'button',
            text: 'New Session',
            variant: 'primary-button',
            onClick: () => setShowNewSessionForm(true)
          }
        ]}
      />

      {sessionId && (
        <Alert
          type="info"
          dismissible
          onDismiss={() => setSessionId(null)}
          header="Active Session"
        >
          Session ID: {sessionId}
        </Alert>
      )}

      <AppLayout
        navigationHide
        toolsHide
        content={<ComplianceQuestionnaire sessionId={sessionId || undefined} />}
      />

      <Modal
        visible={showNewSessionForm}
        onDismiss={() => setShowNewSessionForm(false)}
        header="Create New Assessment Session"
        footer={
          <Box float="right">
            <SpaceBetween direction="horizontal" size="xs">
              <Button variant="link" onClick={() => setShowNewSessionForm(false)}>
                Cancel
              </Button>
              <Button
                variant="primary"
                onClick={handleCreateSession}
                disabled={!customerName || !analystName}
              >
                Create Session
              </Button>
            </SpaceBetween>
          </Box>
        }
      >
        <SpaceBetween size="l">
          <FormField label="Customer Name" description="Enter the customer organization name">
            <Input
              value={customerName}
              onChange={({ detail }) => setCustomerName(detail.value)}
              placeholder="Enter customer name"
            />
          </FormField>
          <FormField label="Analyst Name" description="Enter the analyst conducting the assessment">
            <Input
              value={analystName}
              onChange={({ detail }) => setAnalystName(detail.value)}
              placeholder="Enter analyst name"
            />
          </FormField>
        </SpaceBetween>
      </Modal>
    </>
  );
};

export default Compliance;
