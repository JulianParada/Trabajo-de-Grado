import { ComponentFixture, TestBed } from '@angular/core/testing';

import { KumuIntegrationComponent } from './kumu-integration.component';

describe('KumuIntegrationComponent', () => {
  let component: KumuIntegrationComponent;
  let fixture: ComponentFixture<KumuIntegrationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ KumuIntegrationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(KumuIntegrationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
