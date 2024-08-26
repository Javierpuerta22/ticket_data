import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { route } from '../app.component';

@Injectable({
  providedIn: 'root'
})
export class MonthlyService {

  constructor(private http: HttpClient) { }

  get_info() {
    return this.http.get(route + '/monthly/data');
  }



}
