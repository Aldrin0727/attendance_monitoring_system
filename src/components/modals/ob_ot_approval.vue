<template>
    <div class="modal" v-if="isVisible">
        <div class="modal-dialog">
            <div class="modal-content">

                <!-- HEADER -->
                <div class="modal-header py-1">
                    <font-awesome-icon :icon="['fas', 'clock']" class="font-awesome-icon" />
                    <h5 class="modal-title">{{ ob_ot_Request.type }} Request Details</h5>
                    <button type="button" class="btn-close" @click="closeModal"></button>
                </div>

                <!-- BODY -->
                <div class="modal-body pb-1">

                    <!-- USER INFORMATION -->
                    <div class="section">
                        <div class="section-title">User Information</div>
                        <hr class="mt-0">

                        <div class="row mb-3">
                            <div class="col-12">
                                <label class="form-label label-sm">User</label>
                                <input type="text" class="form-control" v-model="ob_ot_Request.fullName" readonly />
                            </div>
                        </div>

                        <div class="row mb-3">
                            <div class="col-6">
                                <label class="form-label label-sm">Position</label>
                                <input type="text" class="form-control" v-model="ob_ot_Request.position" readonly />
                            </div>

                            <div class="col-6">
                                <label class="form-label label-sm">Department</label>
                                <input type="text" class="form-control" v-model="ob_ot_Request.department" readonly />
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-6">
                                <label class="form-label label-sm">Address</label>
                                <input type="text" class="form-control" v-model="ob_ot_Request.address" readonly />
                            </div>

                            <div class="col-6">
                                <label class="form-label label-sm">Contact Number</label>
                                <input type="text" class="form-control" v-model="ob_ot_Request.contact" readonly />
                            </div>
                        </div>
                    </div>

                    <!-- OB/OT DETAILS -->
                    <div class="section mt-3">
                        <div class="section-title">{{ ob_ot_Request.type }} Request</div>
                        <hr class="mt-0">

                        <div class="row mb-3">
                            <div class="col-4">
                                <label class="form-label label-sm">Reference Number</label>
                                <input type="text" class="form-control" v-model="ob_ot_Request.ref_number" readonly />
                            </div>

                            <div class="col-4">
                                <label class="form-label label-sm">Type</label>
                                <input type="text" class="form-control" v-model="ob_ot_Request.type" readonly />
                            </div>

                            <div class="col-4">
                                <label class="form-label label-sm">Category</label>
                                <input type="text" class="form-control" v-model="ob_ot_Request.category" readonly />
                            </div>


                        </div>

                        <div class="row mb-3">
                            <div class="col-4">
                                <label class="form-label label-sm">Destination</label>
                                <input type="text" class="form-control" v-model="ob_ot_Request.destination" readonly />
                            </div>
                            <div class="col-4">
                                <label class="form-label label-sm">Requested Date From</label>
                                <input type="datetime-local" class="form-control"
                                    :value="formatDateTime(ob_ot_Request.req_from)" readonly />
                            </div>

                            <div class="col-4">
                                <label class="form-label label-sm">Requested Date To</label>
                                <input type="datetime-local" class="form-control"
                                    :value="formatDateTime(ob_ot_Request.req_to)" readonly />
                            </div>


                        </div>

                        <div class="row">
                            <div class="col-6">
                                <label class="form-label label-sm">Reason</label>
                                <textarea class="form-control" rows="2" v-model="ob_ot_Request.reason"
                                    readonly></textarea>
                            </div>
                            <div class="col-6">
                                <label class="form-label label-sm">Project</label>
                                <textarea class="form-control" rows="2" v-model="ob_ot_Request.project"
                                    readonly></textarea>
                            </div>
                        </div>
                    </div>

                    <!-- ACTUAL OB/OT DATE INPUTS (Visible Only When Approved) -->
                    <div class="section mt-3" v-if="ob_ot_Request.status === 'APPROVED'">
                        <div class="section-title">Actual {{ ob_ot_Request.type }} Execution</div>
                        <hr class="mt-0">

                        <div class="row">
                            <div class="col-5">
                                <label class="form-label label-sm">Actual Start Date & Time</label>
                                <input type="datetime-local" class="form-control" v-model="actualDates.actual_from" />
                            </div>

                            <div class="col-5">
                                <label class="form-label label-sm">Actual End Date & Time</label>
                                <input type="datetime-local" class="form-control" v-model="actualDates.actual_to" />
                            </div>
                            <div class="col-2">
                                <label class="form-label label-sm">Hours</label>
                                <input type="input" class="form-control total_hours" v-model="total_time" readonly />
                            </div>
                        </div>


                    </div>


                    <!-- APPROVER INFO -->
                    <div class="section mt-3">
                        <div class="section-title">Approver & Status</div>
                        <hr class="mt-0">

                        <div class="row">
                            <div class="col-4">
                                <label class="form-label label-sm">Approved By</label>
                                <input type="text" class="form-control" v-model="ob_ot_Request.approved_by" readonly />
                            </div>

                            <div class="col-4">
                                <label class="form-label label-sm">Status</label>
                                <input type="text" class="form-control" v-model="ob_ot_Request.status" readonly />
                            </div>

                            <div class="col-4">
                                <label class="form-label label-sm">Date Approved</label>
                                <input type="text" class="form-control"
                                    :value="formatDisplayDate(ob_ot_Request.date_approved)" readonly />
                            </div>
                        </div>
                    </div>

                </div>

                <!-- FOOTER -->
                <div class="modal-footer">
                    <div v-if="canApprove">
                        <button class="btn btn-secondary me-2" @click="approveRequest">Approve</button>
                        <button class="btn btn-danger" @click="denyRequest">Deny</button>
                    </div>

                    <div v-if="ob_ot_Request.status === 'APPROVED'">
                        <button class="btn btn-success me-2" @click="saveActualDates">
                            Save Actual {{ ob_ot_Request.type }} Dates
                        </button>
                        <button class="btn btn-info" @click="closeModal">Close</button>
                    </div>

                    <div v-else>
                        <button class="btn btn-info" @click="closeModal">Close</button>
                    </div>
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
        isVisible: Boolean,
        ob_ot_Request: Object
    },

    data() {
        return {
            user: getUserData() || {},
            actualDates: {
                actual_from: "",
                actual_to: ""
            },

            total_time: ""

        };
    },

    computed: {
        canApprove() {
            return (
                this.user.job_title === "Department Head" &&
                this.ob_ot_Request.status === "FOR DEPARTMENT HEAD APPROVAL"
            );
        }
    },

    watch: {
        "actualDates.actual_from": function () {
            this.calculateHours();
        },
        "actualDates.actual_to": function () {
            this.calculateHours();
        }
    },


    methods: {
        closeModal() {
            this.$emit("close");
        },

        formatDateTime(dt) {
            if (!dt) return "";
            const d = new Date(dt);
            return d.toISOString().slice(0, 16); // yyyy-mm-ddTHH:mm
        },

        formatDisplayDate(dt) {
            if (!dt) return "";
            return new Date(dt).toISOString().slice(0, 10);
        },

        approveRequest() {
            this.submitDecision("APPROVED");
        },

        denyRequest() {
            this.submitDecision("DENIED");
        },

        calculateHours() {
            const start = this.actualDates.actual_from;
            const end = this.actualDates.actual_to;

            // Clear when empty
            if (!start || !end) {
                this.total_time = "";
                return;
            }

            const startDate = new Date(start);
            const endDate = new Date(end);

            // Invalid: End earlier than Start
            if (endDate <= startDate) {
                Swal.fire({
                    icon: "warning",
                    title: "Invalid Actual Dates",
                    text: "Actual end date/time cannot be earlier than the actual start date/time.",
                });
                this.total_time = "";
                return;
            }

            // ✔ Valid — Compute hours
            const diffMs = endDate - startDate;
            let diffMinutes = Math.floor(diffMs / (1000 * 60));

            let hours = Math.floor(diffMinutes / 60);
            let minutes = diffMinutes % 60;

            if (minutes < 10) minutes = "0" + minutes;

            this.total_time = `${hours}h ${minutes}m`;
        },

        submitDecision(decision) {
            fetch(`${API_BASE}/update_approved_deny_otob`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    args: decision,
                    ref_number: this.ob_ot_Request.ref_number,
                    user: `${this.user.first_name} ${this.user.last_name}`
                })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire("Success", `Request ${decision}`, "success");
                        this.$emit("updateDataTable");
                        this.closeModal();
                    } else {
                        Swal.fire("Error", data.error || "Request failed", "error");
                    }
                })
                .catch(err => {
                    console.error(err);
                    Swal.fire("Error", "Something went wrong", "error");
                });
        },

        saveActualDates() {


            // Required validation
            if (!this.actualDates.actual_from || !this.actualDates.actual_to) {
                Swal.fire("Missing Fields", "Please provide both Actual Start and Actual End.", "warning");
                return;
            }

            const payload = {
                ref_number: this.ob_ot_Request.ref_number,
                actual_from: this.actualDates.actual_from,
                actual_to: this.actualDates.actual_to,
                actual_hours: this.total_time,
                user: `${this.user.first_name} ${this.user.last_name}`
            };

            console.log(payload)
            fetch(`${API_BASE}/save_actual_otob_dates`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {

                        Swal.fire({
                            icon: "success",
                            title: `${this.ob_ot_Request.type} Actual Dates Saved`,
                            text: `Total Time: ${total_hours}`,
                        });

                        // refresh parent table
                        this.$emit("updateDataTable");

                        // close modal
                        this.closeModal();

                    } else {
                        Swal.fire("Error", data.error || "Failed to save actual dates.", "error");
                    }
                })
                .catch(err => {
                    console.error(err);
                    Swal.fire("Error", "Something went wrong while saving.", "error");
                });
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
    color: #5ac5c5 !important;
    width: 20px;
    height: 45px;
    margin-right: 10px;
}

.label-sm {
    text-transform: uppercase;
}

.form-control {
    background-color: #e9ecef !important;
    font-size: 13px !important;
}

.total_hours {
    background-color: #b3cadc !important;
    border: #fff !important;
}

textarea {
    background-color: #e9ecef !important;
}
</style>
