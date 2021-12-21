import { Injectable } from '@angular/core';
import { StoreConfig, Store } from '@datorama/akita';
import { ModelReport, Overall } from 'src/app/domain/report';

export interface Column {
  batch_name: string;
  file_timestamp: string;
  scores: { [featureName: string]: Overall };
  batch_rows_count: number;
}

export interface FeatureUnsucceedCount {
  failed: number;
  suspicious: number;
}

export type FeaturesOverall = { [featureName: string]: FeatureUnsucceedCount };

export interface AggregationBatch {
  model_name: string;
  model_version: number;
  rows_count: number;
  batch_name: string;
  file_timestamp: string;
  feature_overall: FeaturesOverall;
}

export interface Aggregation {
  model_name: string;
  model_version: number;
  features: string[];
  batches: AggregationBatch[];
}

export interface DashboardState {
  aggregation: Aggregation | null;
  batchReport: ModelReport | null;
}

function createInitialState() {
  return {
    aggregation: null,
    batchReport: null,
  };
}

@Injectable({ providedIn: 'root' })
@StoreConfig({ name: 'visualization' })
export class DashboardStore extends Store<DashboardState> {
  constructor() {
    super(createInitialState());
  }
}
