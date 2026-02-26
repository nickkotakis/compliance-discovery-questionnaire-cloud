import React, { useState } from 'react';
import { Save, User, Building2, CheckSquare, Clock } from 'lucide-react';

interface SettingsProps {
  customerName: string;
  analystName: string;
  frameworks: string[];
  onSave: (settings: { customerName: string; analystName: string; frameworks: string[] }) => void;
  recentSessions?: Array<{
    id: string;
    customer_name: string;
    created_at: string;
    status: string;
  }>;
  onLoadSession?: (sessionId: string) => void;
}

const Settings: React.FC<SettingsProps> = ({
  customerName,
  analystName,
  frameworks,
  onSave,
  recentSessions = [],
  onLoadSession,
}) => {
  const [localCustomerName, setLocalCustomerName] = useState(customerName);
  const [localAnalystName, setLocalAnalystName] = useState(analystName);
  const [localFrameworks, setLocalFrameworks] = useState<string[]>(frameworks);

  const availableFrameworks = [
    'NIST 800-53',
    'SOC 2',
    'ISO 27001',
    'PCI DSS',
    'HIPAA',
    'FedRAMP',
  ];

  const handleFrameworkToggle = (framework: string) => {
    if (localFrameworks.includes(framework)) {
      setLocalFrameworks(localFrameworks.filter((f) => f !== framework));
    } else {
      setLocalFrameworks([...localFrameworks, framework]);
    }
  };

  const handleSave = () => {
    onSave({
      customerName: localCustomerName,
      analystName: localAnalystName,
      frameworks: localFrameworks,
    });
  };

  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Session Settings</h2>
          <p className="text-gray-600">Configure your assessment session details</p>
        </div>

        <div className="space-y-6">
          {/* Session Information */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <User size={20} className="text-indigo-600" />
              Session Information
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Building2 size={16} className="inline mr-1" />
                  Customer Name
                </label>
                <input
                  type="text"
                  value={localCustomerName}
                  onChange={(e) => setLocalCustomerName(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="Enter customer organization name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <User size={16} className="inline mr-1" />
                  Analyst Name
                </label>
                <input
                  type="text"
                  value={localAnalystName}
                  onChange={(e) => setLocalAnalystName(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="Enter your name"
                />
              </div>
            </div>
          </div>

          {/* Frameworks */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <CheckSquare size={20} className="text-indigo-600" />
              Compliance Frameworks
            </h3>
            <div className="grid grid-cols-2 gap-3">
              {availableFrameworks.map((framework) => (
                <button
                  key={framework}
                  onClick={() => handleFrameworkToggle(framework)}
                  className={`px-4 py-3 rounded-lg border-2 text-left transition-all ${
                    localFrameworks.includes(framework)
                      ? 'border-indigo-500 bg-indigo-50 text-indigo-900'
                      : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <div
                      className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
                        localFrameworks.includes(framework)
                          ? 'border-indigo-500 bg-indigo-500'
                          : 'border-gray-300'
                      }`}
                    >
                      {localFrameworks.includes(framework) && (
                        <CheckSquare size={16} className="text-white" />
                      )}
                    </div>
                    <span className="font-medium">{framework}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Recent Sessions */}
          {recentSessions.length > 0 && (
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Clock size={20} className="text-indigo-600" />
                Recent Sessions
              </h3>
              <div className="space-y-2">
                {recentSessions.slice(0, 5).map((session) => (
                  <button
                    key={session.id}
                    onClick={() => onLoadSession?.(session.id)}
                    className="w-full px-4 py-3 bg-gray-50 hover:bg-indigo-50 rounded-lg text-left transition-colors border border-gray-200 hover:border-indigo-300"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium text-gray-900">
                          {session.customer_name || 'Unnamed Session'}
                        </div>
                        <div className="text-sm text-gray-500">
                          {new Date(session.created_at).toLocaleDateString()}
                        </div>
                      </div>
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-medium ${
                          session.status === 'active'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {session.status}
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Save Button */}
          <button
            onClick={handleSave}
            className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 px-6 rounded-lg font-medium hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
          >
            <Save size={20} />
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings;
