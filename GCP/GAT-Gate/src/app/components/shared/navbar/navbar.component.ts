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
  public isAdmin = false;
  public tituloNavBar = 'Bienvenido';
  public UsuarioBoton = 'Ingresar';
  public userUid: string = '';
  public link :string ="public/login"
  public texto :string ='Login'
  public clase :string ='glyphicon glyphicon-log-in'

  ngOnInit(): void {
    this.getCurrentUser();
    //window.location.reload();
  }

  getCurrentUser() {
    let aux = this.usersService.getToken();

    let rol = aux.substring(aux.length-5, aux.length)

    if(rol == "Admin"){
      this.isAdmin = true;
    }else{
      this.isAdmin = false;
    }
    if(aux==""){
      this.isLogged = false;
    }else{
      this.isLogged = true;
    }
  }

  onLogin(){
    this.router.navigate(['public/login']);
  }

  onLogout() {
    this.logout();
    //this.router.navigate(['public/welcome']);
  }

  realizarOperacion(){
    console.log("entre al onclick")
    let aux = this.usersService.getToken();
    if(aux==""){
      this.clase ='glyphicon glyphicon-log-in'
      this.texto = 'Login'
      this.link = "public/login"
      this.router.navigate(['public/login']);
    }else{
      this.logout();
      this.clase ='glyphicon glyphicon-log-out'
      this.texto = 'Logout'
      this.link = "public/welcome"
      this.router.navigate(['public/welcome']);
    }
  }

  logout(){
    this.usersService.setToken("");
    this.isAdmin = false;
    this.isLogged = false;
  }

  iconClick() {}

  buscar() {}

  registrarse() {}

  iniciarSesion() {}

  verPerfil() {}
}
