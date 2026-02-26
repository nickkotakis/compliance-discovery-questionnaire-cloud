import React, { useState, useEffect } from 'react';
import { complianceApi, Control, Question, ControlDetail } from '../services/complianceApi';
import { AlertCircle, ChevronDown, ChevronRight, FileText, Search, CheckCircle2, Circle, MessageSquare, Shield } from 'lucide-react';
import Sidebar from './Sidebar';
import Dashboard from './Dashboard';
import InterviewMode from './InterviewMode';
import AWSImplementationGuide from './AWSImplementationGuide';
import Settings from './Settings';

// NIST 800-53 Family Name Mappings
const FAMILY_NAMES: Record<string, string> = {
  'ac': 'Access Control',
  'at': 'Awareness and Training',
  'au': 'Audit and Accountability',
  'ca': 'Assessment, Authorization, and Monitoring',
  'cm': 'Configuration Management',
  'cp': 'Contingency Planning',
  'ia': 'Identification and Authentication',
  'ir': 'Incident Response',
  'ma': 'Maintenance',
  'mp': 'Media Protection',
  'pe': 'Physical and Environmental Protection',
  'pl': 'Planning',
  'pm': 'Program Management',
  'ps': 'Personnel Security',
  'pt': 'PII Processing and Transparency',
  'ra': 'Risk Assessment',
  'sa': 'System and Services Acquisition',
  'sc': 'System and Communications Protection',
  'si': 'System and Information Integrity',
  'sr': 'Supply Chain Risk Management'
};

const getFamilyFullName = (familyCode: string): string => {
  return FAMILY_NAMES[familyCode.toLowerCase()] || familyCode.toUpperCase();
};

interface ComplianceQuestionnaireProps {
  sessionId?: string;
}

const ComplianceQuestionnaire: React.FC<ComplianceQuestionnaireProps> = ({ sessionId: initialSessionId }) => {
  const [controls, setControls] = useState<Control[]>([]);
  const [selectedControl, setSelectedControl] = useState<ControlDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedControl, setExpandedControl] = useState<string | null>(null);
  const [responses, setResponses] = useState<Record<string, string>>({});
  const [selectedFamily, setSelectedFamily] = useState<string>('all');
  const [selectedResponsibility, setSelectedResponsibility] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeView, setActiveView] = useState<string>('questionnaire');
  const [allQuestions, setAllQuestions] = useState<Record<string, Question[]>>({});
  const [interviewControl, setInterviewControl] = useState<ControlDetail | null>(null);
  const [sessionId, setSessionId] = useState<string | undefined>(initialSessionId);

  useEffect(() => {
    loadControls();
  }, [selectedFamily]);

  const loadControls = async () => {
    try {
      setLoading(true);
      const family = selectedFamily === 'all' ? undefined : selectedFamily;
      const data = await complianceApi.getControls(family);
      setControls(data.controls);
      setError(null);
    } catch (err) {
      setError('Failed to load controls. Please ensure the API server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadControlDetail = async (controlId: string) => {
    try {
      const detail = await complianceApi.getControl(controlId);
      setSelectedControl(detail);
      setExpandedControl(controlId);
      // Store questions for this control
      setAllQuestions(prev => ({
        ...prev,
        [controlId]: detail.questions
      }));
    } catch (err) {
      setError(`Failed to load control ${controlId}`);
      console.error(err);
    }
  };

  const handleResponseChange = (questionId: string, value: string) => {
    setResponses(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const saveResponse = async (questionId: string) => {
    if (!sessionId) return;

    try {
      await complianceApi.recordResponse(sessionId, {
        question_id: questionId,
        answer: responses[questionId] || '',
      });
    } catch (err) {
      console.error('Failed to save response:', err);
    }
  };

  const families = Array.from(new Set(controls.map(c => c.family))).sort();

  const filteredControls = controls.filter(control => {
    const matchesFamily = selectedFamily === 'all' || control.family === selectedFamily;
    const matchesSearch = searchQuery === '' || 
      control.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      control.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      control.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesResponsibility = selectedResponsibility === 'all' || control.aws_responsibility === selectedResponsibility;
    
    return matchesFamily && matchesSearch && matchesResponsibility;
  });

  const totalQuestions = Object.values(allQuestions).flat().length;
  const answeredQuestions = Object.keys(responses).length;

  if (loading) {
    return (
      <div className="flex h-screen">
        <Sidebar activeView={activeView} onViewChange={setActiveView} controlCount={0} />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <div className="text-gray-600">Loading controls...</div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-screen">
        <Sidebar activeView={activeView} onViewChange={setActiveView} controlCount={0} />
        <div className="flex-1 flex items-center justify-center p-8">
          <div className="bg-red-50 border border-red-200 rounded-xl p-6 max-w-md">
            <div className="flex items-center gap-3 text-red-800">
              <AlertCircle size={24} />
              <div>
                <div className="font-semibold mb-1">Connection Error</div>
                <div className="text-sm">{error}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-50 to-indigo-50">
      <Sidebar 
        activeView={activeView} 
        onViewChange={setActiveView} 
        controlCount={controls.length}
        completionRate={totalQuestions > 0 ? Math.round((answeredQuestions / totalQuestions) * 100) : 0}
      />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 px-8 py-8 shadow-lg">
          <div className="max-w-6xl mx-auto">
            <h1 className="text-3xl font-bold text-white mb-2">
              NIST 800-53 Rev 5 Moderate Baseline
            </h1>
            <p className="text-indigo-100">
              Comprehensive compliance assessment questionnaire • {filteredControls.length} {filteredControls.length === controls.length ? 'controls' : `of ${controls.length} controls`}
              {selectedResponsibility !== 'all' && (
                <span className="ml-2">
                  ({selectedResponsibility === 'aws' ? '🟠 AWS Only' : selectedResponsibility === 'shared' ? '🟢 Shared' : '🔵 Customer Only'})
                </span>
              )}
              {selectedFamily !== 'all' && (
                <span className="ml-2">
                  • {selectedFamily.toUpperCase()} - {getFamilyFullName(selectedFamily)}
                </span>
              )}
            </p>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-indigo-200 px-8 py-4">
          <div className="max-w-6xl mx-auto flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-indigo-400" size={20} />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search controls by ID, title, or description..."
                className="w-full pl-10 pr-4 py-3 border-2 border-indigo-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white shadow-sm"
              />
            </div>
            <select
              value={selectedFamily}
              onChange={(e) => setSelectedFamily(e.target.value)}
              className="px-4 py-3 border-2 border-indigo-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white shadow-sm font-medium"
            >
              <option value="all">All Families</option>
              {families.map(family => (
                <option key={family} value={family}>
                  {family.toUpperCase()} - {getFamilyFullName(family)}
                </option>
              ))}
            </select>
            <select
              value={selectedResponsibility}
              onChange={(e) => setSelectedResponsibility(e.target.value)}
              className="px-4 py-3 border-2 border-indigo-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white shadow-sm font-medium"
            >
              <option value="all">All Responsibilities</option>
              <option value="aws">🟠 AWS Only</option>
              <option value="shared">🟢 Shared</option>
              <option value="customer">🔵 Customer Only</option>
            </select>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-8 py-6">
          <div className="max-w-6xl mx-auto">
            {activeView === 'dashboard' && (
              <Dashboard 
                totalControls={controls.length}
                answeredQuestions={answeredQuestions}
                totalQuestions={totalQuestions}
              />
            )}
            
            {activeView === 'settings' && (
              <Settings 
                sessionId={sessionId}
                onSessionChange={setSessionId}
              />
            )}
            
            {activeView === 'questionnaire' && (
              <div className="space-y-4">
                {filteredControls.map(control => {
                  const controlQuestions = allQuestions[control.id] || [];
                  const answeredCount = controlQuestions.filter(q => responses[q.id]).length;
                  const isComplete = answeredCount === controlQuestions.length && controlQuestions.length > 0;
                  
                  return (
                    <div
                      key={control.id}
                      className={`card transition-all duration-200 hover:shadow-xl border-2 ${
                        isComplete 
                          ? 'border-emerald-300 bg-gradient-to-br from-emerald-50 to-green-50' 
                          : 'border-indigo-200 bg-white hover:border-indigo-300'
                      }`}
                    >
                      <div
                        className="p-6 cursor-pointer"
                        onClick={() => {
                          if (expandedControl === control.id) {
                            setExpandedControl(null);
                            setSelectedControl(null);
                          } else {
                            loadControlDetail(control.id);
                          }
                        }}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex items-start gap-4 flex-1">
                            <div className="flex-shrink-0 mt-1">
                              {isComplete ? (
                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center shadow-lg">
                                  <CheckCircle2 className="text-white" size={24} />
                                </div>
                              ) : (
                                <div className="w-10 h-10 rounded-full border-3 border-gray-300 flex items-center justify-center">
                                  <Circle className="text-gray-300" size={24} />
                                </div>
                              )}
                            </div>
                            <div className="flex-1">
                              <div className="flex items-center gap-3 mb-2">
                                <span 
                                  className="font-mono text-base font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent cursor-help"
                                  title={`${control.id.toUpperCase()} - ${control.title}`}
                                >
                                  {control.id.toUpperCase()}
                                </span>
                                <span 
                                  className="badge bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold shadow-sm cursor-help"
                                  title={getFamilyFullName(control.family)}
                                >
                                  {control.family.toUpperCase()} - {getFamilyFullName(control.family)}
                                </span>
                                {controlQuestions.length > 0 && (
                                  <span className="badge bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 font-semibold">
                                    {answeredCount}/{controlQuestions.length} answered
                                  </span>
                                )}
                              </div>
                              <h3 className="text-lg font-bold text-gray-900 mb-2">
                                {control.title}
                              </h3>
                              <p className="text-sm text-gray-600 line-clamp-2 mb-4">
                                {control.description}
                              </p>
                              {controlQuestions.length > 0 && (
                                <button
                                  onClick={async (e) => {
                                    e.stopPropagation();
                                    const detail = await complianceApi.getControl(control.id);
                                    setInterviewControl(detail);
                                  }}
                                  className="btn-primary text-sm py-2 px-5 flex items-center gap-2 shadow-md hover:shadow-lg"
                                >
                                  <MessageSquare size={16} />
                                  Start Interview
                                </button>
                              )}
                            </div>
                          </div>
                          <div className="ml-4 flex-shrink-0">
                            {expandedControl === control.id ? (
                              <ChevronDown className="text-indigo-400" size={24} />
                            ) : (
                              <ChevronRight className="text-gray-400" size={24} />
                            )}
                          </div>
                        </div>
                      </div>

                      {/* Expanded Control Details */}
                      {expandedControl === control.id && selectedControl && (
                        <div className="border-t border-gray-200 bg-white p-8 space-y-6">
                          {/* AWS Implementation Guide */}
                          {selectedControl.aws_controls && selectedControl.aws_controls.length > 0 && (
                            <AWSImplementationGuide
                              controlId={selectedControl.control.id}
                              awsControls={selectedControl.aws_controls}
                            />
                          )}

                          {/* AWS Responsibility Indicator */}
                          {selectedControl.aws_applicability && selectedControl.aws_applicability.responsibility && (
                            <div className="flex items-center gap-3">
                              <span className="text-xs font-semibold text-gray-600">AWS Responsibility:</span>
                              <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold ${
                                selectedControl.aws_applicability.responsibility === 'aws'
                                  ? 'bg-orange-100 text-orange-800 border border-orange-300'
                                  : selectedControl.aws_applicability.responsibility === 'shared'
                                  ? 'bg-green-100 text-green-800 border border-green-300'
                                  : 'bg-blue-100 text-blue-800 border border-blue-300'
                              }`}>
                                {selectedControl.aws_applicability.responsibility === 'aws' && (
                                  <AlertCircle size={14} />
                                )}
                                {selectedControl.aws_applicability.responsibility === 'shared' && (
                                  <CheckCircle2 size={14} />
                                )}
                                {selectedControl.aws_applicability.responsibility === 'customer' && (
                                  <AlertCircle size={14} />
                                )}
                                {selectedControl.aws_applicability.responsibility === 'aws' && 'AWS Only'}
                                {selectedControl.aws_applicability.responsibility === 'shared' && 'Shared'}
                                {selectedControl.aws_applicability.responsibility === 'customer' && 'Customer Only'}
                              </span>
                              
                              {/* Evidence link for AWS-only controls */}
                              {selectedControl.aws_applicability.responsibility === 'aws' && (
                                <a
                                  href="https://console.aws.amazon.com/artifact/"
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold bg-orange-600 text-white hover:bg-orange-700 transition-colors"
                                >
                                  <Shield size={14} />
                                  Get Evidence from AWS Artifact
                                </a>
                              )}
                            </div>
                          )}

                          {/* Framework Relevance */}
                          {selectedControl.framework_relevance && selectedControl.framework_relevance.relevant_frameworks.length > 0 && (
                            <div className="bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200 rounded-xl p-5">
                              <h4 className="font-semibold text-purple-900 mb-3 flex items-center gap-2">
                                <FileText size={18} />
                                Relevant Compliance Frameworks
                              </h4>
                              <div className="flex flex-wrap gap-2 mb-3">
                                {selectedControl.framework_relevance.relevant_frameworks.map((framework, idx) => (
                                  <span
                                    key={idx}
                                    className="inline-flex items-center px-3 py-1 rounded-md text-xs font-semibold bg-purple-100 text-purple-800 border border-purple-300"
                                  >
                                    {framework}
                                  </span>
                                ))}
                              </div>
                              {selectedControl.framework_relevance.has_specific_mappings && (
                                <p className="text-sm text-purple-700 mb-2">
                                  ✓ Specific framework mappings available for this control
                                </p>
                              )}
                              <p className="text-sm text-purple-600 italic">
                                {selectedControl.framework_relevance.notes}
                              </p>
                            </div>
                          )}

                          {/* AWS Hints (fallback if no detailed controls) */}
                          {(!selectedControl.aws_controls || selectedControl.aws_controls.length === 0) && selectedControl.aws_hints.length > 0 && (
                            <div className="bg-gradient-to-br from-blue-50 to-cyan-50 border-2 border-blue-300 rounded-xl p-5">
                              <h4 className="font-semibold text-blue-900 mb-3 flex items-center gap-2">
                                <FileText size={18} />
                                AWS Managed Controls
                              </h4>
                              <ul className="text-sm text-blue-800 space-y-2">
                                {selectedControl.aws_hints.map((hint, idx) => (
                                  <li key={idx} className="flex gap-2">
                                    <span className="text-blue-400 flex-shrink-0">•</span>
                                    <span>{hint}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {/* Questions */}
                          <div className="space-y-5">
                            <div className="flex items-center justify-between mb-6">
                              <h4 className="text-xl font-bold text-gray-900">
                                Discovery Questions
                              </h4>
                              <span className="badge bg-blue-100 text-blue-700 text-sm px-3 py-1">
                                {selectedControl.questions.length} questions
                              </span>
                            </div>
                            {selectedControl.questions.map((question, idx) => {
                              const isAnswered = !!responses[question.id];
                              return (
                                <div
                                  key={question.id}
                                  className={`bg-gray-50 border-2 rounded-xl p-6 transition-all ${
                                    isAnswered ? 'border-green-300 bg-green-50' : 'border-gray-200 hover:border-gray-300'
                                  }`}
                                >
                                  <div className="flex items-start gap-4 mb-4">
                                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-sm">
                                      {idx + 1}
                                    </div>
                                    <div className="flex-1">
                                      <div className="flex items-center gap-2 mb-3">
                                        <span className="badge bg-purple-100 text-purple-800 font-semibold">
                                          {question.question_type.replace(/_/g, ' ').toUpperCase()}
                                        </span>
                                        {isAnswered && (
                                          <span className="badge bg-green-100 text-green-800 font-semibold">
                                            ✓ Answered
                                          </span>
                                        )}
                                      </div>
                                      <p className="text-gray-900 mb-4 font-medium text-base leading-relaxed">
                                        {question.question_text}
                                      </p>
                                      
                                      {question.aws_service_guidance && (
                                        <div className="mb-4 text-sm bg-blue-50 border-l-4 border-blue-400 p-4 rounded-r-lg">
                                          <div className="flex items-start gap-2">
                                            <FileText className="text-blue-600 flex-shrink-0 mt-0.5" size={16} />
                                            <div>
                                              <strong className="text-blue-900 block mb-1">AWS Guidance:</strong>
                                              <span className="text-blue-800">{question.aws_service_guidance}</span>
                                            </div>
                                          </div>
                                        </div>
                                      )}

                                      <textarea
                                        value={responses[question.id] || ''}
                                        onChange={(e) => handleResponseChange(question.id, e.target.value)}
                                        onBlur={() => saveResponse(question.id)}
                                        placeholder="Enter your detailed response here..."
                                        className="input-field resize-y min-h-[140px] font-normal"
                                      />
                                    </div>
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Interview Mode Modal */}
      {interviewControl && (
        <InterviewMode
          control={interviewControl}
          responses={responses}
          onResponseChange={handleResponseChange}
          onSave={saveResponse}
          onClose={() => setInterviewControl(null)}
        />
      )}
    </div>
  );
};

export default ComplianceQuestionnaire;
