import { Check } from './check';

export interface Overall {
  failed: number;
  suspicious: number;
  succeed: number;
  count: number;
}

export enum DataRowStatus {
  HAS_FAILED = 'has_failed',
  HAS_SUSPICIOUS = 'has_suspicious',
  HEALTHY = 'healthy',
}

export interface DataRowReport {
  id: number;
  features_checks: { [featureName: string]: any };
  status: DataRowStatus;
}

export interface ModelReport {
  model_name: string;
  model_version: number;
  batch_name: string;
  file_timestamp: string;
  report: DataRowReport[];
}
