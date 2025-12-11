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
                        <div class="col-7">
                            <input type="datetime-local" id="time_in" class="form-control" v-model="time_in"
                                :max="maxDate" required />
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
                        <div class="col-7">
                            <input type="datetime-local" id="time_out" class="form-control" v-model="time_out"
                                :max="maxDate" required />
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
import { attendance_Colors } from '@/utils/badge_colors';

DataTable.use(DataTablesLib);

export default {
    components: {
        datetime,
        DataTable
    },
    data() {
        return {
            user: getUserData() || {},
            time_in: '',
            time_out: '',
            maxDate: this.getMaxDate(),
            attendanceList: [],
            datatableKey: 0,
            columns: [
                { title: 'Employee ID', data: 'emp_id' },
                { title: 'Name', data: 'full_name' },
                {
                    title: 'Time In', data: 'time_in',
                    render: function (data) {
                        return data ? new Date(data).toISOString().slice(0, 19).replace("T", " ") : '';
                    }
                },
                {
                    title: 'Time Out', data: 'time_out',
                    render: function (data) {
                        return data ? new Date(data).toISOString().slice(0, 19).replace("T", " ") : '';
                    }
                },
                { title: 'Hours Worked', data: 'work_hours' },
           {
                    title: 'Remarks',
                    data: 'remarks',
                    render: function (data) {
                        if (!data) return "";

                        // Split by comma, trim spaces
                        const parts = data.split(",").map(r => r.trim());

                        // Generate multiple badges
                        return parts.map(r => {
                            const statusClass = attendance_Colors[r] || 'badge bg-secondary text-white fw-normal';
                            return `<span class="${statusClass}" style="margin-right:4px;">${r}</span>`;
                        }).join(" ");
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
    mounted() {
        this.fetchUserAttendnce();
    },
    methods: {
        fetchUserAttendnce() {
            const payload = {
                emp_id: this.user.emp_id || '',
            };
            fetch(`${API_BASE}/check_attendance_by_emp`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            })
                .then(response => response.json())
                .then(data => {
                    this.attendanceList = data.alllist || [];
                    this.datatableKey++;
                })
                .catch(error => {
                    console.error("Error fetching attendance data:", error);
                });
        },

        getMaxDate() {
            const today = new Date();
            const year = today.getFullYear();
            const month = (today.getMonth() + 1).toString().padStart(2, '0');
            const day = today.getDate().toString().padStart(2, '0');
            const hours = today.getHours().toString().padStart(2, '0');
            const minutes = today.getMinutes().toString().padStart(2, '0');
            const seconds = today.getSeconds().toString().padStart(2, '0');
            return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
        },

        markTimeIn() {
            if (!this.time_in) {
                Swal.fire("Warning", "Please select a valid Time In.", "warning");
                return;
            }
            const date = new Date(this.time_in);
            const formattedTimeIn = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`;

            const payload = {
                emp_id: this.user.emp_id,
                fullName: `${this.user.first_name} ${this.user.last_name}`,
                time_in: formattedTimeIn,
                args: 'TIME IN',
            };

            fetch(`${API_BASE}/time_check`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire("Success", "Time IN marked successfully", "success");
                        this.time_in = ''
                        this.fetchUserAttendnce();
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
            if (!this.time_out) {
                Swal.fire("Warning", "Please select a valid Time Out.", "warning");
                return;
            }

            // Get the selected Time Out date and format it as YYYY-MM-DD HH:mm:ss
            const timeOutDate = new Date(this.time_out);
            const formattedTimeOut = `${timeOutDate.getFullYear()}-${(timeOutDate.getMonth() + 1).toString().padStart(2, '0')}-${timeOutDate.getDate().toString().padStart(2, '0')} ${timeOutDate.getHours().toString().padStart(2, '0')}:${timeOutDate.getMinutes().toString().padStart(2, '0')}:${timeOutDate.getSeconds().toString().padStart(2, '0')}`;

            // Extract the date portion (YYYY-MM-DD) from the Time Out
            const timeOutDateOnly = formattedTimeOut.slice(0, 10);  // "YYYY-MM-DD"
            console.log('Time Out Date Only:', timeOutDateOnly);  // Log the formatted Time Out date for debugging

            // Log the attendanceList to check its structure
            console.log('Attendance List:', this.attendanceList);

            // Check if a Time In has already been marked for the same date
            const timeInRecord = this.attendanceList.find(item => {
                if (item.time_in) {
                    // Parse the time_in string into a Date object
                    const timeInDate = new Date(item.time_in);
                    // Format the date portion as YYYY-MM-DD
                    const timeInDateOnly = `${timeInDate.getFullYear()}-${(timeInDate.getMonth() + 1).toString().padStart(2, '0')}-${timeInDate.getDate().toString().padStart(2, '0')}`;
                    return timeInDateOnly === timeOutDateOnly;
                }
                return false;
            });

            console.log('Time In Record:', timeInRecord);  // Log the found Time In record for debugging

            if (!timeInRecord) {
                Swal.fire("Error", "You must mark Time In first before Time Out.", "error");
                return;
            }

            const payload = {
                emp_id: this.user.emp_id,
                fullName: `${this.user.first_name} ${this.user.last_name}`,
                time_in: '', // No need to send time_in for this request
                time_out: formattedTimeOut,
                args: 'TIME OUT'
            };

            fetch(`${API_BASE}/time_check`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire("Success", "Time OUT marked successfully", "success");
                        this.fetchUserAttendnce();  // Re-fetch attendance data to update the table
                        this.time_out = ''
                    } else {
                        Swal.fire("Error", data.error || "Failed to submit attendance", "error");
                    }
                })
                .catch(error => {
                    console.error("Error submitting attendance:", error);
                    Swal.fire("Error", "Something went wrong", "error");
                });
        }





    }
}
</script>


<style scoped>
@import url(../../public/global.css);
@import url(../assets/css/dataTable.css);
@import url(../assets/css/buttons.css);
@import url(../assets/css/modal.css);
</style>
