<template>
    <div>
        <!-- Header -->
        <div class="row">
            <!-- Dashboard Header -->
            <div class="col-lg-12 d-flex justify-content-between align-items-center">
                <h2>OB/OT Lists</h2>
                <div class="d-flex align-items-center">
                    <datetime />
                </div>
            </div>
        </div>
        <hr class="mt-0 mb-3">





        <div class="row mt-3">

            <div class="col-lg-3">
                <div class="d-flex justify-content-between align-items-center">
                    <!-- Leave Status Dropdown -->
                    <!-- <select v-model="selectedStatus" class="form-select me-2" @change="fetchUserLeaveRequests">
                        <option value="" disabled>Select Status</option>
                        <option value="FOR DEPARTMENT HEAD APPROVAL">Pending</option>
                        <option value="APPROVED">Approved</option>
                        <option value="DENIED">Denied</option>
                    </select>    -->
              
                </div>
            </div>
            <div class="col-lg-9 d-flex justify-content-end align-items-center">
                <button class="btn btn-secondary ob_ot" @click="file_leave_btn">
                    <font-awesome-icon :icon="['fas', 'circle-plus']" class="me-2" /> File an OT/OB
                </button>

            </div>
        </div>



        <!-- DataTable -->
        <div class="card p-4 mt-3">
            <DataTable v-if="leaveRequests.length" :key="datatableKey"
                class="table table-striped table-bordered display custom-table" :columns="columns" :data="leaveRequests"
                :options="datatableOptions" />
        </div>
    </div>

     <file_ob_ot v-if="is_file_ob_ot_modal_visible" :isVisible="is_file_ob_ot_modal_visible"
    @close="close_file_ob_ot_modal" />

</template>

<script>
import DataTable from 'datatables.net-vue3';
import DataTablesLib from 'datatables.net';
import datetime from '@/components/datetime.vue';
import { getUserData } from '@/utils/get_user_data'
import API_BASE from '@/utils/api_config';
import { statusColors, leave_type_Colors } from '@/utils/badge_colors';
import file_ob_ot from '@/components/modals/file_ob_ot.vue';


DataTable.use(DataTablesLib);

export default {
    components: {
        datetime,
        DataTable,
        file_ob_ot
    },
    data() {
        return {
            user: getUserData() || {},
            leaveRequests: [],
            datatableKey: 0,
            is_file_ob_ot_modal_visible: false,

            columns: [
                {
                    title: 'Type', data: 'leave_type',
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
    methods: {

        file_leave_btn() {
            this.is_file_ob_ot_modal_visible = true;
            console.log('open modal')
        },

      
        close_file_ob_ot_modal() {
            this.is_file_ob_ot_modal_visible = false;
            // console.log('Modal closed:', this.is_modal_visible);
        }

    },
    mounted() {
   
    }
}
</script>

<style>
@import url(../../public/global.css);
@import url(../assets/css/dataTable.css);
@import url(../assets/css/buttons.css);
@import url(../assets/css/modal.css);

.ob_ot{
    background-color: #df7a8a !important;
}

.ob_ot:focus, .ob_ot:hover{
     background-color: #5ac5c5 !important;
}
</style>
