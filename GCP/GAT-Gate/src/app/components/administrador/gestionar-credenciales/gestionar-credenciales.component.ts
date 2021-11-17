import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/models/User';
import { UsersService } from 'src/app/services/users.service';

@Component({
  selector: 'app-gestionar-credenciales',
  templateUrl: './gestionar-credenciales.component.html',
  styleUrls: ['./gestionar-credenciales.component.css']
})
export class GestionarCredencialesComponent implements OnInit {
  public users : User[] = [];

  constructor(private usersService: UsersService) { }

  ngOnInit(): void {
    //this.getUsers();
  }

  getUsers(){
    this.usersService.getUsers().subscribe(
      response => {
        this.users = JSON.parse(response);
      },
      error  => { console.log(error) }
    );
  }

  getUser(email: string){
    this.usersService.getUser(email).subscribe(
      (response) => { console.log('Usuario! ', response) }
    );
  }

  updatePswUser(user: User){
    this.usersService.updateUserPsw(user).subscribe(
      (response) => { console.log('Usuario actualizado!', response) }
    );
  }

  updateRolUser(user: User){
    this.usersService.updateUserRol(user).subscribe(
      (response) => { console.log('Rol actualizado!', response) }
    );
  }

  updateEstadoUser(user: User){
    this.usersService.updateEstadoUser(user).subscribe(
      (response) => { console.log('Estado actualizado!', response) }
    );
  }

}
