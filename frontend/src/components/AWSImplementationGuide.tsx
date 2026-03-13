import React, { useState } from 'react';
import ExpandableSection from '@cloudscape-design/components/expandable-section';
import Container from '@cloudscape-design/components/container';
import Header from '@cloudscape-design/components/header';
import SpaceBetween from '@cloudscape-design/components/space-between';
import Box from '@cloudscape-design/components/box';
import Button from '@cloudscape-design/components/button';
import Badge from '@cloudscape-design/components/badge';
import ColumnLayout from '@cloudscape-design/components/column-layout';
import Link from '@cloudscape-design/components/link';
import Alert from '@cloudscape-design/components/alert';
import Flashbar from '@cloudscape-design/components/flashbar';
import Icon from '@cloudscape-design/components/icon';

interface AWSControl {
  control_id: string;
  title: string;
  description: string;
  services: string[];
  config_rules: string[];
  security_hub_controls: string[];
  control_tower_ids: string[];
  frameworks: string[];
  priority?: 'core' | 'recommended' | 'enhanced';
}

interface AWSImplementationGuideProps {
  controlId: string;
  awsControls?: AWSControl[];
}

const PRIORITY_META: Record<string, { label: string; color: string; badgeColor: 'blue' | 'green' | 'grey'; icon: string; desc: string }> = {
  core: {
    label: 'Core',
    color: '#037f0c',
    badgeColor: 'green',
    icon: 'status-positive',
    desc: 'Fundamental controls for audit readiness'
  },
  recommended: {
    label: 'Recommended',
    color: '#0972d3',
    badgeColor: 'blue',
    icon: 'status-info',
    desc: 'Important controls most organizations should implement'
  },
  enhanced: {
    label: 'Enhanced',
    color: '#687078',
    badgeColor: 'grey',
    icon: 'status-pending',
    desc: 'Advanced controls for mature security programs'
  }
};

const AWSImplementationGuide: React.FC<AWSImplementationGuideProps> = ({
  controlId,
  awsControls = []
}) => {
  const [copiedSection, setCopiedSection] = useState<string | null>(null);
  const [flashbarItems, setFlashbarItems] = useState<any[]>([]);

  if (!awsControls || awsControls.length === 0) {
    return null;
  }

  const copyToClipboard = (text: string, section: string) => {
    navigator.clipboard.writeText(text);
    setCopiedSection(section);
    setFlashbarItems([{
      type: 'success',
      content: 'Copied to clipboard',
      dismissible: true,
      onDismiss: () => setFlashbarItems([]),
      id: 'copy-success'
    }]);
    setTimeout(() => {
      setCopiedSection(null);
      setFlashbarItems([]);
    }, 2000);
  };

  const generateImplementationReport = () => {
    let report = `AWS Implementation Guide for ${controlId.toUpperCase()}\n`;
    report += `${'='.repeat(60)}\n\n`;

    const tiers = ['core', 'recommended', 'enhanced'] as const;
    for (const tier of tiers) {
      const tierControls = awsControls.filter(c => (c.priority || 'recommended') === tier);
      if (tierControls.length === 0) continue;
      const meta = PRIORITY_META[tier];
      report += `--- ${meta.label.toUpperCase()} CONTROLS (${tierControls.length}) ---\n`;
      report += `${meta.desc}\n\n`;

      tierControls.forEach((control, idx) => {
        report += `${idx + 1}. ${control.title}\n`;
        report += `   Control ID: ${control.control_id}\n`;
        report += `   Description: ${control.description}\n\n`;
        if (control.config_rules.length > 0) {
          report += `   Config Rules:\n`;
          control.config_rules.forEach(rule => { report += `   - ${rule}\n`; });
          report += `\n`;
        }
        if (control.security_hub_controls.length > 0) {
          report += `   Security Hub Controls:\n`;
          control.security_hub_controls.forEach(hub => { report += `   - ${hub}\n`; });
          report += `\n`;
        }
        if (control.control_tower_ids.length > 0) {
          report += `   Control Tower Controls:\n`;
          control.control_tower_ids.forEach(ct => { report += `   - ${ct}\n`; });
          report += `\n`;
        }
      });
      report += `\n`;
    }
    return report;
  };

  const coreControls = awsControls.filter(c => c.priority === 'core');
  const recommendedControls = awsControls.filter(c => (c.priority || 'recommended') === 'recommended');
  const enhancedControls = awsControls.filter(c => c.priority === 'enhanced');

  const renderControlCard = (control: AWSControl) => {
    const tier = control.priority || 'recommended';
    const meta = PRIORITY_META[tier];
    return (
      <div key={control.control_id} style={{ borderLeft: `4px solid ${meta.color}`, paddingLeft: '12px', marginBottom: '8px' }}>
        <SpaceBetween size="xs">
          <Box>
            <SpaceBetween size="xs" direction="horizontal">
              <Badge color={meta.badgeColor}>{meta.label}</Badge>
              <Badge>{control.control_id}</Badge>
            </SpaceBetween>
            <Box variant="strong" margin={{ top: 'xxs' }}>{control.title}</Box>
          </Box>
          <Box variant="small" color="text-body-secondary">{control.description}</Box>
          <ColumnLayout columns={3}>
            {control.config_rules.length > 0 && (
              <div>
                <Box variant="awsui-key-label">Config rules</Box>
                <SpaceBetween size="xxs">
                  {control.config_rules.map((rule, ridx) => (
                    <Box key={ridx} variant="code" fontSize="body-s">{rule}</Box>
                  ))}
                </SpaceBetween>
              </div>
            )}
            {control.security_hub_controls.length > 0 && (
              <div>
                <Box variant="awsui-key-label">Security Hub</Box>
                <SpaceBetween size="xxs" direction="horizontal">
                  {control.security_hub_controls.map((hub, hidx) => (
                    <Badge key={hidx} color="green">{hub}</Badge>
                  ))}
                </SpaceBetween>
              </div>
            )}
            {control.control_tower_ids.length > 0 && (
              <div>
                <Box variant="awsui-key-label">Control Tower</Box>
                <SpaceBetween size="xxs">
                  {control.control_tower_ids.map((ct, ctidx) => (
                    <Box key={ctidx} variant="code" fontSize="body-s">{ct}</Box>
                  ))}
                </SpaceBetween>
              </div>
            )}
          </ColumnLayout>
        </SpaceBetween>
      </div>
    );
  };

  return (
    <>
      <Flashbar items={flashbarItems} />
      <Container
        header={
          <Header
            variant="h3"
            description={`${awsControls.length} AWS control${awsControls.length !== 1 ? 's' : ''} mapped to this subcategory`}
            actions={
              <Button
                onClick={() => copyToClipboard(generateImplementationReport(), 'full')}
                iconName={copiedSection === 'full' ? 'check' : 'copy'}
              >
                {copiedSection === 'full' ? 'Copied' : 'Copy report'}
              </Button>
            }
          >
            AWS implementation guide
          </Header>
        }
      >
        <SpaceBetween size="l">
          {/* Priority tier summary */}
          <ColumnLayout columns={3} variant="text-grid">
            {(['core', 'recommended', 'enhanced'] as const).map(tier => {
              const count = tier === 'core' ? coreControls.length
                : tier === 'recommended' ? recommendedControls.length
                : enhancedControls.length;
              const meta = PRIORITY_META[tier];
              return (
                <div key={tier} style={{ borderLeft: `4px solid ${meta.color}`, paddingLeft: '8px' }}>
                  <Box variant="awsui-key-label">
                    <Icon name={meta.icon as any} /> {meta.label}
                  </Box>
                  <Box variant="h2" fontSize="display-l" fontWeight="bold">{count}</Box>
                  <Box variant="small" color="text-body-secondary">{meta.desc}</Box>
                </div>
              );
            })}
          </ColumnLayout>

          {/* Core controls - expanded by default */}
          {coreControls.length > 0 && (
            <ExpandableSection
              variant="container"
              headerText={`Core controls (${coreControls.length})`}
              headerDescription="Enable these first for audit readiness"
              defaultExpanded
            >
              <SpaceBetween size="m">
                {coreControls.map(renderControlCard)}
              </SpaceBetween>
            </ExpandableSection>
          )}

          {/* Recommended controls - expandable */}
          {recommendedControls.length > 0 && (
            <ExpandableSection
              variant="container"
              headerText={`Recommended controls (${recommendedControls.length})`}
              headerDescription="Important controls most organizations should implement"
              defaultExpanded={coreControls.length === 0}
            >
              <SpaceBetween size="m">
                {recommendedControls.map(renderControlCard)}
              </SpaceBetween>
            </ExpandableSection>
          )}

          {/* Enhanced controls - collapsed by default */}
          {enhancedControls.length > 0 && (
            <ExpandableSection
              variant="container"
              headerText={`Enhanced controls (${enhancedControls.length})`}
              headerDescription="Advanced controls for mature security programs"
            >
              <SpaceBetween size="m">
                {enhancedControls.map(renderControlCard)}
              </SpaceBetween>
            </ExpandableSection>
          )}

          <Alert type="info" header="Helpful AWS resources">
            <ColumnLayout columns={2}>
              <Link external href="https://console.aws.amazon.com/config/">
                AWS Config console
              </Link>
              <Link external href="https://console.aws.amazon.com/securityhub/">
                Security Hub console
              </Link>
              <Link external href="https://console.aws.amazon.com/controltower/">
                Control Tower console
              </Link>
              <Link external href="https://console.aws.amazon.com/artifact/">
                AWS Artifact (compliance reports)
              </Link>
            </ColumnLayout>
          </Alert>
        </SpaceBetween>
      </Container>
    </>
  );
};

export default AWSImplementationGuide;
