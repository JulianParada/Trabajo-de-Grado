import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UsersService } from 'src/app/services/users.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css'],
})
export class NavbarComponent implements OnInit {
  constructor(private router: Router, private usersService: UsersService) {}
  public isLogged = false;
  public tituloNavBar = 'Bienvenido';
  public UsuarioBoton = 'Ingresar';
  public userUid: string = '';
  public link :string ="public/login"
  public texto :string ='Login'

  ngOnInit(): void {
    this.getCurrentUser();
    let aux = this.usersService.getToken();
    console.log(aux);
    if(aux==""){
      this.texto = 'Login'
      this.link = "public/login"
    }else{
      this.texto = 'Logout'
      this.link = ""
    }
  }


  logout(){
    console.log("pepito")
    this.usersService.setToken("");
    this.texto = 'Login'
    this.link = "public/login"
  }
  getCurrentUser() {}

  onLogout() {}

  iconClick() {}

  buscar() {}

  registrarse() {}

  iniciarSesion() {}

  verPerfil() {}
}
