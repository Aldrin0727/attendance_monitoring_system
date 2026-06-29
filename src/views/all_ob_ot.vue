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

    <!-- Filters -->
    <div class="row mt-3">
      <div class="col-lg-6">
        <div class="d-flex gap-2">
          <select v-model="selectedStatus" class="form-select" @change="fetchAllOTOB">
            <option value="">All Status</option>
            <option value="FOR PRE-APPROVAL">For Pre-Approval</option>
            <option value="PRE-APPROVED">Pre-Approved</option>
            <option value="FOR FINAL APPROVAL">For Final Approval</option>
            <option value="APPROVED">Approved</option>
            <option value="DENIED">Denied</option>
          </select>

          <select v-model="selectedType" class="form-select" @change="fetchAllOTOB">
            <option value="">All Types</option>
            <option value="OB">OB</option>
            <option value="OT">OT</option>
          </select>

          <select v-model="selectedCategory" class="form-select" @change="fetchAllOTOB">
            <option value="">All Categories</option>
            <!-- palitan mo kung ano categories mo -->
            <option value="REGULAR">REGULAR</option>
            <option value="URGENT">URGENT</option>
          </select>
        </div>
      </div>
    </div>

    <!-- DataTable -->
    <div class="card p-4 mt-3">
      <DataTable
        :key="datatableKey"
        class="table table-striped table-bordered display custom-table"
        :columns="columns"
        :data="otobRequests"
        :options="datatableOptions"
      />
    </div>
  </div>

  <!-- MODAL (palitan name kung iba component mo) -->
  <otob_approval
    v-if="is_modal_visible"
    :isVisible="is_modal_visible"
    :ob_ot_Request="selectedRequest"
    @close="closeModal"
    @updateDataTable="handleDataTableUpdate"
  />
</template>

<script>
import "datatables.net-bs5";
import "datatables.net-bs5/css/dataTables.bootstrap5.min.css";
import DataTable from "datatables.net-vue3";
import DataTablesLib from "datatables.net";
import datetime from "@/components/datetime.vue";
import { getUserData } from "@/utils/get_user_data";
import API_BASE from "@/utils/api_config";
import { statusColors, ob_ot_Colors } from "@/utils/badge_colors"; // ✅ add color map for OT/OB if meron
import otob_approval from "@/components/modals/ob_ot_approval.vue"; // ✅ palitan if iba filename mo

DataTable.use(DataTablesLib);

export default {
  components: { datetime, DataTable, otob_approval },

  data() {
    return {
      refreshTimer: null,
      user: getUserData() || {},

      otobRequests: [],
      datatableKey: 0,

      selectedStatus: "",
      selectedType: "",
      selectedCategory: "",

      selectedRequest: null,
      is_modal_visible: false,

      columns: [
        { title: "Reference No.", data: "ref_number" },
        { title: "Employee ID", data: "emp_id" },
        { title: "Employee Name", data: "fullName" },

        {
          title: "Type",
          data: "type",
          render: function (data) {
            const cls = ob_ot_Colors?.[data] || "badge bg-secondary text-white fw-normal";
            return `<span class="${cls}">${data}</span>`;
          },
        },

        { title: "Category", data: "category" },
        { title: "Destination", data: "destination" },

        {
          title: "Requested From",
          data: "req_from",
          render: (data) => (data ? new Date(data).toISOString().slice(0, 19).replace("T", " ") : " "),
        },
        {
          title: "Requested To",
          data: "req_to",
          render: (data) => (data ? new Date(data).toISOString().slice(0, 19).replace("T", " ") : " "),
        },

        {
          title: "Status",
          data: "status",
          render: function (data) {
            const cls = statusColors?.[data] || "badge bg-secondary text-white fw-normal";
            return `<span class="${cls}">${data}</span>`;
          },
        },

        {
          title: "Action",
          data: null,
          render: (row) =>
            `<button class="btn btn-secondary btn-sm view-otob" style="font-size:12px !important" data-id="${row.otob_id}">
              <i class="fas fa-eye"></i>&nbsp;View
            </button>`,
        },
      ],

      datatableOptions: {
        paging: true,
        searching: true,
        ordering: true,
        responsive: true,
        order: [[0, "desc"]],
      },
    };
  },

  computed: {
    deptLabel() {
      return this.user?.dept_code ? `All OB/OT - ${this.user.dept_code}` : "All OB/OT";
    },
  },

  beforeUnmount() {
    this.stopAutoRefresh();
    $(document).off("click", ".view-otob");
  },

  methods: {
    startAutoRefresh() {
      this.stopAutoRefresh();
      this.refreshTimer = setInterval(() => {
        if (this.is_modal_visible) return;
        this.fetchAllOTOB();
      }, 60 * 1000);
    },

    stopAutoRefresh() {
      if (this.refreshTimer) {
        clearInterval(this.refreshTimer);
        this.refreshTimer = null;
      }
    },

    fetchAllOTOB() {
      const payload = {
        dept_code: this.user.dept_code || "",
      };

      if (this.selectedStatus) payload.status = this.selectedStatus;
      if (this.selectedType) payload.type = this.selectedType;
      if (this.selectedCategory) payload.category = this.selectedCategory;

      fetch(`${API_BASE}/depthead_all_otob`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then((r) => r.json())
        .then((data) => {
          this.otobRequests = data.all_list || [];
          this.datatableKey++;
        })
        .catch((err) => console.error("Error fetching OB/OT requests:", err));
    },

    openModal(otobId) {
      const id = Number(otobId);
      this.selectedRequest =
        this.otobRequests.find((r) => Number(r.otob_id) === id) || null;
      this.is_modal_visible = true;
    },

    handleDataTableUpdate() {
      this.fetchAllOTOB();
      this.datatableKey++;
    },

    closeModal() {
      this.is_modal_visible = false;
    },
  },

  mounted() {
    this.fetchAllOTOB();
    this.startAutoRefresh();

    this.$nextTick(() => {
      $(document).on("click", ".view-otob", (event) => {
        const otobId = $(event.currentTarget).data("id");
        this.openModal(otobId);
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
