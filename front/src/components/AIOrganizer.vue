<template>
  <div class="ai-organizer-container">
    <!-- Bouton pour ouvrir/fermer la fenêtre de chat -->
    <button
      @click="toggleIcon"
      class="bg-blue-500 px-3 py-3 m-5 rounded-full w-14 h-14 text-white flex items-center justify-center shadow-md hover:shadow-lg hover:bg-blue-600 transition duration-300 ease-in-out mt-auto active:scale-90 fixed bottom-5 right-5 z-10"
    >
      <component :is="isOpen ? 'X' : 'Bot'" class="w-6 h-6"></component>
    </button>

    <!-- Fenêtre de chat -->
    <div
      v-if="isOpen"
      class="fixed bottom-[7rem] right-5 w-80 h-[26rem] bg-white shadow-xl rounded-lg flex flex-col"
    >
      <!-- En-tête -->
      <div
        class="flex items-center justify-between px-4 py-2 bg-blue-500 text-white rounded-t-lg"
      >
        <div class="flex items-center gap-2">
          <div
            class="rounded-full w-8 h-8 bg-white flex justify-center items-center"
          >
            <Bot class="w-5 h-5 text-blue-500" />
          </div>
          <h3 class="text-sm font-medium">Cal the Bot</h3>
        </div>
        <span class="text-xs">TODAY {{ currentTime }}</span>
      </div>

      <!-- Zone de messages -->
      <div
        class="chat-container flex-grow px-3 py-3 overflow-y-auto custom-scrollbar"
      >
        <div
          v-for="(msg, index) in messages"
          :key="index"
          class="message w-full flex mb-2"
          :class="msg.sender === 'bot' ? 'justify-start' : 'justify-end'"
        >
          <div
            class="p-4 rounded-lg text-sm max-w-[75%]"
            :class="
              msg.sender === 'bot'
                ? 'bg-blue-400 text-white text-left'
                : 'bg-gray-100 text-blue-500 text-right'
            "
            style="word-wrap: break-word; white-space: pre-wrap"
          >
            <p>{{ msg.text }}</p>
          </div>
        </div>
      </div>

      <!-- Champ d'entrée de message -->
      <div
        class="message-input flex items-center border-t border-gray-300 px-3 py-2"
      >
        <input
          type="text"
          v-model="message"
          placeholder="Entrez votre message..."
          class="flex-grow focus:outline-none text-sm"
        />
        <button
          @click="sendMessage"
          class="bg-blue-500 text-white px-4 py-2 rounded-md transition hover:bg-blue-600"
        >
          <SendHorizontal class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";
import { Bot, X, SendHorizontal } from "lucide-vue-next";

export default {
  name: "AIOrganizer",
  components: {
    Bot,
    X,
    SendHorizontal,
  },
  setup() {
    const isOpen = ref(false);
    const messages = ref([
      {
        sender: "bot",
        text: "Hello! How can I assist you today?",
      },
    ]);
    const message = ref("");

    const toggleIcon = () => {
      isOpen.value = !isOpen.value;
    };

    const sendMessage = () => {
      if (message.value.trim()) {
        messages.value.push({ sender: "user", text: message.value });
        messages.value.push({
          sender: "bot",
          text: "Thank you for your message! I'm here to help.",
        });
        message.value = "";
      }
    };

    // Créer une référence pour l'heure
    const currentTime = ref("");

    // Fonction pour formater l'heure
    const formatTime = (date) => {
      const hours = String(date.getHours()).padStart(2, "0");
      const minutes = String(date.getMinutes()).padStart(2, "0");
      const seconds = String(date.getSeconds()).padStart(2, "0");
      return `${hours}:${minutes}:${seconds}`;
    };

    // Mettre à jour l'heure en temps réel
    const updateTime = () => {
      currentTime.value = formatTime(new Date());
    };

    // Utiliser onMounted pour démarrer l'intervalle quand le composant est monté
    onMounted(() => {
      updateTime(); // Pour initialiser avec l'heure actuelle
      const interval = setInterval(updateTime, 1000); // Mettre à jour l'heure toutes les secondes

      // Nettoyer l'intervalle lorsque le composant est démonté
      onUnmounted(() => {
        clearInterval(interval);
      });
    });

    return {
      isOpen,
      toggleIcon,
      messages,
      message,
      sendMessage,
      currentTime,
    };
  },
};
</script>

<style>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}
</style>
