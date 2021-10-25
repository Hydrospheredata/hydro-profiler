import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import {  BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MatButtonModule } from '@angular/material/button';
import {
  AkitaNgRouterStoreModule
} from '@datorama/akita-ng-router-store'
import { ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from './shared/shared.module';
import {LayoutModule} from "./layout/layout.module";

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    AppRoutingModule,
    HttpClientModule,
    MatButtonModule,
    AkitaNgRouterStoreModule,
    SharedModule,
    LayoutModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
