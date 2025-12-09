<template>
    <div>
        <!-- Header -->
        <div class="row">
            <!-- Dashboard Header -->
            <div class="col-lg-12 d-flex justify-content-between align-items-center">
                <h2>Attendance</h2>
                <div class="d-flex align-items-center">
                    <datetime />
                </div>
            </div>
        </div>
        <hr class="mt-0 mb-3">

        <!-- Attendance Form -->
       
       
            <div class="row">
                  <div class="col-lg-4">
                  <div class="section">
                    <div class="row">
                        <!-- <label for="time_in" class="form-label label-sm">
                            Time In <strong style="color: red">*</strong>
                        </label> -->
                        <div class="col-7">
                            <input type="datetime-local" id="time_in" class="form-control" v-model="timeIn" required />
                        </div>
                        <div class="col-5">

                            <button class="btn btn-secondary w-100" @click="markTimeIn">
                                Mark Time In
                            </button>

                        </div>
                    </div>
                </div>
              </div>
                <div class="col-lg-4">
                  <div class="section">
                    <div class="row">
                        <!-- <label for="time_in" class="form-label label-sm">
                            Time In <strong style="color: red">*</strong>
                        </label> -->
                        <div class="col-7">
                            <input type="datetime-local" id="time_in" class="form-control" v-model="timeIn" required />
                        </div>
                        <div class="col-5">

                            <button class="btn btn-danger w-100" @click="markTimeOut">
                                Mark Time Out
                            </button>

                        </div>
                    </div>
                </div>
              </div>
            </div>
          
       

        <!-- Attendance Table -->
        <div class="card p-4 mt-3">
            <DataTable :key="datatableKey" class="table table-striped table-bordered display custom-table"
                :columns="columns" :data="attendanceList" :options="datatableOptions" />
        </div>
    </div>
</template>

<script>
import 'datatables.net-bs5';
import 'datatables.net-bs5/css/dataTables.bootstrap5.min.css';
import DataTable from 'datatables.net-vue3';
import DataTablesLib from 'datatables.net';
import datetime from '@/components/datetime.vue';
import { getUserData } from '@/utils/get_user_data';
import API_BASE from '@/utils/api_config';
import { statusColors } from '@/utils/badge_colors';
import leave_approval from '@/components/modals/leave_approval.vue';

DataTable.use(DataTablesLib);

export default {
    props: ["isVisible"],
    components: {
        datetime,
        DataTable,
        leave_approval
    },
    data() {
        return {
            user: getUserData() || {}, // Assuming the user data includes their name
            timeIn: '',
            timeOut: '',
            attendanceList: [],
            columns: [
                { title: 'Employee ID', data: 'emp_id' },
                { title: 'Name', data: 'fullName' },
                { title: 'Time In', data: 'timeIn' },
                { title: 'Time Out', data: 'timeOut' },
                { title: 'Remarks', data: 'remarks' }
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
        markTimeIn() {
            if (!this.timeIn) {
                Swal.fire("Warning", "Please select a valid Time In.", "warning");
                return;
            }
            const date = new Date(this.timeIn);
            const formattedTimeIn = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`;

            fetch(`${API_BASE}/time_check`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    emp_id: this.user.emp_id,
                    fullName: `${this.user.first_name} ${this.user.last_name}`,
                    time_in: formattedTimeIn,
                    time_out: '',
                    args: 'TIME IN'
                }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log(data)
                        Swal.fire("Success", "Time IN marked successfully", "success");

                    } else {
                        Swal.fire("Error", data.error || "Failed to submit attendance", "error");
                    }
                })
                .catch(error => {
                    console.error("Error submitting attendance:", error);
                    Swal.fire("Error", "Something went wrong", "error");
                });
        },


        markTimeOut() {

        }
    },
    mounted() {

    }
}
</script>

<style scoped>
@import url(../../public/global.css);
@import url(../assets/css/dataTable.css);
@import url(../assets/css/buttons.css);
@import url(../assets/css/modal.css);
</style>
