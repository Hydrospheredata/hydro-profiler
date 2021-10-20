import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Model, ModelsStore } from './models.store';


@Injectable({providedIn: 'root'})
export class ModelsService {
  constructor(private http: HttpClient, private store: ModelsStore) {
  }

  getAll(){
    this.http.get<Model[]>(`http://localhost:5000/models`).subscribe(
      res => this.store.update({models: res})
    )
  }

  addModel(model: Model) {
    const models = this.store.getValue().models
    this.store.update({models: [...models, model]})
  }

  registerModel(fd: FormData) {
    return this.http.post(`http://localhost:5000/model`, fd)
  }

  loadBatch(fd: FormData){
    return this.http.post(`http://localhost:5000/model/batch`, fd)
  }
}
