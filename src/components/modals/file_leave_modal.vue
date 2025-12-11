<template>
    <div>
        <!-- Modal Content -->
        <div class="modal" v-if="isVisible">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header py-1">
                        <font-awesome-icon :icon="['fas', 'circle-plus']" class="font-awesome-icon" />
                        <h5 class="modal-title">Leave Request Form</h5>
                        <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
                    </div>

                    <form @submit.prevent="submitForm">
                        <div class="modal-body pb-0">
                            <!-- User Information Section -->
                            <div class="section">
                                <div class="section-title">User Information</div>
                                <hr class="mt-0">
                                <div class="row">
                                    <div class="col-12 mb-3">
                                        <label for="user" class="form-label label-sm">USER</label>
                                        <input type="text" id="user" class="form-control" v-model="fullName" readonly />
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-6">
                                        <label for="position" class="form-label label-sm">Position</label>
                                        <input type="text" id="position" class="form-control" v-model="user.position" readonly />
                                    </div>
                                    <div class="col-6">
                                        <label for="department" class="form-label label-sm">Department</label>
                                        <input type="text" id="department" class="form-control" v-model="user.department_name" readonly />
                                    </div>
                                </div>
                                <div class="row mb-1">
                                    <div class="col-6">
                                        <label for="address" class="form-label label-sm">Address</label>
                                        <input type="text" id="address" class="form-control" v-model="user.address" readonly />
                                    </div>
                                    <div class="col-6">
                                        <label for="contact" class="form-label label-sm">Contact Number</label>
                                        <input type="text" id="contact" class="form-control" v-model="user.contact" readonly />
                                    </div>
                                </div>
                            </div>

                            <!-- Leave Request Section -->
                            <div class="section">
                                <div class="section-title">Leave Request</div>
                                <hr class="mt-0">

                                <div class="row mb-0">
                                    <div class="col-6 mb-3">
                                        <label class="form-label label-sm">
                                            Type of Leave <strong style="color: red">*</strong>
                                        </label>
                                        <select v-model="selectedTypeofLeave" class="form-select" required>
                                            <option disabled value="">Select Type of Leave</option>
                                            <option value="SL">Sick Leave</option>
                                            <option value="VL">Vacation Leave</option>
                                            <option value="EL">Emergency Leave</option>
                                        </select>
                                    </div>

                                    <div class="col-4">
                                        <label class="form-label label-sm">Half Day? <strong style="color: red">*</strong></label>
                                        <select v-model="leaveForm.half_day" class="form-select">
                                            <option value="">No</option>
                                            <option value="morning">Yes - Morning</option>
                                            <option value="afternoon">Yes - Afternoon</option>
                                        </select>
                                    </div>

                                    <div class="col-2">
                                        <label class="form-label label-sm">Total Days</label>
                                        <input type="text" class="form-control leave_days" :value="leaveForm.total_leave_days" readonly />
                                    </div>
                                </div>

                                <!-- Date Selection Section -->
                                <div class="row mb-3">
                                    <div class="col-6">
                                        <label for="date_from" class="form-label label-sm">
                                            Date of Leave From <strong style="color: red">*</strong>
                                        </label>
                                        <input type="date" id="date_from" class="form-control" v-model="leaveForm.date_from" required />
                                    </div>
                                    <div class="col-6">
                                        <label for="date_to" class="form-label label-sm">
                                            Date of Leave To <strong style="color: red">*</strong>
                                        </label>
                                        <input type="date" id="date_to" class="form-control" v-model="leaveForm.date_to" required />
                                    </div>
                                </div>

                                <div class="row mb-1">
                                    <div class="col-12">
                                        <label for="leave_reason" class="form-label label-sm">
                                            Reason for leave <strong style="color: red">*</strong>
                                        </label>
                                        <textarea class="form-control" rows="1" id="leave_reason" v-model="leaveForm.leave_reason" required></textarea>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Modal Footer -->
                        <div class="modal-footer m-0">
                            <button type="submit" class="btn btn-success">Submit</button>
                            <button type="button" class="btn btn-info" @click="closeModal">Close</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import API_BASE from '@/utils/api_config';
import { getUserData } from '@/utils/get_user_data';

export default {
    props: {
        isVisible: {
            type: Boolean,
            required: true
        }
    },
    data() {
        return {
            user: getUserData() || {},
            selectedTypeofLeave: "",
            leaveForm: {
                date_from: "",
                date_to: "",
                total_leave_days: "",
                leave_reason: "",
                half_day: "",
                approver: "", 
                status: "",
            },
        };
    },
    computed: {
        fullName() {
            return `${this.user.first_name} ${this.user.last_name}`.trim();
        },
    },
    watch: {
        'leaveForm.date_from': 'calculateTotalLeaveDays',
        'leaveForm.date_to': 'calculateTotalLeaveDays',
        'leaveForm.half_day': 'calculateTotalLeaveDays',
    },
    methods: {
        closeModal() {
            // reset fields
            this.selectedTypeofLeave = "";
            this.leaveForm.date_from = "";
            this.leaveForm.date_to = "";
            this.leaveForm.total_leave_days = "";
            this.leaveForm.leave_reason = "";
            this.leaveForm.approver = ""; 
            this.leaveForm.status = ""; 

            this.$emit("close");
        },

calculateTotalLeaveDays() {
    const from = this.leaveForm.date_from;
    const to = this.leaveForm.date_to;
    const halfDay = this.leaveForm.half_day;

    // Ensure the date_to is the same as date_from for half-day
    if (halfDay && from !== to) {
        this.leaveForm.date_to = from; // Force date_to to be the same as date_from
    }

    if (!from || !to) {
        this.leaveForm.total_leave_days = '';
        return;
    }

    const start = new Date(from);
    const end = new Date(to);

    if (isNaN(start) || isNaN(end) || end < start) {
        this.leaveForm.total_leave_days = '';
        return;
    }

    // Convert dates to the beginning of the day to avoid time issues
    const msPerDay = 1000 * 60 * 60 * 24;
    const startDate = new Date(start.getFullYear(), start.getMonth(), start.getDate());
    const endDate = new Date(end.getFullYear(), end.getMonth(), end.getDate());

    let diffDays = Math.floor((endDate - startDate) / msPerDay) + 1;

    // Exclude weekends (Saturday and Sunday)
    let weekendCount = 0;
    for (let current = new Date(startDate); current <= endDate; current.setDate(current.getDate() + 1)) {
        const dayOfWeek = current.getDay(); // 0 is Sunday, 6 is Saturday
        if (dayOfWeek === 0 || dayOfWeek === 6) {
            weekendCount++;
        }
    }

    diffDays -= weekendCount; // Subtract weekends from the total days

    // Apply half-day rule
    if (halfDay) {
        if (diffDays === 1) {
            diffDays = 0.5; // If only one day, it's a half-day leave
        } else {
            diffDays -= 0.5; // Otherwise, subtract half a day
        }
    }

    this.leaveForm.total_leave_days = diffDays;
},


        submitForm() {
            // Ensure the user cannot submit with incorrect dates
            if (this.selectedTypeofLeave === 'VL') {
                const start = new Date(this.leaveForm.date_from);
                const now = new Date();

                const startDay = new Date(start.getFullYear(), start.getMonth(), start.getDate());
                const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

                if (startDay.getTime() === today.getTime()) {
                    Swal.fire(
                        "Not allowed",
                        "Vacation Leave (VL) cannot be filed for today. Please choose a future date.",
                        "warning"
                    );
                    return;
                }
            }

            const formData = {
                selectedTypeofLeave: this.selectedTypeofLeave,
                fullName: this.fullName,
                total_leave_days: this.leaveForm.total_leave_days,
                date_from: this.leaveForm.date_from,
                date_to: this.leaveForm.date_to,
                leave_reason: this.leaveForm.leave_reason,
                department_name: this.user.dept_code,
                emp_id: this.user.emp_id,
            };

            fetch(`${API_BASE}/create_leave`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire("Success", "Leave filed successfully", "success");

                    } else {
                        Swal.fire("Error", data.error || "Failed to submit leave", "error");
                    }
                })
                .catch(error => {
                    console.error("Error submitting form:", error);
                    Swal.fire("Error", "Something went wrong", "error");
                });

            this.closeModal();
        }
    }
};
</script>

<style scoped>
@import url(../../assets/css/modal.css);
@import url(../../assets/css/buttons.css);
@import url(../../assets/css/swal.css);
@import url(../../../public/global.css);

.font-awesome-icon {
    color: #df7a8a !important;
    width: 20px;
    height: 45px;
    margin-right: 10px;
}

.label-sm {
    text-transform: uppercase;
}

input:focus {
    background-color: #e9ecef;
}

.modal-title {
    color: #699dc8
}

.form-control,
.form-select {
    color: #333 !important;
    background-color: #e9ecef !important;
}

.leave_days {
    background-color: #b3cadc !important;
    border: #fff !important;
}

#leave_reason:focus {
    background-color: #fff !important;
    font-size: 12px !important;
}
</style>
