import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http:HttpClient,private route:Router) { }

  private apiurl=" http://127.0.0.1:8000";

  addUser(data:any):Observable<any>{
    return this.http.post<any>(`${this.apiurl}/signup/`,data);
  }

  login(data:any):Observable<any>{
    return this.http.post<any>(`${this.apiurl}/signin/`,data);
  }
}
