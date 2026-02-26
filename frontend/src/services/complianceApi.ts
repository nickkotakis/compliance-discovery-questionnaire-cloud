/**
 * API client for Compliance Discovery Questionnaire
 */

const API_BASE_URL = 'http://localhost:5001/api';

export interface Control {
  id: string;
  title: string;
  description: string;
  family: string;
  in_moderate_baseline: boolean;
  parameter_count?: number;
  enhancement_count?: number;
  parameters?: Parameter[];
  enhancements?: Enhancement[];
}

export interface Parameter {
  id: string;
  label: string;
  description: string;
  constraints?: string[];
}

export interface Enhancement {
  id: string;
  title: string;
  description: string;
  in_moderate_baseline: boolean;
}

export interface Question {
  id: string;
  control_id: string;
  question_text: string;
  question_type: string;
  family: string;
  aws_service_guidance?: string;
}

export interface Session {
  id: string;
  customer_name: string;
  analyst_name: string;
  frameworks: string[];
  created_at: string;
  updated_at: string;
  status: string;
  responses: Record<string, Response>;
  evidence: Record<string, any>;
}

export interface Response {
  answer: string;
  notes?: string;
  timestamp: string;
}

export interface ControlDetail {
  control: Control;
  questions: Question[];
  aws_hints: string[];
  aws_applicability?: {
    applicable: boolean;
    responsibility: 'aws' | 'customer' | 'shared' | 'unknown';
    message: string;
    artifact_links: Array<{
      name: string;
      url: string;
      description: string;
    }>;
    controls: string[];
  };
  aws_controls?: Array<{
    control_id: string;
    title: string;
    description: string;
    services: string[];
    config_rules: string[];
    security_hub_controls: string[];
    control_tower_ids: string[];
    frameworks: string[];
  }>;
}

export interface TemplateMetadata {
  template_version: string;
  baseline_version: string;
  export_date: string;
  total_control_count: number;
  frameworks_included: string[];
}

export interface BlankTemplate {
  metadata: TemplateMetadata;
  controls: Control[];
  questions: Record<string, Question[]>;
}

class ComplianceApi {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    return response.json();
  }

  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    return this.fetch('/health');
  }

  async getControls(family?: string): Promise<{ controls: Control[]; total: number }> {
    const params = family ? `?family=${encodeURIComponent(family)}` : '';
    return this.fetch(`/controls${params}`);
  }

  async getControl(controlId: string): Promise<ControlDetail> {
    return this.fetch(`/controls/${encodeURIComponent(controlId)}`);
  }

  async getQuestions(filters?: {
    control_id?: string;
    family?: string;
    question_type?: string;
  }): Promise<{ questions: Question[]; total: number }> {
    const params = new URLSearchParams();
    if (filters?.control_id) params.append('control_id', filters.control_id);
    if (filters?.family) params.append('family', filters.family);
    if (filters?.question_type) params.append('question_type', filters.question_type);

    const queryString = params.toString();
    return this.fetch(`/questions${queryString ? `?${queryString}` : ''}`);
  }

  async createSession(data: {
    customer_name: string;
    analyst_name: string;
    frameworks: string[];
  }): Promise<Session> {
    return this.fetch('/session', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getSession(sessionId: string): Promise<Session> {
    return this.fetch(`/session/${encodeURIComponent(sessionId)}`);
  }

  async recordResponse(
    sessionId: string,
    data: {
      question_id: string;
      answer: string;
      notes?: string;
    }
  ): Promise<{ success: boolean }> {
    return this.fetch(`/session/${encodeURIComponent(sessionId)}/response`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async exportTemplate(format: 'json' | 'csv' | 'excel' = 'json'): Promise<BlankTemplate> {
    return this.fetch(`/export?format=${format}`);
  }
}

export const complianceApi = new ComplianceApi();
