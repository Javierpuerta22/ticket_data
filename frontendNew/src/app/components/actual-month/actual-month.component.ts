import { Component, OnInit } from '@angular/core';
import { Monthly_data } from 'src/app/core/interfaces/monthly';
import { MainService } from 'src/app/services/main.service';
import { MonthlyService } from 'src/app/services/monthly.service';

@Component({
  selector: 'app-actual-month',
  templateUrl: './actual-month.component.html',
  styleUrls: ['./actual-month.component.css']
})
export class ActualMonthComponent implements OnInit{

  data!:Monthly_data

  constructor(private dataService:MonthlyService) { }


  ngOnInit(): void {
    this.dataService.get_info().subscribe((data: any) => {
      this.data = data;
    });
  }

}
