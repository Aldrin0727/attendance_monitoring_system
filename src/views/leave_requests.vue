<template>
    <div>
        <!-- Header -->
        <div class="row">
            <!-- Dashboard Header -->
            <div class="col-lg-12 d-flex justify-content-between align-items-center">
                <h2>Leave Requests Management</h2>
                <div class="d-flex align-items-center">
                    <datetime />
                </div>
            </div>
        </div>
        <hr class="mt-0 mb-3">

        <div class="row mt-3">
            <div class="col-lg-3">
                <div class="d-flex">
                    <select v-model="selectedStatus" class="form-select me-2" @change="fetchUserLeaveRequests">
                        <option value="" disabled>Select Status</option>
                        <option value="FOR DEPARTMENT HEAD APPROVAL">Pending</option>
                        <option value="APPROVED">Approved</option>
                        <option value="DENIED">Denied</option>
                    </select>

                    <select v-model="selectedLeaveType" class="form-select" @change="fetchUserLeaveRequests">
                        <option value="" disabled>Select Leave Type</option>
                        <option value="EL">Emergency Leave</option>
                        <option value="VL">Vacation Leave</option>
                        <option value="SL">Sick Leave</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- DataTable -->
    <div class="card p-4 mt-3">
            <DataTable v-if="leaveRequests.length" :key="datatableKey"
                class="table table-striped table-bordered display custom-table" :columns="columns" :data="leaveRequests"
                :options="datatableOptions" />
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
    props: ["status", "job_title", "isVisible"],
    components: {
        datetime,
        DataTable,
        leave_approval
    },
    data() {
        return {
            user: getUserData() || {},
            leaveRequests: [],
            datatableKey: 0,
            selectedStatus: '',
            selectedLeaveType: '',
            selectedLeaveRequest: null,
            is_modal_visible: false,

            columns: [
                { title: 'Type', data: 'leave_type',
                     render: function (data) {
                        const statusClass = leave_type_Colors[data] || 'badge bg-secondary text-white fw-normal';
                        return `<span class="${statusClass}">${data}</span>`;
                    }
                 },
                {
                    title: 'Date From', data: 'leave_from',
                    render: function (data) {
                        if (!data) return ' ';
                        return new Date(data).toISOString().slice(0, 10);
                    }
                },
                {
                    title: 'Date To', data: 'leave_to', render: function (data) {
                        if (!data) return ' ';
                        return new Date(data).toISOString().slice(0, 10);
                    }
                },
                { title: 'Total Days', data: 'leave_number' },
                {
                    title: 'Date Submitted', data: 'date_created',
                    render: function (data) {
                        return new Date(data).toISOString().slice(0, 19).replace("T", " ");
                    }
                },
                {
                    title: 'Status', data: 'status',
                    render: function (data) {
                        const statusClass = statusColors[data] || 'badge bg-secondary text-white fw-normal';
                        return `<span class="${statusClass}">${data}</span>`;
                    }
                },
             {
                    title: 'Action', data: null,
                    render: (data) => {
                        return `<button class="btn btn-secondary btn-sm view-leave-req" style="font-size: 12px !important" data-id="${data.id}"><i class="fas fa-eye"></i>&nbsp;View</button>`;
                    }
                }

            ],

            datatableOptions: {
                paging: true,
                searching: true,
                ordering: true,
                responsive: true,
                order: [[5, 'desc']],
            },
        };
    },
    watch: {
        status(newStatus) {
            this.selectedStatus = newStatus;  // Update local status when prop changes
            this.fetchUserLeaveRequests();  // Re-fetch data
        },
        job_title(newJobTitle) {
            this.fetchUserLeaveRequests();  // Re-fetch data when job title changes
        }
    },
    methods: {
      

        fetchUserLeaveRequests() {
            const payload = {
                fullName: `${this.user.first_name} ${this.user.last_name}`,
                status: this.selectedStatus || '' || this.status,
                leave_type: this.selectedLeaveType || '',
                job_title: this.job_title || '',
                dept_code: this.user.dept_code || '',
<<<<<<< HEAD
                emp_id: this.user.emp_id
=======
                emp_id: this.user.emp_id || '',
>>>>>>> origin/lj_branch
            };
            // console.log(payload)

            fetch(`${API_BASE}/all_leave_details`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    this.leaveRequests = data.all_list || [];
                    this.datatableKey++;  // Re-render the DataTable
                })
                .catch(error => {
                    console.error("Error fetching leave requests:", error);
                });
        },


       openModal(leaveRequestId) {
            const selectedRequest = this.leaveRequests.find(req => req.id === leaveRequestId);
            this.selectedLeaveRequest = selectedRequest;
            this.is_modal_visible = true;
        },

        handleDataTableUpdate() {
            this.fetchUserLeaveRequests();
            this.datatableKey++;
        },

        closeModal() {
            this.is_modal_visible = false;
            // console.log('Modal closed:', this.is_modal_visible);
        }

    },
    mounted() {
        this.fetchUserLeaveRequests();  // Fetch leave requests initially

        this.$nextTick(() => {
            // Use jQuery to handle event delegation for dynamically generated elements
            $(document).on("click", ".view-leave-req", (event) => {
                const leaveRequestId = $(event.currentTarget).data("id");
                this.openModal(leaveRequestId);
            });
        });
    }
}
</script>

<style>
@import url(../../public/global.css);
@import url(../assets/css/dataTable.css);
@import url(../assets/css/buttons.css);
@import url(../assets/css/modal.css);
</style>
