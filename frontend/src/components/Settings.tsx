import React, { useState, useEffect } from 'react';
import { Save, Download, Upload, FileText, Database, User, Building2, CheckCircle, AlertCircle } from 'lucide-react';
import { complianceApi } from '../services/complianceApi';

interface SettingsProps {
  sessionId?: string;
  onSessionChange?: (sessionId: string) => void;
}

const Settings: React.FC<SettingsProps> = ({ sessionId, onSessionChange }) => {
  const [activeTab, setActiveTab] = useState<'session' | 'export'>('session');
  
  // Session Management State
  const [customerName, setCustomerName] = useState('');
  const [analystName, setAnalystName] = useState('');
  const [selectedFrameworks, setSelectedFrameworks] = useState<string[]>(['NIST 800-53']);
  const [sessions, setSessions] = useState<any[]>([]);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');
  
  // Export Options State
  const [exportFormat, setExportFormat] = useState<'excel' | 'pdf' | 'json' | 'yaml'>('excel');
  const [includeUnanswered, setIncludeUnanswered] = useState(true);
  const [includeAWSHints, setIncludeAWSHints] = useState(true);
  const [includeFrameworkMappings, setIncludeFrameworkMappings] = useState(true);
  const [exportStatus, setExportStatus] = useState<'idle' | 'exporting' | 'success' | 'error'>('idle');

  const availableFrameworks = [
    'NIST 800-53',
    'PCI-DSS',
    'HIPAA',
    'SOX',
    'FFIEC',
    'GLBA',
    'FedRAMP',
    'GDPR',
    'CCPA'
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
      alert('Please enter a customer name');
      return;
    }

    setSaveStatus('saving');
    try {
      const session = await complianceApi.createSession({
        customer_name: customerName,
        analyst_name: analystName || 'Unknown',
        frameworks: selectedFrameworks,
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
    setSelectedFrameworks(session.frameworks || ['NIST 800-53']);
    
    if (onSessionChange) {
      onSessionChange(session.id);
    }
  };

  const handleExport = async () => {
    setExportStatus('exporting');
    try {
      const blob = await complianceApi.exportQuestionnaire(exportFormat, {
        include_unanswered: includeUnanswered,
        include_aws_hints: includeAWSHints,
        include_framework_mappings: includeFrameworkMappings,
      });
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      
      // Map format to proper file extension
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
      setTimeout(() => setExportStatus('idle'), 3000);
    } catch (error) {
      console.error('Export failed:', error);
      setExportStatus('error');
      setTimeout(() => setExportStatus('idle'), 3000);
    }
  };

  const toggleFramework = (framework: string) => {
    if (selectedFrameworks.includes(framework)) {
      setSelectedFrameworks(selectedFrameworks.filter(f => f !== framework));
    } else {
      setSelectedFrameworks([...selectedFrameworks, framework]);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Settings</h2>
        <p className="text-gray-600">Manage assessment sessions and export options</p>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200">
        <div className="border-b border-gray-200">
          <div className="flex">
            <button
              onClick={() => setActiveTab('session')}
              className={`flex-1 px-6 py-4 text-sm font-medium transition-colors ${
                activeTab === 'session'
                  ? 'border-b-2 border-indigo-600 text-indigo-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className="flex items-center justify-center gap-2">
                <Database size={18} />
                Session Management
              </div>
            </button>
            <button
              onClick={() => setActiveTab('export')}
              className={`flex-1 px-6 py-4 text-sm font-medium transition-colors ${
                activeTab === 'export'
                  ? 'border-b-2 border-indigo-600 text-indigo-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className="flex items-center justify-center gap-2">
                <Download size={18} />
                Export Options
              </div>
            </button>
          </div>
        </div>

        <div className="p-6">
          {/* Session Management Tab */}
          {activeTab === 'session' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Current Assessment</h3>
                
                <div className="space-y-4">
                  {/* Customer Name */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <div className="flex items-center gap-2">
                        <Building2 size={16} />
                        Customer Name *
                      </div>
                    </label>
                    <input
                      type="text"
                      value={customerName}
                      onChange={(e) => setCustomerName(e.target.value)}
                      placeholder="Enter customer/organization name"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>

                  {/* Analyst Name */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <div className="flex items-center gap-2">
                        <User size={16} />
                        Analyst Name
                      </div>
                    </label>
                    <input
                      type="text"
                      value={analystName}
                      onChange={(e) => setAnalystName(e.target.value)}
                      placeholder="Enter your name"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>

                  {/* Frameworks */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <div className="flex items-center gap-2">
                        <FileText size={16} />
                        Target Frameworks
                      </div>
                    </label>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                      {availableFrameworks.map((framework) => (
                        <button
                          key={framework}
                          onClick={() => toggleFramework(framework)}
                          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                            selectedFrameworks.includes(framework)
                              ? 'bg-indigo-600 text-white shadow-md'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          {framework}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Save Button */}
                  <div className="flex items-center gap-3 pt-4">
                    <button
                      onClick={handleSaveSession}
                      disabled={saveStatus === 'saving'}
                      className="btn-primary flex items-center gap-2"
                    >
                      <Save size={18} />
                      {saveStatus === 'saving' ? 'Saving...' : 'Save Session'}
                    </button>
                    
                    {saveStatus === 'saved' && (
                      <div className="flex items-center gap-2 text-green-600">
                        <CheckCircle size={18} />
                        <span className="text-sm font-medium">Session saved!</span>
                      </div>
                    )}
                    
                    {saveStatus === 'error' && (
                      <div className="flex items-center gap-2 text-red-600">
                        <AlertCircle size={18} />
                        <span className="text-sm font-medium">Failed to save session</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Recent Sessions */}
              {sessions.length > 0 && (
                <div className="border-t border-gray-200 pt-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Sessions</h3>
                  <div className="space-y-2">
                    {sessions.slice(0, 5).map((session) => (
                      <button
                        key={session.id}
                        onClick={() => handleLoadSession(session)}
                        className="w-full text-left p-4 border border-gray-200 rounded-lg hover:border-indigo-300 hover:bg-indigo-50 transition-all"
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="font-medium text-gray-900">{session.customer_name}</div>
                            <div className="text-sm text-gray-500">
                              Analyst: {session.analyst_name} • {new Date(session.created_at).toLocaleDateString()}
                            </div>
                          </div>
                          <Upload size={18} className="text-gray-400" />
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Export Options Tab */}
          {activeTab === 'export' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Export Questionnaire</h3>
                
                <div className="space-y-4">
                  {/* Export Format */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Export Format
                    </label>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                      {(['excel', 'pdf', 'json', 'yaml'] as const).map((format) => (
                        <button
                          key={format}
                          onClick={() => setExportFormat(format)}
                          className={`px-4 py-3 rounded-lg text-sm font-medium transition-all ${
                            exportFormat === format
                              ? 'bg-indigo-600 text-white shadow-md'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          {format.toUpperCase()}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Export Options */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-3">
                      Include in Export
                    </label>
                    <div className="space-y-2">
                      <label className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={includeUnanswered}
                          onChange={(e) => setIncludeUnanswered(e.target.checked)}
                          className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                        />
                        <div>
                          <div className="text-sm font-medium text-gray-900">Unanswered Questions</div>
                          <div className="text-xs text-gray-500">Include controls without responses</div>
                        </div>
                      </label>

                      <label className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={includeAWSHints}
                          onChange={(e) => setIncludeAWSHints(e.target.checked)}
                          className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                        />
                        <div>
                          <div className="text-sm font-medium text-gray-900">AWS Implementation Guidance</div>
                          <div className="text-xs text-gray-500">Include AWS Config rules, Security Hub controls, etc.</div>
                        </div>
                      </label>

                      <label className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={includeFrameworkMappings}
                          onChange={(e) => setIncludeFrameworkMappings(e.target.checked)}
                          className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                        />
                        <div>
                          <div className="text-sm font-medium text-gray-900">Framework Mappings</div>
                          <div className="text-xs text-gray-500">Include PCI-DSS, HIPAA, SOX, FFIEC mappings</div>
                        </div>
                      </label>
                    </div>
                  </div>

                  {/* Export Button */}
                  <div className="flex items-center gap-3 pt-4">
                    <button
                      onClick={handleExport}
                      disabled={exportStatus === 'exporting'}
                      className="btn-primary flex items-center gap-2"
                    >
                      <Download size={18} />
                      {exportStatus === 'exporting' ? 'Exporting...' : `Export as ${exportFormat.toUpperCase()}`}
                    </button>
                    
                    {exportStatus === 'success' && (
                      <div className="flex items-center gap-2 text-green-600">
                        <CheckCircle size={18} />
                        <span className="text-sm font-medium">Export successful!</span>
                      </div>
                    )}
                    
                    {exportStatus === 'error' && (
                      <div className="flex items-center gap-2 text-red-600">
                        <AlertCircle size={18} />
                        <span className="text-sm font-medium">Export failed</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Export Info */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex gap-3">
                  <FileText className="text-blue-600 flex-shrink-0" size={20} />
                  <div className="text-sm text-blue-800">
                    <p className="font-medium mb-1">Export Information</p>
                    <ul className="list-disc list-inside space-y-1 text-xs">
                      <li>Excel: Includes multiple worksheets with controls, questions, and AWS hints</li>
                      <li>PDF: Formatted report suitable for client delivery</li>
                      <li>JSON/YAML: Machine-readable format for integration with other tools</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Settings;
