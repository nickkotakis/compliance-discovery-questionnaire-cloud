import React, { useState, useEffect } from 'react';
import Container from '@cloudscape-design/components/container';
import Header from '@cloudscape-design/components/header';
import SpaceBetween from '@cloudscape-design/components/space-between';
import FormField from '@cloudscape-design/components/form-field';
import Input from '@cloudscape-design/components/input';
import Button from '@cloudscape-design/components/button';
import Multiselect from '@cloudscape-design/components/multiselect';
import Alert from '@cloudscape-design/components/alert';
import Box from '@cloudscape-design/components/box';
import Cards from '@cloudscape-design/components/cards';
import { complianceApi } from '../services/complianceApi';

interface SettingsProps {
  sessionId?: string;
  onSessionChange?: (sessionId: string) => void;
}

const Settings: React.FC<SettingsProps> = ({ onSessionChange }) => {
  const [customerName, setCustomerName] = useState('');
  const [analystName, setAnalystName] = useState('');
  const [selectedFrameworks, setSelectedFrameworks] = useState<Array<{ label: string; value: string }>>([
    { label: 'NIST 800-53', value: 'NIST 800-53' }
  ]);
  const [sessions, setSessions] = useState<any[]>([]);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');

  const availableFrameworks = [
    { label: 'NIST 800-53', value: 'NIST 800-53' },
    { label: 'PCI-DSS', value: 'PCI-DSS' },
    { label: 'HIPAA', value: 'HIPAA' },
    { label: 'SOX', value: 'SOX' },
    { label: 'FFIEC', value: 'FFIEC' },
    { label: 'GLBA', value: 'GLBA' },
    { label: 'FedRAMP', value: 'FedRAMP' },
    { label: 'GDPR', value: 'GDPR' },
    { label: 'CCPA', value: 'CCPA' }
  ];

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const data = await complianceApi.getSessions();
      setSessions(data.sessions || []);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    }
  };

  const handleSaveSession = async () => {
    if (!customerName.trim()) {
      setSaveStatus('error');
      return;
    }

    setSaveStatus('saving');
    try {
      const session = await complianceApi.createSession({
        customer_name: customerName,
        analyst_name: analystName || 'Unknown',
        frameworks: selectedFrameworks.map(f => f.value),
      });
      
      setSaveStatus('saved');
      setTimeout(() => setSaveStatus('idle'), 2000);
      
      if (onSessionChange) {
        onSessionChange(session.id);
      }
      
      await loadSessions();
    } catch (error) {
      console.error('Failed to save session:', error);
      setSaveStatus('error');
      setTimeout(() => setSaveStatus('idle'), 3000);
    }
  };

  const handleLoadSession = async (session: any) => {
    setCustomerName(session.customer_name);
    setAnalystName(session.analyst_name);
    setSelectedFrameworks(
      (session.frameworks || ['NIST 800-53']).map((f: string) => ({ label: f, value: f }))
    );
    
    if (onSessionChange) {
      onSessionChange(session.id);
    }
  };

  return (
    <SpaceBetween size="l">
      <Header variant="h1" description="Manage assessment sessions and customer information">
        Session management
      </Header>

      <Container header={<Header variant="h2">Current assessment</Header>}>
        <SpaceBetween size="l">
          <FormField
            label="Customer name"
            description="Enter the customer or organization name"
            constraintText="Required"
          >
            <Input
              value={customerName}
              onChange={({ detail }) => setCustomerName(detail.value)}
              placeholder="Enter customer name"
            />
          </FormField>

          <FormField
            label="Analyst name"
            description="Enter the name of the analyst conducting the assessment"
          >
            <Input
              value={analystName}
              onChange={({ detail }) => setAnalystName(detail.value)}
              placeholder="Enter analyst name"
            />
          </FormField>

          <FormField
            label="Target frameworks"
            description="Select the compliance frameworks for this assessment"
          >
            <Multiselect
              selectedOptions={selectedFrameworks}
              onChange={({ detail }) => setSelectedFrameworks(detail.selectedOptions.map(opt => ({ label: opt.label || '', value: opt.value || '' })))}
              options={availableFrameworks}
              placeholder="Choose frameworks"
              filteringType="auto"
            />
          </FormField>

          <Box>
            <Button
              variant="primary"
              onClick={handleSaveSession}
              loading={saveStatus === 'saving'}
              disabled={!customerName.trim()}
            >
              Save session
            </Button>
          </Box>

          {saveStatus === 'saved' && (
            <Alert type="success" dismissible onDismiss={() => setSaveStatus('idle')}>
              Session saved successfully
            </Alert>
          )}

          {saveStatus === 'error' && (
            <Alert type="error" dismissible onDismiss={() => setSaveStatus('idle')}>
              Failed to save session. Please ensure customer name is provided.
            </Alert>
          )}
        </SpaceBetween>
      </Container>

      {sessions.length > 0 && (
        <Container header={<Header variant="h2">Recent sessions</Header>}>
          <Cards
            cardDefinition={{
              header: (item) => item.customer_name,
              sections: [
                {
                  id: 'analyst',
                  header: 'Analyst',
                  content: (item) => item.analyst_name
                },
                {
                  id: 'date',
                  header: 'Created',
                  content: (item) => new Date(item.created_at).toLocaleDateString()
                },
                {
                  id: 'frameworks',
                  header: 'Frameworks',
                  content: (item) => (item.frameworks || []).join(', ')
                }
              ]
            }}
            items={sessions.slice(0, 5)}
            cardsPerRow={[{ cards: 1 }, { minWidth: 500, cards: 2 }]}
            onSelectionChange={({ detail }) => {
              if (detail.selectedItems.length > 0) {
                handleLoadSession(detail.selectedItems[0]);
              }
            }}
            selectionType="single"
          />
        </Container>
      )}

      <Alert type="info" header="Export options">
        Export options are available on the main questionnaire page for easier access.
      </Alert>
    </SpaceBetween>
  );
};

export default Settings;
