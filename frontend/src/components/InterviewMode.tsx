import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, CheckCircle, AlertCircle, FileText, Cloud, Shield, BookOpen } from 'lucide-react';
import { Question, ControlDetail } from '../services/complianceApi';
import AWSImplementationGuide from './AWSImplementationGuide';

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

interface InterviewModeProps {
  control: ControlDetail;
  responses: Record<string, string>;
  onResponseChange: (questionId: string, value: string) => void;
  onSave: (questionId: string) => void;
  onClose: () => void;
}

const InterviewMode: React.FC<InterviewModeProps> = ({
  control,
  responses,
  onResponseChange,
  onSave,
  onClose
}) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const questions = control.questions || [];
  
  // Safety check - close if no questions
  if (questions.length === 0) {
    return (
      <div className="fixed inset-0 bg-gray-900 bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4">No Questions Available</h3>
          <p className="text-gray-600 mb-6">This control does not have any questions generated yet.</p>
          <button onClick={onClose} className="btn-primary w-full">
            Close
          </button>
        </div>
      </div>
    );
  }
  
  const currentQuestion = questions[currentQuestionIndex];
  const answeredCount = questions.filter(q => responses[q.id]).length;
  const progress = Math.round((answeredCount / questions.length) * 100);

  const goToNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const goToPrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const isAnswered = !!responses[currentQuestion.id];

  return (
    <div className="fixed inset-0 bg-gray-900 bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-5xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-8 py-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <span 
                  className="font-mono text-lg font-bold cursor-help"
                  title={`${control.control.id.toUpperCase()} - ${control.control.title}`}
                >
                  {control.control.id.toUpperCase()}
                </span>
                <span 
                  className="badge bg-white bg-opacity-20 text-white cursor-help"
                  title={getFamilyFullName(control.control.family)}
                >
                  {control.control.family.toUpperCase()} - {getFamilyFullName(control.control.family)}
                </span>
              </div>
              <h2 className="text-2xl font-bold">{control.control.title}</h2>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-white hover:bg-opacity-20 rounded-lg p-2 transition-colors"
            >
              ✕
            </button>
          </div>
          
          {/* Progress */}
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="flex items-center justify-between text-sm mb-2">
                <span>Progress: {answeredCount}/{questions.length} questions</span>
                <span className="font-bold">{progress}%</span>
              </div>
              <div className="w-full bg-white bg-opacity-20 rounded-full h-2">
                <div
                  className="bg-white h-2 rounded-full transition-all duration-500"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-8">
          <div className="max-w-3xl mx-auto space-y-6">
            {/* Question Number */}
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 text-white flex items-center justify-center font-bold text-lg shadow-lg">
                {currentQuestionIndex + 1}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="badge bg-purple-100 text-purple-800 font-semibold">
                    {currentQuestion.question_type.replace(/_/g, ' ').toUpperCase()}
                  </span>
                  {isAnswered && (
                    <span className="badge bg-green-100 text-green-800 font-semibold flex items-center gap-1">
                      <CheckCircle size={14} />
                      Answered
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-500">
                  Question {currentQuestionIndex + 1} of {questions.length}
                </p>
              </div>
            </div>

            {/* Question Text */}
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-indigo-200 rounded-xl p-6">
              <p className="text-xl text-gray-900 font-medium leading-relaxed">
                {currentQuestion.question_text}
              </p>
            </div>

            {/* AWS Guidance - Only show if no detailed AWS Implementation Guide */}
            {currentQuestion.aws_service_guidance && 
             (!control.aws_controls || control.aws_controls.length === 0) && (
              <div className="bg-gradient-to-br from-orange-50 to-amber-50 border-2 border-orange-200 rounded-xl p-5">
                <div className="flex items-start gap-3">
                  <Cloud className="text-orange-600 flex-shrink-0 mt-1" size={24} />
                  <div>
                    <h4 className="font-bold text-orange-900 mb-2 flex items-center gap-2">
                      AWS Implementation Guidance
                    </h4>
                    <p className="text-orange-800 leading-relaxed">
                      {currentQuestion.aws_service_guidance}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* AWS Responsibility Indicator */}
            {control.aws_applicability && control.aws_applicability.responsibility && (
              <div className="flex items-center gap-3">
                <span className="text-xs font-semibold text-gray-600">AWS Responsibility:</span>
                <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold ${
                  control.aws_applicability.responsibility === 'aws'
                    ? 'bg-orange-100 text-orange-800 border border-orange-300'
                    : control.aws_applicability.responsibility === 'shared'
                    ? 'bg-green-100 text-green-800 border border-green-300'
                    : 'bg-blue-100 text-blue-800 border border-blue-300'
                }`}>
                  {control.aws_applicability.responsibility === 'aws' && (
                    <AlertCircle size={14} />
                  )}
                  {control.aws_applicability.responsibility === 'shared' && (
                    <CheckCircle size={14} />
                  )}
                  {control.aws_applicability.responsibility === 'customer' && (
                    <AlertCircle size={14} />
                  )}
                  {control.aws_applicability.responsibility === 'aws' && 'AWS Only'}
                  {control.aws_applicability.responsibility === 'shared' && 'Shared'}
                  {control.aws_applicability.responsibility === 'customer' && 'Customer Only'}
                </span>
                
                {/* Evidence link for AWS-only controls */}
                {control.aws_applicability.responsibility === 'aws' && (
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
            {control.framework_relevance && control.framework_relevance.relevant_frameworks.length > 0 && (
              <div className="bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200 rounded-xl p-4">
                <div className="flex items-start gap-3">
                  <BookOpen className="text-purple-600 flex-shrink-0 mt-0.5" size={20} />
                  <div className="flex-1">
                    <h4 className="font-bold text-purple-900 mb-2">Relevant Compliance Frameworks</h4>
                    <div className="flex flex-wrap gap-2 mb-2">
                      {control.framework_relevance.relevant_frameworks.map((framework, idx) => (
                        <span
                          key={idx}
                          className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold bg-purple-100 text-purple-800 border border-purple-300"
                        >
                          {framework}
                        </span>
                      ))}
                    </div>
                    {control.framework_relevance.has_specific_mappings && (
                      <p className="text-xs text-purple-700 mt-2">
                        ✓ Specific framework mappings available for this control
                      </p>
                    )}
                    <p className="text-xs text-purple-600 mt-1 italic">
                      {control.framework_relevance.notes}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* AWS Implementation Guide */}
            {control.aws_controls && control.aws_controls.length > 0 && (
              <AWSImplementationGuide
                controlId={control.control.id}
                awsControls={control.aws_controls}
              />
            )}

            {/* AWS Hints (fallback if no detailed controls) */}
            {(!control.aws_controls || control.aws_controls.length === 0) && control.aws_hints.length > 0 && (
              <div className="bg-gradient-to-br from-cyan-50 to-blue-50 border-2 border-cyan-200 rounded-xl p-5">
                <div className="flex items-start gap-3">
                  <Shield className="text-cyan-600 flex-shrink-0 mt-1" size={24} />
                  <div className="flex-1">
                    <h4 className="font-bold text-cyan-900 mb-3">AWS Managed Controls</h4>
                    <ul className="space-y-2">
                      {control.aws_hints.map((hint, idx) => (
                        <li key={idx} className="flex gap-2 text-sm text-cyan-800">
                          <span className="text-cyan-400 flex-shrink-0">▸</span>
                          <span>{hint}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}

            {/* Framework Mappings - Removed static content, will be populated from MCP data */}

            {/* Response Area */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">
                Client Response
              </label>
              <textarea
                value={responses[currentQuestion.id] || ''}
                onChange={(e) => onResponseChange(currentQuestion.id, e.target.value)}
                onBlur={() => onSave(currentQuestion.id)}
                placeholder="Document the client's response here..."
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-y min-h-[150px] text-base"
              />
            </div>
          </div>
        </div>

        {/* Footer Navigation */}
        <div className="border-t border-gray-200 px-8 py-4 bg-gray-50">
          <div className="flex items-center justify-between">
            <button
              onClick={goToPrevious}
              disabled={currentQuestionIndex === 0}
              className="btn-secondary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeft size={20} />
              Previous
            </button>
            
            <div className="text-sm text-gray-600">
              Question {currentQuestionIndex + 1} of {questions.length}
            </div>
            
            <button
              onClick={goToNext}
              disabled={currentQuestionIndex === questions.length - 1}
              className="btn-primary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
              <ChevronRight size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InterviewMode;
