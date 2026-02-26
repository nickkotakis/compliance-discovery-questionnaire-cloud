import React, { useState } from 'react';
import { Cloud, Shield, CheckCircle, Copy, ChevronDown, ChevronUp, ExternalLink } from 'lucide-react';

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
  const [isExpanded, setIsExpanded] = useState(false);
  const [copiedSection, setCopiedSection] = useState<string | null>(null);

  if (!awsControls || awsControls.length === 0) {
    return null;
  }

  const copyToClipboard = (text: string, section: string) => {
    navigator.clipboard.writeText(text);
    setCopiedSection(section);
    setTimeout(() => setCopiedSection(null), 2000);
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

  // Group controls by service
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
    <div className="bg-gradient-to-br from-indigo-50 to-purple-50 border-2 border-indigo-300 rounded-xl overflow-hidden">
      {/* Header */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-white hover:bg-opacity-30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center">
            <Cloud className="text-white" size={20} />
          </div>
          <div className="text-left">
            <h3 className="font-bold text-indigo-900 text-lg">
              AWS Implementation Guide
            </h3>
            <p className="text-sm text-indigo-700">
              {awsControls.length} AWS Control{awsControls.length !== 1 ? 's' : ''} • 
              {allConfigRules.length > 0 && ` ${allConfigRules.length} Config Rules •`}
              {allSecurityHubControls.length > 0 && ` ${allSecurityHubControls.length} Security Hub Controls •`}
              {allControlTowerIds.length > 0 && ` ${allControlTowerIds.length} Control Tower Controls`}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={(e) => {
              e.stopPropagation();
              copyToClipboard(generateImplementationReport(), 'full');
            }}
            className="px-3 py-2 bg-white rounded-lg border border-indigo-300 hover:border-indigo-500 hover:shadow-md transition-all flex items-center gap-2 text-sm font-medium text-indigo-700"
          >
            {copiedSection === 'full' ? (
              <>
                <CheckCircle size={16} />
                Copied!
              </>
            ) : (
              <>
                <Copy size={16} />
                Copy Report
              </>
            )}
          </button>
          {isExpanded ? (
            <ChevronUp className="text-indigo-700" size={24} />
          ) : (
            <ChevronDown className="text-indigo-700" size={24} />
          )}
        </div>
      </button>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="px-6 pb-6 space-y-6">
          {/* Quick Summary */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg p-4 border border-indigo-200">
              <div className="text-2xl font-bold text-indigo-600">{allServices.length}</div>
              <div className="text-xs text-gray-600 mt-1">AWS Services</div>
            </div>
            <div className="bg-white rounded-lg p-4 border border-indigo-200">
              <div className="text-2xl font-bold text-blue-600">{allConfigRules.length}</div>
              <div className="text-xs text-gray-600 mt-1">Config Rules</div>
            </div>
            <div className="bg-white rounded-lg p-4 border border-indigo-200">
              <div className="text-2xl font-bold text-purple-600">{allSecurityHubControls.length}</div>
              <div className="text-xs text-gray-600 mt-1">Security Hub</div>
            </div>
            <div className="bg-white rounded-lg p-4 border border-indigo-200">
              <div className="text-2xl font-bold text-pink-600">{allControlTowerIds.length}</div>
              <div className="text-xs text-gray-600 mt-1">Control Tower</div>
            </div>
          </div>

          {/* AWS Services */}
          {allServices.length > 0 && (
            <div className="bg-white rounded-lg p-5 border border-indigo-200">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-bold text-gray-900 flex items-center gap-2">
                  <Cloud size={18} className="text-indigo-600" />
                  AWS Services to Implement
                </h4>
                <button
                  onClick={() => copyToClipboard(allServices.join('\n'), 'services')}
                  className="text-xs text-indigo-600 hover:text-indigo-800 flex items-center gap-1"
                >
                  {copiedSection === 'services' ? <CheckCircle size={14} /> : <Copy size={14} />}
                  {copiedSection === 'services' ? 'Copied' : 'Copy'}
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {allServices.map((service, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm font-medium"
                  >
                    {service}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Config Rules */}
          {allConfigRules.length > 0 && (
            <div className="bg-white rounded-lg p-5 border border-blue-200">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-bold text-gray-900 flex items-center gap-2">
                  <Shield size={18} className="text-blue-600" />
                  AWS Config Rules to Enable
                </h4>
                <button
                  onClick={() => copyToClipboard(allConfigRules.join('\n'), 'config')}
                  className="text-xs text-blue-600 hover:text-blue-800 flex items-center gap-1"
                >
                  {copiedSection === 'config' ? <CheckCircle size={14} /> : <Copy size={14} />}
                  {copiedSection === 'config' ? 'Copied' : 'Copy'}
                </button>
              </div>
              <ul className="space-y-2">
                {allConfigRules.map((rule, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm">
                    <span className="text-blue-400 flex-shrink-0 mt-1">▸</span>
                    <code className="font-mono text-blue-800 bg-blue-50 px-2 py-1 rounded">
                      {rule}
                    </code>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Security Hub Controls */}
          {allSecurityHubControls.length > 0 && (
            <div className="bg-white rounded-lg p-5 border border-purple-200">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-bold text-gray-900 flex items-center gap-2">
                  <Shield size={18} className="text-purple-600" />
                  Security Hub Controls to Monitor
                </h4>
                <button
                  onClick={() => copyToClipboard(allSecurityHubControls.join('\n'), 'securityhub')}
                  className="text-xs text-purple-600 hover:text-purple-800 flex items-center gap-1"
                >
                  {copiedSection === 'securityhub' ? <CheckCircle size={14} /> : <Copy size={14} />}
                  {copiedSection === 'securityhub' ? 'Copied' : 'Copy'}
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {allSecurityHubControls.map((control, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-mono font-medium"
                  >
                    {control}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Control Tower Controls */}
          {allControlTowerIds.length > 0 && (
            <div className="bg-white rounded-lg p-5 border border-pink-200">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-bold text-gray-900 flex items-center gap-2">
                  <Shield size={18} className="text-pink-600" />
                  Control Tower Controls (if using Control Tower)
                </h4>
                <button
                  onClick={() => copyToClipboard(allControlTowerIds.join('\n'), 'controltower')}
                  className="text-xs text-pink-600 hover:text-pink-800 flex items-center gap-1"
                >
                  {copiedSection === 'controltower' ? <CheckCircle size={14} /> : <Copy size={14} />}
                  {copiedSection === 'controltower' ? 'Copied' : 'Copy'}
                </button>
              </div>
              <ul className="space-y-2">
                {allControlTowerIds.map((ct, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm">
                    <span className="text-pink-400 flex-shrink-0 mt-1">▸</span>
                    <code className="font-mono text-pink-800 bg-pink-50 px-2 py-1 rounded">
                      {ct}
                    </code>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Detailed Controls - Organized by Service */}
          <div className="space-y-4">
            <h4 className="font-bold text-gray-900 text-lg">AWS Control Guides by Service</h4>
            {Object.entries(controlsByService).map(([service, controls]) => (
              <div key={service} className="bg-white rounded-lg border-2 border-indigo-200 overflow-hidden">
                {/* Service Header */}
                <div className="bg-gradient-to-r from-indigo-100 to-purple-100 px-5 py-3 border-b border-indigo-200">
                  <div className="flex items-center gap-3">
                    <Cloud size={20} className="text-indigo-600" />
                    <h5 className="font-bold text-indigo-900">{service}</h5>
                    <span className="ml-auto px-3 py-1 bg-indigo-200 text-indigo-800 rounded-full text-xs font-semibold">
                      {controls.length} control{controls.length !== 1 ? 's' : ''}
                    </span>
                  </div>
                </div>

                {/* Controls for this service */}
                <div className="p-5 space-y-4">
                  {controls.map((control, idx) => (
                    <div key={idx} className="border-l-4 border-indigo-300 pl-4 py-2">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs font-mono">
                              {control.control_id}
                            </span>
                            <h6 className="font-semibold text-gray-900 text-sm">{control.title}</h6>
                          </div>
                          <p className="text-sm text-gray-600 leading-relaxed">{control.description}</p>
                        </div>
                      </div>

                      {/* Managed Controls for this specific control */}
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-3">
                        {control.config_rules.length > 0 && (
                          <div>
                            <div className="text-xs font-semibold text-blue-600 mb-1">Config Rules</div>
                            <div className="space-y-1">
                              {control.config_rules.map((rule, ridx) => (
                                <div key={ridx} className="text-xs font-mono text-blue-700 bg-blue-50 px-2 py-1 rounded">
                                  {rule}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {control.security_hub_controls.length > 0 && (
                          <div>
                            <div className="text-xs font-semibold text-purple-600 mb-1">Security Hub</div>
                            <div className="flex flex-wrap gap-1">
                              {control.security_hub_controls.map((hub, hidx) => (
                                <span key={hidx} className="text-xs font-mono px-2 py-1 bg-purple-50 text-purple-700 rounded">
                                  {hub}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        {control.control_tower_ids.length > 0 && (
                          <div>
                            <div className="text-xs font-semibold text-pink-600 mb-1">Control Tower</div>
                            <div className="space-y-1">
                              {control.control_tower_ids.map((ct, ctidx) => (
                                <div key={ctidx} className="text-xs font-mono text-pink-700 bg-pink-50 px-2 py-1 rounded">
                                  {ct}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Quick Links */}
          <div className="bg-gradient-to-r from-indigo-100 to-purple-100 rounded-lg p-5 border border-indigo-300">
            <h4 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
              <ExternalLink size={18} className="text-indigo-600" />
              Helpful AWS Resources
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <a
                href="https://console.aws.amazon.com/config/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm text-indigo-700 hover:text-indigo-900 hover:underline"
              >
                <ExternalLink size={14} />
                AWS Config Console
              </a>
              <a
                href="https://console.aws.amazon.com/securityhub/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm text-indigo-700 hover:text-indigo-900 hover:underline"
              >
                <ExternalLink size={14} />
                Security Hub Console
              </a>
              <a
                href="https://console.aws.amazon.com/controltower/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm text-indigo-700 hover:text-indigo-900 hover:underline"
              >
                <ExternalLink size={14} />
                Control Tower Console
              </a>
              <a
                href="https://console.aws.amazon.com/artifact/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm text-indigo-700 hover:text-indigo-900 hover:underline"
              >
                <ExternalLink size={14} />
                AWS Artifact (Compliance Reports)
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AWSImplementationGuide;
