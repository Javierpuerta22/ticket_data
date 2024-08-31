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
import { PricesTimelineComponent } from './components/prices-timeline/prices-timeline.component';
import { MonthlyService } from './services/monthly.service';
import { PricesService } from './services/prices.service';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    MultiChartCardComponent,
    NavegatorComponent,
    AddTicketComponent,
    ActualMonthComponent,
    CardInfoComponent,
    PricesTimelineComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule
  ],
  providers: [
    MainService, MonthlyService, PricesService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
