import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {

  constructor(private fb:FormBuilder, private route:Router,private authService:AuthService){}

  signupform!: FormGroup;
  errorMessage:string='';
  submitted=false;

  ngOnInit():void{
    this.signupform=this.fb.group({
      username:['',Validators.required],
      email:['',Validators.required],
      password:['',Validators.required],
      confirm_password:['',Validators.required]
    })

    // Watch for changes in both password fields
    this.signupform.valueChanges.subscribe(() => {
      this.checkPasswordsMatch();
    });
  }

  checkPasswordsMatch(): void {
    const password = this.signupform.get('password')?.value;
    const confirmPassword = this.signupform.get('confirm_password')?.value;

    // Set the error when passwords do not match
    if (password !== confirmPassword) {
      this.signupform.get('confirm_password')?.setErrors({ mismatch: true });
    } else {
      this.signupform.get('confirm_password')?.setErrors(null);
    }
  }
  

  onSubmit(){
    this.submitted=true;
    if(this.signupform.valid){
      const data=this.signupform.value;
      this.authService.addUser(data).subscribe({
        next: (res)=>{
          this.signupform.reset();
          this.submitted=false;
          this.errorMessage='';
          this.route.navigate(['']);
        },
        error:(err)=>{
          this.errorMessage=err.error['error'];
        }
      })
    }
  }
}
