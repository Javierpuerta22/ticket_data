import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NavegatorComponent } from './navegator.component';

describe('NavegatorComponent', () => {
  let component: NavegatorComponent;
  let fixture: ComponentFixture<NavegatorComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [NavegatorComponent]
    });
    fixture = TestBed.createComponent(NavegatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
