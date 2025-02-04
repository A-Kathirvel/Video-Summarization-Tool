import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SigninComponent } from './signin/signin.component';
import { SignupComponent } from './signup/signup.component';
import { UploadVideoComponent } from './upload-video/upload-video.component';
import { UserProfileComponent } from './user-profile/user-profile.component';

const routes: Routes = [
  { path:'', component:SigninComponent },
  { path:'signin', component: SigninComponent },
  { path:'signup', component: SignupComponent },
  { path:'upload', component:UploadVideoComponent},
  { path:'profile', component:UserProfileComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
