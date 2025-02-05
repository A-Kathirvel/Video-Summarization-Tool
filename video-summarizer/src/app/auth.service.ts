import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private loggedInUser: string | null = null;
  private loggedInUserSubject:BehaviorSubject<string | null> = new BehaviorSubject<string | null>(this.loggedInUser);

  constructor(private http:HttpClient,private route:Router, private cookieService: CookieService) {
    this.loggedInUser = sessionStorage.getItem('username');
    this.loggedInUserSubject.next(this.loggedInUser);
   }

  private apiurl=" http://127.0.0.1:8000";

  addUser(data:any):Observable<any>{
    return this.http.post<any>(`${this.apiurl}/signup/`,data);
  }

  login(data:any):Observable<any>{
    return this.http.post<any>(`${this.apiurl}/signin/`,data);
  }

  saveSession(token: string,user:string) {
    this.loggedInUser = user;
    sessionStorage.setItem('token', token);
    sessionStorage.setItem('username', user);
    this.loggedInUserSubject.next(this.loggedInUser);
  }

  
  isLoggedIn() {
    return sessionStorage.getItem('token');
  }

  getUsername(){
    console.log(this.loggedInUserSubject.asObservable());
    return this.loggedInUserSubject.asObservable();
  }

  logout() {
    this.loggedInUser = null;
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('username');
    this.route.navigate(['']);
    this.loggedInUserSubject.next(null);
  }

  getUserdetails(data:any){
    return this.http.post(`${this.apiurl}/getuserdetails/`,data);
  }

  updatePassword(username: string, oldPassword:string, newPassword: string): Observable<any> {
    return this.http.put(`${this.apiurl}/updatepassword/`, { username, oldPassword, newPassword });
  }
}
