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
                    <div class="modal-body pb-1">
                        <!-- User Information Section -->
                        <div class="section">
                            <div class="section-title">User Information</div>
                            <hr class="mt-0">
                            <div class="row mb-3">
                                <div class="col-12">
                                    <label class="form-label label-sm">User</label>
                                    <input type="text" class="form-control" v-model="leaveRequest.user" readonly />
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-6">
                                    <label class="form-label label-sm">Position</label>
                                    <input type="text" class="form-control" v-model="leaveRequest.position" readonly />
                                </div>
                                <div class="col-6">
                                    <label class="form-label label-sm">Department</label>
                                    <input type="text" class="form-control" v-model="leaveRequest.department"
                                        readonly />
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-6">
                                    <label class="form-label label-sm">Address</label>
                                    <input type="text" class="form-control" v-model="leaveRequest.address" readonly />
                                </div>
                                <div class="col-6">
                                    <label class="form-label label-sm">Contact Number</label>
                                    <input type="text" class="form-control" v-model="leaveRequest.contact" readonly />
                                </div>
                            </div>
                        </div>

                        <!-- Leave Request Section -->
                        <div class="section mt-3">
                            <div class="section-title">Leave Request</div>
                            <hr class="mt-0">
                            <div class="row mb-3">
                                <div class="col-5">
                                    <label class="form-label label-sm">Type of Leave</label>
                                    <input type="text" class="form-control" :value="formattedLeaveType" readonly />
                                </div>
                                <div class="col-2">
                                    <label class="form-label label-sm">Total Days</label>
                                    <input type="text" class="form-control leave_days"
                                        v-model="editableLeave.leave_number" readonly />

                                </div>
                                <div class="col-5">
                                    <label class="form-label label-sm">REFERENCE NUMBER</label>
                                    <input type="text" class="form-control" v-model="leaveRequest.ref_no" readonly />
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-6">
                                    <label class="form-label label-sm">Date of Leave From</label>
                                    <input type="date" class="form-control" v-model="editableLeave.leave_from"
                                        :readonly="!canUpdate" :min="originalLeaveFrom" />
                                </div>
                                <div class="col-6">
                                    <label class="form-label label-sm">Date of Leave To</label>
                                    <input type="date" class="form-control" v-model="editableLeave.leave_to"
                                        :readonly="!canUpdate" />
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-12">
                                    <label class="form-label label-sm">Reason for Leave</label>

                                    <textarea class="form-control" rows="1" v-model="leaveRequest.leave_reason"
                                        :readonly="!canUpdate">
</textarea>
                                </div>
                            </div>
                        </div>

                        <!-- Approver Buttons for Department Head -->


                        <!-- approver -->
                        <div class="section">
                            <div class="section-title">APPROVER AND STATUS OF LEAVE</div>
                            <hr class="mt-0 mb-2">
                            <div class="row mt-0">
                                <div class="col-4">
                                    <label for="approver" class="form-label label-sm">Approved by</label>
                                    <input type="text" id="approver" class="form-control"
                                        v-model="leaveRequest.approved_by" readonly />
                                </div>
                               
                                <div class="col-3">
                                    <label for="leave_status" class="form-label label-sm">Date Approved</label>
                                    <input type="text" id="leave_status" class="form-control"
                                        v-model="formatteddate_approved" readonly />
                                </div>
                                 <div class="col-5">
                                    <label for="leave_status" class="form-label label-sm">Leave Status</label>
                                    <input type="text" id="leave_status" class="form-control"
                                        v-model="leaveRequest.status" readonly />
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Modal Footer -->
                    <div class="modal-footer">

                        <button v-if="leaveRequest.status === 'APPROVED'" type="button" class="btn btn-primary"
                            @click="downloadLeavePdf">

                            <i class="fas fa-print"></i> Print
                        </button>

                        <div
                            v-if="user.job_title == 'Department Head' && leaveRequest.status == 'FOR DEPARTMENT HEAD APPROVAL'">

                            <button type="button" class="btn btn-secondary" @click="approveLeaveRequest"
                                :disabled="!canApprove">
                                Approve
                            </button>

                            <button v-if="canDeny" class="btn btn-danger" @click="denyLeaveRequest">Deny</button>

                        </div>

                        <div v-if="leaveRequest.status == 'DENIED'">
                            <button type="button" class="btn btn-warning" @click="updateLeave">Update</button>
                        </div>
                        <div v-if="canCancel">
                            <button type="button" class="btn btn-danger" @click="cancelLeave">
                                Cancel Leave
                            </button>
                        </div>


                        <div>
                            <button type="button" class="btn btn-info" @click="closeModal">Close</button>
                        </div>

                    </div>
                </form>

                <leaves_print ref="leavePdf" :request="leaveRequest" v-show="showLeavePdf" />



            </div>
        </div>
    </div>
</template>

<script>
import API_BASE from '@/utils/api_config';
import { getUserData } from '@/utils/get_user_data';
import html2pdf from "html2pdf.js"
import leaves_print from "../prints/leaves_print.vue"

export default {
    components: {
        leaves_print
    },
    props: {
        isVisible: Boolean,
        leaveRequest: Object,
    },
    data() {
        return {
            user: getUserData() || {},
            originalLeaveFrom: "",
            existingLeaves: [],
            editableLeave: {
                leave_from: "",
                leave_to: "",
                leave_reason: "",
                leave_number: "",
            },
            showLeavePdf: false,
        }
    },

    watch: {
        leaveRequest: {
            immediate: true,
            handler(val) {
                if (!val) return;

                const from = this.toDateInput(val.leave_from);
                const to = this.toDateInput(val.leave_to);

                this.originalLeaveFrom = from;
                this.editableLeave.leave_from = from;
                this.editableLeave.leave_to = to;
                this.editableLeave.leave_reason = val.leave_reason || "";
                this.editableLeave.leave_number = val.leave_number || "";
            }
        },

        'editableLeave.leave_from': 'recomputeTotalDays',
        'editableLeave.leave_to': 'recomputeTotalDays',
    },
    mounted() {
        this.fetchExistingLeaves();
    },
    methods: {
        downloadLeavePdf() {

            this.showLeavePdf = true;

            this.$nextTick(() => {
                setTimeout(() => {
                    const element = this.$refs.leavePdf.$el;

                    html2pdf()
                        .set({
                            margin: 10,
                            filename: `${this.leaveRequest.ref_no}.pdf`,
                            image: { type: "jpeg", quality: 0.98 },
                            html2canvas: {
                                scale: 2,
                                useCORS: true
                            },
                            jsPDF: {
                                unit: "mm",
                                format: "a4",
                                orientation: "portrait"
                            }
                        })
                        .from(element)
                        .save()
                        .then(() => {
                            this.showLeavePdf = false;
                        });
                },);
            });
        },


        cancelLeave() {
            Swal.fire({
                title: "Cancel Leave?",
                text: "Are you sure you want to cancel this leave request?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                confirmButtonText: "Yes, cancel it",
            }).then(result => {
                if (!result.isConfirmed) return;

                fetch(`${API_BASE}/approved_deny_leaves`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        args: "CANCELLED",
                        ref_no: this.leaveRequest.ref_no,
                        user: `${this.user.first_name} ${this.user.last_name}`,
                    }),
                })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            Swal.fire("Cancelled", "Leave request has been cancelled.", "success");
                            this.$emit("updateDataTable");
                            this.closeModal();
                        } else {
                            Swal.fire("Error", data.error || "Cancel failed", "error");
                        }
                    })
                    .catch(() => Swal.fire("Error", "Something went wrong", "error"));
            });
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
                    this.existingLeaves = data.alldates || [];
                });
        },

        normalizeDate(d) {
            if (!d) return null;
            const x = new Date(d);
            return new Date(x.getFullYear(), x.getMonth(), x.getDate());
        },

        hasDateConflict(from, to) {
            const newFrom = this.normalizeDate(from);
            const newTo = this.normalizeDate(to);

            return this.existingLeaves.some(lv => {
                if (lv.ref_no === this.leaveRequest.ref_no) return false;

                // ignore denied leaves
                if (lv.status === "DENIED") return false;

                const oldFrom = this.normalizeDate(lv.leave_from);
                const oldTo = this.normalizeDate(lv.leave_to);

                if (!oldFrom || !oldTo) return false;

                // overlap check
                return newFrom <= oldTo && newTo >= oldFrom;
            });
        },



        updateLeave() {
            if (!this.canUpdate) {
                Swal.fire(
                    "Not allowed",
                    "You can only update denied VL if the original Date From is still in the future.",
                    "warning"
                );
                return;
            }

            // CHECK DATE CONFLICT
            if (this.hasDateConflict(this.editableLeave.leave_from, this.editableLeave.leave_to)) {
                Swal.fire(
                    "Date Conflict",
                    "You already have an existing leave that overlaps with the selected dates.",
                    "warning"
                );
                return;
            }

            const result = this.validateLeaveDates({
                from: this.editableLeave.leave_from,
                to: this.editableLeave.leave_to,
                type: "VL",
                halfDay: false,
                isUpdate: true
            });

            if (!result.valid) {
                Swal.fire("Invalid", result.msg || "Invalid leave dates.", "warning");
                return;
            }

            const payload = {
                ref_number: this.leaveRequest.ref_no,
                date_from: this.editableLeave.leave_from,
                date_to: this.editableLeave.leave_to,
                leave_number: result.days,
                leave_reason: this.editableLeave.leave_reason,
                fullName: `${this.user.first_name} ${this.user.last_name}`,
            };

            fetch(`${API_BASE}/update_denied_leaves`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire("Success", "Leave has been updated successfully", "success");
                        this.$emit("updateDataTable");
                        this.closeModal();
                    } else {
                        Swal.fire("Error", data.error || "Update failed", "error");
                    }
                })
                .catch(() => Swal.fire("Error", "Something went wrong", "error"));
        },


        closeModal() {
            this.$emit("close");
        },

        approveLeaveRequest() {
            if (!this.canApprove) {
                Swal.fire(
                    "Cannot Approve",
                    "This leave can no longer be approved because the Date From has already passed.",
                    "warning"
                );
                return;
            }

            fetch(`${API_BASE}/approved_deny_leaves`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    args: "APPROVED",
                    ref_no: this.leaveRequest.ref_no,
                    user: `${this.user.first_name} ${this.user.last_name}`,
                }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire("Success", "Leave request approved", "success");
                        this.$emit("updateDataTable");
                        this.closeModal();
                    } else {
                        Swal.fire("Error", data.error || "Failed to approve leave", "error");
                    }
                })
                .catch(() => {
                    Swal.fire("Error", "Something went wrong", "error");
                });
        },

        denyLeaveRequest() {
            fetch(`${API_BASE}/approved_deny_leaves`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    args: "DENIED",
                    ref_no: this.leaveRequest.ref_no,
                    user: `${this.user.first_name} ${this.user.last_name}`,
                }
                ),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire("Success", "Leave request DENIED", "success");
                        this.$emit('updateDataTable'); // Emit the event
                        this.closeModal(); // Close the modal
                    } else {
                        Swal.fire("Error", data.error || "Failed to submit leave", "error");
                    }
                })
                .catch(error => {
                    console.error("Error submitting form:", error);
                    Swal.fire("Error", "Something went wrong", "error");
                });
        },

        toDateInput(date) {
            if (!date) return "";

            const d = new Date(date);
            const y = d.getFullYear();
            const m = String(d.getMonth() + 1).padStart(2, "0");
            const day = String(d.getDate()).padStart(2, "0");

            return `${y}-${m}-${day}`;
        },


        formatDate(date) {
            if (date) {
                const formattedDate = new Date(date);
                return formattedDate.toISOString().split('T')[0]; // returns yyyy-mm-dd
            }
            return '';
        },

        recomputeTotalDays() {
            if (!this.canUpdate) return;

            const result = this.validateLeaveDates({
                from: this.editableLeave.leave_from,
                to: this.editableLeave.leave_to,
                type: "VL",
                halfDay: false,
                isUpdate: true
            });

            this.editableLeave.leave_number = result.valid ? result.days : "";
        },




    },

    computed: {
        formattedLeaveType() {
            const leaveTypes = {
                'EL': 'Emergency Leave',
                'VL': 'Vacation Leave',
                'SL': 'Sick Leave',
            };
            return leaveTypes[this.leaveRequest.leave_type]
        },
        formattedLeaveTo() {
            return this.formatDate(this.leaveRequest.leave_to);
        },
        formattedLeaveFrom() {
            return this.formatDate(this.leaveRequest.leave_from);
        },
        formatteddate_approved() {
            return this.formatDate(this.leaveRequest.date_approved);
        },
        canDeny() {
            return !['Sick Leave', 'Emergency Leave', 'SL', 'EL'].includes(this.leaveRequest.leave_type);
        },

        todayIsNotDateFrom() {
            if (!this.leaveRequest.leave_from) return false;

            const today = new Date();
            today.setHours(0, 0, 0, 0);

            const from = new Date(this.leaveRequest.leave_from);
            from.setHours(0, 0, 0, 0);

            return today.getTime() !== from.getTime();
        },

        canUpdate() {
            if (!this.leaveRequest) return false;
            if (this.leaveRequest.leave_type !== "VL") return false;
            if (this.leaveRequest.status !== "DENIED") return false;

            const today = new Date();
            today.setHours(0, 0, 0, 0);

            const from = new Date(this.leaveRequest.leave_from);
            from.setHours(0, 0, 0, 0);

            //  edit allowed only if date_from still in future
            return from.getTime() > today.getTime();
        },


        canCancel() {
            if (!this.leaveRequest) return false;

            const status = this.leaveRequest.status;

            if (this.leaveRequest.emp_id !== this.user.emp_id) return false;

            // already cancelled
            if (status === "CANCELLED") return false;

            const today = new Date();
            today.setHours(0, 0, 0, 0);

            const from = new Date(this.leaveRequest.leave_from);
            from.setHours(0, 0, 0, 0);

            // pending approval → always cancelable
            if (status === "FOR DEPARTMENT HEAD APPROVAL") return true;

            // denied or approved → only if date_from is still in the future
            if (["DENIED", "APPROVED"].includes(status)) {
                return from.getTime() > today.getTime();
            }

            return false;
        },

        canApprove() {
            if (!this.leaveRequest) return false;

            if (this.leaveRequest.status !== "FOR DEPARTMENT HEAD APPROVAL") {
                return false;
            }

            const today = new Date();
            today.setHours(0, 0, 0, 0);

            const from = new Date(this.leaveRequest.leave_from);
            from.setHours(0, 0, 0, 0);

            // cannot approve if Date From already passed
            return from.getTime() >= today.getTime();
        },








    },
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
    font-size: 13px !important;
}

.leave_days {
    background-color: #b3cadc !important;
    border: #fff !important;
}

#leave_reason:focus {
    background-color: #fff !important;
    font-size: 12px !important;
}

.pdf-hidden {
    position: fixed;
    top: 0;
    left: -9999px;
    width: 800px;
    background: white;
}
</style>
