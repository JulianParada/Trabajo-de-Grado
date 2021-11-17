import { Component } from '@angular/core';
import { User } from 'src/app/models/User';
import { UsersService } from 'src/app/services/users.service';

@Component({
  selector: 'app-new-user',
  templateUrl: './nuevo-user.component.html',
  styleUrls: ['./nuevo-user.component.css'],
})
export class NewUserComponent {
  user = new User('', '', 'Activo', '');

  constructor(private usersService: UsersService) {}

  addUser() {
    console.log("ENTRE")
    let radiobtn=document.getElementById('admin') as HTMLInputElement;
    if (radiobtn.checked == true) {
      this.user.ROL="Admin";
    } else {
      this.user.ROL="Usuario";
    }
    console.log("ENTRE")
    this.usersService.createUser(this.user).subscribe((response) => {
      console.log('Usuario creado! ', response);
    });
  }
}
