import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-card-info',
  templateUrl: './card-info.component.html',
  styleUrls: ['./card-info.component.css']
})
export class CardInfoComponent {

  @Input() title: string = '';
  @Input() value: string | number = '';
  @Input() label: string = '';

}
