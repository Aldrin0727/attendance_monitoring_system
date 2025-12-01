<template>
  <div class="row">
    <!-- Dashboard Header -->
    <div class="col-lg-12 d-flex justify-content-between align-items-center">
      <h2>Dashboard</h2>
      <div class="d-flex align-items-center">
        <datetime />
      </div>
    </div>
  </div>
  <hr class="mt-0 mb-3">

  <!-- Button for filing leave -->
  <div class="row mt-3">
    <div class="col-lg-12 text-end">
      <button class="btn btn-secondary" @click="file_leave_btn">
        <font-awesome-icon :icon="['fas', 'circle-plus']" class="me-2" /> File a Leave
      </button>
    </div>
  </div>

  <div class="row mt-1 g-3">
    <div class="col-lg-8 col-md-12 col-12">
      <div class="custom-card">
        <FullCalendar :options="calendarOptions" />
      </div>
    </div>

    <!-- Leave Credits Card Section -->
    <div class="col-lg-4 col-md-12 col-12 mb-4">
      <div class="custom-card p-3">
        <h5 class="card-title d-flex justify-content-between align-items-center">LEAVE CREDITS</h5>

        <!-- Vacation Leave Card -->
        <div class="card h-100 mt-2">
          <div class="card-body">
            <div class="d-flex justify-content-around align-items-center ">
              <font-awesome-icon :icon="['fas', 'map']" class="font-awesome-icon" style="color: #ff7f50 !important" />
              <div style="width: 70%">
                <span class="text-muted fw-bold">Vacation | Emergency Leave</span>
                <div class="mt-3">
                  <div class="d-flex justify-content-between">
                    <span class="text-muted">Used Leave</span>
                    <span class="fw-bold">0/15 days</span> <!-- Replace with dynamic value -->
                  </div>
                  <div class="progress  mt-1" style="height: 10px;">
                    <div class="progress-bar" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0"
                      aria-valuemax="15"></div>
                  </div>

                  <div class="d-flex justify-content-between mt-3">
                    <span class="text-muted">Remaining Leave</span>
                    <span class="fw-bold">15 days</span> <!-- Replace with dynamic value -->
                  </div>
                  <div class="progress mt-1" style="height: 10px;">
                    <div class="progress-bar bg-success" role="progressbar" style="width: 100%" aria-valuenow="15"
                      aria-valuemin="0" aria-valuemax="15"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sick Leave Card -->
        <div class="card h-100 mt-3">
          <div class="card-body">
            <div class="d-flex justify-content-around align-items-center ">
              <font-awesome-icon :icon="['fas', 'thermometer']" class="font-awesome-icon"
                style="color: #eb50aa !important" />
              <div style="width: 70%">
                <span class="text-muted fw-bold">Sick Leave</span>
                <div class="mt-3">
                  <div class="d-flex justify-content-between">
                    <span class="text-muted">Used Leave</span>
                    <span class="fw-bold">0/15 days</span> <!-- Replace with dynamic value -->
                  </div>
                  <div class="progress  mt-1" style="height: 10px;">
                    <div class="progress-bar" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0"
                      aria-valuemax="15"></div>
                  </div>

                  <div class="d-flex justify-content-between mt-3">
                    <span class="text-muted">Remaining Leave</span>
                    <span class="fw-bold">15 days</span> <!-- Replace with dynamic value -->
                  </div>
                  <div class="progress mt-1" style="height: 10px;">
                    <div class="progress-bar bg-success" role="progressbar" style="width: 100%" aria-valuenow="15"
                      aria-valuemin="0" aria-valuemax="15"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
  <file_leave_modal v-if="is_file_leave_modal_visible" :isVisible="is_file_leave_modal_visible"
    @close="close_file_leave_modal" />
</template>
<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import datetime from '@/components/datetime.vue';

import bootstrap5Plugin from '@fullcalendar/bootstrap5';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import file_leave_modal from '@/components/modals/file_leave_modal.vue';

export default {
  components: {
    FullCalendar,
    datetime,
    file_leave_modal
  },
  data() {
    return {
      is_file_leave_modal_visible: false,


      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin, bootstrap5Plugin],
        initialView: 'dayGridMonth',
        themeSystem: 'bootstrap5',
        dateClick: this.handleDateClick,
        events: [
          // { title: 'Event 1', date: '2025-11-10', color: '#ff7f50' },
          // { title: 'Event 2', date: '2025-11-12', color: '#7f8c8d' },
          // { title: 'Event 3', date: '2025-11-14', color: '#3498db' }
        ],
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,dayGridWeek'
        },
        eventRender: this.customEventRendering,
      }
    }
  },
  methods: {
    file_leave_btn() {
      // alert('open modal')
      this.is_file_leave_modal_visible = true;
    },

    close_file_leave_modal() {
      this.is_file_leave_modal_visible = false;
    },

    handleDateClick() {
      alert('You clicked on: ' + arg.dateStr)
    },
    customEventRendering(info) {
      const event = info.event;
      event.setProp('backgroundColor', event.extendedProps.color);
      event.setProp('borderColor', event.extendedProps.color);
      event.setProp('textColor', '#ffffff');
    }
  }
}
</script>

<style scoped>
@import url(../assets/css/cards.css);
@import url(../assets/css/buttons.css);

.fc {
  max-width: 100%;
  height: 800px;
  padding: 35px;
  color: #333;
}



.card-footer a:hover {
  text-decoration: underline;
}

.card-body {
  position: relative;
}

p {
  display: flex;
  align-items: center;
}

.font-awesome-icon {
  height: 60px;
}

.row {
  display: flex;
  flex-wrap: wrap;
}
</style>
