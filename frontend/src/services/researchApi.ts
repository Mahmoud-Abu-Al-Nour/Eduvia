import api from './api'
import type {
  ArtifactPromotionResponse,
  ExperimentComparisonResponse,
  ResearchArtifact,
  ResearchEvaluation,
  ResearchExperiment,
  ResearchGenerationRequest,
  ResearchMetric,
  ResearchModelInfo,
  ResearchProject,
  ResearchRun,
  ResearchSnapshot,
  ResearchVariant,
} from '@/types'

export const researchApi = {
  // Models Catalog
  async getModels(): Promise<ResearchModelInfo[]> {
    return api.get<ResearchModelInfo[]>('/research/models')
  },

  // Projects
  async getProjects(): Promise<ResearchProject[]> {
    return api.get<ResearchProject[]>('/research/projects')
  },

  async createProject(data: {
    name: string
    description?: string | null
    research_question?: string | null
    hypothesis?: string | null
    status?: string
  }): Promise<ResearchProject> {
    return api.post<ResearchProject>('/research/projects', data)
  },

  async getProject(id: string): Promise<ResearchProject> {
    return api.get<ResearchProject>(`/research/projects/${id}`)
  },

  async updateProject(id: string, data: Partial<ResearchProject>): Promise<ResearchProject> {
    return api.patch<ResearchProject>(`/research/projects/${id}`, data)
  },

  async deleteProject(id: string): Promise<void> {
    return api.delete(`/research/projects/${id}`)
  },

  // Experiments
  async getExperiments(projectId: string): Promise<ResearchExperiment[]> {
    return api.get<ResearchExperiment[]>(`/research/projects/${projectId}/experiments`)
  },

  async createExperiment(
    projectId: string,
    data: {
      name: string
      description?: string | null
      research_question?: string | null
      hypothesis?: string | null
      status?: string
    }
  ): Promise<ResearchExperiment> {
    return api.post<ResearchExperiment>(`/research/projects/${projectId}/experiments`, data)
  },

  async getExperiment(id: string): Promise<ResearchExperiment> {
    return api.get<ResearchExperiment>(`/research/experiments/${id}`)
  },

  async updateExperiment(id: string, data: Partial<ResearchExperiment>): Promise<ResearchExperiment> {
    return api.patch<ResearchExperiment>(`/research/experiments/${id}`, data)
  },

  async deleteExperiment(id: string): Promise<void> {
    return api.delete(`/research/experiments/${id}`)
  },

  // Variants
  async getVariants(experimentId: string): Promise<ResearchVariant[]> {
    return api.get<ResearchVariant[]>(`/research/experiments/${experimentId}/variants`)
  },

  async createVariant(
    experimentId: string,
    data: {
      name: string
      description?: string | null
      configuration: Record<string, any>
    }
  ): Promise<ResearchVariant> {
    return api.post<ResearchVariant>(`/research/experiments/${experimentId}/variants`, data)
  },

  async cloneVariant(
    variantId: string,
    data: { new_name?: string; override_configuration?: Record<string, any> }
  ): Promise<ResearchVariant> {
    return api.post<ResearchVariant>(`/research/variants/${variantId}/clone`, data)
  },

  // Prompt Studio & Runs
  async executePromptStudio(req: ResearchGenerationRequest): Promise<ResearchRun> {
    return api.post<ResearchRun>('/research/prompt-studio/generate', req)
  },

  async getRun(id: string): Promise<ResearchRun> {
    return api.get<ResearchRun>(`/research/runs/${id}`)
  },

  async cloneRun(
    id: string,
    data: { override_user_prompt?: string; override_model_configuration?: Record<string, any> }
  ): Promise<ResearchRun> {
    return api.post<ResearchRun>(`/research/runs/${id}/clone`, data)
  },

  // Artifacts & Promotion
  async getArtifact(id: string): Promise<ResearchArtifact> {
    return api.get<ResearchArtifact>(`/research/artifacts/${id}`)
  },

  async exportArtifact(
    id: string,
    format: string = 'json'
  ): Promise<{ format: string; content: any; filename: string }> {
    return api.post<{ format: string; content: any; filename: string }>(
      `/research/artifacts/${id}/export?format=${format}`
    )
  },

  async promoteArtifact(
    id: string,
    req: { target_destination: string; notes?: string }
  ): Promise<ArtifactPromotionResponse> {
    return api.post<ArtifactPromotionResponse>(`/research/artifacts/${id}/promote`, req)
  },

  // Metrics & Evaluations
  async getMetrics(experimentId: string): Promise<ResearchMetric[]> {
    return api.get<ResearchMetric[]>(`/research/experiments/${experimentId}/metrics`)
  },

  async createMetric(
    experimentId: string,
    data: {
      name: string
      description?: string | null
      metric_type: string
      configuration?: Record<string, any>
    }
  ): Promise<ResearchMetric> {
    return api.post<ResearchMetric>(`/research/experiments/${experimentId}/metrics`, data)
  },

  async getEvaluations(artifactId: string): Promise<ResearchEvaluation[]> {
    return api.get<ResearchEvaluation[]>(`/research/artifacts/${artifactId}/evaluations`)
  },

  async createEvaluation(
    artifactId: string,
    data: {
      metric_id?: string | null
      metric_name: string
      value: Record<string, any>
      evaluator_type?: string
      notes?: string | null
    }
  ): Promise<ResearchEvaluation> {
    return api.post<ResearchEvaluation>(`/research/artifacts/${artifactId}/evaluations`, data)
  },

  // Comparison
  async getComparison(experimentId: string): Promise<ExperimentComparisonResponse> {
    return api.get<ExperimentComparisonResponse>(`/research/experiments/${experimentId}/compare`)
  },

  // Snapshots
  async getSnapshots(projectId: string): Promise<ResearchSnapshot[]> {
    return api.get<ResearchSnapshot[]>(`/research/projects/${projectId}/snapshots`)
  },

  async createSnapshot(
    projectId: string,
    data: {
      source_type: string
      source_reference: string
      snapshot_data: Record<string, any>
    }
  ): Promise<ResearchSnapshot> {
    return api.post<ResearchSnapshot>(`/research/projects/${projectId}/snapshots`, data)
  },
}
