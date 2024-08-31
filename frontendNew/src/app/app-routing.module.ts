import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { AddTicketComponent } from './components/add-ticket/add-ticket.component';
import { ActualMonthComponent } from './components/actual-month/actual-month.component';
import { PricesTimelineComponent } from './components/prices-timeline/prices-timeline.component';

const routes: Routes = [
  {path: '', redirectTo: '/dashboard', pathMatch: 'full'},
  {path: 'dashboard', component: DashboardComponent},
  {path: 'add_expense', component: AddTicketComponent},
  {path: 'actual_month', component: ActualMonthComponent},
  {path: 'prices_timeline', component: PricesTimelineComponent},
  {path: "**", redirectTo: "/dashboard"}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
