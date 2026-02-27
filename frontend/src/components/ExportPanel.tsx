import React, { useState } from 'react';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Header from '@cloudscape-design/components/header';
import Button from '@cloudscape-design/components/button';
import FormField from '@cloudscape-design/components/form-field';
import RadioGroup from '@cloudscape-design/components/radio-group';
import Checkbox from '@cloudscape-design/components/checkbox';
import Alert from '@cloudscape-design/components/alert';
import Box from '@cloudscape-design/components/box';
import { complianceApi } from '../services/complianceApi';

interface ExportPanelProps {
  onClose: () => void;
}

const ExportPanel: React.FC<ExportPanelProps> = ({ onClose }) => {
  const [exportFormat, setExportFormat] = useState<'excel' | 'pdf' | 'json' | 'yaml'>('excel');
  const [includeUnanswered, setIncludeUnanswered] = useState(true);
  const [includeAWSHints, setIncludeAWSHints] = useState(true);
  const [includeFrameworkMappings, setIncludeFrameworkMappings] = useState(true);
  const [exportStatus, setExportStatus] = useState<'idle' | 'exporting' | 'success' | 'error'>('idle');

  const handleExport = async () => {
    setExportStatus('exporting');
    try {
      const blob = await complianceApi.exportQuestionnaire(exportFormat, {
        include_unanswered: includeUnanswered,
        include_aws_hints: includeAWSHints,
        include_framework_mappings: includeFrameworkMappings,
      });
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      
      const extensionMap: Record<string, string> = {
        'excel': 'xlsx',
        'pdf': 'pdf',
        'json': 'json',
        'yaml': 'yaml'
      };
      const fileExtension = extensionMap[exportFormat] || exportFormat;
      
      a.download = `compliance-questionnaire-${new Date().toISOString().split('T')[0]}.${fileExtension}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      setExportStatus('success');
      setTimeout(() => {
        setExportStatus('idle');
        onClose();
      }, 2000);
    } catch (error) {
      console.error('Export failed:', error);
      setExportStatus('error');
      setTimeout(() => setExportStatus('idle'), 3000);
    }
  };

  return (
    <SpaceBetween size="l">
      <Header variant="h2" description="Export your compliance questionnaire">
        Export questionnaire
      </Header>

      <FormField label="Export format">
        <RadioGroup
          value={exportFormat}
          onChange={({ detail }) => setExportFormat(detail.value as any)}
          items={[
            { value: 'excel', label: 'Excel', description: 'Multi-sheet workbook with controls, questions, and AWS hints' },
            { value: 'pdf', label: 'PDF', description: 'Formatted report suitable for client delivery' },
            { value: 'json', label: 'JSON', description: 'Machine-readable format for API integration' },
            { value: 'yaml', label: 'YAML', description: 'Human-readable configuration format' }
          ]}
        />
      </FormField>

      <FormField label="Include in export">
        <SpaceBetween size="s">
          <Checkbox
            checked={includeUnanswered}
            onChange={({ detail }) => setIncludeUnanswered(detail.checked)}
          >
            Unanswered questions
            <Box variant="small" color="text-body-secondary">
              Include controls without responses
            </Box>
          </Checkbox>

          <Checkbox
            checked={includeAWSHints}
            onChange={({ detail }) => setIncludeAWSHints(detail.checked)}
          >
            AWS implementation guidance
            <Box variant="small" color="text-body-secondary">
              Include AWS Config rules, Security Hub controls, etc.
            </Box>
          </Checkbox>

          <Checkbox
            checked={includeFrameworkMappings}
            onChange={({ detail }) => setIncludeFrameworkMappings(detail.checked)}
          >
            Framework mappings
            <Box variant="small" color="text-body-secondary">
              Include PCI-DSS, HIPAA, SOX, FFIEC mappings
            </Box>
          </Checkbox>
        </SpaceBetween>
      </FormField>

      <Box>
        <SpaceBetween direction="horizontal" size="xs">
          <Button variant="link" onClick={onClose}>
            Cancel
          </Button>
          <Button
            variant="primary"
            onClick={handleExport}
            loading={exportStatus === 'exporting'}
          >
            Export as {exportFormat.toUpperCase()}
          </Button>
        </SpaceBetween>
      </Box>

      {exportStatus === 'success' && (
        <Alert type="success">
          Export successful
        </Alert>
      )}

      {exportStatus === 'error' && (
        <Alert type="error">
          Export failed. Please try again.
        </Alert>
      )}

      <Alert type="info" header="Export formats">
        <Box variant="p">
          <strong>Excel:</strong> Multi-sheet workbook with controls, questions, and AWS hints
        </Box>
        <Box variant="p">
          <strong>PDF:</strong> Formatted report suitable for client delivery
        </Box>
        <Box variant="p">
          <strong>JSON/YAML:</strong> Machine-readable format for API integration
        </Box>
      </Alert>
    </SpaceBetween>
  );
};

export default ExportPanel;
