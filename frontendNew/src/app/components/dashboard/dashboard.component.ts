import { Component } from '@angular/core';
import { MainService } from 'src/app/services/main.service';
import { MultiChartCardProps } from '../multi-chart-card/interface';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {


  constructor(private dataService: MainService) { }

  data:any
  data_semanal:any
  data_gasto_categoria:any

  ngOnInit(): void {
    this.dataService.get_monthly_data().subscribe((data: any) => {
      this.data = data;
    });

    this.dataService.get_weekly_data().subscribe((data: any) => {
      this.data_semanal = data;
    });

    this.dataService.get_gasto_categoria().subscribe((data: any) => {
      this.data_gasto_categoria = data;
    });


  }

}
