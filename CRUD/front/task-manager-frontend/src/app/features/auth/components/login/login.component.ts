import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);

  loginForm: FormGroup = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]]
  });

  isLoading: boolean = false;
  errorMessage: string = '';

  get emailControl() { return this.loginForm.get('email'); }
  get passwordControl() { return this.loginForm.get('password'); }

  onSubmit() {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    const { email, password } = this.loginForm.value;

    console.log(`Intentando entrar con: ${email}`);

    this.authService.login(email, password).subscribe({
      next: (res) => {
        this.isLoading = false;
        console.log('¡El servidor respondió!', res);
        
        if (res && res.token) {
          localStorage.setItem('token', res.token);
          localStorage.setItem('currentUser', JSON.stringify(res.user)); 
          
          this.router.navigate(['/tasks']);
        } else {
          this.errorMessage = 'No se recibió el token de acceso.';
        }
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error de login:', err);
        this.errorMessage = err.error?.error || 'Correo o contraseña incorrectos.';
      }
    });
  }
}