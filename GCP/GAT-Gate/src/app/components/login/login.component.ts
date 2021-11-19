import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/models/User';
import { UsersService } from 'src/app/services/users.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent  {
  email: string = "";
  password: string="";
  iscorrect: boolean = true;

  constructor(private usersService: UsersService, public router: Router) {}

login() {
    const user = {email: this.email, password: this.password};
    this.usersService.login(this.email, this.password).subscribe(
      data => { let users :User[] = JSON.parse(data);
        if (this.email == users[0].EMAIL && this.password == users[0].PASSWORD ){
          this.usersService.setToken("token|"+this.email+ "|" +users[0].ROL);
          this.iscorrect = true;
          this.redireccionar();
          //this.router.navigateByUrl('/public/dashboard');
        }else{
          this.iscorrect = false;
          console.log("error")
        }
      })
  }

  redireccionar(){
    this.router.navigate(['public/dashboard']);
  }
}
