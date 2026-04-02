import { Injectable, inject, signal } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Socket } from 'ngx-socket-io';
import { Task } from '../models/task.model';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class TaskService {
  private http = inject(HttpClient);
  private socket = inject(Socket);
  private apiUrl = 'http://localhost:5000/api/tasks';
  private usersUrl = 'http://localhost:5000/api/users'; 

  private _tasks = signal<Task[]>([]);
  public tasks = this._tasks.asReadonly();

  constructor() {
    this.initSocketListeners();
  }

  private initSocketListeners() {
    this.socket.fromEvent<Task>('task_created').subscribe(t => this._tasks.update(ts => [t, ...ts]));
    this.socket.fromEvent<Task>('task_updated').subscribe(t => this._tasks.update(ts => ts.map(x => x.id === t.id ? t : x)));
    this.socket.fromEvent<string>('task_deleted').subscribe(id => this._tasks.update(ts => ts.filter(x => x.id !== id)));
  }

  loadAllTasks() {
    this.http.get<Task[]>(this.apiUrl).subscribe(data => this._tasks.set(data));
  }

  createTask(task: Task, idempotencyKey: string): Observable<Task> {
    const headers = new HttpHeaders({ 'Idempotency-Key': idempotencyKey });
    return this.http.post<Task>(this.apiUrl, task, { headers });
  }

  updateTask(id: string, task: Partial<Task>): Observable<Task> {
    return this.http.put<Task>(`${this.apiUrl}/${id}`, task);
  }

  deleteTask(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  // Usuarios
  getUsers(): Observable<any[]> {
    return this.http.get<any[]>(this.usersUrl);
  }

  deleteUser(id: string): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });
    return this.http.delete(`${this.usersUrl}/${id}`, { headers });
  }

  updateUserRole(id: string, role: string): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });
    return this.http.put(`${this.usersUrl}/${id}/role`, { role }, { headers });
  }
}