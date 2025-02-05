import { Component } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-upload-video',
  templateUrl: './upload-video.component.html',
  styleUrls: ['./upload-video.component.css']
})
export class UploadVideoComponent {

  username:Observable<string | null>=this.authService.getUsername();

  constructor(private http:HttpClient, private authService:AuthService, private route:Router){}

  selectedFile: File | null = null;
  selectedFileName: string | null = null;
  summary: string = '';
  tamil_summary:string='';
  errorMessage:string='';

  
  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
    if(this.selectedFile){
      this.selectedFileName=this.selectedFile.name;
    }
  }

  uploadFile(){
    if (!this.selectedFile){
      this.errorMessage="Please select a file"
      return;
    }

    const formData=new FormData();
    formData.append('video',this.selectedFile);
    this.http.post('http://127.0.0.1:8001/api/upload/',formData).subscribe({
      next:(res:object)=>{
        this.summary=(res as any).summary;
        this.tamil_summary=(res as any).tamil_summary;
      },
      error:(err)=>{
        console.log(err);
      }
    })
  }
}
