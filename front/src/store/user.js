import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        isAuthenticated: false,
    }),

    actions: {
        async setCsrfToken() {
            try {
                const response = await fetch('http://localhost:8000/csrf/', {
                    method: 'GET',
                    credentials: 'include',
                });
                if (!response.ok) {
                    throw new Error('Failed to set CSRF token.');
                }
            } catch (error) {
                console.error('Error setting CSRF token:', error);
            }
        },

        async register(userData) {
          await this.setCsrfToken(); // Récupère le token CSRF en amont
          try {
              const csrfToken = getCSRFToken();
              if (!csrfToken) {
                  throw new Error('CSRF token not found.');
              }
      
              const response = await fetch('http://localhost:8000/register/', {
                  method: 'POST',
                  credentials: 'include',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': csrfToken,
                  },
                  body: JSON.stringify(userData),
              });
      
              if (!response.ok) {
                  const errorData = await response.json();
                  throw new Error(errorData.error || 'Registration failed.');
              }
      
              const data = await response.json();
              this.user = data.user;
              this.isAuthenticated = true;
          } catch (error) {
              console.error('Error registering user:', error);
              throw error;
          }
      },
      
      async login(username, password) {
        try {
            // Récupérer le token CSRF
            const csrfToken = getCSRFToken();
            if (!csrfToken) {
                throw new Error('CSRF token not found.');
            }
    
            const response = await fetch('http://localhost:8000/login/', {
                method: 'POST',
                credentials: 'include',  // Important pour inclure les cookies (CSRF token)
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,  // Inclure le token CSRF dans les en-têtes
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });
    
            if (response.ok) {
                const data = await response.json();
                this.user = data.user;  // Mettre à jour l'utilisateur connecté
                this.isAuthenticated = true;
                this.error = null;
            } else {
                const errorData = await response.json();
                this.error = errorData.error || 'Invalid credentials';
                this.isAuthenticated = false;
            }
        } catch (error) {
            console.error('Error during login:', error);
            this.error = 'An error occurred while logging in.';
            this.isAuthenticated = false;
        }
    },   
  
      logout() {
        this.user = null;
        this.isAuthenticated = false;
        this.error = null;
      },
    }, 

    persist: true, // Active la persistance automatique
});

// Fonction utilitaire pour récupérer le cookie CSRF
export function getCSRFToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';').map(cookie => cookie.trim());
  const csrfCookie = cookies.find(cookie => cookie.startsWith(`${name}=`));
  if (!csrfCookie) {
      console.error('Missing CSRF cookie.');
      return null;
  }
  return csrfCookie.split('=')[1];
}
