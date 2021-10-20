import { Injectable } from '@angular/core';
import { Query } from '@datorama/akita';
import { DashboardState, DashboardStore,  } from './dashboard.store';

@Injectable({providedIn: 'root'})
export class DashboardQuery extends Query<DashboardState> {
  agg$ = this.select(state => state.aggregation);
  batch$ = this.select(state => state.batchReport);

  constructor(protected store: DashboardStore) {
    super(store);
  }
}
