import React from 'react';
import { FileText, Download, Settings, Home, Activity } from 'lucide-react';

interface SidebarProps {
  activeView: string;
  onViewChange: (view: string) => void;
  controlCount: number;
  completionRate: number;
}

const Sidebar: React.FC<SidebarProps> = ({ activeView, onViewChange, controlCount, completionRate }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'questionnaire', label: 'Questionnaire', icon: FileText },
    { id: 'export', label: 'Export', icon: Download },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="w-64 bg-white border-r border-gray-200 h-screen flex flex-col">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-lg flex items-center justify-center shadow-lg">
            <Home className="text-white" size={20} />
          </div>
          <div>
            <h1 className="text-lg font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              Compliance
            </h1>
            <p className="text-xs text-gray-500">Discovery Tool</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4">
        <div className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onViewChange(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  isActive
                    ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-medium shadow-md'
                    : 'text-gray-700 hover:bg-indigo-50 hover:text-indigo-700'
                }`}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </nav>

      <div className="p-4 border-t border-gray-200 space-y-3">
        <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl p-4 text-white shadow-lg">
          <div className="text-sm mb-1 font-medium opacity-90">Total Controls</div>
          <div className="text-3xl font-bold">{controlCount}</div>
          <div className="text-xs mt-1 opacity-75">NIST 800-53 Rev 5</div>
        </div>
        <div className="bg-gradient-to-br from-emerald-500 to-green-600 rounded-xl p-4 text-white shadow-lg">
          <div className="text-sm mb-1 font-medium opacity-90">Completion</div>
          <div className="text-3xl font-bold">{completionRate}%</div>
          <div className="w-full bg-white bg-opacity-30 rounded-full h-2 mt-2">
            <div
              className="bg-white h-2 rounded-full transition-all duration-500 shadow-sm"
              style={{ width: `${completionRate}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
