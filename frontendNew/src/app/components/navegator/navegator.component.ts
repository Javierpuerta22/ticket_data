import { Component } from '@angular/core';
import { Navigator } from 'src/app/core/interfaces/navigator';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-navegator',
  templateUrl: './navegator.component.html',
  styleUrls: ['./navegator.component.css']
})
export class NavegatorComponent {

  constructor(private naviService: MainService) { }

  menu: Navigator[] = []

  ngOnInit(): void {
    this.naviService.get_navigator().subscribe((data: any) => {
      this.menu = data.navigator;
    });

    console.log(this.menu)

  }

}
