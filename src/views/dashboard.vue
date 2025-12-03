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
                    <span class="fw-bold">{{ vl_used }}/{{ vl_total }} days</span>
                  </div>
                  <div class="progress mt-1" style="height: 10px;">
                    <div class="progress-bar used-leave-bar" role="progressbar" :style="{ width: vlUsedPercent + '%' }"
                      :aria-valuenow="vl_used" aria-valuemin="0" :aria-valuemax="vl_total"></div>
                  </div>

                  <div class="d-flex justify-content-between mt-3">
                    <span class="text-muted">Remaining Leave</span>
                    <span class="fw-bold">{{ vlRemaining }} days</span>
                  </div>
                  <div class="progress mt-1" style="height: 10px;">
                    <div class="progress-bar bg-success" role="progressbar" :style="{ width: vlRemainingPercent + '%' }"
                      :aria-valuenow="vlRemaining" aria-valuemin="0" :aria-valuemax="vl_total"></div>
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
                    <span class="fw-bold">{{ sl_used }}/{{ sl_total }} days</span>
                  </div>
                  <div class="progress mt-1" style="height: 10px;">
                    <div class="progress-bar used-leave-bar" role="progressbar" :style="{ width: slUsedPercent + '%' }"
                      :aria-valuenow="sl_used" aria-valuemin="0" :aria-valuemax="sl_total"></div>
                  </div>

                  <div class="d-flex justify-content-between mt-3">
                    <span class="text-muted">Remaining Leave</span>
                    <span class="fw-bold">{{ slRemaining }} days</span>
                  </div>
                  <div class="progress mt-1" style="height: 10px;">
                    <div class="progress-bar bg-success" role="progressbar" :style="{ width: slRemainingPercent + '%' }"
                      :aria-valuenow="slRemaining" aria-valuemin="0" :aria-valuemax="sl_total"></div>
                  </div>

                </div>
              </div>
            </div>
          </div>
        </div>

      </div>


      <!-- Custom Card for Security Check -->
      <div class="custom-card p-3 mb-4 mt-3">
        <h5 class="card-title d-flex justify-content-between align-items-center">
          PENDING
        </h5>


        <div class="card h-100 mt-2">
          <div class="card-body has-fav-padding d-flex justify-content-between align-items-center">
            <font-awesome-icon :icon="['fas', 'hourglass-half']" class="font-awesome-icon" style="color:#edc55b" />
            <div class="text-end">
              <h3 class="fw-bold mb-0">{{ for_dept_head_approval_pending ?? 0 }}</h3>
              <span class="text-muted">Pending for Department Head Approval</span>
            </div>
          </div>
          <div class="card-footer py-1 px-2">
            <a href="#" class="text-white d-flex justify-content-between align-items-center m-0"
              style="text-decoration:none;" @click.prevent="goToLeaveRequests('FOR DEPARTMENT HEAD APPROVAL', '')">
              <span>View Details</span>
              <i class="fas fa-arrow-right"></i>
            </a>
          </div>
        </div>

        <div class="card h-100 mt-3" v-if="user.job_title == 'Department Head'">
          <div class="card-body has-fav-padding d-flex justify-content-between align-items-center">
            <font-awesome-icon :icon="['fas', 'user-check']" class="font-awesome-icon" style="color:#0dcaf0" />
            <div class="text-end">
              <h3 class="fw-bold mb-0">{{ for_dept_head?? 0 }}</h3>
              <span class="text-muted">Pending for Your Approval (Only for DH)</span>
            </div>
          </div>
          <div class="card-footer py-1 px-2">
            <a href="#" class="text-white d-flex justify-content-between align-items-center m-0"
              style="text-decoration:none;" @click.prevent="goToLeaveRequests('FOR DEPARTMENT HEAD APPROVAL', user.job_title)">
              <span>View Details</span>
              <i class="fas fa-arrow-right"></i>
            </a>
          </div>
        </div>




      </div>

    </div>
  </div>
  <file_leave_modal v-if="is_file_leave_modal_visible" :isVisible="is_file_leave_modal_visible"
    @close="close_file_leave_modal" />
</template>

<script>
import { getUserData } from '@/utils/get_user_data';
import API_BASE from '@/utils/api_config';
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
      user: getUserData() || {},
      is_file_leave_modal_visible: false,

      vl_total: 15,
      vl_used: 0,
      sl_total: 15,
      sl_used: 0,

      for_dept_head_approval_pending: 0,
      for_dept_head: 0,

      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin, bootstrap5Plugin],
        initialView: 'dayGridMonth',
        themeSystem: 'bootstrap5',
        dateClick: this.handleDateClick,
        events: [
          { title: 'Event 1', date: '2025-11-10', color: '#ff7f50' },
          { title: 'Event 2', date: '2025-11-12', color: '#7f8c8d' },
          { title: 'Event 3', date: '2025-11-14', color: '#3498db' }
        ],
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,dayGridWeek'
        },
        eventContent: this.customEventRendering,
      }
    }
  },
  mounted() {
    this.fetchForApprovalCount();
  },

  computed: {
    vlRemaining() {
      return Math.max(this.vl_total - this.vl_used, 0);
      
    },
    slRemaining() {
      return Math.max(this.sl_total - this.sl_used, 0);
    },
    vlUsedPercent() {
      if (!this.vl_total) return 0;
      return Math.min((this.vl_used / this.vl_total) * 100, 100);
    },
    vlRemainingPercent() {
      if (!this.vl_total) return 0;
      return Math.min((this.vlRemaining / this.vl_total) * 100, 100);
    },
    slUsedPercent() {
      if (!this.sl_total) return 0;
      return Math.min((this.sl_used / this.sl_total) * 100, 100);
    },
    slRemainingPercent() {
      if (!this.sl_total) return 0;
      return Math.min((this.slRemaining / this.sl_total) * 100, 100);
    },
  },

  methods: {
    goToLeaveRequests(status, job_title) {
   
        this.$router.push({ 
              name: 'LeaveRequests', 
              query: { 
                status: status, job_title: job_title } 
              });

    },

    file_leave_btn() {
      // alert('open modal')
      this.is_file_leave_modal_visible = true;
    },

    close_file_leave_modal() {
      this.is_file_leave_modal_visible = false;
    },

    handleDateClick() {
      alert('You clicked on: ')
    },

    customEventRendering(info) {
      const event = info.event;
      // event.setProp('backgroundColor', event.extendedProps.color);
      // event.setProp('borderColor', event.extendedProps.color);
      // event.setProp('textColor', '#ffffff');
      const customContent = document.createElement('div');
      customContent.innerHTML = `<span style="color: ${event.extendedProps.color};">${event.title}</span>`;
      return { domNodes: [customContent] };
    },

    fetchForApprovalCount() {

      fetch(`${API_BASE}/for_approval_count`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          fullName: `${this.user.first_name} ${this.user.last_name}`,
          job_title: this.user.job_title,
          department: this.user.dept_code,
        })
      })
        .then(res => res.json())
        .then(data => {
          // console.log(data)
          if (data.success) {
            this.for_dept_head_approval_pending = data.fapp_count || 0;
            this.for_dept_head= data.app_count || 0;
            
            this.vl_used = data.used_vl || 0;
            this.sl_used = data.used_sl || 0;
          } else {
            console.error('for_approval_count error:', data.error);
          }
        })
        .catch(err => {
          console.error("Error fetching department head ticket statuses:", err);
        });
    },


  }
}
</script>

<style scoped>
@import url(../assets/css/cards.css);
@import url(../assets/css/buttons.css);
@import url(../../public/global.css);

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
