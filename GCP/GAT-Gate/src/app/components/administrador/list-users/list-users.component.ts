import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/models/User';
import { UsersService } from 'src/app/services/users.service';

@Component({
  selector: 'app-list-users',
  templateUrl: './list-users.component.html',
  styleUrls: ['./list-users.component.css']
})
export class ListUsersComponent implements OnInit {
  public users : User[] = [];

  constructor(private usersService: UsersService) { }

  ngOnInit(): void {
    this.getUsers();
  }

  getUsers(){
    this.usersService.getUsers().subscribe(
      response => {
        this.users = JSON.parse(response);
      },
      error  => { console.log(error) }
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
