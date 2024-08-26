import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { MultiChartCardComponent } from './components/multi-chart-card/multi-chart-card.component';
import { MainService } from './services/main.service';
import { HttpClientModule } from '@angular/common/http';
import { NavegatorComponent } from './components/navegator/navegator.component';
import { AddTicketComponent } from './components/add-ticket/add-ticket.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ActualMonthComponent } from './components/actual-month/actual-month.component';
import { CardInfoComponent } from './components/card-info/card-info.component';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    MultiChartCardComponent,
    NavegatorComponent,
    AddTicketComponent,
    ActualMonthComponent,
    CardInfoComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule
  ],
  providers: [
    MainService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
