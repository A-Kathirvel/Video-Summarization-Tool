import { Component } from '@angular/core';
import { HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-upload-video',
  templateUrl: './upload-video.component.html',
  styleUrls: ['./upload-video.component.css']
})
export class UploadVideoComponent {

  constructor(private http:HttpClient){}

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
        console.log(res);
        this.summary=(res as any).summary;
        this.tamil_summary=(res as any).tamil_summary;
        console.log((res as any).message);
      },
      error:(err)=>{
        console.log(err);
      }
    })

  }


  // async uploadFile() {
  //   if (!this.selectedFile) {
  //     this.errorMessage="Please select a file"
  //     // alert('Please select a file first!');
  //     return;
  //   }

  //   const formData = new FormData();
  //   formData.append('video', this.selectedFile);

  //   try {
  //     const response = await axios.post('http://127.0.0.1:8000/api/upload/', formData);
  //     this.summary = response.data.summary;
  //     this.tamil_summary=response.data.tamil_summary;
  //     console.log(response.data.message)
  //   } catch (error) {
  //     console.error('Error uploading video:', error);
  //   }
  // }
}
