import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent {
  constructor(private fb:FormBuilder, private route:Router,private authService:AuthService){}
  
    signinform!: FormGroup;
    errorMessage:string='';
    submitted=false;
  
    ngOnInit():void{
      this.signinform=this.fb.group({
        email:['',Validators.required],
        password:['',Validators.required],
      })
    }

    onSubmit(){
      this.submitted=true;
      if(this.signinform.valid){
        const data=this.signinform.value;
        this.authService.login(data).subscribe({
          next:(res)=>{
            console.log(res);
            this.signinform.reset();
            this.submitted=false;
            this.errorMessage='';
            this.route.navigate(['upload']);
          },
          error:(err)=>{
            this.errorMessage=err.error['error'];
            console.log(err);
            console.log(err.error);
          }
        })
      }
    }
}
