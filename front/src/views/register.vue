<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Formulaire -->
    <div class="w-1/2 bg-white flex items-center justify-center">
      <div class="max-w-md w-full p-6">
        <div class="flex justify-center items-center mb-8">
          <Calendar class="w-8 h-8 text-gray-800" />
          <h2 class="text-3xl text-gray-800 font-bold">
            Calen.<span class="text-blue-500">IO</span>
          </h2>
        </div>
        <h1 class="text-2xl font-bold text-gray-800 mb-4 text-center">
          Create an Account
        </h1>
        <!-- Add this alert for success message -->
        <div v-if="successMessage" class="alert alert-success">
          {{ successMessage }}
        </div>
        <form @submit.prevent="handleRegister">
          <!-- Champ Username -->
          <div class="mb-4">
            <label for="username" class="block text-gray-700">Username</label>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="Enter your username"
              class="w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <!-- Champ Password -->
          <div class="mb-4">
            <label for="password" class="block text-gray-700">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Enter your password"
              class="w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <!-- Champ Confirm Password -->
          <div class="mb-6">
            <label for="confirm-password" class="block text-gray-700">
              Confirm Password
            </label>
            <input
              id="confirm-password"
              v-model="confirmPassword"
              type="password"
              placeholder="Confirm your password"
              class="w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <!-- Bouton d'inscription -->
          <button
            type="submit"
            class="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 font-semibold"
          >
            Sign Up
          </button>
        </form>

        <!-- Message d'erreur -->
        <div v-if="error" class="mt-4 text-center text-red-500 font-medium">
          {{ error }}
        </div>

        <!-- Lien vers la page de connexion -->
        <div class="mt-4 text-center">
          <p class="text-gray-700">
            Already have an account?
            <router-link to="/login" class="text-blue-600 hover:underline font-medium">
              Log in
            </router-link>
          </p>
        </div>
      </div>
    </div>

    <!-- Section droite -->
    <div
      class="w-1/2 bg-gradient-to-br from-blue-500 via-blue-200 to-white-300 flex flex-col items-center justify-center text-center"
    >
      <p class="text-4xl text-white font-bold mb-11 w-96">
        Planifiez mieux, accomplissez plus.
      </p>
      <img
        src="../assets/background-register.jpg"
        alt="Interface calendrier"
        class="h-80 w-80 shadow-lg rounded-lg"
      />
    </div>
  </div>
</template>

<script>
import { Calendar } from "lucide-vue-next";
import { ref } from "vue";
import { useAuthStore } from "@/store/user";
import { useRouter } from "vue-router";

export default {
  components: { Calendar },
  setup() {
    const userStore = useAuthStore();
    const router = useRouter();
    const username = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const error = ref(null);
    const successMessage = ref(null);

    const handleRegister = async () => {
      error.value = null;
      successMessage.value = null;

      // Password validation
      if (password.value !== confirmPassword.value) {
        error.value = "Passwords do not match!";
        return;
      }

      try {
        await userStore.setCsrfToken();
        const userData = { username: username.value, password: password.value };

        const csrfToken = document.cookie.split("csrftoken=")[1]?.split(";")[0];
        const response = await fetch("http://localhost:8000/api/user/register/", {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify(userData),
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.error || "Registration failed");
        }

        // Show success message
        successMessage.value = "Registration successful! Redirecting to login...";

        // Reset form
        username.value = "";
        password.value = "";
        confirmPassword.value = "";

        // Wait 2 seconds before redirect
        setTimeout(() => {
          router.push("/login");
        }, 2000);
      } catch (err) {
        error.value = err.message || "An error occurred during registration";
        console.error(err);
      }
    };

    return { username, password, confirmPassword, error, successMessage, handleRegister };
  },
};
</script>

<style scoped>
.alert {
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 4px;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}
</style>
