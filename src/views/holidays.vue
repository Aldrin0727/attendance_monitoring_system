<template>
    <div>
        <!-- Header -->
        <div class="row">
            <!-- Dashboard Header -->
            <div class="col-lg-12 d-flex justify-content-between align-items-center">
                <h2>Holidays</h2>
                <div class="d-flex align-items-center">
                    <datetime />
                </div>
            </div>
        </div>
        <hr class="mt-0 mb-3">

        <div class="row mt-3">

            <div class="col-lg-3"></div>

            <div class="col-lg-9 d-flex justify-content-end align-items-center">
                <button class="btn btn-secondary ob_ot" @click="add_holiday_btn">
                    <font-awesome-icon :icon="['fas', 'circle-plus']" class="me-2" />
                    Add holiday
                </button>
            </div>
        </div>
        <!-- DataTable -->
        <div class="card p-4 mt-3">
            <!-- <DataTable v-if="leaveRequests.length" :key="datatableKey"
                class="table table-striped table-bordered display custom-table" :columns="columns" :data="leaveRequests"
                :options="datatableOptions" /> -->

            <DataTable :key="datatableKey" class="table table-striped table-bordered display custom-table"
                :columns="columns" :data="holidays" :options="datatableOptions" />

        </div>

    </div>

    <add_holiday_modal :isVisible="is_add_holiday_modal" :user="user" :holidaySet="holidaySet"
        @close="closeAddHolidayModal" @saved="onHolidaySaved" />

    <view_edit_holiday :isVisible="is_holiday_modal" :user="user" :holiday="selectedHoliday" :mode="holidayModalMode"
        :holidaySet="holidaySet" @close="closeHolidayModal" @saved="onHolidaySaved" />


</template>

<script>
import 'datatables.net-bs5';
import 'datatables.net-bs5/css/dataTables.bootstrap5.min.css';
import DataTable from 'datatables.net-vue3';
import DataTablesLib from 'datatables.net';
import datetime from '@/components/datetime.vue';
import { getUserData } from '@/utils/get_user_data'
import API_BASE from '@/utils/api_config';
import { holiday_status_colors } from '@/utils/badge_colors';
import add_holiday_modal from '@/components/modals/add_holiday_modal.vue';
import view_edit_holiday from '@/components/modals/view_edit_holiday.vue';


DataTable.use(DataTablesLib);

export default {
    props: ["status", "job_title", "isVisible"],
    components: {
        datetime,
        DataTable,
        add_holiday_modal,
        view_edit_holiday
    },

    data() {
        return {
            user: getUserData() || {},
            datatableKey: 0,
            is_add_holiday_modal: false,
            holidays: [],
            holidaySet: new Set(),

            is_holiday_modal: false,
            selectedHoliday: null,
            holidayModalMode: "view",

            columns: [
                { title: 'ID', data: 'id' },
                { title: 'Holiday Name', data: 'holiday_name' },
                { title: 'Holiday Date <span class="text-muted" style="font-size:12px;">(MM-DD)</span>', data: 'holiday_date',},
                {
                    title: 'Status', data: 'status',
                    render: function (data) {
                        const statusClass = holiday_status_colors[data] || 'badge bg-secondary text-white fw-normal';
                        return `<span class="${statusClass}">${data}</span>`;
                    }
                },
                {
                    title: 'Action',
                    data: null,
                    orderable: false,
                    searchable: false,
                    render: (row) => {
                        return `
                            <button class="btn btn-secondary btn-sm view-holiday" style="font-size:12px" data-id="${row.id}">
                            <i class="fas fa-eye"></i>&nbsp;View
                            </button>

                            <button class="btn btn-warning btn-sm edit-holiday" style="font-size:12px" data-id="${row.id}">
                            <i class="fas fa-pen-to-square"></i>&nbsp;Edit
                            </button>
                        
                        `;
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
        add_holiday_btn() {
            this.is_add_holiday_modal = true;
        },
        closeAddHolidayModal() {
            this.is_add_holiday_modal = false;
        },
        onHolidaySaved() {
            this.fetchHolidays();
            this.datatableKey++;
        },

        fetchHolidays() {
            fetch(`${API_BASE}/holidays_list`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({})
            })
                .then(res => res.json())
                .then(data => {
                    if (!data.success) throw new Error(data.error || "Failed to fetch holidays");

                    this.holidays = data.holidays || [];

                    this.datatableKey++;
                })
                .catch(err => {
                    console.error(err);
                    this.holidays = [];
                    this.holidaySet = new Set();
                    this.datatableKey++;
                });
        },

        openHolidayModal(id, mode) {
            const found = this.holidays.find(h => Number(h.id) === Number(id));
            this.selectedHoliday = found ? { ...found } : null; // clone para safe sa edit
            this.holidayModalMode = mode;
            this.is_holiday_modal = true;
        },

        closeHolidayModal() {
            this.is_holiday_modal = false;
            this.selectedHoliday = null;
            this.holidayModalMode = "view";
        },

        onHolidaySaved() {
            this.fetchHolidays();
            this.datatableKey++;
            this.closeHolidayModal();
        },

    },

    mounted() {
        this.fetchHolidays();

        this.$nextTick(() => {
            $(document).off("click", ".view-holiday");
            $(document).off("click", ".edit-holiday");

            $(document).on("click", ".view-holiday", (event) => {
                const id = $(event.currentTarget).data("id");
                this.openHolidayModal(id, "view");
            });

            $(document).on("click", ".edit-holiday", (event) => {
                const id = $(event.currentTarget).data("id");
                this.openHolidayModal(id, "edit");
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

.ob_ot {
    background-color: #dca95e !important;
}

.ob_ot:hover,
.ob_ot:focus {
    background-color: #c7913f !important;
}
</style>
