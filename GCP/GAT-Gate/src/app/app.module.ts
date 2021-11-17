import { NgModule } from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './components/shared/navbar/navbar.component';
import { FooterComponent } from './components/shared/footer/footer.component';
import { LoginComponent } from './components/login/login.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { WelcomeComponent } from './components/welcome/welcome.component';
import { KumuIntegrationComponent } from './components/kumu-integration/kumu-integration.component';
import { NewUserComponent } from './components/administrador/new-user/nuevo-user.component';
import { ListUsersComponent } from './components/administrador/list-users/list-users.component';
import { UsersService } from './services/users.service';
import { GestionarCredencialesComponent } from './components/administrador/gestionar-credenciales/gestionar-credenciales.component';
import { CookieService } from 'ngx-cookie-service';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    FooterComponent,
    LoginComponent,
    DashboardComponent,
    WelcomeComponent,
    KumuIntegrationComponent,
    NewUserComponent,
    ListUsersComponent,
    GestionarCredencialesComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [UsersService, CookieService],
  bootstrap: [AppComponent]
})
export class AppModule { }
