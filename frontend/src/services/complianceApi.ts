/**
 * API client for Compliance Discovery Questionnaire
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://zr5mc40584.execute-api.us-east-1.amazonaws.com/prod/api';

export interface Framework {
  id: string;
  label: string;
  functions?: Record<string, string>;
}

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
  aws_responsibility?: 'aws' | 'shared' | 'customer';
  function_name?: string;
  category?: string;
  category_name?: string;
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
    priority?: 'core' | 'recommended' | 'enhanced';
  }>;
  framework_relevance?: {
    control_id: string;
    family: string;
    relevant_frameworks: string[];
    notes: string;
    specific_mappings: Record<string, string[]>;
    has_specific_mappings: boolean;
  };
  organizational_requirements?: Array<{
    category: string;
    title: string;
    description: string;
  }>;
  organizational_category_metadata?: Record<string, {
    label: string;
    icon: string;
    color: string;
  }>;
  framework?: string;
  framework_label?: string;
  preventive_controls?: {
    scps: Array<{
      scp_name: string;
      scp_id: string;
      description: string;
      example_actions: string;
      priority?: 'core' | 'recommended' | 'enhanced';
    }>;
    opa_rules: Array<{
      opa_rule: string;
      description: string;
      resource_types: string;
      severity: string;
      priority?: 'core' | 'recommended' | 'enhanced';
    }>;
  };
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

  async getFrameworks(): Promise<{ frameworks: Framework[] }> {
    return this.fetch('/frameworks');
  }

  async getControls(family?: string, framework?: string): Promise<{ controls: Control[]; total: number; framework?: string; framework_label?: string }> {
    const params = new URLSearchParams();
    if (family) params.append('family', family);
    if (framework) params.append('framework', framework);
    const qs = params.toString();
    return this.fetch(`/controls${qs ? `?${qs}` : ''}`);
  }

  async getControl(controlId: string, framework?: string): Promise<ControlDetail> {
    const params = framework ? `?framework=${encodeURIComponent(framework)}` : '';
    return this.fetch(`/controls/${encodeURIComponent(controlId)}${params}`);
  }

  async getQuestions(filters?: {
    control_id?: string;
    family?: string;
    question_type?: string;
    framework?: string;
  }): Promise<{ questions: Question[]; total: number }> {
    const params = new URLSearchParams();
    if (filters?.control_id) params.append('control_id', filters.control_id);
    if (filters?.family) params.append('family', filters.family);
    if (filters?.question_type) params.append('question_type', filters.question_type);
    if (filters?.framework) params.append('framework', filters.framework);
    const qs = params.toString();
    return this.fetch(`/questions${qs ? `?${qs}` : ''}`);
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

  async exportTemplate(format: 'json' | 'csv' | 'excel' = 'json', framework?: string): Promise<BlankTemplate> {
    const params = new URLSearchParams();
    params.append('format', format);
    if (framework) params.append('framework', framework);
    return this.fetch(`/export?${params.toString()}`);
  }

  async getSessions(): Promise<{ sessions: Session[]; total: number }> {
    return this.fetch('/sessions');
  }

  async exportQuestionnaire(
    format: 'excel' | 'pdf' | 'json' | 'yaml',
    options?: {
      include_unanswered?: boolean;
      include_aws_hints?: boolean;
      include_framework_mappings?: boolean;
      framework?: string;
    }
  ): Promise<Blob> {
    const params = new URLSearchParams();
    params.append('format', format);
    if (options?.include_unanswered !== undefined) {
      params.append('include_unanswered', String(options.include_unanswered));
    }
    if (options?.include_aws_hints !== undefined) {
      params.append('include_aws_hints', String(options.include_aws_hints));
    }
    if (options?.include_framework_mappings !== undefined) {
      params.append('include_framework_mappings', String(options.include_framework_mappings));
    }
    if (options?.framework) {
      params.append('framework', options.framework);
    }

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (format === 'excel') {
      headers['Accept'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
    } else if (format === 'pdf') {
      headers['Accept'] = 'application/pdf';
    } else {
      headers['Accept'] = 'application/json';
    }

    const response = await fetch(`${this.baseUrl}/export?${params.toString()}`, {
      headers,
    });
    if (!response.ok) {
      throw new Error(`Export failed: ${response.statusText}`);
    }
    return response.blob();
  }
  async aiChat(message: string, engagementContext: Record<string, unknown>): Promise<{ response: string; model: string }> {
    const res = await fetch(`${this.baseUrl}/ai/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, engagement_context: engagementContext }),
    });
    if (!res.ok) throw new Error(`AI chat failed: ${res.statusText}`);
    return res.json();
  }
}

export const complianceApi = new ComplianceApi();
