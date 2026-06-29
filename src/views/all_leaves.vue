<template>
  <div>
    <!-- Header -->
    <div class="row">
      <div class="col-lg-12 d-flex justify-content-between align-items-center">
        <h2>{{ deptLabel }}</h2>
        <div class="d-flex align-items-center">
          <datetime />
        </div>
      </div>
    </div>
    <hr class="mt-0 mb-3" />

    <div class="row mt-3">
      <div class="col-lg-4">
               <div class="d-flex gap-2">
                    <!-- ✅ allow ALL -->
                    <select v-model="selectedStatus" class="form-select" @change="fetchAllLeave">
                        <option value="">All Status</option>
                        <option value="FOR DEPARTMENT HEAD APPROVAL">Pending</option>
                        <option value="APPROVED">Approved</option>
                        <option value="DENIED">Denied</option>
                        <option value="CANCELLED">Cancelled</option>
                    </select>

                    <select v-model="selectedLeaveType" class="form-select" @change="fetchAllLeave">
                        <option value="">All Types</option>
                        <option value="EL">Emergency Leave</option>
                        <option value="VL">Vacation Leave</option>
                        <option value="SL">Sick Leave</option>
                    </select>

    

        </div>
      </div>
    </div>

    <div class="card p-4 mt-3">
      <DataTable
        :key="datatableKey"
        class="table table-striped table-bordered display custom-table"
        :columns="columns"
        :data="leaveRequests"
        :options="datatableOptions"
      />
    </div>
  </div>

  <leave_approval
    v-if="is_modal_visible"
    :isVisible="is_modal_visible"
    :leaveRequest="selectedLeaveRequest"
    @close="closeModal"
    @updateDataTable="handleDataTableUpdate"
  />
</template>


<script>
import 'datatables.net-bs5';
import 'datatables.net-bs5/css/dataTables.bootstrap5.min.css';
import DataTable from 'datatables.net-vue3';
import DataTablesLib from 'datatables.net';
import datetime from '@/components/datetime.vue';
import { getUserData } from '@/utils/get_user_data'
import API_BASE from '@/utils/api_config';
import { statusColors, leave_type_Colors } from '@/utils/badge_colors';
import leave_approval from '@/components/modals/leave_approval.vue';

DataTable.use(DataTablesLib);

export default {
  components: { datetime, DataTable, leave_approval },

  data() {
    return {
      refreshTimer: null,
      user: getUserData() || {},
      leaveRequests: [],
      datatableKey: 0,

      // ✅ for ALL LEAVES default: show all
      selectedStatus: "",
      selectedLeaveType: "",

      selectedLeaveRequest: null,
      is_modal_visible: false,

      columns: [
        { title: "Reference No.", data: "ref_no" },
        { title: "Employee ID", data: "emp_id" },
        { title: "Employee Name", data: "user" },
        {
          title: "Type",
          data: "leave_type",
          render: function (data) {
            const statusClass = leave_type_Colors[data] || "badge bg-secondary text-white fw-normal";
            return `<span class="${statusClass}">${data}</span>`;
          },
        },
        {
          title: "Date From",
          data: "leave_from",
          render: (data) => (data ? new Date(data).toISOString().slice(0, 10) : " "),
        },
        {
          title: "Date To",
          data: "leave_to",
          render: (data) => (data ? new Date(data).toISOString().slice(0, 10) : " "),
        },
        { title: "Total Days", data: "leave_number" },
        {
          title: "Date Submitted",
          data: "date_created",
          render: (data) => new Date(data).toISOString().slice(0, 19).replace("T", " "),
        },
        {
          title: "Status",
          data: "status",
          render: function (data) {
            const statusClass = statusColors[data] || "badge bg-secondary text-white fw-normal";
            return `<span class="${statusClass}">${data}</span>`;
          },
        },
        {
          title: "Action",
          data: null,
          render: (row) =>
            `<button class="btn btn-secondary btn-sm view-leave-req" style="font-size: 12px !important" data-id="${row.id}">
              <i class="fas fa-eye"></i>&nbsp;View
            </button>`,
        },
      ],

      datatableOptions: {
        paging: true,
        searching: true,
        ordering: true,
        responsive: true,
        order: [[7, "desc"]],
      },
    };
  },

  computed: {
    deptLabel() {
      return this.user?.dept_code ? `All Leaves - ${this.user.dept_code}` : "All Leaves";
    },
  },

  beforeUnmount() {
    this.stopAutoRefresh();
    $(document).off("click", ".view-leave-req");
  },

  methods: {
    startAutoRefresh() {
      this.stopAutoRefresh();
      this.refreshTimer = setInterval(() => {
        if (this.is_modal_visible) return;
        this.fetchAllLeave();
      }, 60 * 1000);
    },

    stopAutoRefresh() {
      if (this.refreshTimer) {
        clearInterval(this.refreshTimer);
        this.refreshTimer = null;
      }
    },

    fetchAllLeave() {
      const payload = {
        dept_code: this.user.dept_code || "",
      };

      if (this.selectedStatus) payload.status = this.selectedStatus;
      if (this.selectedLeaveType) payload.leave_type = this.selectedLeaveType;

      fetch(`${API_BASE}/depthead_all_leaves`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then((r) => r.json())
        .then((data) => {
          this.leaveRequests = data.all_list || [];
          this.datatableKey++;
        })
        .catch((err) => console.error("Error fetching leave requests:", err));
    },

    openModal(leaveRequestId) {
      const id = Number(leaveRequestId); // ✅ ensure match
      this.selectedLeaveRequest = this.leaveRequests.find((req) => Number(req.id) === id) || null;
      this.is_modal_visible = true;
    },

    handleDataTableUpdate() {
       this.fetchAllLeave();   
      this.datatableKey++;
    },

    closeModal() {
      this.is_modal_visible = false;
    },
  },

  mounted() {
    this.fetchAllLeave();   
    this.startAutoRefresh();

    this.$nextTick(() => {
      $(document).on("click", ".view-leave-req", (event) => {
        const leaveRequestId = $(event.currentTarget).data("id");
        this.openModal(leaveRequestId);
      });
    });
  },
};

</script>

<style>
@import url(../../public/global.css);
@import url(../assets/css/dataTable.css);
@import url(../assets/css/buttons.css);
@import url(../assets/css/modal.css);
</style>
