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

        <!-- DataTable -->
        <div class="card p-4 mt-3">
            <DataTable v-if="leaveRequests.length" :key="datatableKey"
                class="table table-striped table-bordered display custom-table" :columns="columns" :data="leaveRequests"
                :options="datatableOptions" />

        </div>

    </div>

</template>


<script>

import 'datatables.net-bs5';
import 'datatables.net-bs5/css/dataTables.bootstrap5.min.css';
import DataTable from 'datatables.net-vue3';
import DataTablesLib from 'datatables.net';
import datetime from '@/components/datetime.vue';

import { getUserData } from '@/utils/get_user_data'
import API_BASE from '@/utils/api_config';
import { statusColors } from '@/utils/badge_colors';

DataTable.use(DataTablesLib);

export default {
    props: ["status"],
    components: {
        datetime,
        DataTable,
    },
    data() {
        return {
            user: getUserData() || {},

            leaveRequests: [],
            datatableKey: 0,

            columns: [
                { title: 'Type', data: 'leave_type' },
                {
                    title: 'Date From', data: 'leave_from',
                    render: function (data) {
                        if (!data) return ' ';
                        return new Date(data).toISOString().slice(0, 10); // "YYYY-MM-DD"
                    }

                },
                {
                    title: 'Date To', data: 'leave_to', render: function (data) {
                        if (!data) return ' ';
                        return new Date(data).toISOString().slice(0, 10); // "YYYY-MM-DD"
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
                        const statusClass = statusColors[data] || 'badge bg-secondary text-white fw-normal'; // Default class
                        return `<span class="${statusClass}">${data}</span>`;
                    }
                },

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

    },

    methods: {
        fetchUserLeaveRequests() {
            fetch(`${API_BASE}/leave_list`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    fullName: `${this.user.first_name} ${this.user.last_name}`
                })
            })
                .then(response => response.json())
                .then(data => {
                    // console.log('API response:', data);
                    this.leaveRequests = data.data || [];
                    this.datatableKey++;
                })
                .catch(error => {
                    console.error("Error fetching tickets:", error);
                });
        },

    },
    mounted() {
        this.fetchUserLeaveRequests();
    },

};
</script>

<style>
@import url(../../public/global.css);
@import url(../assets/css/dataTable.css);

</style>