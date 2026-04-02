import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LoginComponent } from './features/auth/components/login/login.component';
import { TaskListComponent } from './features/tasks/components/task-list/task-list.component';
import { TaskFormComponent } from './features/tasks/components/task-form/task-form.component';
import { authGuard } from './features/auth/guards/auth.guard';

export const routes: Routes = [
  { 
    path: 'login', 
    component: LoginComponent 
  },
  { 
    path: 'tasks', 
    component: TaskListComponent,
    canActivate: [authGuard] 
  },
  { 
    path: '', 
    redirectTo: 'tasks', 
    pathMatch: 'full'
  },
  { 
    path: '**', 
    redirectTo: 'tasks' 
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }