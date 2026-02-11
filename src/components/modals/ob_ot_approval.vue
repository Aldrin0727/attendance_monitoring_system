<template>
    <div class="modal" v-if="isVisible">

        <div class="modal-dialog">
            <div class="modal-content">
                <div v-if="approving" class="screen-loader" role="dialog" aria-modal="true">
                    <div class="loader-card">
                        <div class="spinner-border" aria-hidden="true"></div>
                        <div class="loader-title">{{ loaderTitle }}</div>
                        <div class="loader-subtitle">{{ loaderSubtitle }}</div>
                    </div>
                </div>


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

  <!-- row 1 -->
  <div class="row g-3 mb-3">
    <div class="col-12 col-md-4">
      <label class="form-label label-sm">Reference Number</label>
      <input type="text" class="form-control" v-model="ob_ot_Request.ref_number" readonly />
    </div>

    <div class="col-12 col-md-4">
      <label class="form-label label-sm">Type</label>
      <input type="text" class="form-control" v-model="ob_ot_Request.type" readonly />
    </div>

    <div class="col-12 col-md-4">
      <label class="form-label label-sm">Category</label>
      <input type="text" class="form-control" v-model="ob_ot_Request.category" readonly />
    </div>
  </div>

  <!-- row 2 -->
  <div class="row g-3 mb-3">
    <div class="col-12 col-md-4">
      <label class="form-label label-sm">Destination</label>
      <input type="text" class="form-control" v-model="ob_ot_Request.destination" readonly />
    </div>

    <div class="col-12 col-md-4">
      <label class="form-label label-sm">Requested Date From</label>
      <input type="text" class="form-control" :value="formatDisplayDT(ob_ot_Request.req_from)" readonly />
    </div>

    <div class="col-12 col-md-4">
      <label class="form-label label-sm">Requested Date To</label>
      <input type="text" class="form-control" :value="formatDisplayDT(ob_ot_Request.req_to)" readonly />
    </div>
  </div>

  <!-- row 3: shops chips full width -->
  <div class="row g-3 mb-3" v-if="ob_ot_Request.destination === 'Shops' && shopList.length">
    <div class="col-12">
      <label class="form-label label-sm">Shop(s)</label>
      <div class="chips-wrap">
        <span class="chip" v-for="s in shopList" :key="s">{{ s }}</span>
      </div>
    </div>
  </div>

  <!-- row 4 -->
  <div class="row g-3">
    <div class="col-12 col-md-6">
      <label class="form-label label-sm">Reason</label>
      <textarea class="form-control" rows="2" v-model="ob_ot_Request.request_reason" readonly></textarea>
    </div>

    <div class="col-12 col-md-6">
      <label class="form-label label-sm">Project</label>
      <textarea class="form-control" rows="2" v-model="ob_ot_Request.project" readonly></textarea>
    </div>
  </div>
</div>


                    <!-- ACTUAL OB/OT DATE INPUTS (Visible Only When Approved) -->
                    <div class="section mt-3"
                        v-if="['APPROVED', 'PRE-APPROVED', 'FOR FINAL APPROVAL'].includes(ob_ot_Request.status)">
                        <div class="section-title">
                            Actual {{ ob_ot_Request.type }} Execution
                        </div>
                        <hr class="mt-0">

                        <div class="row">
                            <div class="col-5">
                                <label class="form-label label-sm">Actual Start Date & Time</label>
                                <input type="datetime-local" class="form-control" v-model="actualDates.actual_from"
                                    :readonly="isHrRecord || isActualDateReadOnly" />
                            </div>

                            <div class="col-5">
                                <label class="form-label label-sm">Actual End Date & Time</label>
                                <input type="datetime-local" class="form-control" v-model="actualDates.actual_to"
                                    :readonly="isHrRecord || isActualDateReadOnly" />
                            </div>

                            <div class="col-2">
                                <label class="form-label label-sm">Hours</label>
                                <input type="text" class="form-control total_hours" v-model="total_time" readonly />
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
                <div class="modal-footer justify-content-between">
                    <div v-if="canDownloadPdf">
                        <button class="btn btn-primary" @click="downloadPdf">
                            <i class="fas fa-print"></i> Print
                        </button>
                    </div>

                    <div v-if="canApprove">
                        <button class="btn btn-secondary me-2" @click="approveRequest"
                            :disabled="approving">Approve</button>
                        <button class="btn btn-danger" @click="denyRequest" :disabled="approving">Deny</button>
                    </div>


                    <button class="btn btn-secondary me-2" @click="finalApproval" v-if="canFinalApprove"
                        :disabled="approving">Approve</button>
                    <button class="btn btn-danger" @click="denyRequest" v-if="canFinalApprove"
                        :disabled="approving">Deny</button>

                    <div v-if="ob_ot_Request.status === 'PRE-APPROVED'">
                        <button class="btn btn-success me-2" @click="saveActualDates" :disabled="approving">
                            <span v-if="approving">Saving...</span>
                            <span v-else>Save Actual {{ ob_ot_Request.type }} Dates</span>
                        </button>
                    </div>

                </div>



                <ot_ob_print ref="pdfTemplate" :request="ob_ot_Request" v-show="showPdf" />


            </div>


        </div>
    </div>
</template>

<script>
import API_BASE from '@/utils/api_config';
import { getUserData } from '@/utils/get_user_data';
import html2pdf from "html2pdf.js";
import ot_ob_print from '../prints/ot_ob_print.vue';


export default {
    components: {
        ot_ob_print
    },

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
            showPdf: false,
            total_time: "",

            approving: false,
            loaderTitle: "Processing",
            loaderSubtitle: "Please wait...",

        };
    },

    computed: {
          shopList() {
    const raw = this.ob_ot_Request?.shop_location || "";
    return raw.split(",").map(s => s.trim()).filter(Boolean);
  },

        isHrRecord() {
            return this.ob_ot_Request.status === 'APPROVED';
        },
        isActualDateReadOnly() {
            return this.ob_ot_Request.status === 'FOR FINAL APPROVAL';
        },
        canApprove() {
            return (
                this.user.job_title === "Department Head" &&
                this.ob_ot_Request.status === "FOR PRE-APPROVAL"
            );
        },
        canFinalApprove() {
            return (
                this.user.job_title === "Department Head" &&
                this.ob_ot_Request.status === "FOR FINAL APPROVAL"
            );
        },
        canDownloadPdf() {
            return ["APPROVED"].includes(this.ob_ot_Request.status);
        }
    },

    watch: {
        ob_ot_Request: {
            immediate: true,
            deep: true,
            handler(val) {
                //   console.log('RAW actual_from:', val.actual_from);

                if (['FOR FINAL APPROVAL', 'APPROVED'].includes(val.status)) {
                    this.actualDates.actual_from =
                        this.formatForDateTimeLocal(val.actual_from);

                    this.actualDates.actual_to =
                        this.formatForDateTimeLocal(val.actual_to);

                    this.total_time = val.actual_hours || '';
                }
            }
        },

        "actualDates.actual_from"() {
            this.calculateHours();
        },
        "actualDates.actual_to"() {
            this.calculateHours();
        }
    },


    methods: {
        formatDateTime(date) {
            if (!date) return '';

            const parts = date.split(' ');
            const day = parts[1];
            const month = parts[2];
            const year = parts[3];
            const time = parts[4]; // 13:51:52

            return `${year}-${this.monthToNumber(month)}-${day} ${time}`;
        },

        downloadPdf() {
            this.showPdf = true;

            this.$nextTick(() => {
                const element = this.$refs.pdfTemplate.$el;

                html2pdf()
                    .set({
                        margin: 10,
                        filename: `${this.ob_ot_Request.ref_number}.pdf`,
                        image: { type: "jpeg", quality: 0.98 },
                        html2canvas: { scale: 2 },
                        jsPDF: { unit: "mm", format: "a4", orientation: "portrait" }
                    })
                    .from(element)
                    .save()
                    .then(() => {
                        this.showPdf = false;
                    });
            });
        },

        generateOBOTPdfBlob() {
            this.showPdf = true;

            return this.$nextTick().then(() => {
                const element = this.$refs.pdfTemplate.$el;

                return html2pdf()
                    .set({
                        margin: 10,
                        image: { type: "jpeg", quality: 0.98 },
                        html2canvas: { scale: 2, useCORS: true },
                        jsPDF: { unit: "mm", format: "a4", orientation: "portrait" }
                    })
                    .from(element)
                    .outputPdf("blob")
                    .then((blob) => {
                        this.showPdf = false;
                        return blob;
                    });
            });
        },



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
            return new Date(dt).toISOString().slice(0, 19).replace("T", " ");
        },


        approveRequest() {
            // this.submitDecision("APPROVED");
            this.submitDecision("PRE-APPROVED");
        },
        finalApproval() {
            // this.submitDecision("APPROVED");
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

            //  — Compute hours
            const diffMs = endDate - startDate;
            let diffMinutes = Math.floor(diffMs / (1000 * 60));

            let hours = Math.floor(diffMinutes / 60);
            let minutes = diffMinutes % 60;

            if (minutes < 10) minutes = "0" + minutes;

            this.total_time = `${hours}h ${minutes}m`;
        },

        // submitDecision(decision) {
        //     fetch(`${API_BASE}/update_approved_deny_otob`, {
        //         method: "POST",
        //         headers: { "Content-Type": "application/json" },
        //         body: JSON.stringify({
        //             args: decision,
        //             ref_number: this.ob_ot_Request.ref_number,
        //             user: `${this.user.first_name} ${this.user.last_name}`
        //         })
        //     })
        //         .then(res => res.json())
        //         .then(data => {
        //             if (data.success) {
        //                 Swal.fire("Success", `Request ${decision}`, "success");
        //                 this.$emit("updateDataTable");
        //                 this.closeModal();
        //             } else {
        //                 Swal.fire("Error", data.error || "Request failed", "error");
        //             }
        //         })
        //         .catch(err => {
        //             console.error(err);
        //             Swal.fire("Error", "Something went wrong", "error");
        //         });
        // },

        async submitDecision(decision) {
            if (this.approving) return;

            this.approving = true;
            this.loaderTitle = "Processing approval";
            this.loaderSubtitle = decision === "APPROVED"
                ? "Please wait while we generate PDF & send the email."
                : "Please wait while we update the request status.";

            try {
                let pdfBlob = null;
                if (decision === "APPROVED") {
                    pdfBlob = await this.generateOBOTPdfBlob();
                }

                const fd = new FormData();
                fd.append("args", decision);
                fd.append("ref_number", this.ob_ot_Request.ref_number);
                fd.append("user", `${this.user.first_name} ${this.user.last_name}`);
                // fd.append("emp_id", this.ob_ot_Request.emp_id);
                fd.append("emp_id", this.user.emp_id);

                if (pdfBlob) {
                    fd.append("pdf", pdfBlob, `${this.ob_ot_Request.ref_number}.pdf`);
                }

                const res = await fetch(`${API_BASE}/update_approved_deny_otob`, {
                    method: "POST",
                    body: fd,
                });

                const data = await res.json();
                if (!res.ok || !data.success) throw new Error(data.error || "Request failed");

                await Swal.fire({
                    icon: "success",
                    title: `Request ${decision}`,
                    html: decision === "APPROVED" ? "<b>Email sent to HR.</b>" : "",
                    confirmButtonColor: "#28a745",
                });

                this.$emit("updateDataTable");
                this.closeModal();

            } catch (err) {
                Swal.fire("Error", err?.message || "Something went wrong", "error");
            } finally {
                this.approving = false;
                this.loaderTitle = "Processing";
                this.loaderSubtitle = "Please wait...";
            }
        },




        // formatDateTime2(date) {
        //     if (!date) return '';

        //     const d = new Date(date);

        //     const year = d.getFullYear();
        //     const month = String(d.getMonth() + 1).padStart(2, '0');
        //     const day = String(d.getDate()).padStart(2, '0');

        //     const hours = String(d.getHours()).padStart(2, '0');
        //     const minutes = String(d.getMinutes()).padStart(2, '0');
        //     const seconds = String(d.getSeconds()).padStart(2, '0');

        //     return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        // },

        formatForDateTimeLocal(value) {
            if (!value) return '';

            const d = new Date(value);

            const year = d.getUTCFullYear();
            const month = String(d.getUTCMonth() + 1).padStart(2, '0');
            const day = String(d.getUTCDate()).padStart(2, '0');
            const hours = String(d.getUTCHours()).padStart(2, '0');
            const minutes = String(d.getUTCMinutes()).padStart(2, '0');

            return `${year}-${month}-${day}T${hours}:${minutes}`;
        },

        async saveActualDates() {
            if (this.approving) return;

            if (!this.actualDates.actual_from || !this.actualDates.actual_to) {
                Swal.fire("Missing Fields", "Please provide both Actual Start and Actual End.", "warning");
                return;
            }

            this.approving = true;
            this.loaderTitle = "Saving actual dates";
            this.loaderSubtitle = "Please wait while we save actual dates & notify your Department Head.";

            try {
                const payload = {
                    ref_number: this.ob_ot_Request.ref_number,
                    actual_from: this.formatDateTime(this.actualDates.actual_from),
                    actual_to: this.formatDateTime(this.actualDates.actual_to),
                    actual_hours: this.total_time,
                    user: `${this.user.first_name} ${this.user.last_name}`
                };

                const res = await fetch(`${API_BASE}/update_actual_date`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });

                const data = await res.json();
                if (!res.ok || !data.success) throw new Error(data.error || "Failed to save actual dates.");

                await Swal.fire({
                    icon: "success",
                    title: `${this.ob_ot_Request.type} Actual Dates Saved`,
                    text: `Total Time: ${this.total_time}`,
                    confirmButtonColor: "#28a745",
                });

                this.$emit("updateDataTable");
                this.closeModal();

            } catch (err) {
                Swal.fire("Error", err?.message || "Something went wrong while saving.", "error");
            } finally {
                this.approving = false;
                this.loaderTitle = "Processing";
                this.loaderSubtitle = "Please wait...";
            }
        },

        formatDisplayDT(dt) {
    if (!dt) return "";
    const d = new Date(dt);
    if (isNaN(d.getTime())) return String(dt);

    // output: MM/DD/YYYY hh:mm AM/PM
    return d.toLocaleString("en-US", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true
    });
  },

  // for API payload saving actual dates (datetime-local -> ISO-ish)
  toBackendDT(dtLocal) {
    if (!dtLocal) return null;
    const d = new Date(dtLocal);
    return d.toISOString().slice(0, 19).replace("T", " "); // yyyy-mm-dd HH:MM:SS
  },


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

.pdf-hidden {
    position: fixed;
    top: 0;
    left: 0;
    opacity: 0;
    pointer-events: none;
    z-index: -1;
}

.screen-loader {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.45);
    /* dark overlay */
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    padding: 16px;
}

.loader-card {
    width: min(360px, 100%);
    background: #fff;
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, .18);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.loader-title {
    margin-top: 12px;
    font-weight: 700;
    font-size: 16px;
    color: #2b6777;
}

.loader-subtitle {
    margin-top: 6px;
    font-size: 13px;
    color: #475569;
    line-height: 1.4;
}

.chips-wrap {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 10px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    min-height: 42px;
}

.chip {
    display: inline-flex;
    align-items: center;
    padding: 6px;
    border-radius: 999px;
    border: 1px solid rgba(43, 103, 119, .25);
    background: rgba(90, 197, 197, .12);
    color: #2b6777;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .2px;
}
</style>
