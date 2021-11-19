import { Component, NgZone, OnInit } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  viz: any;
  constructor(public router: Router, private zone: NgZone) {
  }

  ngOnInit(): void {
    //this.reloadComponent();
  }

  ngAfterViewChecked() {
    //location.reload();
    //this.reloadComponent();
  }


 reloadComponent() {
  let currentUrl = this.router.url;
      this.router.routeReuseStrategy.shouldReuseRoute = () => false;
      this.router.onSameUrlNavigation = 'reload';
      this.router.navigate([currentUrl]);
  }

}
