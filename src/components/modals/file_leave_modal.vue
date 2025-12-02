<template>
    <div class="modal" v-if="isVisible">
        <div class="modal-dialog">
            <div class="modal-content">
                <!-- Modal Header -->
                <div class="modal-header py-1">
                    <font-awesome-icon :icon="['fas', 'circle-plus']" class="font-awesome-icon" />
                    <h5 class="modal-title">Leave Request Form</h5>
                    <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
                </div>

                <!-- Form -->
                <form @submit.prevent="submitForm">
                    <div class="modal-body">
                        <!-- User Information -->
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
                                    <label for="user" class="form-label label-sm">Position</label>
                                    <input type="text" id="user" class="form-control" v-model="user.position"
                                        readonly />
                                </div>
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">department</label>
                                    <input type="text" id="department" class="form-control"
                                        v-model="user.department_name" readonly />
                                </div>
                            </div>
                            <div class="row mb-1">
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Address</label>
                                    <input type="text" id="user" class="form-control" v-model="user.address" readonly />
                                </div>
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Contact Number</label>
                                    <input type="text" id="user" class="form-control" v-model="user.contact" readonly />
                                </div>
                            </div>
                        </div>

                        <!-- Leave Credits -->
                        <div class="section">
                            <div class="section-title">Leave Request</div>
                            <hr class="mt-0">

                            <div class="row">
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
                                    <input type="text" class="form-control leave_days"
                                        :value="leaveForm.total_leave_days" readonly />
                                </div>

                            </div>

                            <div class="row mb-3">
                                <div class="col-6">
                                    <label for="date_from" class="form-label label-sm">
                                        Date of Leave From <strong style="color: red">*</strong>
                                    </label>
                                    <input type="date" id="date_from" class="form-control"
                                        v-model="leaveForm.date_from" required />
                                </div>
                                <div class="col-6">
                                    <label for="date_to" class="form-label label-sm">
                                        Date of Leave To <strong style="color: red">*</strong>
                                    </label>
                                    <input type="date" id="date_to" class="form-control"
                                        v-model="leaveForm.date_to" required />
                                </div>
                            </div>

                            <div class="row mb-3">
                                <div class="col-12">
                                    <label for="leave_reason" class="form-label label-sm">
                                        Reason for leave <strong style="color: red">*</strong>
                                    </label>
                                    <textarea class="form-control" rows="2" id="leave_reason"
                                        v-model="leaveForm.leave_reason" required></textarea>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Modal Footer -->
                    <div class="modal-footer mt-2">
                        <button type="submit" class="btn btn-success">Submit</button>
                        <button type="button" class="btn btn-info" @click="closeModal">Close</button>
                    </div>
                </form>

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
            },
            leave_reason: "",
        };
    },
    computed: {
        fullName() {
            return `${this.user.first_name} ${this.user.last_name}`.trim();
        },
    },
    mounted() {

    },

    watch: {
        'leaveForm.date_from': 'calculateTotalLeaveDays',
        'leaveForm.date_to': 'calculateTotalLeaveDays',
        'leaveForm.half_day': 'calculateTotalLeaveDays',
    },

    methods: {
        // formatDateTime(value) {
        //     if (!value) return null;

        //     const iso = String(value);

        //     const parts = iso.split('T');
        //     const date = parts[0] || null;
        //     const timePart = parts[1] || '';

        //     if (!date) return null;

        //     const timePieces = timePart.split(':'); 
        //     const hh = timePieces[0] || '00';
        //     const mm = timePieces[1] || '00';

        //     return `${date} ${hh}:${mm}:00`;
        // },

        closeModal() {
            // reset fields
            this.selectedTypeofLeave = "";
            this.leaveForm.date_from = "";
            this.leaveForm.date_to = "";
            this.leaveForm.total_leave_days = "";
            this.leaveForm.leave_reason = "";

            this.$emit("close");
        },

        calculateTotalLeaveDays() {
            const from = this.leaveForm.date_from;
            const to = this.leaveForm.date_to;
            const halfDay = this.leaveForm.half_day;

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

            const msPerDay = 1000 * 60 * 60 * 24;
            const startDate = new Date(start.getFullYear(), start.getMonth(), start.getDate());
            const endDate = new Date(end.getFullYear(), end.getMonth(), end.getDate());

            let diffDays = Math.floor((endDate - startDate) / msPerDay) + 1;

            // apply half-day rule
            if (halfDay) {
                // if both dates are the same
                if (diffDays === 1) {
                    diffDays = 0.5;
                } else {
                    diffDays = diffDays - 0.5;
                }
            }

            this.leaveForm.total_leave_days = diffDays;
        },


        submitForm() {
            // console.log({
            //     type_of_leave: this.selectedTypeofLeave,
            //     ...this.leaveForm,
            //     ...this.user,
            // });

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
                department_name: this.user.dept_code
            };

            console.log(formData)

            fetch(`${API_BASE}/create_leave`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            })
                .then(response => response.json())
                .then(data => {
                    // console.log(data)
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

            // after successful submit, close modal
            this.closeModal();
        },
    },
};
</script>




<style scoped>
@import url(../../assets/css/modal.css);
@import url(../../assets/css/buttons.css);
@import url(../../assets/css/swal.css);

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
