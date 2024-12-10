<script>
import { defineComponent } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { INITIAL_EVENTS, createEventId } from '../event-utils'
import Popup from '../components/popup.vue'

export default defineComponent({
  components: {
    FullCalendar,
    Popup,
  },
  data() {
    return {
      showPopup: false, // gerer la visibilité du popup
      newEventTitle: '', // Stocke le titre du nouvel événement
      selectedDates: null, // Stocke les informations de la sélection de dates
      calendarOptions: {
        plugins: [
          dayGridPlugin,
          timeGridPlugin,
          interactionPlugin // nécessaire pour gérer les clics sur le calendrier
        ],
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        initialView: 'dayGridMonth',
        initialEvents: INITIAL_EVENTS, // évènements initiaux
        editable: true,
        selectable: true,
        selectMirror: true,
        dayMaxEvents: true,
        weekends: true,
        select: this.handleDateSelect, // Gère la sélection des dates
        eventClick: this.handleEventClick,
        eventsSet: this.handleEvents,
      },
      currentEvents: [], // Liste des événements actuels
    }
  },
  methods: {
    handleDateSelect(selectInfo) {
      // Enregistre les informations des dates sélectionnées et affiche le popup
      this.selectedDates = selectInfo;
      this.showPopup = true;
    },
    closePopup() {
      this.showPopup = false; // Ferme le popup
      this.newEventTitle = ''; // Réinitialise le titre
    },
    saveEvent() {
      // Ajoute un nouvel événement basé sur les informations du popup
      const calendarApi = this.selectedDates.view.calendar;
      calendarApi.unselect(); // Efface la sélection des dates dans le calendrier

      if (this.newEventTitle) {
        calendarApi.addEvent({
          id: createEventId(),
          title: this.newEventTitle,
          start: this.selectedDates.startStr,
          end: this.selectedDates.endStr,
          allDay: this.selectedDates.allDay,
        });
      }
      this.closePopup(); // Ferme le popup après l'enregistrement
    },
    handleEventClick(clickInfo) {
      if (confirm(`Are you sure you want to delete the event '${clickInfo.event.title}'`)) {
        clickInfo.event.remove();
      }
    },
    handleEvents(events) {
      this.currentEvents = events;
    },
  },
});
</script>
<template>
  <div class="demo-app">
    <div class="demo-app-sidebar">
      <div class="demo-app-sidebar-section">
        <h2>Instructions</h2>
        <ul>
          <li>Select dates and you will be prompted to create a new event</li>
          <li>Drag, drop, and resize events</li>
          <li>Click an event to edit or delete it</li>
        </ul>
      </div>
      <div class="demo-app-sidebar-section">
        <label>
          <input
            type="checkbox"
            :checked="calendarOptions.weekends"
            @change="calendarOptions.weekends = !calendarOptions.weekends"
          />
          Toggle weekends
        </label>
      </div>
      <div class="demo-app-sidebar-section">
        <h2>All Events ({{ currentEvents.length }})</h2>
        <ul>
          <li v-for="event in currentEvents" :key="event.id">
            <b>{{ event.startStr }}</b>
            <i>{{ event.title }}</i>
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
          <b>{{ arg.timeText }}</b>
          <i>{{ arg.event.title }}</i>
        </template>
      </FullCalendar>
    </div>
    <!-- Popup -->
    <Popup
      :show="showPopup"
      @close="closePopup"
      @save="saveEvent"
      :event="null"
    />
  </div>
</template>


<style lang='css'>

h2 {
  margin: 0;
  font-size: 16px;
}

ul {
  margin: 0;
  padding: 0 0 0 1.5em;
}

li {
  margin: 1.5em 0;
  padding: 0;
}

b { /* used for event dates/times */
  margin-right: 3px;
}

.demo-app {
  display: flex;
  min-height: 100%;
  font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
  font-size: 14px;
}

.demo-app-sidebar {
  width: 300px;
  line-height: 1.5;
  background: #eaf9ff;
  border-right: 1px solid #d3e2e8;
}

.demo-app-sidebar-section {
  padding: 2em;
}

.demo-app-main {
  flex-grow: 1;
  padding: 3em;
}

.fc { /* the calendar root */
  max-width: 1100px;
  margin: 0 auto;
}

</style>