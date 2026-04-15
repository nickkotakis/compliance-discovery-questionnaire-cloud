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

export interface ScheduleMeeting {
  id: string;
  topic: string;
  functions: string;
  controls: string;
  duration: number;
  proserve: string;
  attendees: string[];
  agendaItems: { topic: string; controls: string; minutes: number }[];
}

export interface EvidenceItem {
  id: string;
  meeting: string;
  artifact: string;
  controlMapping: string;
  status: string;
  notes: string;
}

interface EngagementContextType {
  activeEngagement: SavedEngagement | null;
  savedEngagements: SavedEngagement[];
  setActiveEngagement: (eng: SavedEngagement | null) => void;
  saveEngagement: (config: EngagementConfig) => SavedEngagement;
  deleteEngagement: (id: string) => void;
  updateActiveConfig: (config: EngagementConfig) => void;
  // Schedule
  scheduleMeetings: ScheduleMeeting[];
  setScheduleMeetings: (meetings: ScheduleMeeting[]) => void;
  // Evidence
  evidenceItems: EvidenceItem[];
  setEvidenceItems: (items: EvidenceItem[]) => void;
  updateEvidenceStatus: (id: string, status: string) => void;
  updateEvidenceNotes: (id: string, notes: string) => void;
}

const STORAGE_KEY = 'sas-engagements';
const ACTIVE_KEY = 'sas-active-engagement';
const SCHEDULE_KEY = 'sas-schedule';
const EVIDENCE_KEY = 'sas-evidence';

const loadSaved = (): SavedEngagement[] => { try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch { return []; } };
const loadActiveId = (): string | null => localStorage.getItem(ACTIVE_KEY);
const loadSchedule = (engId: string): ScheduleMeeting[] => { try { return JSON.parse(localStorage.getItem(`${SCHEDULE_KEY}-${engId}`) || '[]'); } catch { return []; } };
const loadEvidence = (engId: string): EvidenceItem[] => { try { return JSON.parse(localStorage.getItem(`${EVIDENCE_KEY}-${engId}`) || '[]'); } catch { return []; } };

const EngagementContext = createContext<EngagementContextType | null>(null);

export const EngagementProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [savedEngagements, setSavedEngagements] = useState<SavedEngagement[]>(loadSaved());
  const [activeEngagement, setActiveState] = useState<SavedEngagement | null>(null);
  const [scheduleMeetings, setScheduleState] = useState<ScheduleMeeting[]>([]);
  const [evidenceItems, setEvidenceState] = useState<EvidenceItem[]>([]);

  useEffect(() => {
    const activeId = loadActiveId();
    if (activeId) {
      const eng = savedEngagements.find(e => e.id === activeId);
      if (eng) {
        setActiveState(eng);
        setScheduleState(loadSchedule(eng.id));
        setEvidenceState(loadEvidence(eng.id));
      }
    }
  }, []);

  const persist = (engs: SavedEngagement[]) => { localStorage.setItem(STORAGE_KEY, JSON.stringify(engs)); setSavedEngagements(engs); };

  const setActiveEngagement = (eng: SavedEngagement | null) => {
    setActiveState(eng);
    localStorage.setItem(ACTIVE_KEY, eng?.id || '');
    if (eng) {
      setScheduleState(loadSchedule(eng.id));
      setEvidenceState(loadEvidence(eng.id));
    } else {
      setScheduleState([]);
      setEvidenceState([]);
    }
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
    localStorage.removeItem(`${SCHEDULE_KEY}-${id}`);
    localStorage.removeItem(`${EVIDENCE_KEY}-${id}`);
    if (activeEngagement?.id === id) setActiveEngagement(null);
  };

  const updateActiveConfig = (config: EngagementConfig) => {
    if (!activeEngagement) return;
    const eng: SavedEngagement = { ...activeEngagement, config: { ...config }, savedAt: new Date().toISOString() };
    const updated = savedEngagements.filter(e => e.id !== eng.id);
    updated.push(eng);
    persist(updated);
    setActiveState(eng);
  };

  const setScheduleMeetings = (meetings: ScheduleMeeting[]) => {
    setScheduleState(meetings);
    if (activeEngagement) localStorage.setItem(`${SCHEDULE_KEY}-${activeEngagement.id}`, JSON.stringify(meetings));
  };

  const setEvidenceItems = (items: EvidenceItem[]) => {
    setEvidenceState(items);
    if (activeEngagement) localStorage.setItem(`${EVIDENCE_KEY}-${activeEngagement.id}`, JSON.stringify(items));
  };

  const updateEvidenceStatus = (id: string, status: string) => {
    const updated = evidenceItems.map(i => i.id === id ? { ...i, status } : i);
    setEvidenceItems(updated);
  };

  const updateEvidenceNotes = (id: string, notes: string) => {
    const updated = evidenceItems.map(i => i.id === id ? { ...i, notes } : i);
    setEvidenceItems(updated);
  };

  return (
    <EngagementContext.Provider value={{
      activeEngagement, savedEngagements, setActiveEngagement,
      saveEngagement, deleteEngagement, updateActiveConfig,
      scheduleMeetings, setScheduleMeetings,
      evidenceItems, setEvidenceItems, updateEvidenceStatus, updateEvidenceNotes,
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
