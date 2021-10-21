import { Injectable } from '@angular/core';
import { Store, StoreConfig } from '@datorama/akita';

export interface Model {
  name: string;
  version: number;
}
export interface ModelsState {
  models: Model[];
}

function createInitialState(): ModelsState {
  return {
    models: [],
  };
}

@Injectable({ providedIn: 'root' })
@StoreConfig({ name: 'models' })
export class ModelsStore extends Store<ModelsState> {
  constructor() {
    super(createInitialState());
  }
}
