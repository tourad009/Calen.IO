<script>
import { defineComponent } from "vue";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import Popup from "../components/popup.vue";
import AIOrganizer from "../components/AIOrganizer.vue";
import { useRouter } from 'vue-router';

export default defineComponent({
  components: {
    FullCalendar,
    Popup,
    AIOrganizer,
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  data() {
    return {
      showPopup: false,
      selectedTask: null,
      selectedDates: null,
      calendarOptions: {
        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
        headerToolbar: {
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,timeGridWeek,timeGridDay",
        },
        initialView: 'dayGridMonth',
        editable: true,
        selectable: true,
        selectMirror: true,
        dayMaxEvents: true,
        weekends: true,
        select: this.handleDateSelect,
        eventClick: this.handleEventClick,
        eventDrop: this.handleEventDrop,
        eventResize: this.handleEventResize,
        events: this.fetchEvents,
      },
      currentEvents: [],
      userData: {
        username: '',
        email: ''
      },
      formEvent: {
        id: null,
        title: '',
        start: '',
        end: '',
        priority: 'medium',
      },
      taskFilter: 'all',
    }
  },
  computed: {
    filteredEvents() {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      const weekEnd = new Date(today);
      weekEnd.setDate(today.getDate() + 7);

      return this.currentEvents.filter(event => {
        const eventDate = new Date(event.start);
        switch (this.taskFilter) {
          case 'today':
            return eventDate.toDateString() === today.toDateString();
          case 'week':
            return eventDate >= today && eventDate <= weekEnd;
          case 'high':
            return event.extendedProps.priority === 'high';
          case 'medium':
            return event.extendedProps.priority === 'medium';
          case 'low':
            return event.extendedProps.priority === 'low';
          case 'completed':
            return event.extendedProps.completed;
          default:
            return true;
        }
      });
    }
  },
  methods: {
    getPriorityColor(priority) {
      const colors = {
        low: '#4CAF50',    // Vert
        medium: '#FFA726', // Orange
        high: '#EF5350'    // Rouge
      };
      return colors[priority] || colors.medium;
    },

    async fetchEvents(fetchInfo, successCallback, failureCallback) {
      try {
        const response = await fetch('http://localhost:8000/api/tasks/', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const tasks = await response.json();
        const events = tasks.map(task => ({
          id: task.id,
          title: task.title,
          start: task.due_date,
          end: task.end_date || task.due_date,
          backgroundColor: this.getPriorityColor(task.priority),
          borderColor: this.getPriorityColor(task.priority),
          textColor: '#fff',
          classNames: [
            task.completed ? 'completed-event' : '',
            `priority-${task.priority}`
          ],
          extendedProps: {
            description: task.description,
            priority: task.priority,
            completed: task.completed
          }
        }));

        successCallback(events);
        this.currentEvents = events;
      } catch (error) {
        console.error('Erreur lors du chargement des événements:', error);
        failureCallback(error);
      }
    },

    handleWeekendsToggle() {
      this.calendarOptions.weekends = !this.calendarOptions.weekends;
    },

    handleDateSelect(selectInfo) {
      this.selectedDates = selectInfo;
      this.selectedTask = {
        due_date: selectInfo.startStr,
        end_date: selectInfo.endStr,
      };
      this.showPopup = true;
    },

    async handleEventClick(clickInfo) {
      try {
        const response = await fetch(`http://localhost:8000/tasks/${clickInfo.event.id}/`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.selectedTask = data;
        this.showPopup = true;
      } catch (error) {
        console.error('Erreur lors du chargement de la tâche:', error);
      }
    },

    async handleEventDrop(dropInfo) {
      try {
        const response = await fetch(`http://localhost:8000/api/tasks/update/${dropInfo.event.id}/`, {
          method: 'PUT',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            due_date: dropInfo.event.startStr,
            end_date: dropInfo.event.endStr,
          })
        });

        if (response.status === 401) {
          window.location.href = '/login';
          return;
        }

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      } catch (error) {
        console.error('Erreur lors de la mise à jour de la tâche:', error);
        dropInfo.revert();
      }
    },

    async handleEventResize(resizeInfo) {
      try {
        const response = await fetch(`http://localhost:8000/api/tasks/update/${resizeInfo.event.id}/`, {
          method: 'PUT',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            end_date: resizeInfo.event.endStr,
          })
        });

        if (response.status === 401) {
          window.location.href = '/login';
          return;
        }

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      } catch (error) {
        console.error('Erreur lors de la mise à jour de la tâche:', error);
        resizeInfo.revert();
      }
    },

    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return '';
    },

    closePopup() {
      this.showPopup = false;
      this.selectedTask = null;
      const calendarApi = this.$refs.calendar.getApi();
      calendarApi.refetchEvents();
    },

    async onTaskSaved(taskData) {
      try {
        const calendarApi = this.$refs.calendar.getApi();
        await calendarApi.refetchEvents();
      } catch (error) {
        console.error('Erreur lors du rafraîchissement du calendrier:', error);
      }
    },

    handleEvents(events) {
      this.currentEvents = events;
    },

    async fetchUserData() {
      try {
        const response = await fetch('http://localhost:8000/api/user/current/', {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error('Erreur lors de la récupération des données utilisateur');
        }

        const data = await response.json();
        this.userData = data;
      } catch (error) {
        console.error('Erreur:', error);
        throw error;
      }
    },

    async handleLogout() {
      try {
        const csrfToken = this.getCookie('csrftoken');
        const response = await fetch('http://localhost:8000/api/user/logout/', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          }
        });

        if (!response.ok) {
          throw new Error('Erreur lors de la déconnexion');
        }

        this.$router.push('/login');
      } catch (error) {
        console.error('Erreur lors de la déconnexion:', error);
      }
    },

    async handleSaveEvent() {
      try {
        const url = this.formEvent.id 
          ? `http://localhost:8000/api/tasks/update/${this.formEvent.id}/`
          : `http://localhost:8000/api/tasks/create/`;

        const method = this.formEvent.id ? 'PUT' : 'POST';
        const csrfToken = this.getCookie('csrftoken');

        const response = await fetch(url, {
          method,
          credentials: 'include',
          headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({
            title: this.formEvent.title,
            due_date: this.formEvent.start,
            end_date: this.formEvent.end || this.formEvent.start,
            priority: this.formEvent.priority,
          }),
        });

        if (!response.ok) throw new Error(`Erreur HTTP ! status: ${response.status}`);
        
        const calendarApi = this.$refs.calendar.getApi();
        await calendarApi.refetchEvents();
        this.resetForm();
      } catch (error) {
        console.error('Erreur lors de la sauvegarde de l\'événement :', error);
      }
    },

    resetForm() {
      this.formEvent = {
        id: null,
        title: '',
        start: '',
        end: '',
        priority: 'medium',
      };
    },

    editEvent(event) {
      this.formEvent = {
        id: event.id,
        title: event.title,
        start: event.start,
        end: event.end || event.start,
        priority: event.extendedProps.priority,
      };
    },

    async deleteEvent(eventId) {
      if (!confirm('Êtes-vous sûr de vouloir supprimer cette tâche ?')) return;
      
      try {
        const response = await fetch(`http://localhost:8000/api/tasks/delete/${eventId}/`, {
          method: 'DELETE',
          credentials: 'include',
        });
        if (!response.ok) throw new Error(`Erreur HTTP ! status: ${response.status}`);
        
        const calendarApi = this.$refs.calendar.getApi();
        await calendarApi.refetchEvents();
      } catch (error) {
        console.error('Erreur lors de la suppression de l\'événement :', error);
      }
    },
  },
  async mounted() {
    await this.fetchUserData();
    // Charger les événements au montage du composant
    const calendarApi = this.$refs.calendar.getApi();
    calendarApi.refetchEvents();
  }
});
</script>

<template>
  <div class="demo-app">
    <div class="demo-app-sidebar">
      <div class="demo-app-sidebar-section user-info">
        <div class="user-welcome">
          <button 
            @click="handleLogout" 
            class="logout-button"
          >
            Se déconnecter
          </button>
          <h2 class="welcome-text">Bienvenue, {{ userData.username }} 👋</h2>
        </div>
      </div>
      <div class="demo-app-sidebar-section">
        <label>
          <input
            type="checkbox"
            :checked="calendarOptions.weekends"
            @change="handleWeekendsToggle"
          />
          Afficher les weekends
        </label>
      </div>
      <div class="demo-app-sidebar-section">
        <h2>Gérer les Tâches</h2>
        <form @submit.prevent="handleSaveEvent" class="event-form">
          <input 
            type="text" 
            v-model="formEvent.title" 
            placeholder="Titre de l'événement" 
            required 
            class="form-input"
          />
          <input 
            type="date" 
            v-model="formEvent.start" 
            required 
            class="form-input"
          />
          <input 
            type="date" 
            v-model="formEvent.end" 
            class="form-input"
          />
          <select v-model="formEvent.priority" required class="form-input">
            <option value="low">Basse</option>
            <option value="medium">Moyenne</option>
            <option value="high">Haute</option>
          </select>
          <div class="form-buttons">
            <button type="submit" class=" bg-blue-500 text-white p-2 rounded-md">
              {{ formEvent.id ? 'Modifier' : 'Ajouter' }}
            </button>
            <button 
              v-if="formEvent.id" 
              type="button" 
              @click="resetForm" 
              class="btn-cancel"
            >
              Annuler
            </button>
          </div>
        </form>
      </div>
      <div class="demo-app-sidebar-section">
        <div class="tasks-header">
          <h2>Tâches ({{ currentEvents.length }})</h2>
          <select v-model="taskFilter" class="task-filter">
            <option value="all">Toutes les tâches</option>
            <option value="today">Aujourd'hui</option>
            <option value="week">Cette semaine</option>
            <option value="high">Priorité haute</option>
            <option value="medium">Priorité moyenne</option>
            <option value="low">Priorité basse</option>
            <option value="completed">Terminées</option>
          </select>
        </div>
        <ul class="sidebar-events">
          <li v-for="event in filteredEvents" :key="event.id">
            <div 
              class="sidebar-event-item"
              :class="[
                `priority-${event.extendedProps.priority}`,
                { 'completed-event': event.extendedProps.completed }
              ]"
            >
              <div class="event-header">
                <span class="event-date">{{ new Date(event.start).toLocaleDateString() }}</span>
                <div class="event-actions">
                  <button @click="editEvent(event)" class="btn-edit">✏️</button>
                  <button @click="deleteEvent(event.id)" class="btn-delete">🗑️</button>
                </div>
              </div>
              <div class="event-title">{{ event.title }}</div>
              <div class="event-description" v-if="event.extendedProps.description">
                {{ event.extendedProps.description }}
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div class="demo-app-main">
      <FullCalendar
        ref="calendar"
        class="demo-app-calendar"
        :options="calendarOptions"
      >
        <template v-slot:eventContent="arg">
          <div 
            class="event-content"
            :class="{ 'completed': arg.event.extendedProps.completed }"
          >
            <b>{{ arg.timeText }}</b>
            <i>{{ arg.event.title }}</i>
          </div>
        </template>
      </FullCalendar>
      <div class="ai-organizer-wrapper">
        <AIOrganizer />
      </div>
    </div>

    <Popup
      :show="showPopup"
      :task="selectedTask"
      @close="closePopup"
      @taskSaved="onTaskSaved"
    />
  </div>
</template>

<style>
  h2 {
  margin: 0 0 1em;
  font-size: 16px;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0 0 0 1.5em;
}

li {
  margin: 0.5em 0;
}

b {
  margin-right: 5px;
}

.demo-app {
  display: flex;
  min-height: 100vh;
  font-family: Arial, sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
}

.demo-app-sidebar {
  width: 300px;
  background: #f8f9fa;
  border-right: 1px solid #dee2e6;
  box-shadow: 2px 0 5px rgba(0,0,0,0.05);
}

.demo-app-sidebar-section {
  padding: 1.5em;
  border-bottom: 1px solid #dee2e6;
}

.demo-app-sidebar-section:last-child {
  border-bottom: none;
}

.demo-app-main {
  flex-grow: 1;
  padding: 2em;
  position: relative;
  overflow: hidden;
}

.demo-app-calendar {
  border: 1px solid #d3e2e8;
  border-radius: 4px;
  background: #fff;
  padding: 1em;
}

AIOrganizer {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 1em;
  z-index: 10;
}

.demo-app-calendar {
  border: 1px solid #d3e2e8;
  border-radius: 4px;
  background: #fff;
  padding: 1em;
  position: relative; /* S'assure que le calendrier respecte son propre contexte */
  z-index: 1; /* Z-index inférieur au chatbot */
}

.fc {
  z-index: 0; /* Base du calendrier */
}

.event-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
}

.priority-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.completed {
  text-decoration: line-through;
  opacity: 0.7;
}

.event-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.priority-low {
  border-left: 3px solid #4CAF50;
}

.priority-medium {
  border-left: 3px solid #FFA726;
}

.priority-high {
  border-left: 3px solid #EF5350;
}

.user-info {
  padding: 1.5em;
  border-bottom: 1px solid #d3e2e8;
  background-color: #f8f9fa;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-details {
  flex: 1;
}

.username {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
}

.user-email {
  margin: 0.2rem 0 0;
  font-size: 0.9rem;
  color: #666;
}

.user-welcome {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 1rem;
  padding: 0.5rem 0;
}

.welcome-text {
  margin: 0;
  font-size: 1.2rem;
  color: #2c3e50;
  font-weight: 600;
  width: 100%;
  text-align: center;
}

.logout-button {
  margin-right: 5rem;
  padding: 8px 16px;
  background-color: #fff;
  border: 2px solid #dc3545;
  border-radius: 20px;
  color: #dc3545;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-button:hover {
  background-color: #dc3545;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Styles pour les événements dans le calendrier */
.fc-event {
  padding: 4px 8px;
  margin: 2px 0;
  border-radius: 4px;
  cursor: pointer;
}

.completed-event {
  opacity: 0.7;
  text-decoration: line-through;
}

.priority-high {
  background-color: #EF5350 !important;
  border-left: 4px solid #B71C1C;
}

.priority-medium {
  background-color: #FFA726 !important;
  border-left: 4px solid #E65100;
}

.priority-low {
  background-color: #4CAF50 !important;
  border-left: 4px solid #1B5E20;
}

/* Amélioration de l'affichage des événements */
.fc-daygrid-event-harness {
  margin: 2px 0;
}

.fc-daygrid-day-events {
  padding: 2px;
}

/* Style pour le survol des événements */
.fc-event:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.2s ease;
}

.sidebar-events {
  padding: 0;
  margin: 0;
}

.sidebar-event-item {
  margin: 8px 0;
  padding: 12px;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.2s ease;
}

.sidebar-event-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.15);
}

.sidebar-event-item.priority-high {
  border-left: 4px solid #EF5350;
}

.sidebar-event-item.priority-medium {
  border-left: 4px solid #FFA726;
}

.sidebar-event-item.priority-low {
  border-left: 4px solid #4CAF50;
}

.event-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  font-size: 0.9em;
  color: #666;
}

.event-title {
  font-weight: 600;
  color: #2c3e50;
  margin: 4px 0;
}

.event-description {
  font-size: 0.9em;
  color: #666;
  margin-top: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.event-priority {
  text-transform: capitalize;
  font-size: 0.8em;
  padding: 2px 6px;
  border-radius: 12px;
  background-color: #f5f5f5;
}

.completed-event {
  opacity: 0.7;
}

.completed-event .event-title {
  text-decoration: line-through;
}

.event-form {
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-buttons {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

.btn-save {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-save:hover {
  background-color: #218838;
  transform: translateY(-1px);
}

.btn-cancel {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background-color: #5a6268;
  transform: translateY(-1px);
}

.event-actions {
  display: flex;
  gap: 8px;
}

.btn-edit,
.btn-delete {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 4px;
  transition: transform 0.2s ease;
}

.btn-edit:hover,
.btn-delete:hover {
  transform: scale(1.1);
}

.btn-delete {
  color: #dc3545;
}

.btn-edit {
  color: #007bff;
}

.tasks-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.task-filter {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  font-size: 14px;
  color: #2c3e50;
  cursor: pointer;
  transition: all 0.2s ease;
}

.task-filter:hover {
  border-color: #007bff;
}

.task-filter:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
}
</style>
