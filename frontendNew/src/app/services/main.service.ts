import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { route } from '../app.component';

@Injectable({
  providedIn: 'root'
})
export class MainService {

  constructor(private http: HttpClient) { }


  get_monthly_data() {
    return this.http.get(route + '/get_month');
  }
  get_weekly_data() {
    return this.http.get(route + '/get_week');
  }

  get_gasto_categoria() {
    return this.http.get(route + '/get_tipo');
  }

  get_week_data_count() {
    return this.http.get(route + '/get_week_count');
  }

  // --------------- Navigator ----------------

  get_navigator() {
    return this.http.get("./assets/navigator.json");
  }


  // --------------- Add Ticket ----------------

  add_ticket(data: any) {
    return this.http.post(route + '/add_ticket', data);
  }


}
