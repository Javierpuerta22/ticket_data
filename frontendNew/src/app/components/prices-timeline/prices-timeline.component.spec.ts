import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PricesTimelineComponent } from './prices-timeline.component';

describe('PricesTimelineComponent', () => {
  let component: PricesTimelineComponent;
  let fixture: ComponentFixture<PricesTimelineComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PricesTimelineComponent]
    });
    fixture = TestBed.createComponent(PricesTimelineComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
