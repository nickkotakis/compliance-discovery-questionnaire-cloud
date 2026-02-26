import React, { useState } from 'react';
import { Download, Plus } from 'lucide-react';
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
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <h1 className="text-2xl font-bold text-gray-900">
                Compliance Discovery Questionnaire
              </h1>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={handleExportTemplate}
                className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <Download size={18} />
                Export Template
              </button>
              {!sessionId && (
                <button
                  onClick={() => setShowNewSessionForm(true)}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Plus size={18} />
                  New Session
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* New Session Form Modal */}
      {showNewSessionForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full mx-4">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Create New Assessment Session
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Customer Name
                </label>
                <input
                  type="text"
                  value={customerName}
                  onChange={(e) => setCustomerName(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter customer name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Analyst Name
                </label>
                <input
                  type="text"
                  value={analystName}
                  onChange={(e) => setAnalystName(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter analyst name"
                />
              </div>
              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => setShowNewSessionForm(false)}
                  className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreateSession}
                  disabled={!customerName || !analystName}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  Create Session
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Session Info */}
      {sessionId && (
        <div className="bg-blue-50 border-b border-blue-200">
          <div className="max-w-7xl mx-auto px-6 py-3">
            <div className="flex items-center justify-between">
              <div className="text-sm text-blue-900">
                <strong>Active Session:</strong> {sessionId}
              </div>
              <button
                onClick={() => setSessionId(null)}
                className="text-sm text-blue-700 hover:text-blue-900 underline"
              >
                End Session
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <ComplianceQuestionnaire sessionId={sessionId || undefined} />
    </div>
  );
};

export default Compliance;
