import { Injectable } from '@angular/core';
import { Aggregation, DashboardStore } from './dashboard.store';
import { ProfilerHttpService } from '../profiler-http.service';

@Injectable({ providedIn: 'root' })
export class DashboardService {
  constructor(private http: ProfilerHttpService, private store: DashboardStore) {}

  getAggregation(modelName: string, modelVersion: number) {
    this.http.get<Aggregation>(`aggregation/${modelName}/${modelVersion}`).subscribe((res) => {
      const sorted = res.scores.sort(
        (a, b) =>
          new Date(b.file_timestamp).getMilliseconds() -
          new Date(a.file_timestamp).getMilliseconds(),
      );

      this.store.update({ aggregation: { ...res, scores: sorted } });
    });
  }

  resetBatch() {
    this.store.update({ batchReport: null });
  }

  getBatch(modelName: string, modelVersion: number, batchName: string) {
    this.http
      .get(`report/${modelName}/${modelVersion}/${batchName}`)
      .subscribe((res) => this.store.update({ batchReport: res }));
  }
}
