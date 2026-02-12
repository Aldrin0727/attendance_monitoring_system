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
                                <!-- <div class="col-6">
                                    <label class="form-label label-sm">Date of Leave From</label>
                                    <input type="date" class="form-control" v-model="editableLeave.leave_from"
                                        :readonly="!canUpdate" :min="originalLeaveFrom" />
                                </div> -->
                                <div class="col-6">
                                    <label class="form-label label-sm">Date of Leave From</label>

                                    <!-- VIEW MODE -->
                                    <input v-if="!canUpdate" type="text" class="form-control"
                                        :value="toYMD(leaveRequest.leave_from)" readonly />

                                    <!-- EDIT MODE -->
                                    <input v-else type="date" class="form-control" v-model="editableLeave.leave_from"
                                        :min="originalLeaveFrom" />
                                </div>

                                <!-- <div class="col-6">
                                    <label class="form-label label-sm">Date of Leave To</label>
                                    <input type="date" class="form-control" v-model="editableLeave.leave_to"
                                        :readonly="!canUpdate" />
                                </div> -->
                                <div class="col-6">
                                    <label class="form-label label-sm">Date of Leave To</label>

                                    <!-- VIEW MODE -->
                                    <input v-if="!canUpdate" type="text" class="form-control"
                                        :value="toYMD(leaveRequest.leave_to)" readonly />

                                    <!-- EDIT MODE -->
                                    <input v-else type="date" class="form-control" v-model="editableLeave.leave_to"
                                        :min="originalLeaveFrom" />
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

                                <div class="col-4">
                                    <label for="leave_status" class="form-label label-sm">Date Approved</label>
                                    <input type="text" id="leave_status" class="form-control"
                                        v-model="formatteddate_approved" readonly />
                                </div>
                                <div class="col-4">
                                    <label for="leave_status" class="form-label label-sm">Leave Status</label>
                                    <input type="text" id="leave_status" class="form-control"
                                        v-model="leaveRequest.status" readonly />
                                </div>
                            </div>
                        </div>

                        <!-- LEAVE BALANCE SUMMARY -->
                        <div class="section" v-if="leaveRequest.status === 'APPROVED'">
                            <div class="section-title">LEAVE BALANCE SUMMARY</div>
                            <hr class="mt-0 mb-2">

                            <div class="row">
                                <div class="col-4">
                                    <label class="form-label label-sm">Remaining Before</label>
                                    <input type="text" class="form-control" :value="leaveBalanceComputed.before"
                                        readonly />

                                </div>

                                <div class="col-4">
                                    <label class="form-label label-sm">Leave Applied</label>
                                    <input type="text" class="form-control leave_days"
                                        :value="leaveBalanceComputed.applied" readonly />
                                </div>

                                <div class="col-4">
                                    <label class="form-label label-sm">Remaining Balance</label>

                                    <input type="text" class="form-control remaining_balance"
                                        :class="{ 'text-danger border-danger': isExcessLeave }"
                                        :value="leaveBalanceComputed.after" readonly />
                                </div>
                                <div v-if="isExcessLeave" class="mt-2 text-danger"
                                    style="font-size: 12px; font-weight: 600;">
                                    ⚠ Excess leave detected. This may be subject to salary deduction.
                                </div>

                            </div>
                        </div>

                      <!-- LEAVE HISTORY -->
                        <div class="section mt-3"  v-if="leaveRequest.status === 'APPROVED' || leaveRequest.status === 'FOR DEPARTMENT HEAD APPROVAL'">
                            <div class="section-title">LEAVE HISTORY</div>
                            <hr class="mt-0 mb-2">

                            <div class="row">
                                <div class="col-6">
                                    <label class="form-label label-sm">Last Approved Leave Taken</label>
                                    <!-- <input type="text" class="form-control" :value="toYMD(lastApprovedLeaveTaken)"
                                        readonly /> -->
                                    <input type="text" class="form-control" :value="lastApprovedLeaveTaken || '-'" readonly />
                                    <!-- <small style="color:#6b7280;font-size:12px;display:block;margin-top:4px;">
                                        Based on the latest approved leave.
                                    </small> -->
                                </div>
                            </div>
                        </div>

                    </div>

                    <!-- Modal Footer -->
                    <div class="modal-footer d-flex justify-content-between align-items-center">

                        <!-- LEFT SIDE ACTIONS -->
                        <div class="d-flex align-items-center gap-2">

                            <!-- Print -->
                            <button v-if="leaveRequest.status === 'APPROVED'" type="button" class="btn btn-primary"
                                @click="downloadLeavePdf">
                                <i class="fas fa-print"></i>&nbsp;Print
                            </button>

                            <!-- Approve  -->
                            <button v-if="user.job_title === 'Department Head'
                                && leaveRequest.status === 'FOR DEPARTMENT HEAD APPROVAL'" type="button"
                                class="btn btn-success" @click="approveLeaveRequest"
                                :disabled="!canApprove || approving || denying">
                                <span v-if="approving">
                                    <i class="fas fa-spinner fa-spin"></i>&nbsp;Approving...
                                </span>
                                <span v-else>
                                    <i class="fas fa-circle-check"></i>&nbsp;Approve
                                </span>
                            </button>

                            <!-- Update (DENIED only) -->
                            <button v-if="canUpdate" type="button" class="btn btn-warning"
                                :disabled="approving || denying" @click="updateLeave">
                                <i class="fas fa-pen-to-square"></i>&nbsp;Update
                            </button>


                        </div>

                        <div class="d-flex align-items-center gap-2">

                            <!-- Deny -->
                            <button v-if="user.job_title === 'Department Head'
                                && leaveRequest.status === 'FOR DEPARTMENT HEAD APPROVAL'" class="btn btn-danger"
                                @click="denyLeaveRequest" :disabled="!canDeny || approving || denying">
                                <span v-if="denying">
                                    <i class="fas fa-spinner fa-spin"></i>&nbsp;Denying...
                                </span>
                                <span v-else>
                                    <i class="fas fa-circle-xmark"></i>&nbsp;Deny
                                </span>
                            </button>


                            <!-- Cancel Leave -->
                            <button v-if="canCancel" type="button" class="btn btn-danger" @click="cancelLeave">
                                Cancel Leave
                            </button>


                        </div>

                  </div>

                    <div v-if="approving" class="screen-loader" role="dialog" aria-modal="true"
                        aria-label="Processing approval">
                        <div class="loader-card">
                            <div class="spinner-border" aria-hidden="true"></div>

                            <div class="loader-title">Processing approval</div>
                            <div class="loader-subtitle">Please wait while we send the email to HR.</div>
                        </div>
                    </div>

                </form>

                <leaves_print ref="leavePdf" :request="leaveRequest" v-show="showLeavePdf"  :last-approved-leave-taken="lastApprovedLeaveTaken" />



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

            approving: false,
            denying: false,
            lastApprovedLeaveTaken: null, 
            
        }
    },

    watch: {
        leaveRequest: {
            immediate: true,
            handler(val) {
                if (!val) return;


                this.originalLeaveFrom = val.leave_from;
                this.editableLeave.leave_from = val.leave_from;
                this.editableLeave.leave_to = val.leave_to;
                this.editableLeave.leave_reason = val.leave_reason || "";
                this.editableLeave.leave_number = val.leave_number || "";

                this.fetchExistingLeaves();
            }
        },

        'editableLeave.leave_from': 'recomputeTotalDays',
        'editableLeave.leave_to': 'recomputeTotalDays',

    },
    mounted() {
        this.fetchExistingLeaves();
    },
    methods: {
        generateLeavePdfBlob() {
            this.showLeavePdf = true;

            return this.$nextTick().then(() => {
                const element = this.$refs.leavePdf.$el;

                return html2pdf()
                    .set({
                        margin: 10,
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
                    .outputPdf("blob")
                    .then(blob => {
                        this.showLeavePdf = false;
                        return blob;
                    });
            });
        },

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

                const fd = new FormData();
                fd.append("args", "CANCELLED");
                fd.append("ref_no", this.leaveRequest.ref_no);
                fd.append("user", `${this.user.first_name} ${this.user.last_name}`);
                fd.append("emp_id", this.user.emp_id);
                fd.append("dept_code", this.user.dept_code);


                fetch(`${API_BASE}/approved_deny_leaves`, {
                    method: "POST",
                    body: fd
                })
                    .then(res => res.json())
                    .then(data => {
                        console.log(data)
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

        // fetchExistingLeaves() {
        //     console.log(this.user.emp_id)
        //     fetch(`${API_BASE}/get_leaves_for_approval_request_date`, {
        //         method: "POST",
        //         headers: { "Content-Type": "application/json" },
        //         body: JSON.stringify({
        //             emp_id: this.user.emp_id
        //         })
        //     })
        //         .then(res => res.json())
        //         .then(data => {
        //             console.log(data)
        //             this.existingLeaves = data.alldates || [];
                    
        //         });
        // },

        fetchExistingLeaves() {
            const empId = this.leaveRequest?.emp_id;
            const leaveType = this.leaveRequest?.leave_type;
            const ref_no = this.leaveRequest?.ref_no;
            if (!empId) return;


            fetch(`${API_BASE}/get_leaves_for_approval_request_date`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    emp_id: empId,
                    leave_type: leaveType,
                    ref_no: ref_no
                })
            })
                .then(res => res.json())
                .then(data => {
                    
                   console.log(data)
                    if (!data.success) throw new Error(data.error || "Fetch failed");

                    this.existingLeaves = data.alldates || [];
                    this.lastApprovedLeaveTaken = data.last_taken || null; //  from backend

                    console.log(data.last_taken)
                    
                })
                .catch(() => {
                    this.existingLeaves = [];
                    this.lastApprovedLeaveTaken = null;
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

            const days = this.calculateDays(this.editableLeave.leave_from, this.editableLeave.leave_to);
            if (days <= 0) {
                Swal.fire("Invalid", "Invalid leave date range.", "warning");
                return;
            }

            // CONFIRMATION FIRST
            Swal.fire({
                title: "Update this leave request?",
                html: `
      Are you sure you want to update this denied leave request?<br><br>
      <div style="text-align:left; font-size:13px;">
        <b>Reference:</b> ${this.leaveRequest.ref_no}<br>
        <b>Date From:</b> ${this.toYMD(this.editableLeave.leave_from)}<br>
        <b>Date To:</b> ${this.toYMD(this.editableLeave.leave_to)}<br>
        <b>Total Days:</b> ${days}<br>
      </div>
      <br>
      This will be re-submitted for approval.
    `,
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "Yes, update",
                cancelButtonText: "No, cancel",
                confirmButtonColor: "#f0ad4e",
            }).then(result => {
                if (!result.isConfirmed) return;

                const payload = {
                    ref_number: this.leaveRequest.ref_no,
                    date_from: this.editableLeave.leave_from,
                    date_to: this.editableLeave.leave_to,
                    leave_number: days,
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
                            Swal.fire({
                                icon: "success",
                                title: "Updated",
                                html: `The denied leave request has been updated and re-submitted for department head approval.`,
                                confirmButtonColor: "#28a745"
                            });

                            this.$emit("updateDataTable");
                            this.closeModal();
                        } else {
                            Swal.fire("Error", data.error || "Update failed", "error");
                        }
                    })
                    .catch(() => Swal.fire("Error", "Something went wrong", "error"));
            });
        },




        closeModal() {
            this.$emit("close");
        },

approveLeaveRequest() {
  if (!this.canApprove || this.approving) return;

  this.approving = true;

const fd = new FormData();
fd.append("args", "APPROVED");
fd.append("ref_no", this.leaveRequest.ref_no);
fd.append("user", `${this.user.first_name} ${this.user.last_name}`);

fd.append("requester_emp_id", this.leaveRequest.emp_id);
fd.append("approver_emp_id", this.user.emp_id);

fd.append("dept_code", this.user.dept_code);

//   alert(this.user.dept_code)

  // STEP 1: approve only (backend recompute + update DB)
  fetch(`${API_BASE}/approved_deny_leaves`, { method: "POST", body: fd })
    .then(res => res.json())
    .then(data1 => {
      if (!data1.success) throw new Error(data1.error || "Approval failed");

      // ✅ IMPORTANT: update local leaveRequest with DB-updated values
      if (data1.updated) {
        Object.assign(this.leaveRequest, data1.updated);
      } else {
        // fallback
        this.leaveRequest.status = "APPROVED";
      }

      // STEP 2: generate PDF based on UPDATED leaveRequest
      return this.generateLeavePdfBlob();
    })
    .then(pdfBlob => {
      // STEP 3: send email with pdf=
      const fd2 = new FormData();
        fd2.append("args", "APPROVED");
        fd2.append("ref_no", this.leaveRequest.ref_no);
        fd2.append("user", `${this.user.first_name} ${this.user.last_name}`);

        fd2.append("requester_emp_id", this.leaveRequest.emp_id);
        fd2.append("approver_emp_id", this.user.emp_id);

        fd2.append("dept_code", this.user.dept_code);
        fd2.append("pdf", pdfBlob, `${this.leaveRequest.ref_no}.pdf`);

    //   alert(this.user.dept_code)

      return fetch(`${API_BASE}/approved_deny_leaves`, { method: "POST", body: fd2 });
    })
    .then(res2 => res2.json())
    .then(data2 => {
      if (!data2.success) throw new Error(data2.error || "Email sending failed");

      return Swal.fire({
        icon: "success",
        title: "Leave approved successfully.",
        html: "<b>Email sent to HR.</b>",
        confirmButtonColor: "#28a745"
      });
    })
    .then(() => {
      this.$emit("updateDataTable");
    })
    .catch(err => {
      Swal.fire("Error", err.message || "Something went wrong", "error");
    })
    .finally(() => {
      this.approving = false;
    });
},


        denyLeaveRequest() {
            this.denying = true;

            const fd = new FormData();
            fd.append("args", "DENIED");
            fd.append("ref_no", this.leaveRequest.ref_no);
            fd.append("user", `${this.user.first_name} ${this.user.last_name}`);
            fd.append("emp_id", this.leaveRequest.emp_id);
            fd.append("dept_code", this.user.dept_code);

            fetch(`${API_BASE}/approved_deny_leaves`, {
                method: "POST",
                body: fd
            })
                .then(res => res.json())
                .then(data => {
                    // console.log(data)
                    if (data.success) {
                        Swal.fire("Success", "Leave request denied", "success");
                        this.$emit("updateDataTable");
                        this.closeModal();
                    } else {
                        Swal.fire("Error", data.error || "Failed to deny leave", "error");
                    }
                })
                .catch(() => {
                    Swal.fire("Error", "Something went wrong", "error");
                })
                .finally(() => {
                    this.denying = false;
                });
        },


        // toDateInput(date) {
        //     if (!date) return "";

        //     const d = new Date(date);
        //     const y = d.getFullYear();
        //     const m = String(d.getMonth() + 1).padStart(2, "0");
        //     const day = String(d.getDate()).padStart(2, "0");

        //     return `${y}-${m}-${day}`;
        // },




        // toDateInput(date) {
        //     if (!date) return '';

        //     const d = new Date(date);

        //     const year = d.getFullYear();
        //     const month = String(d.getMonth() + 1).padStart(2, '0');
        //     const day = String(d.getDate()).padStart(2, '0');

        //     return `${year}-${month}-${day}`;
        // },



        formatDate(date) {
            if (date) {
                const formattedDate = new Date(date);
                return formattedDate.toISOString().split('T')[0]; // returns yyyy-mm-dd
            }
            return '';
            // return this.toYMD(date);
        },

        formatDateTime(date) {
            if (!date) return '';

            const parts = date.split(' ');
            const day = parts[1];
            const month = parts[2];
            const year = parts[3];
            const time = parts[4]; // 13:51:52

            return `${year}-${this.monthToNumber(month)}-${day} ${time}`;
        },

        monthToNumber(month) {
            const map = {
                Jan: '01', Feb: '02', Mar: '03', Apr: '04',
                May: '05', Jun: '06', Jul: '07', Aug: '08',
                Sep: '09', Oct: '10', Nov: '11', Dec: '12'
            };
            return map[month];
        },

        toYMD(dateStr) {
            if (!dateStr) return '';

            const d = new Date(dateStr);

            const year = d.getFullYear();
            const month = String(d.getMonth() + 1).padStart(2, '0');
            const day = String(d.getDate()).padStart(2, '0');

            return `${year}-${month}-${day}`;
        },



        recomputeTotalDays() {
            if (!this.canUpdate) return;

            const days = this.calculateDays(
                this.editableLeave.leave_from,
                this.editableLeave.leave_to
            );

            this.editableLeave.leave_number = days > 0 ? days : "";
        },


        calculateDays(from, to) {
            if (!from || !to) return 0;

            const start = new Date(from);
            const end = new Date(to);

            if (end < start) return 0;

            const diffTime = end - start;
            const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24)) + 1;

            return diffDays;
        },

        getLastApprovedLeaveTaken() {
            const todayUtc = new Date();
            const todayUtcMidnight = new Date(Date.UTC(
                todayUtc.getUTCFullYear(),
                todayUtc.getUTCMonth(),
                todayUtc.getUTCDate()
            ));

            const currentRef = this.leaveRequest?.ref_no;
            const currentType = this.leaveRequest?.leave_type; // filter by this

            const rows = (this.existingLeaves || [])
                .filter(lv => lv.status === "APPROVED")
                .filter(lv => lv.ref_no !== currentRef)                 // ignore current request
                .filter(lv => String(lv.leave_type).trim() === String(currentType).trim()) // sAME TYPE
                .filter(lv => lv.leave_to)
                .map(lv => {
                    const toUTC = this.utcMidnight(lv.leave_to);
                    return { ...lv, _toUTC: toUTC };
                })
                .filter(lv => lv._toUTC) // valid dates only
                .filter(lv => lv._toUTC.getTime() <= todayUtcMidnight.getTime()) // taken = ended
                .sort((a, b) => b._toUTC - a._toUTC);

            return rows.length ? rows[0].leave_to : null;
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
        // formattedLeaveTo() {
        //     return this.leaveRequest.leave_to;
        // },
        // formattedLeaveFrom() {
        //     return this.leaveRequest.leave_from;
        // },

        // lastApprovedLeaveTakenYMD() {
        //     return this.lastApprovedLeaveTaken ? this.toYMD(this.lastApprovedLeaveTaken) : "-";
        // },
        formatteddate_approved() {

            return this.formatDateTime(this.leaveRequest.date_approved);
        },
        canDeny() {
            if (!this.leaveRequest) return false;

            // only Department Head
            if (this.user.job_title !== "Department Head") return false;

            // only pending
            if (this.leaveRequest.status !== "FOR DEPARTMENT HEAD APPROVAL") return false;

            // SL & EL cannot be denied
            if (["SL", "EL"].includes(this.leaveRequest.leave_type)) return false;

            const today = new Date();
            today.setHours(0, 0, 0, 0);

            const from = new Date(this.leaveRequest.leave_from);
            from.setHours(0, 0, 0, 0);

            // deny disabled if date_from already passed
            return from.getTime() >= today.getTime();
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

            return from.getTime() > today.getTime();
        },


        canCancel() {
            if (!this.leaveRequest) return false;

            const status = this.leaveRequest.status;

            if (this.leaveRequest.emp_id !== this.user.emp_id) return false;

            if (this.leaveRequest.leave_type !== 'VL') return false;

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

            if (this.leaveRequest.leave_type == 'SL' || this.leaveRequest.leave_type == 'EL') return true;

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

        leaveBalanceComputed() {
            const applied = Number(this.leaveRequest.leave_number || 0);

            let remainingAfter = 0;

            if (this.leaveRequest.leave_type === 'SL') {
                remainingAfter = Number(this.leaveRequest.sl_remaining || 0);
            } else {
                // VL & EL
                remainingAfter = Number(this.leaveRequest.vl_remaining || 0);
            }

            return {
                before: remainingAfter + applied,
                applied,
                after: remainingAfter
            };
        },

        isExcessLeave() {
            return this.leaveBalanceComputed.after < 0;
        }










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

.leave_days {
    background-color: #b3cadc !important;
}

.remaining_balance {
    background-color: #80e183dc !important;
}

.screen-loader{
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45); /* dark overlay */
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 16px;
}

.loader-card{
  width: min(360px, 100%);
  background: #fff;
  border-radius: 16px;
  padding: 18px 20px;
  box-shadow: 0 20px 60px rgba(0,0,0,.18);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.loader-title{
  margin-top: 12px;
  font-weight: 700;
  font-size: 16px;
  color: #2b6777;
}

.loader-subtitle{
  margin-top: 6px;
  font-size: 13px;
  color: #475569;
  line-height: 1.4;
}

</style>
