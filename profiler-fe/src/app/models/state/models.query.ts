import { Injectable } from '@angular/core';
import { Query } from '@datorama/akita';
import { ModelsState, ModelsStore } from './models.store';

@Injectable({ providedIn: 'root' })
export class ModelsQuery extends Query<ModelsState> {
  models$ = this.select((state) => state.models);

  constructor(protected store: ModelsStore) {
    super(store);
  }
}
