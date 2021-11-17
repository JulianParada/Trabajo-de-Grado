import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { KumuIntegrationComponent } from './components/kumu-integration/kumu-integration.component';
import { WelcomeComponent } from './components/welcome/welcome.component';
import { LoginComponent } from './components/login/login.component'
import { GestionarCredencialesComponent } from './components/administrador/gestionar-credenciales/gestionar-credenciales.component';

const routes: Routes = [
  {path: 'public/welcome', component: WelcomeComponent},
  {path: 'public/kumu', component: KumuIntegrationComponent},
  {path: 'public/login', component: LoginComponent},
  {path: 'public/dashboard', component:DashboardComponent},
  {path: 'admin/gestionar', component:GestionarCredencialesComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes, {useHash: true})],
  exports: [RouterModule]
})
export class AppRoutingModule { }
