<script>
import { ref } from 'vue';
import { useAuthStore } from '@/store/user'; // Assurez-vous que le chemin d'import est correct
import { useRouter } from 'vue-router'; // Importez le routeur de Vue

export default {
  setup() {
    const authStore = useAuthStore();
    const router = useRouter(); // Initialisez le routeur
    const username = ref('');
    const password = ref('');
    const error = ref(null);
    const success = ref(null);

    const handleLogin = async () => {
      await authStore.login(username.value, password.value);
      if (authStore.error) {
        error.value = authStore.error;
        success.value = null; // Réinitialiser success si une erreur se produit
      } else {
        success.value = "Connexion réussie ! Redirection...";
        router.push("/calendar"); // Redirection vers /calendar après une connexion réussie
      }
    };

    const resetError = () => {
      error.value = null;
      success.value = null; // Réinitialiser success lors de l'édition des champs
    };

    return {
      username,
      password,
      handleLogin,
      error,
      success,
      resetError,
      isAuthenticated: authStore.isAuthenticated,
      user: authStore.user,
    };
  },
};
</script>

<template>
  <div
    class="bg-surface-50 dark:bg-surface-950 flex items-center justify-center h-screen min-w-full overflow-hidden"
  >
    <div class="flex flex-col items-center justify-center">
      <div
        class="rounded-[56px] p-1 bg-gradient-to-b from-primary to-transparent"
      >
        <div
          class="w-full bg-surface-0 dark:bg-surface-900 py-20 px-8 sm:px-20 rounded-[53px]"
        >
          <div class="text-center mb-8">
            <div class="flex justify-center items-center mb-6">
              <Calendar class="w-8 h-8 text-gray-800" />
              <h2 class="text-3xl text-gray-800 font-bold">
                Calen.<span class="text-blue-500">IO</span>
              </h2>
            </div>
            <div
              class="text-surface-900 dark:text-surface-0 text-3xl font-medium mb-4"
            >
              Bienvenue
            </div>
            <span class="text-muted-color font-medium"
              >Connectez-vous pour continuer</span
            >
          </div>

          <div>
            <label
              for="email1"
              class="block text-surface-900 dark:text-surface-0 text-xl font-medium mb-2"
              >Username</label
            >
            <input
              id="email1"
              type="text"
              placeholder="Username"
              class="w-full md:w-[30rem] mb-8 p-3 border border-gray-300 rounded-md"
              v-model="username"
              @input="resetError"
            />

            <label
              for="password1"
              class="block text-surface-900 dark:text-surface-0 font-medium text-xl mb-2"
              >Mot de passe</label
            >
            <input
              id="password1"
              type="password"
              placeholder="Mot de passe"
              class="w-full md:w-[30rem] mb-4 p-3 border border-gray-300 rounded-md"
              v-model="password"
              @input="resetError"
            />

            <div v-if="error" class="text-red-500 mb-4">{{ error }}</div>
            <div v-if="success" class="text-green-500 mb-4">{{ success }}</div>

            <div class="flex items-center justify-between mt-2 mb-8 gap-8">
              <div class="flex items-center">
                <input
                  type="checkbox"
                  id="rememberme1"
                  class="mr-2"
                />
                <label
                  for="rememberme1"
                  class="text-surface-900 dark:text-surface-0"
                  >Se souvenir de moi</label
                >
              </div>
              <span
                class="font-medium no-underline ml-2 text-right cursor-pointer text-primary"
                >Mot de passe oublié ?</span
              >
            </div>
            <button
              class="w-full bg-blue-500 text-white py-3 rounded-md font-semibold"
              @click.prevent="handleLogin"
            >
              Se connecter
            </button>
            <!-- Lien vers l'inscription -->
            <div class="mt-4 text-center">
              <p class="text-gray-700">
                Don't have an account?
                <a
                  href="./Register"
                  class="text-blue-600 hover:underline font-medium"
                >
                  Sign Up here.
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
