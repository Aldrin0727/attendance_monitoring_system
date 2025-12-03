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
<<<<<<< HEAD
                                    <label class="form-label label-sm">Half Day? <strong style="color: red">*</strong></label>
=======
                                    <label class="form-label label-sm">Half Day? <strong
                                            style="color: red">*</strong></label>
>>>>>>> origin/lj_branch
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
<<<<<<< HEAD
                                    <input type="date" id="date_from" class="form-control"
                                        v-model="leaveForm.date_from" required />
=======
                                    <input type="date" id="date_from" class="form-control" v-model="leaveForm.date_from"
                                        required />
>>>>>>> origin/lj_branch
                                </div>
                                <div class="col-6">
                                    <label for="date_to" class="form-label label-sm">
                                        Date of Leave To <strong style="color: red">*</strong>
                                    </label>
<<<<<<< HEAD
                                    <input type="date" id="date_to" class="form-control"
                                        v-model="leaveForm.date_to" required />
=======
                                    <input type="date" id="date_to" class="form-control" v-model="leaveForm.date_to"
                                        required />
>>>>>>> origin/lj_branch
                                </div>
                            </div>

                            <div class="row mb-1">
                                <div class="col-12">
                                    <label for="leave_reason" class="form-label label-sm">
                                        Reason for leave <strong style="color: red">*</strong>
                                    </label>
<<<<<<< HEAD
                                    <textarea class="form-control" rows="2" id="leave_reason"
=======
                                    <textarea class="form-control" rows="1" id="leave_reason"
>>>>>>> origin/lj_branch
                                        v-model="leaveForm.leave_reason" required></textarea>
                                </div>
                            </div>
                        </div>

                         <!-- approver
                        <div class="section">
                            <div class="section-title">APPROVER AND STATUS OF LEAVE</div>
                            <hr class="mt-0">
                            <div class="row">
                                <div class="col-6">
                                    <label for="approver" class="form-label label-sm">Approver</label>
                                    <input type="text" id="approver" class="form-control" v-model="leaveForm.approver" readonly />
                                </div>
                                <div class="col-6">
                                    <label for="leave_status" class="form-label label-sm">Leave Status</label>
                                    <input type="text" id="leave_status" class="form-control" v-model="leaveForm.status" readonly />
                                </div>
                            </div>
                        </div> -->
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
<<<<<<< HEAD
=======
                approver: "", 
                status: "",
>>>>>>> origin/lj_branch
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
<<<<<<< HEAD

=======
        // this.fetchDepartmentHead();
>>>>>>> origin/lj_branch
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

<<<<<<< HEAD
=======
       



>>>>>>> origin/lj_branch
        closeModal() {
            // reset fields
            this.selectedTypeofLeave = "";
            this.leaveForm.date_from = "";
            this.leaveForm.date_to = "";
            this.leaveForm.total_leave_days = "";
            this.leaveForm.leave_reason = "";
<<<<<<< HEAD
=======
            this.leaveForm.approver = ""; 
            this.leaveForm.status = ""; 
>>>>>>> origin/lj_branch

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
<<<<<<< HEAD
                const start = new Date(this.leaveForm.date_from); 
=======
                const start = new Date(this.leaveForm.date_from);
>>>>>>> origin/lj_branch
                const now = new Date();

                const startDay = new Date(start.getFullYear(), start.getMonth(), start.getDate());
                const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

                if (startDay.getTime() === today.getTime()) {
                    Swal.fire(
                        "Not allowed",
                        "Vacation Leave (VL) cannot be filed for today. Please choose a future date.",
                        "warning"
                    );
<<<<<<< HEAD
                    return; 
=======
                    return;
>>>>>>> origin/lj_branch
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

<<<<<<< HEAD
            console.log(formData)
=======
            // console.log(formData)
>>>>>>> origin/lj_branch

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
<<<<<<< HEAD
                         Swal.fire("Success", "Leave filed successfully", "success");
                        
=======
                        Swal.fire("Success", "Leave filed successfully", "success");

>>>>>>> origin/lj_branch
                    } else {
                        Swal.fire("Error", data.error || "Failed to submit leave", "error");
                    }
                })
                .catch(error => {
                    console.error("Error submitting form:", error);
                    Swal.fire("Error", "Something went wrong", "error");
                });
<<<<<<< HEAD
=======

>>>>>>> origin/lj_branch

            // after successful submit, close modal
            this.closeModal();
        },
    },
//      fetchDepartmentHead() {
//             console.log(this.user.dept_code)
//             fetch(`${API_BASE}/get_depthead`, {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                 },
//                 body: JSON.stringify({ department: this.user.dept_code }),
//             })
//                 .then(response => response.json())
//                 .then(data => {
//                     console.log(data)
//                     if (data.success) {

//                         if (data.all_list && data.all_list.length > 0) {

//                             this.leaveForm.approver = data.all_list[1].fullName;
//                         } else {
//                             console.error('No department head found for the given department');
//                         }
//                     } else {
//                         console.error('Error fetching department head');
//                     }
//                 })
//                 .catch(error => {
//                     console.error('Error fetching department head:', error);
//                 });
// },

};
</script>




<style scoped>
@import url(../../assets/css/modal.css);
@import url(../../assets/css/buttons.css);
@import url(../../assets/css/swal.css);
<<<<<<< HEAD
<<<<<<< HEAD
=======
@import url(../../../public/global.css);
>>>>>>> origin/lj_branch
=======
>>>>>>> d442d2c3b064e9b3f1318ac7f55b2acca7468f5a

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
