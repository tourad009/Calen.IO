<script>
export default {
  name: "Popup",
  props: ["show", "close"],
  data() {
    return {
      title: "",
      description: "",
      due_date: "",
      end_date: "",
      completed: false,
      priority: "medium",
      loading: false,
      error: null,
      taskId: null,
    };
  },
  methods: {
    async saveEvent() {
      this.error = null;

      // Vérifications de base
      if (!this.title || !this.due_date) {
        this.error = "Veuillez remplir tous les champs obligatoires.";
        return;
      }

      // Vérification des dates
      if (this.due_date && this.end_date && new Date(this.due_date) > new Date(this.end_date)) {
        this.error = "La date de début doit être antérieure à la date de fin.";
        return;
      }

      this.loading = true;

      try {
        const payload = {
          title: this.title,
          description: this.description,
          due_date: this.due_date,
          end_date: this.end_date,
          completed: this.completed,
          priority: this.priority,
        };

        let response;
        const options = {
          method: this.taskId ? 'PUT' : 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify(payload)
        };

        if (this.taskId) {
          response = await fetch(`http://localhost:8000/api/tasks/update/${this.taskId}/`, options);
        } else {
          response = await fetch('http://localhost:8000/api/tasks/create/', options);
        }

        if (response.status === 401) {
          window.location.href = '/login';
          return;
        }

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        this.$emit("taskSaved", data);
        this.closeModal();
      } catch (error) {
        console.error("Erreur :", error);
        this.error = "Une erreur s'est produite lors de l'enregistrement.";
      } finally {
        this.loading = false;
      }
    },

    // Méthode utilitaire pour récupérer les cookies
    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return '';
    },

    closeModal() {
      this.$emit("close");
      this.resetForm();
    },

    resetForm() {
      this.title = "";
      this.description = "";
      this.due_date = "";
      this.end_date = "";
      this.completed = false;
      this.priority = "medium";
      this.error = null;
      this.taskId = null;
    },

    handleKeydown(event) {
      if (event.key === "Escape") {
        this.closeModal();
      }
    },
  },
  mounted() {
    window.addEventListener("keydown", this.handleKeydown);
  },
  beforeUnmount() {
    window.removeEventListener("keydown", this.handleKeydown);
  },
};
</script>

<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center z-50">
    <div 
      class="fixed inset-0 bg-black bg-opacity-50 transition-opacity duration-300"
      @click="closeModal"
    ></div>
    
    <div 
      class="bg-white border border-gray-300 shadow-lg p-8 rounded-lg max-w-lg w-11/12 transform transition-transform duration-500 relative z-10"
    >
      <h2 class="text-2xl font-semibold mb-4 text-gray-800 text-center">
        {{ taskId ? "Modifier l'événement" : "Ajouter un événement" }}
      </h2>

      <!-- Message d'erreur -->
      <div v-if="error" class="text-red-600 text-center mb-4">{{ error }}</div>

      <!-- Champ pour le titre -->
      <input
        type="text"
        v-model="title"
        placeholder="Titre de la tâche"
        class="w-full p-3 mb-4 border border-gray-300 rounded-lg"
      />

      <!-- Date de début -->
      <input
        type="datetime-local"
        v-model="due_date"
        class="w-full p-3 mb-4 border border-gray-300 rounded-lg"
      />

      <!-- Date de fin -->
      <input
        type="datetime-local"
        v-model="end_date"
        class="w-full p-3 mb-4 border border-gray-300 rounded-lg"
      />

      <!-- Description -->
      <textarea
        v-model="description"
        placeholder="Description"
        class="w-full p-3 mb-4 border border-gray-300 rounded-lg"
        rows="4"
      ></textarea>

      <!-- Priorité -->
      <select
        v-model="priority"
        class="w-full p-3 mb-4 border border-gray-300 rounded-lg"
      >
        <option value="low">Basse</option>
        <option value="medium">Moyenne</option>
        <option value="high">Haute</option>
      </select>

      <!-- Statut -->
      <div class="flex items-center mb-4">
        <input
          type="checkbox"
          v-model="completed"
          id="completed"
          class="mr-2"
        />
        <label for="completed">Tâche terminée</label>
      </div>

      <!-- Boutons -->
      <div class="flex justify-end space-x-4 mt-5">
        <button
          @click="closeModal"
          class="bg-gray-200 text-gray-800 py-3 px-6 rounded-lg text-lg transition duration-300 hover:bg-gray-300"
        >
          Annuler
        </button>
        <button
          @click="saveEvent"
          class="bg-blue-500 text-white py-3 px-6 rounded-lg text-lg transition duration-300 hover:bg-blue-700"
          :disabled="loading"
        >
          {{ loading ? "En cours..." : "Enregistrer" }}
        </button>
      </div>
    </div>
  </div>
</template>
  