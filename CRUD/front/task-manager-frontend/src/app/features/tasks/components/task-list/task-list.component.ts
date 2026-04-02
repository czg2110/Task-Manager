import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Task } from '../../models/task.model';
import { TaskFormComponent } from '../task-form/task-form.component';
import { TaskService } from '../../services/task.service'; 
import { AuthService } from '../../../auth/services/auth.service'; 

@Component({
  selector: 'app-task-list',
  standalone: true,
  imports: [CommonModule, FormsModule, TaskFormComponent],
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.css']
})
export class TaskListComponent implements OnInit {
  private taskService = inject(TaskService);
  private authService = inject(AuthService); 
  private router = inject(Router);

  filterAssignee = signal('');
  filterStartDate = signal('');
  filterEndDate = signal('');

  filteredTasks = computed(() => {
    const ts = this.taskService.tasks();
    const a = this.filterAssignee();
    const s = this.filterStartDate();
    const e = this.filterEndDate();
    return ts.filter(t => {
      if (a && t.assignee !== a) return false;
      if (s && (!t.startDate || t.startDate < s)) return false;
      if (e && (!t.endDate || t.endDate > e)) return false;
      return true;
    });
  });

  users: any[] = []; 
  taskToEdit: Task | null = null;
  isModalOpen = false;
  currentView: 'board' | 'reports' | 'users' = 'board';
  isAdmin = false; 
  currentUserId = '';

  isRegisterModalOpen = false;
  regName = ''; regEmail = ''; regPassword = ''; regRole = 'user';
  regError = ''; regMessage = '';

  ngOnInit() {
    this.taskService.loadAllTasks();
    this.loadUsers();
    const userData = localStorage.getItem('currentUser');
    if (userData) {
      const u = JSON.parse(userData);
      this.isAdmin = u.role === 'admin';
      this.currentUserId = u.id;
    }
  }

  loadUsers() { this.taskService.getUsers().subscribe(d => this.users = d); }
  getTasksByStatus(status: string) { return this.filteredTasks().filter(t => t.status === status); }
  
  get userStats() {
    return this.users.map(u => {
      const uts = this.taskService.tasks().filter(t => t.assignee === u.name);
      const c = uts.filter(t => t.status === 'completed').length;
      return { name: u.name, completed: c, total: uts.length, percentage: uts.length ? Math.round((c/uts.length)*100) : 0 };
    }).sort((a, b) => b.completed - a.completed);
  }

  logout() { localStorage.clear(); this.router.navigate(['/login']); }
  switchView(v: 'board' | 'reports' | 'users') { this.currentView = v; }
  clearFilters() { this.filterAssignee.set(''); this.filterStartDate.set(''); this.filterEndDate.set(''); }
  
  changeStatus(t: Task, s: any) { if (t.id) this.taskService.updateTask(t.id, { status: s }).subscribe(); }
  deleteTask(id: string | undefined) { if (id) this.taskService.deleteTask(id).subscribe(); }

  openNewTaskModal() { this.taskToEdit = null; this.isModalOpen = true; }
  editTask(t: Task) { this.taskToEdit = { ...t }; this.isModalOpen = true; }
  closeModal() { this.isModalOpen = false; }

  onTaskAdded(t: Task) { this.taskService.createTask(t, crypto.randomUUID()).subscribe(() => this.closeModal()); }
  onTaskUpdated(t: Task) { if (t.id) this.taskService.updateTask(t.id, t).subscribe(() => this.closeModal()); }

  openRegisterModal() {
    this.isRegisterModalOpen = true;
    this.regError = '';
    this.regMessage = '';
  }

  closeRegisterModal() {
    this.isRegisterModalOpen = false;
  }

  registerUser() {
    this.authService.register(this.regName, this.regEmail, this.regPassword, this.regRole).subscribe({
      next: () => { 
        this.regMessage = '¡Éxito!'; 
        this.loadUsers(); 
        setTimeout(() => this.closeRegisterModal(), 1500);
      },
      error: e => this.regError = e.error?.error || 'Error'
    });
  }
  changeUserRole(id: string, r: string) { this.taskService.updateUserRole(id, r).subscribe(); }
  deleteUserAccount(id: string) { if (confirm("¿Borrar?")) this.taskService.deleteUser(id).subscribe(() => this.loadUsers()); }
}