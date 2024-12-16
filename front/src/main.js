import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import "./style.css";
import "./styles/tailwind.css";

// Créer l'application et Pinia
const app = createApp(App);
const pinia = createPinia();

// Utiliser Pinia et le routeur dans l'application
app.use(pinia);
app.use(router);

// Monter l'application
app.mount("#app");
