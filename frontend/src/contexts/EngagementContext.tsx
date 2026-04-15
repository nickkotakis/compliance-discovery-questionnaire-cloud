import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export interface EngagementConfig {
  customerName: string;
  framework: string;
  scope: string;
  regulator: string;
  engagementWeeks: number;
  meetingFrequency: string;
  maxMeetingDuration: number;
}

export interface SavedEngagement {
  id: string;
  config: EngagementConfig;
  savedAt: string;
}

interface EngagementContextType {
  activeEngagement: SavedEngagement | null;
  savedEngagements: SavedEngagement[];
  setActiveEngagement: (eng: SavedEngagement | null) => void;
  saveEngagement: (config: EngagementConfig) => SavedEngagement;
  deleteEngagement: (id: string) => void;
  updateActiveConfig: (config: EngagementConfig) => void;
}

const STORAGE_KEY = 'sas-engagements';
const ACTIVE_KEY = 'sas-active-engagement';

const loadSaved = (): SavedEngagement[] => {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }
  catch { return []; }
};

const loadActiveId = (): string | null => {
  return localStorage.getItem(ACTIVE_KEY);
};

const EngagementContext = createContext<EngagementContextType | null>(null);

export const EngagementProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [savedEngagements, setSavedEngagements] = useState<SavedEngagement[]>(loadSaved());
  const [activeEngagement, setActiveState] = useState<SavedEngagement | null>(null);

  // Load active engagement on mount
  useEffect(() => {
    const activeId = loadActiveId();
    if (activeId) {
      const eng = savedEngagements.find(e => e.id === activeId);
      if (eng) setActiveState(eng);
    }
  }, []);

  const persist = (engs: SavedEngagement[]) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(engs));
    setSavedEngagements(engs);
  };

  const setActiveEngagement = (eng: SavedEngagement | null) => {
    setActiveState(eng);
    localStorage.setItem(ACTIVE_KEY, eng?.id || '');
  };

  const saveEngagement = (config: EngagementConfig): SavedEngagement => {
    const id = activeEngagement?.id || `eng-${Date.now()}`;
    const eng: SavedEngagement = { id, config: { ...config }, savedAt: new Date().toISOString() };
    const updated = savedEngagements.filter(e => e.id !== id);
    updated.push(eng);
    persist(updated);
    setActiveEngagement(eng);
    return eng;
  };

  const deleteEngagement = (id: string) => {
    const updated = savedEngagements.filter(e => e.id !== id);
    persist(updated);
    if (activeEngagement?.id === id) {
      setActiveEngagement(null);
    }
  };

  const updateActiveConfig = (config: EngagementConfig) => {
    if (!activeEngagement) return;
    const eng: SavedEngagement = { ...activeEngagement, config: { ...config }, savedAt: new Date().toISOString() };
    const updated = savedEngagements.filter(e => e.id !== eng.id);
    updated.push(eng);
    persist(updated);
    setActiveState(eng);
  };

  return (
    <EngagementContext.Provider value={{
      activeEngagement, savedEngagements, setActiveEngagement,
      saveEngagement, deleteEngagement, updateActiveConfig,
    }}>
      {children}
    </EngagementContext.Provider>
  );
};

export const useEngagement = (): EngagementContextType => {
  const ctx = useContext(EngagementContext);
  if (!ctx) throw new Error('useEngagement must be used within EngagementProvider');
  return ctx;
};

export const FRAMEWORK_LABELS: Record<string, string> = {
  'nist-csf': 'NIST CSF 2.0',
  'nist-800-53': 'NIST 800-53 Rev 5',
  'cmmc': 'CMMC Level 2',
};
