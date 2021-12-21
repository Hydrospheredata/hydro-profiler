import { Injectable } from '@angular/core';
import { Aggregation, DashboardStore } from './dashboard.store';
import { ProfilerHttpService } from '../profiler-http.service';

@Injectable({ providedIn: 'root' })
export class DashboardService {
  constructor(private http: ProfilerHttpService, private store: DashboardStore) {}

  getAggregation(modelName: string, modelVersion: number) {
    this.http
      .get<Aggregation>(`aggregation/${modelName}/${modelVersion}`)
      .subscribe((aggregation) => {
        const sorted = aggregation.batches.sort(
          (a, b) => new Date(a.file_timestamp).getTime() - new Date(b.file_timestamp).getTime(),
        );

        this.store.update({ aggregation: { ...aggregation, batches: sorted } });
      });
  }

  resetBatch() {
    this.store.update({ batchReport: null });
  }

  getBatch(modelName: string, modelVersion: number, batchName: string) {
    this.http
      .get(`report/${modelName}/${modelVersion}/${batchName}`)
      .subscribe((res: any) => this.store.update({ batchReport: res }));
  }
}
