import { Component, EventEmitter, Input, Output, OnChanges, SimpleChanges, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Task } from '../../models/task.model';
import { TaskService } from '../../services/task.service';

@Component({
  selector: 'app-task-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './task-form.component.html',
  styleUrls: ['./task-form.component.css']
})
export class TaskFormComponent implements OnChanges, OnInit {
  @Input() taskToEdit: Task | null = null; 
  @Output() taskAdded = new EventEmitter<Task>();
  @Output() taskUpdated = new EventEmitter<Task>(); 
  @Output() cancelEdit = new EventEmitter<void>();  

  taskForm: FormGroup;
  users: any[] = [];

  private taskService = inject(TaskService);
  private fb = inject(FormBuilder);

  constructor() {
    this.taskForm = this.fb.group({
      title: ['', Validators.required],
      description: [''],
      status: ['pending'],
      assignee: [''],
      startDate: [''],
      endDate: ['']
    });
  }

  ngOnInit() {
    this.taskService.getUsers().subscribe({
      next: (data) => this.users = data,
      error: (err) => console.error('Error al cargar usuarios', err)
    });
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['taskToEdit'] && this.taskToEdit) {
      this.taskForm.patchValue({
        title: this.taskToEdit.title,
        description: this.taskToEdit.description,
        status: this.taskToEdit.status,
        assignee: this.taskToEdit.assignee || '',
        startDate: this.taskToEdit.startDate || '',
        endDate: this.taskToEdit.endDate || ''
      });
    }
  }

  onSubmit() {
    if (this.taskForm.valid) {
      const taskData: Task = {
        title: this.taskForm.value.title,
        description: this.taskForm.value.description,
        status: this.taskForm.value.status,
        assignee: this.taskForm.value.assignee,
        startDate: this.taskForm.value.startDate,
        endDate: this.taskForm.value.endDate
      };

      if (this.taskToEdit && this.taskToEdit.id) {
        taskData.id = this.taskToEdit.id;
        this.taskUpdated.emit(taskData);
      } else {
        this.taskAdded.emit(taskData);
      }

      this.resetForm();
    }
  }

  onCancel() {
    this.resetForm();
    this.cancelEdit.emit();
  }

  private resetForm() {
    this.taskForm.reset({ status: 'pending', assignee: '', startDate: '', endDate: '' });
    this.taskToEdit = null;
  }
}