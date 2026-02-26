import React, { useState } from 'react';
import { Download, FileText, FileSpreadsheet, FileJson, FileCode } from 'lucide-react';

interface ExportOptionsProps {
  onExport: (format: 'excel' | 'pdf' | 'json' | 'yaml') => void;
}

const ExportOptions: React.FC<ExportOptionsProps> = ({ onExport }) => {
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async (format: 'excel' | 'pdf' | 'json' | 'yaml') => {
    setIsExporting(true);
    try {
      // Call the API to download the file
      const response = await fetch(`http://localhost:5001/api/export?format=${format}`);
      
      if (!response.ok) {
        throw new Error(`Export failed: ${response.statusText}`);
      }
      
      // Get the blob and create a download link
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      
      // Set filename based on format
      const date = new Date().toISOString().split('T')[0].replace(/-/g, '');
      const extension = format === 'excel' ? 'xlsx' : format;
      a.download = `compliance_questionnaire_${date}.${extension}`;
      
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      await onExport(format);
    } catch (error) {
      console.error('Export error:', error);
      alert(`Export failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsExporting(false);
    }
  };

  const exportFormats = [
    {
      id: 'excel' as const,
      name: 'Excel Workbook',
      description: 'Comprehensive spreadsheet with all controls and questions',
      icon: FileSpreadsheet,
      color: 'from-green-500 to-emerald-600',
    },
    {
      id: 'pdf' as const,
      name: 'PDF Document',
      description: 'Professional fillable PDF for printing and signatures',
      icon: FileText,
      color: 'from-red-500 to-rose-600',
    },
    {
      id: 'json' as const,
      name: 'JSON Format',
      description: 'Machine-readable format for automation and integration',
      icon: FileJson,
      color: 'from-blue-500 to-indigo-600',
    },
    {
      id: 'yaml' as const,
      name: 'YAML Format',
      description: 'Human-readable configuration format',
      icon: FileCode,
      color: 'from-purple-500 to-violet-600',
    },
  ];

  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Export Questionnaire</h2>
          <p className="text-gray-600">
            Download your compliance questionnaire in your preferred format
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {exportFormats.map((format) => {
            const Icon = format.icon;
            return (
              <button
                key={format.id}
                onClick={() => handleExport(format.id)}
                disabled={isExporting}
                className="group relative bg-white rounded-xl border-2 border-gray-200 p-6 text-left hover:border-indigo-500 hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div className="flex items-start gap-4">
                  <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${format.color} flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform`}>
                    <Icon className="text-white" size={24} />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">
                      {format.name}
                    </h3>
                    <p className="text-sm text-gray-600">{format.description}</p>
                  </div>
                  <Download className="text-gray-400 group-hover:text-indigo-600 transition-colors" size={20} />
                </div>
              </button>
            );
          })}
        </div>

        {isExporting && (
          <div className="mt-8 bg-indigo-50 border border-indigo-200 rounded-lg p-4">
            <div className="flex items-center gap-3">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-indigo-600"></div>
              <span className="text-indigo-900 font-medium">Generating export...</span>
            </div>
          </div>
        )}

        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">Export Information</h3>
          <ul className="space-y-2 text-sm text-blue-800">
            <li className="flex items-start gap-2">
              <span className="text-blue-600 mt-0.5">•</span>
              <span><strong>Excel:</strong> Best for detailed analysis and data manipulation</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-600 mt-0.5">•</span>
              <span><strong>PDF:</strong> Professional format with fillable fields for manual completion</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-600 mt-0.5">•</span>
              <span><strong>JSON:</strong> Ideal for API integration and automated processing</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-600 mt-0.5">•</span>
              <span><strong>YAML:</strong> Human-readable format for configuration management</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ExportOptions;
