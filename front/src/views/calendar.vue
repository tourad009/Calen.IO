<script>
import { defineComponent } from "vue";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import { INITIAL_EVENTS, createEventId } from "../event-utils";
import Popup from "../components/popup.vue";
import AIOrganizer from "../components/AIOrganizer.vue";

export default defineComponent({
  components: {
    FullCalendar,
    Popup,
    AIOrganizer,
  },
  data() {
    return {
      showPopup: false,
      newEventTitle: '',
      selectedDates: null,
      calendarOptions: {
        plugins: [
          dayGridPlugin,
          timeGridPlugin,
          interactionPlugin
        ],
        headerToolbar: {
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,timeGridWeek,timeGridDay",
        },
        initialView: 'dayGridMonth',
        initialEvents: INITIAL_EVENTS,
        editable: true,
        selectable: true,
        selectMirror: true,
        dayMaxEvents: true,
        weekends: true,
        select: this.handleDateSelect,
        eventClick: this.handleEventClick,
        eventsSet: this.handleEvents,
      },
      currentEvents: [],
    }
  },
  methods: {
    handleWeekendsToggle() {
      this.calendarOptions.weekends = !this.calendarOptions.weekends;
    },
    handleDateSelect(selectInfo) {
      this.selectedDates = selectInfo;
      this.showPopup = true;
    },
    updateEventTitle(title) {
      this.newEventTitle = title;
    },
    closePopup() {
      this.showPopup = false;
      this.newEventTitle = '';
    },
    saveEvent() {
      const calendarApi = this.selectedDates.view.calendar;
      calendarApi.unselect();

      if (this.newEventTitle) {
        calendarApi.addEvent({
          id: createEventId(),
          title: this.newEventTitle,
          start: this.selectedDates.startStr,
          end: this.selectedDates.endStr,
          allDay: this.selectedDates.allDay,
        });
      }
      this.closePopup();
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
          <li>Click an event to delete it</li>
        </ul>
      </div>
      <div class="demo-app-sidebar-section">
        <label>
          <input
            type="checkbox"
            :checked="calendarOptions.weekends"
            @change="handleWeekendsToggle"
          />
          toggle weekends
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
      <div class="ai-organizer-wrapper">
        <AIOrganizer />
      </div>
    </div>
    <!-- Popup -->
    <Popup
      :show="showPopup"
      @close="closePopup"
      @save="saveEvent"
      :event-title="newEventTitle"
      @update-title="updateEventTitle"
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
  background: #eaf9ff;
  border-right: 1px solid #d3e2e8;
}

.demo-app-sidebar-section {
  padding: 1.5em;
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
</style>
