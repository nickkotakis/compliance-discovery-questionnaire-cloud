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

interface AWSControl {
  control_id: string;
  title: string;
  description: string;
  services: string[];
  config_rules: string[];
  security_hub_controls: string[];
  control_tower_ids: string[];
  frameworks: string[];
}

interface AWSImplementationGuideProps {
  controlId: string;
  awsControls?: AWSControl[];
}

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

    awsControls.forEach((control, idx) => {
      report += `${idx + 1}. ${control.title}\n`;
      report += `   Control ID: ${control.control_id}\n`;
      report += `   Description: ${control.description}\n\n`;

      if (control.services.length > 0) {
        report += `   AWS Services:\n`;
        control.services.forEach(service => {
          report += `   • ${service}\n`;
        });
        report += `\n`;
      }

      if (control.config_rules.length > 0) {
        report += `   Config Rules:\n`;
        control.config_rules.forEach(rule => {
          report += `   • ${rule}\n`;
        });
        report += `\n`;
      }

      if (control.security_hub_controls.length > 0) {
        report += `   Security Hub Controls:\n`;
        control.security_hub_controls.forEach(hub => {
          report += `   • ${hub}\n`;
        });
        report += `\n`;
      }

      if (control.control_tower_ids.length > 0) {
        report += `   Control Tower Controls:\n`;
        control.control_tower_ids.forEach(ct => {
          report += `   • ${ct}\n`;
        });
        report += `\n`;
      }

      report += `\n`;
    });

    return report;
  };

  const allConfigRules = [...new Set(awsControls.flatMap(c => c.config_rules))];
  const allSecurityHubControls = [...new Set(awsControls.flatMap(c => c.security_hub_controls))];
  const allControlTowerIds = [...new Set(awsControls.flatMap(c => c.control_tower_ids))];
  const allServices = [...new Set(awsControls.flatMap(c => c.services))];

  const controlsByService = awsControls.reduce((acc, control) => {
    control.services.forEach(service => {
      if (!acc[service]) {
        acc[service] = [];
      }
      acc[service].push(control);
    });
    return acc;
  }, {} as Record<string, AWSControl[]>);

  return (
    <>
      <Flashbar items={flashbarItems} />
      <Container
        header={
          <Header
            variant="h3"
            description={`${awsControls.length} AWS control${awsControls.length !== 1 ? 's' : ''} • ${allConfigRules.length} Config rules • ${allSecurityHubControls.length} Security Hub controls • ${allControlTowerIds.length} Control Tower controls`}
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
          <ColumnLayout columns={4} variant="text-grid">
            <div>
              <Box variant="awsui-key-label">AWS services</Box>
              <Box variant="h1" fontSize="display-l" fontWeight="bold">
                {allServices.length}
              </Box>
            </div>
            <div>
              <Box variant="awsui-key-label">Config rules</Box>
              <Box variant="h1" fontSize="display-l" fontWeight="bold">
                {allConfigRules.length}
              </Box>
            </div>
            <div>
              <Box variant="awsui-key-label">Security Hub</Box>
              <Box variant="h1" fontSize="display-l" fontWeight="bold">
                {allSecurityHubControls.length}
              </Box>
            </div>
            <div>
              <Box variant="awsui-key-label">Control Tower</Box>
              <Box variant="h1" fontSize="display-l" fontWeight="bold">
                {allControlTowerIds.length}
              </Box>
            </div>
          </ColumnLayout>

          {allServices.length > 0 && (
            <Container
              header={
                <Header
                  variant="h3"
                  actions={
                    <Button
                      variant="inline-icon"
                      iconName={copiedSection === 'services' ? 'check' : 'copy'}
                      onClick={() => copyToClipboard(allServices.join('\n'), 'services')}
                    />
                  }
                >
                  AWS services to implement
                </Header>
              }
            >
              <SpaceBetween size="xs" direction="horizontal">
                {allServices.map((service, idx) => (
                  <Badge key={idx} color="blue">{service}</Badge>
                ))}
              </SpaceBetween>
            </Container>
          )}

          {allConfigRules.length > 0 && (
            <Container
              header={
                <Header
                  variant="h3"
                  actions={
                    <Button
                      variant="inline-icon"
                      iconName={copiedSection === 'config' ? 'check' : 'copy'}
                      onClick={() => copyToClipboard(allConfigRules.join('\n'), 'config')}
                    />
                  }
                >
                  AWS Config rules to enable
                </Header>
              }
            >
              <SpaceBetween size="xs">
                {allConfigRules.map((rule, idx) => (
                  <Box key={idx} variant="code">{rule}</Box>
                ))}
              </SpaceBetween>
            </Container>
          )}

          {allSecurityHubControls.length > 0 && (
            <Container
              header={
                <Header
                  variant="h3"
                  actions={
                    <Button
                      variant="inline-icon"
                      iconName={copiedSection === 'securityhub' ? 'check' : 'copy'}
                      onClick={() => copyToClipboard(allSecurityHubControls.join('\n'), 'securityhub')}
                    />
                  }
                >
                  Security Hub controls to monitor
                </Header>
              }
            >
              <SpaceBetween size="xs" direction="horizontal">
                {allSecurityHubControls.map((control, idx) => (
                  <Badge key={idx} color="green">{control}</Badge>
                ))}
              </SpaceBetween>
            </Container>
          )}

          {allControlTowerIds.length > 0 && (
            <Container
              header={
                <Header
                  variant="h3"
                  actions={
                    <Button
                      variant="inline-icon"
                      iconName={copiedSection === 'controltower' ? 'check' : 'copy'}
                      onClick={() => copyToClipboard(allControlTowerIds.join('\n'), 'controltower')}
                    />
                  }
                >
                  Control Tower controls
                </Header>
              }
            >
              <SpaceBetween size="xs">
                {allControlTowerIds.map((ct, idx) => (
                  <Box key={idx} variant="code">{ct}</Box>
                ))}
              </SpaceBetween>
            </Container>
          )}

          <ExpandableSection headerText="AWS control guides by service" variant="container">
            <SpaceBetween size="m">
              {Object.entries(controlsByService).map(([service, controls]) => (
                <Container
                  key={service}
                  header={
                    <Header
                      variant="h3"
                      counter={`(${controls.length})`}
                    >
                      {service}
                    </Header>
                  }
                >
                  <SpaceBetween size="m">
                    {controls.map((control, idx) => (
                      <Box key={idx}>
                        <SpaceBetween size="xs">
                          <Box>
                            <Badge>{control.control_id}</Badge>
                            <Box variant="strong" display="inline" margin={{ left: 'xs' }}>
                              {control.title}
                            </Box>
                          </Box>
                          <Box variant="p">{control.description}</Box>
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
                      </Box>
                    ))}
                  </SpaceBetween>
                </Container>
              ))}
            </SpaceBetween>
          </ExpandableSection>

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
