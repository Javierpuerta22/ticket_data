import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { PricesService } from 'src/app/services/prices.service';

@Component({
  selector: 'app-prices-timeline',
  templateUrl: './prices-timeline.component.html',
  styleUrls: ['./prices-timeline.component.css']
})
export class PricesTimelineComponent {

  constructor(private pricesservices: PricesService, private formgg: FormBuilder) { 
    this.form = this.formgg.group({
      type: '',
      producto: ''
    });
  }

  types: string[] = [];
  products: string[] = [];
  form!: FormGroup;
  data: any;

  ngOnInit(): void {

    this.pricesservices.getTypes().subscribe((data: any) => {
      this.types = data;
      this.form.patchValue({
        type: this.types[0]
      });
      this.pricesservices.getProducts(this.types[0]).subscribe((data: any) => {
        this.products = data;
        this.form.patchValue({
          producto: this.products[0]
    });})

  });
  }


  onChangeType(type: any) {
    this.pricesservices.getProducts(type.target.value).subscribe((data: any) => {
      this.products = data;
    });
  }

  onChangeProduct(product: any) {
    this.pricesservices.get_timeline_data(product.target.value).subscribe((data: any) => {
      this.data = data;
    });
  }

}
