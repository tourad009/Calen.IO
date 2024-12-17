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
        <div v-if="error" class="mt-4 text-center text-red-500 font-medium">
          {{ error }}
        </div>
        <div class="mt-4 text-center">
          <p class="text-gray-700">
            Already have an account?
            <a href="./Login" class="text-blue-600 hover:underline font-medium">
              Log in
            </a>
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

export default {
  components: { Calendar },
  setup() {
    const userStore = useAuthStore();
    const username = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const error = ref(null);

    const handleRegister = async () => {
      if (password.value !== confirmPassword.value) {
        error.value = "Passwords do not match!";
        return;
      }

      try {
        await userStore.setCsrfToken();
        const userData = { username: username.value, password: password.value };
        await userStore.register(userData);

        if (userStore.error) {
          error.value = userStore.error;
        }
      } catch (err) {
        error.value = "An error occurred while registering.";
        console.error(err);
      }
    };

    return { username, password, confirmPassword, error, handleRegister };
  },
};
</script>
