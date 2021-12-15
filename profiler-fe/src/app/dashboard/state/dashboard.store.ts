import { Injectable } from '@angular/core';
import { StoreConfig, Store } from '@datorama/akita';

export interface Aggregation {
  features: string[];
  scores: Array<{
    batch_name: string;
    file_timestamp: string;
    scores: { [featureName: string]: number };
  }>;
}

export interface DashboardState {
  aggregation: Aggregation;
  batchReport: any;
}

function createInitialState() {
  return {
    aggregation: undefined,
    batchReport: undefined,
  };
}

@Injectable({ providedIn: 'root' })
@StoreConfig({ name: 'visualization' })
export class DashboardStore extends Store<DashboardState> {
  constructor() {
    super(createInitialState());
  }
}
