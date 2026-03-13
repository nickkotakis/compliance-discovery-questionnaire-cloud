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
import Popover from '@cloudscape-design/components/popover';

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
  framework?: string;
  preventiveControls?: {
    scps: Array<{
      scp_name: string;
      scp_id: string;
      description: string;
      example_actions: string;
      priority?: 'core' | 'recommended' | 'enhanced';
    }>;
    opa_rules: Array<{
      opa_rule: string;
      description: string;
      resource_types: string;
      severity: string;
      priority?: 'core' | 'recommended' | 'enhanced';
    }>;
  };
}

const FRAMEWORK_CLASSIFICATION_INFO: Record<string, { name: string; explanation: string }> = {
  'nist-csf': {
    name: 'NIST CSF 2.0',
    explanation: 'For NIST CSF, controls are classified based on how directly they support the CSF function and subcategory objectives. Core controls have AWS Config rules enabling automated compliance validation and appear in major benchmarks (CIS, PCI DSS, SOC 2). Recommended controls have Security Hub or Control Tower support, or broad framework coverage, but may lack Config rules. Enhanced controls are service-specific or advanced implementations for mature programs.'
  },
  'nist-800-53': {
    name: 'NIST 800-53 Rev 5',
    explanation: 'For NIST 800-53, controls are classified based on alignment with the control family objectives and baseline impact levels. Core controls have AWS Config rules for automated validation and are referenced across major frameworks (CIS Benchmarks, PCI DSS, FedRAMP). Recommended controls have Security Hub or Control Tower managed controls, or appear in multiple compliance frameworks. Enhanced controls provide defense-in-depth for organizations with advanced security requirements.'
  },
  'cmmc': {
    name: 'CMMC Level 2',
    explanation: 'For CMMC Level 2, controls are classified based on their alignment with NIST SP 800-171 practice requirements and AWS automation capabilities. Core controls have AWS Config rules for automated compliance validation and map to practices commonly assessed during CMMC certification. Recommended controls have Security Hub or Control Tower support, providing monitoring and alerting capabilities. Enhanced controls are advanced implementations for organizations seeking defense-in-depth beyond baseline CMMC requirements.'
  }
};

const DEFAULT_CLASSIFICATION_INFO = {
  name: 'this framework',
  explanation: 'Controls are classified based on their automation capabilities and cross-framework coverage. Core controls have AWS Config rules for automated compliance validation and appear across major industry benchmarks. Recommended controls have Security Hub or Control Tower support, or broad framework coverage. Enhanced controls are advanced implementations for mature security programs.'
};

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
  awsControls = [],
  framework = 'nist-800-53',
  preventiveControls
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
    
    // Add preventive controls
    if (preventiveControls) {
      if (preventiveControls.scps.length > 0) {
        report += `--- SERVICE CONTROL POLICIES (${preventiveControls.scps.length}) ---\n`;
        report += `Preventive guardrails via AWS Organizations\n\n`;
        preventiveControls.scps.forEach((scp, idx) => {
          report += `${idx + 1}. ${scp.scp_name}\n`;
          report += `   ${scp.description}\n`;
          report += `   Actions: ${scp.example_actions}\n\n`;
        });
      }
      if (preventiveControls.opa_rules.length > 0) {
        report += `--- IaC POLICY RULES (${preventiveControls.opa_rules.length}) ---\n`;
        report += `Pre-deployment validation via OPA/Rego\n\n`;
        preventiveControls.opa_rules.forEach((rule, idx) => {
          report += `${idx + 1}. ${rule.opa_rule} [${rule.severity}]\n`;
          report += `   ${rule.description}\n`;
          report += `   Resources: ${rule.resource_types}\n\n`;
        });
      }
    }
    return report;
  };

  const coreControls = awsControls.filter(c => c.priority === 'core');
  const recommendedControls = awsControls.filter(c => (c.priority || 'recommended') === 'recommended');
  const enhancedControls = awsControls.filter(c => c.priority === 'enhanced');

  // Categorize preventive controls by priority
  const coreScps = preventiveControls?.scps?.filter(s => (s as any).priority === 'core') || [];
  const recommendedScps = preventiveControls?.scps?.filter(s => (s as any).priority === 'recommended') || [];
  const enhancedScps = preventiveControls?.scps?.filter(s => (s as any).priority === 'enhanced') || [];
  const coreOpa = preventiveControls?.opa_rules?.filter(r => (r as any).priority === 'core') || [];
  const recommendedOpa = preventiveControls?.opa_rules?.filter(r => (r as any).priority === 'recommended') || [];
  const enhancedOpa = preventiveControls?.opa_rules?.filter(r => (r as any).priority === 'enhanced') || [];

  const totalCore = coreControls.length + coreScps.length + coreOpa.length;
  const totalRecommended = recommendedControls.length + recommendedScps.length + recommendedOpa.length;
  const totalEnhanced = enhancedControls.length + enhancedScps.length + enhancedOpa.length;

  const renderScpCard = (scp: any, idx: number) => (
    <div key={`scp-${idx}`} style={{ borderLeft: '4px solid #ff9900', paddingLeft: '12px', marginBottom: '8px' }}>
      <SpaceBetween size="xxs">
        <Box>
          <SpaceBetween size="xxs" direction="horizontal">
            <Badge color="green">Preventive</Badge>
            <Box variant="small" color="text-body-secondary">AWS Organizations — SCP</Box>
          </SpaceBetween>
          <Box variant="strong" margin={{ top: 'xxs' }}>{scp.scp_name}</Box>
        </Box>
        <Box variant="small" color="text-body-secondary">{scp.description}</Box>
        <Box variant="code" fontSize="body-s">{scp.example_actions}</Box>
      </SpaceBetween>
    </div>
  );

  const renderOpaCard = (rule: any, idx: number) => (
    <div key={`opa-${idx}`} style={{ borderLeft: '4px solid #9469d6', paddingLeft: '12px', marginBottom: '8px' }}>
      <SpaceBetween size="xxs">
        <Box>
          <SpaceBetween size="xxs" direction="horizontal">
            <Badge color="green">Preventive</Badge>
            <Badge color={rule.severity === 'CRITICAL' ? 'red' : rule.severity === 'HIGH' ? 'blue' : 'grey'}>
              {rule.severity}
            </Badge>
            <Box variant="small" color="text-body-secondary">CI/CD Pipeline — OPA/Rego</Box>
          </SpaceBetween>
          <Box variant="strong" margin={{ top: 'xxs' }}>{rule.opa_rule}</Box>
        </Box>
        <Box variant="small" color="text-body-secondary">{rule.description}</Box>
        <Box variant="code" fontSize="body-s">Resources: {rule.resource_types}</Box>
      </SpaceBetween>
    </div>
  );

  const renderControlCard = (control: AWSControl) => {
    const tier = control.priority || 'recommended';
    const meta = PRIORITY_META[tier];
    const hasDetective = control.config_rules.length > 0 || control.security_hub_controls.length > 0;
    const hasPreventive = control.control_tower_ids.length > 0;
    return (
      <div key={control.control_id} style={{ borderLeft: `4px solid ${meta.color}`, paddingLeft: '12px', marginBottom: '8px' }}>
        <SpaceBetween size="xs">
          <Box>
            <SpaceBetween size="xs" direction="horizontal">
              <Badge color={meta.badgeColor}>{meta.label}</Badge>
              {hasDetective && <Badge color="blue">Detective</Badge>}
              {hasPreventive && <Badge color="green">Preventive</Badge>}
            </SpaceBetween>
            <Box variant="strong" margin={{ top: 'xxs' }}>{control.title}</Box>
          </Box>
          <Box variant="small" color="text-body-secondary">{control.description}</Box>
          <ColumnLayout columns={3}>
            {control.config_rules.length > 0 && (
              <div>
                <Box variant="awsui-key-label">
                  <SpaceBetween size="xxs" direction="horizontal">
                    <span>Config rules</span>
                    <Box variant="small" color="text-body-secondary">(AWS Config — Detective)</Box>
                  </SpaceBetween>
                </Box>
                <SpaceBetween size="xxs">
                  {control.config_rules.map((rule, ridx) => (
                    <Box key={ridx} variant="code" fontSize="body-s">{rule}</Box>
                  ))}
                </SpaceBetween>
              </div>
            )}
            {control.security_hub_controls.length > 0 && (
              <div>
                <Box variant="awsui-key-label">
                  <SpaceBetween size="xxs" direction="horizontal">
                    <span>Security Hub</span>
                    <Box variant="small" color="text-body-secondary">(Detective)</Box>
                  </SpaceBetween>
                </Box>
                <SpaceBetween size="xxs" direction="horizontal">
                  {control.security_hub_controls.map((hub, hidx) => (
                    <Badge key={hidx} color="green">{hub}</Badge>
                  ))}
                </SpaceBetween>
              </div>
            )}
            {control.control_tower_ids.length > 0 && (
              <div>
                <Box variant="awsui-key-label">
                  <SpaceBetween size="xxs" direction="horizontal">
                    <span>Control Tower</span>
                    <Box variant="small" color="text-body-secondary">(Preventive)</Box>
                  </SpaceBetween>
                </Box>
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

  const classificationInfo = FRAMEWORK_CLASSIFICATION_INFO[framework] || DEFAULT_CLASSIFICATION_INFO;

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
            <SpaceBetween size="xs" direction="horizontal">
              <span>AWS implementation guide</span>
              <Popover
                header="How are controls classified?"
                content={
                  <SpaceBetween size="s">
                    <Box variant="p">{classificationInfo.explanation}</Box>
                    <SpaceBetween size="xs">
                      <Box><Box variant="strong" color="text-status-success">Core</Box> — Has AWS Config rules for automated validation; referenced in major industry benchmarks (CIS, PCI DSS, SOC 2, FedRAMP)</Box>
                      <Box><Box variant="strong" color="text-status-info">Recommended</Box> — Has Security Hub or Control Tower managed controls, or appears in 3+ compliance frameworks</Box>
                      <Box><Box variant="strong" color="text-body-secondary">Enhanced</Box> — Advanced or service-specific controls for mature security programs</Box>
                    </SpaceBetween>
                    <Box variant="p" margin={{ top: 's' }}>Each control is also labeled as <Box variant="strong" display="inline" color="text-status-info">Detective</Box> (monitors after deployment via Config/Security Hub) or <Box variant="strong" display="inline" color="text-status-success">Preventive</Box> (blocks non-compliant actions via SCPs/Control Tower/OPA).</Box>
                  </SpaceBetween>
                }
                triggerType="custom"
                size="large"
              >
                <span style={{ cursor: 'pointer', verticalAlign: 'middle' }}>
                  <Icon name="status-info" variant="link" />
                </span>
              </Popover>
            </SpaceBetween>
          </Header>
        }
      >
        <SpaceBetween size="l">
          {/* Priority tier summary */}
          <ColumnLayout columns={3} variant="text-grid">
            {(['core', 'recommended', 'enhanced'] as const).map(tier => {
              const count = tier === 'core' ? totalCore
                : tier === 'recommended' ? totalRecommended
                : totalEnhanced;
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
          {totalCore > 0 && (
            <ExpandableSection
              variant="container"
              headerText={`Core controls (${totalCore})`}
              headerDescription="Enable these first for audit readiness"
              defaultExpanded
            >
              <SpaceBetween size="m">
                {coreControls.map(renderControlCard)}
                {coreScps.map((scp, idx) => renderScpCard(scp, idx))}
                {coreOpa.map((rule, idx) => renderOpaCard(rule, idx))}
              </SpaceBetween>
            </ExpandableSection>
          )}

          {/* Recommended controls - expandable */}
          {totalRecommended > 0 && (
            <ExpandableSection
              variant="container"
              headerText={`Recommended controls (${totalRecommended})`}
              headerDescription="Important controls most organizations should implement"
              defaultExpanded={totalCore === 0}
            >
              <SpaceBetween size="m">
                {recommendedControls.map(renderControlCard)}
                {recommendedScps.map((scp, idx) => renderScpCard(scp, idx))}
                {recommendedOpa.map((rule, idx) => renderOpaCard(rule, idx))}
              </SpaceBetween>
            </ExpandableSection>
          )}

          {/* Enhanced controls - collapsed by default */}
          {totalEnhanced > 0 && (
            <ExpandableSection
              variant="container"
              headerText={`Enhanced controls (${totalEnhanced})`}
              headerDescription="Advanced controls for mature security programs"
            >
              <SpaceBetween size="m">
                {enhancedControls.map(renderControlCard)}
                {enhancedScps.map((scp, idx) => renderScpCard(scp, idx))}
                {enhancedOpa.map((rule, idx) => renderOpaCard(rule, idx))}
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
              <Link external href="https://console.aws.amazon.com/organizations/">
                AWS Organizations (SCPs)
              </Link>
              <Link external href="https://www.openpolicyagent.org/docs/latest/">
                Open Policy Agent (OPA)
              </Link>
            </ColumnLayout>
          </Alert>
        </SpaceBetween>
      </Container>
    </>
  );
};

export default AWSImplementationGuide;
