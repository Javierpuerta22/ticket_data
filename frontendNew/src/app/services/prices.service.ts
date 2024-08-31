import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { route } from '../app.component';

@Injectable({
  providedIn: 'root'
})
export class PricesService {

  constructor(private http: HttpClient) { }


  getTypes() {
    return this.http.get(route + '/prices/data/type');
  }

  getProducts(type: string) {
    return this.http.get(route + '/prices/data/subtype', { params: { type: type } });
  }

  get_timeline_data(product:string) {
    return this.http.post(route + '/prices/data/timeline', { product: product });
  }


}
