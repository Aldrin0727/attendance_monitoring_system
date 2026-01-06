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
                                        <input type="text" id="position" class="form-control" v-model="user.position"
                                            readonly />
                                    </div>
                                    <div class="col-6">
                                        <label for="department" class="form-label label-sm">Department</label>
                                        <input type="text" id="department" class="form-control"
                                            v-model="user.department_name" readonly />
                                    </div>
                                </div>
                                <div class="row mb-1">
                                    <div class="col-6">
                                        <label for="address" class="form-label label-sm">Address</label>
                                        <input type="text" id="address" class="form-control" v-model="user.address"
                                            readonly />
                                    </div>
                                    <div class="col-6">
                                        <label for="contact" class="form-label label-sm">Contact Number</label>
                                        <input type="text" id="contact" class="form-control" v-model="user.contact"
                                            readonly />
                                    </div>
                                </div>
                            </div>

                            <!-- Leave Request Section -->
                            <div class="section">
                                <div class="section-title d-flex justify-content-between align-items-center">
                                    <span>Leave Request</span>

                                    <small v-if="selectedTypeofLeave" style="color: #df7a8a">
                                        <i>Remaining {{ getBalanceType(selectedTypeofLeave) }}:
                                            {{ remainingLeaves[getBalanceType(selectedTypeofLeave)] ?? 0 }} day(s)
                                        </i>
                                    </small>
                                </div>

                                <hr class="mt-0">

                                <div class="row">
                                    <div class="col-6">
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

                                    <div class="col-4" v-if="showLeaveDetails">
                                        <label class="form-label label-sm">Half Day? <strong
                                                style="color: red">*</strong></label>
                                        <select v-model="leaveForm.half_day" class="form-select">
                                            <option value="">No</option>
                                            <option value="AM">Yes - Morning</option>
                                            <option value="PM">Yes - Afternoon</option>
                                        </select>
                                    </div>

                                    <div class="col-2" v-if="showLeaveDetails">
                                        <label class="form-label label-sm">Total Days</label>
                                        <input type="text" class="form-control leave_days"
                                            :value="leaveForm.total_leave_days" readonly />
                                    </div>
                                </div>

                                <!-- Date Selection Section -->
                                <div class="row mb-3 mt-3" v-if="showLeaveDetails">
                                    <div class="col-6">
                                        <label for="date_from" class="form-label label-sm">
                                            Date of Leave From <strong style="color: red">*</strong>
                                        </label>
                                        <input type="date" id="date_from" class="form-control"
                                            v-model="leaveForm.date_from" required :max="maxDateForLeave" />
                                    </div>
                                    <div class="col-6">
                                        <label for="date_to" class="form-label label-sm">
                                            Date of Leave To <strong style="color: red">*</strong>
                                        </label>
                                        <input type="date" id="date_to" class="form-control" v-model="leaveForm.date_to"
                                            :max="maxDateForLeave" required />
                                    </div>
                                </div>

                                <div class="row mb-2" v-if="showLeaveDetails">
                                    <div class="col-12">
                                        <label for="leave_reason" class="form-label label-sm">
                                            Reason for leave <strong style="color: red">*</strong>
                                        </label>
                                        <textarea class="form-control" rows="1" id="leave_reason"
                                            v-model="leaveForm.leave_reason" required></textarea>
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
            existingLeaves: [],
            leaveForm: {
                date_from: "",
                date_to: "",
                total_leave_days: "",
                leave_reason: "",
                half_day: "",
                approver: "",
                status: "",
            },
            remainingLeaves: {
                VL: 0,
                SL: 0,
            },
        };
    },
    computed: {
        fullName() {
            return `${this.user.first_name} ${this.user.last_name}`.trim();
        },
        maxDateForLeave() {
            if (this.selectedTypeofLeave === 'SL') {
                const today = new Date();
                const y = today.getFullYear();
                const m = String(today.getMonth() + 1).padStart(2, '0');
                const d = String(today.getDate()).padStart(2, '0');
                return `${y}-${m}-${d}`;
            }
            return null;
        },
         showLeaveDetails() {
            return !!this.selectedTypeofLeave;
        },



    },
    watch: {
        'leaveForm.date_from': 'calculateTotalLeaveDays',
        'leaveForm.date_to': 'calculateTotalLeaveDays',
        'leaveForm.half_day': 'calculateTotalLeaveDays',
    },
    methods: {
        getBalanceType(type) {

            if (type === 'EL') return 'VL';
            return type;
        },
        fetchExistingLeaves() {
            fetch(`${API_BASE}/get_leaves_for_approval_request_date`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    emp_id: this.user.emp_id
                })
            })
                .then(res => res.json())
                .then(data => {
                    // console.log(data)
                    this.existingLeaves = data.alldates || [];

                });
        },
        normalizeDate(d) {
            if (!d) return null;

            const x = new Date(d);

            return new Date(
                Date.UTC(
                    x.getUTCFullYear(),
                    x.getUTCMonth(),
                    x.getUTCDate()
                )
            );
        },
        hasDateConflict(from, to) {
            const newFrom = this.normalizeDate(from);
            const newTo = this.normalizeDate(to);

            return this.existingLeaves.some(lv => {
                // Block ALL except denied
                if (lv.status === "DENIED") return false;

                const oldFrom = this.normalizeDate(lv.leave_from);
                const oldTo = this.normalizeDate(lv.leave_to);

                if (!oldFrom || !oldTo) return false;

                return newFrom <= oldTo && newTo >= oldFrom;
            });
        },


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

            if (!this.selectedTypeofLeave) {
                this.leaveForm.total_leave_days = "";
                return;
            }


            if (!from || !to) {
                this.leaveForm.total_leave_days = '';
                return;
            }

            const start = new Date(from);
            const end = new Date(to);

            const today = new Date();
            const todayOnly = new Date(today.getFullYear(), today.getMonth(), today.getDate());
            const startOnly = new Date(start.getFullYear(), start.getMonth(), start.getDate());

            // revent TO < FROM
            if (end < start) {
                Swal.fire(
                    "Invalid Date Range",
                    "'Date To' cannot be earlier than 'Date From'.",
                    "warning"
                );
                this.leaveForm.date_to = "";
                this.leaveForm.total_leave_days = "";
                return;
            }

            //  SL cannot be future date AND cannot be today
            if (this.selectedTypeofLeave === "SL") {
                if (startOnly.getTime() > todayOnly.getTime()) {
                    Swal.fire(
                        "Not Allowed",
                        "Sick Leave (SL) cannot be filed for future dates.",
                        "warning"
                    );
                    this.leaveForm.date_from = "";
                    this.leaveForm.date_to = "";
                    this.leaveForm.total_leave_days = "";
                    return;
                }

                if (startOnly.getTime() === todayOnly.getTime()) {
                    Swal.fire(
                        "Warning",
                        "You cannot schedule Sick Leave (SL) dated today. SL is only for absences already incurred.",
                        "warning"
                    );
                    this.leaveForm.date_from = "";
                    this.leaveForm.date_to = "";
                    this.leaveForm.total_leave_days = "";
                    return;
                }
            }

            // Enforce half-day rule
            if (halfDay && from !== to) {
                this.leaveForm.date_to = from;
            }

            // Convert dates to start of day
            const msPerDay = 1000 * 60 * 60 * 24;
            const startDate = new Date(start.getFullYear(), start.getMonth(), start.getDate());
            const endDate = new Date(end.getFullYear(), end.getMonth(), end.getDate());

            let diffDays = Math.floor((endDate - startDate) / msPerDay) + 1;


            let weekendCount = 0;
            for (let current = new Date(startDate); current <= endDate; current.setDate(current.getDate() + 1)) {
                const dayOfWeek = current.getDay();
                if (dayOfWeek === 0 || dayOfWeek === 6) weekendCount++;
            }
            diffDays -= weekendCount;


            if (halfDay) {
                diffDays = diffDays <= 1 ? 0.5 : diffDays - 0.5;
            }

            this.leaveForm.total_leave_days = diffDays;




        },


        submitForm() {

            if (!this.leaveForm.total_leave_days || Number(this.leaveForm.total_leave_days) <= 0) {
                Swal.fire("Invalid", "No valid leave days selected (weekends are excluded).", "warning");
                return;
            }

            if (this.hasDateConflict(this.leaveForm.date_from, this.leaveForm.date_to)) {
                Swal.fire(
                    "Not Allowed",
                    "You already have a filed leave that overlaps with the selected dates.",
                    "warning"
                );
                return;
            }

            // -------------------------------
            // LEAVE TYPE DATE RULES
            // -------------------------------
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

            if (this.selectedTypeofLeave === 'SL') {
                const start = new Date(this.leaveForm.date_from);
                const now = new Date();

                const startDay = new Date(start.getFullYear(), start.getMonth(), start.getDate());
                const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

                if (startDay.getTime() > today.getTime()) {
                    Swal.fire(
                        "Not allowed",
                        "Sick Leave (SL) cannot be filed for a future date.",
                        "warning"
                    );
                    return;
                }
            }

            // COMMON 
            const requestedDays = Number(this.leaveForm.total_leave_days);
            const balanceType = this.getBalanceType(this.selectedTypeofLeave);
            const remaining = Number(this.remainingLeaves[balanceType] || 0);

            const proceedSubmit = (isSalaryDeduction = false, excessDays = 0) => {
                const formData = {
                    selectedTypeofLeave: this.selectedTypeofLeave,
                    fullName: this.fullName,
                    total_leave_days: requestedDays,
                    date_from: this.leaveForm.date_from,
                    date_to: this.leaveForm.date_to,
                    leave_reason: this.leaveForm.leave_reason,
                    department_name: this.user.dept_code,
                    emp_id: this.user.emp_id,
                    halfday: this.leaveForm.half_day,

                    is_salary_deduction: isSalaryDeduction ? 1 : 0,
                    excess_days: excessDays
                };

                console.log(formData)

                fetch(`${API_BASE}/create_leave`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(formData),
                })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            Swal.fire(
                                "Success",
                                isSalaryDeduction
                                    ? "Leave filed. Excess days will be deducted from salary."
                                    : "Leave filed successfully.",
                                "success"
                            );
                            this.$emit("leave-submitted");
                            this.closeModal();
                        } else {
                            Swal.fire("Error", data.error || "Failed to submit leave", "error");
                        }
                    })
                    .catch(() => {
                        Swal.fire("Error", "Something went wrong", "error");
                    });
            };

            // EXCEEDS BALANCE → CONFIRM
            if (requestedDays > remaining) {
                const excessDays = requestedDays - remaining;

                Swal.fire({
                    icon: "warning",
                    title: "Leave Balance Exceeded",
                    html: `
                You only have <b>${remaining}</b> remaining ${balanceType} day(s).<br><br>
                <b>${excessDays}</b> day(s) will be treated as
                <span style="color:red;font-weight:bold;">salary deduction (unpaid leave)</span>.<br><br>
                Do you want to proceed?
            `,
                    showCancelButton: true,
                    confirmButtonText: "Yes, proceed",
                    cancelButtonText: "Cancel",
                    confirmButtonColor: "#df7a8a"
                }).then(result => {
                    if (result.isConfirmed) {
                        proceedSubmit(true, excessDays);
                    }
                });

                return;
            }

            proceedSubmit(false, 0);
        },



        fetchRemainingLeaves() {
            fetch(`${API_BASE}/get_remaining_leaves`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    emp_id: this.user.emp_id
                })
            })
                .then(res => res.json())
                .then(data => {
                    this.remainingLeaves = {
                        VL: Number(data.remaining?.VL || 0),
                        SL: Number(data.remaining?.SL || 0)
                    };
                })
                .catch(() => {
                    this.remainingLeaves = { VL: 0, SL: 0 };
                });
        },

    },
    mounted() {
        this.fetchExistingLeaves();
        this.fetchRemainingLeaves();
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
