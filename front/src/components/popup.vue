<script>
export default {
  name: "Popup", // nom du composant
  props: ["show", "close"], // propriétés du composant
  data() {
    // Données réactives
    return {
      title: "", // Titre saisi par l'utilisateur
      eventTime: "", // Heure choisie pour l'événement
      description: "", // Description de l'événement
      file: null, // Fichier joint
    };
  },
  methods: {
    // Fermer la popup
    closeModal() {
      this.$emit("close"); // Émettre un événement pour fermer la popup
    },
    
    // Gérer les pressions de touches clavier
    handleKeydown(event) {
      if (event.key === "Escape") {
        this.closeModal(); // Fermer la popup si "Échap" est pressé
      }
    },

    // Gérer l'importation de fichiers
    handleFileUpload(event) {
      this.file = event.target.files[0]; // Stocker le fichier joint
    },  

    // Sauvegarder l'événement
    saveEvent() {
      console.log("Titre :", this.title);
      console.log("Heure :", this.eventTime);
      console.log("Description :", this.description);
      console.log("Fichier :", this.file);
      this.closeModal(); // Fermer le popup après enregistrement
    },
  },
  mounted() {
    // Ajouter un écouteur d'événement pour les touches clavier
    window.addEventListener("keydown", this.handleKeydown);
  },
  beforeUnmount() {
    // Supprimer l'écouteur d'événement au démontage du composant
    window.removeEventListener("keydown", this.handleKeydown);
  },
};
</script>

<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center z-50">
    <!-- Fond semi-transparent -->
    <div 
      class="fixed inset-1 bg-black bg-opacity-50 transition-opacity duration-300"
      @click="closeModal"
    ></div>
    <!-- Contenu de la popup -->
    <div 
      class="bg-white border border-gray-300 shadow-lg p-8 rounded-lg max-w-lg w-11/12 transform scale-95 opacity-0 transition-transform duration-500 ease-in-out"
      :class="{ 'scale-100 opacity-100': show }"
    >
      <div>
        <h2 class="text-2xl font-semibold mb-4 text-gray-800 text-center">Ajouter un événement</h2>
        <!-- Champ pour le titre -->
        <input 
          type="text" 
          v-model="title" 
          placeholder="Entrez un titre"
          class="w-full p-3 mt-2 mb-2 border border-gray-300 rounded-lg bg-gray-100 focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
        />
        <!-- Champ pour l'heure -->
        <input 
          type="time" 
          v-model="eventTime" 
          class="w-full p-3 mt-2 mb-2 border border-gray-300 rounded-lg bg-gray-100 focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
        />
        <!-- Champ pour la description -->
        <textarea 
          v-model="description" 
          placeholder="Entrez une description"
          class="w-full p-3 mt-2 mb-2 border border-gray-300 rounded-lg bg-gray-100 focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
        ></textarea>
        <!-- Champ pour la pièce jointe -->
        <input 
          type="file" 
          @change="handleFileUpload"
          class="w-full p-4 mt-2 mb-4 border border-gray-300 rounded-lg bg-gray-100"
        />
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
          >
            Enregistrer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
