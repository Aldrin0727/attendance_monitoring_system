<template>
    <div>
        <!-- Header -->
        <div class="row">
            <div class="col-lg-12 d-flex justify-content-between align-items-center">
                <h2>OB/OT Lists</h2>
                <datetime />
            </div>
        </div>
        <hr class="mt-0 mb-3">

        <!-- Top Row -->
        <div class="row mt-3">

            <div class="col-lg-3"></div>

            <div class="col-lg-9 d-flex justify-content-end align-items-center">
                <button class="btn btn-secondary ob_ot" @click="file_leave_btn">
                    <font-awesome-icon :icon="['fas', 'circle-plus']" class="me-2" />
                    File an OT/OB
                </button>
            </div>
        </div>

        <!-- DataTable -->
        <div class="card p-4 mt-3">
            <DataTable v-if="ob_ot_Requests.length" :key="datatableKey"
                class="table table-striped table-bordered display custom-table" :columns="columns"
                :data="ob_ot_Requests" :options="datatableOptions" />
        </div>
    </div>

    <!-- File OB/OT Modal -->
    <file_ob_ot v-if="is_file_ob_ot_modal_visible" :isVisible="is_file_ob_ot_modal_visible"
        @close="close_file_ob_ot_modal" />

    <!-- Approval Modal -->
    <ob_ot_approval v-if="is_modal_visible" :isVisible="is_modal_visible" :ob_ot_Request="selectedRequestOBOT"
        @close="closeModal" @updateDataTable="fetchUserOBOTRequests" />
</template>

<script>
import DataTable from 'datatables.net-vue3';
import DataTablesLib from 'datatables.net';
import datetime from '@/components/datetime.vue';
import { getUserData } from '@/utils/get_user_data';
import API_BASE from '@/utils/api_config';
import { statusColors, ob_ot_Colors } from '@/utils/badge_colors';
import file_ob_ot from '@/components/modals/file_ob_ot.vue';
import ob_ot_approval from '@/components/modals/ob_ot_approval.vue';

DataTable.use(DataTablesLib);

export default {
    props: ["status", "job_title"],
    components: {
        datetime,
        DataTable,
        file_ob_ot,
        ob_ot_approval
    },

    data() {
        return {
            user: getUserData() || {},

            ob_ot_Requests: [],
            datatableKey: 0,

            is_file_ob_ot_modal_visible: false,
            is_modal_visible: false,

            selectedStatus: "",
            selectedRequestOBOT: null,

            columns: [
                { title: "Employee ID", data: "emp_id" },
                { title: "Employee Name", data: "fullName" },
                {
                    title: "Type",
                    data: "type",
                    render(data) {
                        const statusClass = ob_ot_Colors[data] || "badge bg-secondary";
                        return `<span class="${statusClass}">${data}</span>`;
                    }
                },
                {
                    title: "Category",
                    data: "category",
                    render(data) {
                        const statusClass = ob_ot_Colors[data] || "badge bg-secondary";
                        return `<span class="${statusClass}">${data}</span>`;
                    }
                },
                {
                    title: "Requested Date From",
                    data: "req_from",
                    render(data) {
                        return data ? new Date(data).toISOString().slice(0, 10) : "";
                    }
                },
                {
                    title: "Requested Date To",
                    data: "req_to",
                    render(data) {
                        return data ? new Date(data).toISOString().slice(0, 10) : "";
                    }
                },
                {
                    title: "Status",
                    data: "status",
                    render(data) {
                        const statusClass = statusColors[data] || "badge bg-secondary";
                        return `<span class="${statusClass}">${data}</span>`;
                    }
                },
                {
                    title: "Action",
                    data: null,
                    render(row) {
                        return `
        <button class="btn btn-secondary btn-sm view-ob_ot-req" 
            data-id="${row.otob_id}">
            <i class="fas fa-eye"></i> View
        </button>`;
                    }

                }
            ],

            datatableOptions: {
                paging: true,
                searching: true,
                ordering: true,
                responsive: true,
                order: [[4, "desc"]], // sort by date_from
            }
        };
    },

    mounted() {
        this.fetchUserOBOTRequests();

        // bind click event for buttons created by DataTables
        this.$nextTick(() => {
            $(document).on("click", ".view-ob_ot-req", (event) => {
                const id = $(event.currentTarget).data("id");
                this.openModal(id);
            });
        });
    },

    methods: {
        file_leave_btn() {
            this.is_file_ob_ot_modal_visible = true;
        },

        close_file_ob_ot_modal() {
            this.is_file_ob_ot_modal_visible = false;
        },

        closeModal() {
            this.is_modal_visible = false;
        },

        fetchUserOBOTRequests() {
            const payload = {
                status: this.selectedStatus || this.status || "",
                job_title: this.job_title || "",
                department: this.user.dept_code,
                emp_id: this.user.emp_id,
            };

            fetch(`${API_BASE}/get_otob_for_approval`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            })
                .then((res) => res.json())
                .then((data) => {
                    this.ob_ot_Requests = data.forapp_list || [];
                    // console.log(data)
                    this.datatableKey++;
                })
                .catch((err) => console.error("Error fetching OB/OT list:", err));
        },

        openModal(id) {
            const selectedOBOT = this.ob_ot_Requests.find(req => req.otob_id == id);
            this.selectedRequestOBOT = selectedOBOT;

            // console.log("Selected OB/OT:", selectedOBOT);

            this.is_modal_visible = true;
        }


    }
};
</script>

<style>
@import url(../../public/global.css);
@import url(../assets/css/dataTable.css);
@import url(../assets/css/buttons.css);
@import url(../assets/css/modal.css);

.ob_ot {
    background-color: #df7a8a !important;
}

.ob_ot:hover,
.ob_ot:focus {
    background-color: #5ac5c5 !important;
}
</style>
