import { Injectable } from '@angular/core';
import { User } from '../models/User';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CookieService } from "ngx-cookie-service";

@Injectable({
  providedIn: 'root'
})

export class UsersService {
  urlBase =  "https://us-central1-gat-gate.cloudfunctions.net/app";
  //urlBase =  "http://localhost:8081";
  constructor(private http: HttpClient, private cookies: CookieService) {  }

  getUsers(): Observable<any>{
    return this.http.get(this.urlBase + '/getAll_Usuarios');
  };

  getUser(email: string){
    let query = 'STR' + email;
    return this.http.get(this.urlBase + '/getOne_usuario?data=' + query);
  }

  createUser(userN: User){
    console.log("ENTRE 2")
    let query = 'STR' + userN.NOMBRE + '|PASSWORD' + '|MAIL' + userN.EMAIL + '|STR' + userN.ESTADO + '|STR' + userN.ROL;
    return this.http.get(this.urlBase + '/add_One_usuario?data=' + query);
  }

  updateUserPsw(userN: User){
    let query = userN.EMAIL;
    return this.http.get(this.urlBase + '/reset_password?data=' + query);
  }

  updateUserRol(userN: User){
    let nRol;
    if(userN.ROL == "Admin"){
      nRol="Usuario";
    }else{
      nRol="Admin";
    }
    let query = userN.EMAIL + '|STRrol=' + nRol;
    return this.http.get(this.urlBase + '/update_One_usuario?data=' + query);
  }

  updateEstadoUser(userN: User){
    let nEstado;
    if(userN.ESTADO == "Activo"){
      nEstado="Inactivo";
    }else{
      nEstado="Activo";
    }
    let query = userN.EMAIL + '|STRESTADO=' + nEstado;
    return this.http.get(this.urlBase + '/update_One_usuario?data=' + query);
  }

  login(email: string, psw: string): Observable<any> {
    return this.http.get(this.urlBase + "/getOne_usuario?data=" + email);
  }

  setToken(token: string) {
    this.cookies.set("token", token);
  }
  getToken() {
    return this.cookies.get("token");
  }
}
