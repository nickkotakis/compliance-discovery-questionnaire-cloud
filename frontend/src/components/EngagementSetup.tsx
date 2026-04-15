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
import ColumnLayout from '@cloudscape-design/components/column-layout';
import { useEngagement, EngagementConfig, FRAMEWORK_LABELS } from '../contexts/EngagementContext';

const EngagementSetup: React.FC = () => {
  const { savedEngagements, setActiveEngagement, saveEngagement, deleteEngagement } = useEngagement();
  const [config, setConfig] = useState<EngagementConfig>({
    customerName: '', framework: 'nist-csf', scope: 'AWS Environment Only',
    regulator: '', engagementWeeks: 10, meetingFrequency: 'weekly', maxMeetingDuration: 75,
  });

  const handleCreate = () => {
    if (!config.customerName.trim()) return;
    saveEngagement(config);
  };

  return (
    <SpaceBetween size="l">
      {savedEngagements.length > 0 && (
        <Container header={<Header variant="h2">Resume an engagement</Header>}>
          <SpaceBetween size="s">
            {savedEngagements.map(eng => (
              <div key={eng.id} style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                padding: '12px 16px', borderRadius: '8px', cursor: 'pointer',
                border: '1px solid #e9ebed', background: '#fff',
              }}
                onClick={() => setActiveEngagement(eng)}
                onMouseEnter={e => (e.currentTarget.style.borderColor = '#0972d3')}
                onMouseLeave={e => (e.currentTarget.style.borderColor = '#e9ebed')}
              >
                <SpaceBetween size="xxs">
                  <Box variant="strong" fontSize="heading-m">{eng.config.customerName}</Box>
                  <SpaceBetween size="xxs" direction="horizontal">
                    <Badge color="blue">{FRAMEWORK_LABELS[eng.config.framework]}</Badge>
                    <Box variant="small" color="text-body-secondary">{eng.config.scope}</Box>
                    {eng.config.regulator && <Box variant="small" color="text-body-secondary">| {eng.config.regulator}</Box>}
                    <Box variant="small" color="text-body-secondary">| {eng.config.engagementWeeks} weeks</Box>
                  </SpaceBetween>
                </SpaceBetween>
                <Button variant="icon" iconName="remove" onClick={(e) => { e.stopPropagation(); deleteEngagement(eng.id); }} />
              </div>
            ))}
          </SpaceBetween>
        </Container>
      )}

      <Container header={<Header variant="h2" description="Set up your engagement profile — this will be shared across Schedule, Evidence Tracker, and Facilitation Guide">Create new engagement</Header>}>
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
            <FormField label="Interview weeks">
              <Select selectedOption={{ label: `${config.engagementWeeks} weeks`, value: String(config.engagementWeeks) }} onChange={({ detail }) => setConfig({ ...config, engagementWeeks: parseInt(detail.selectedOption.value || '10') })} options={[4,6,8,10,12,14,16].map(w => ({ label: `${w} weeks`, value: String(w) }))} />
            </FormField>
            <FormField label="Meeting frequency">
              <Select selectedOption={{ label: config.meetingFrequency === 'weekly' ? 'Weekly' : 'Bi-weekly', value: config.meetingFrequency }} onChange={({ detail }) => setConfig({ ...config, meetingFrequency: detail.selectedOption.value || 'weekly' })} options={[{ label: 'Weekly', value: 'weekly' }, { label: 'Bi-weekly', value: 'biweekly' }]} />
            </FormField>
            <FormField label="Max meeting duration">
              <Select selectedOption={{ label: `${config.maxMeetingDuration} min`, value: String(config.maxMeetingDuration) }} onChange={({ detail }) => setConfig({ ...config, maxMeetingDuration: parseInt(detail.selectedOption.value || '75') })} options={[{ label: '60 min', value: '60' }, { label: '75 min', value: '75' }, { label: '90 min', value: '90' }]} />
            </FormField>
          </ColumnLayout>
          <Button variant="primary" onClick={handleCreate} disabled={!config.customerName.trim()}>Create engagement</Button>
        </SpaceBetween>
      </Container>
    </SpaceBetween>
  );
};

export default EngagementSetup;
