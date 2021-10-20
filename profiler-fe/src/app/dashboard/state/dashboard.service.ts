import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Aggregation, DashboardStore } from './dashboard.store';

export interface CreateTaskRequest {
  transformer: string;
  modelVersionId: number;
}


@Injectable({providedIn: 'root'})
export class DashboardService {
  constructor(private http: HttpClient, private store: DashboardStore) {
  }

  getAggregation(modelName: string, modelVersion: number) {
    this.http.get<Aggregation>(`http://localhost:5000/aggregation/${modelName}/${modelVersion}`).subscribe(
      res => this.store.update({aggregation: res})
    )
  }

  resetBatch(){
    this.store.update({batchReport: null})
  }
  // TODO: varivables 
  getBatch(modelName: string, modelVersion: number, batchName: string) {
    this.http.get(`http://localhost:5000/report/${modelName}/${modelVersion}/${batchName}`).subscribe(
      res => this.store.update({batchReport: res})
    )
  }
}