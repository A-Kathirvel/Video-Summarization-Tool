import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../auth.service';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent {

  username:Observable<string | null>=this.authService.getUsername();
  passwordform!: FormGroup;
  userDetails: any;
  showPasswordForm: boolean = false;
  showProfile:boolean=true;
  newPassword: string = '';
  oldPassword: string ='';
  isLoading: boolean = true;
  submitted: boolean = false;
  errorMessage: string = '';

  constructor(private fb: FormBuilder, private http:HttpClient, private authService:AuthService, private route:Router){}
  ngOnInit(): void {
    this.getUserDetails();

    this.passwordform = this.fb.group({
      oldPassword: ['',Validators.required],
      password: ['', Validators.required]
    })
  }

  getUserDetails() {
    this.username.subscribe(usernameValue => {
      if (usernameValue) {
        console.log(usernameValue)
        this.authService.getUserdetails({ "username": usernameValue }).subscribe({
          next: (res) => {
            this.userDetails = res;
          },
        error: (err) => {
          console.log(err);
        }
      });
    }
  });
}

  togglePasswordForm() {
    this.showPasswordForm = !this.showPasswordForm;
    this.showProfile =!this.showProfile;
  }

  updatePassword() {
    this.submitted = true;
    if (this.passwordform.valid) {
      this.newPassword = this.passwordform.value.password;
      this.oldPassword = this.passwordform.value.oldPassword;
      this.authService.updatePassword(this.userDetails.username, this.oldPassword,this.newPassword).subscribe({
        next: (response) => {
          alert('Password updated successfully!');
          this.showPasswordForm = false;
          this.showProfile=!this.showProfile;
          this.passwordform.reset();
          this.submitted =false;
        },
        error: (error) => {
          console.log(error);
          console.log(error.message);
          console.log(error.error);
          this.errorMessage = error.error.error;
        }
      });
    }
  }
}
