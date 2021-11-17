import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionarCredencialesComponent } from './gestionar-credenciales.component';

describe('GestionarCredencialesComponent', () => {
  let component: GestionarCredencialesComponent;
  let fixture: ComponentFixture<GestionarCredencialesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GestionarCredencialesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GestionarCredencialesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
