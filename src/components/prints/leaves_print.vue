<template>
    <div class="pdf-wrapper">

        <!-- HEADER -->
        <div class="header">
            <h2>{{ leaveType }} Form</h2>
            <p class="subtitle">For HR Record</p>
        </div>

        <!-- USER INFO -->
        <div class="card">
            <div class="card-title">USER INFORMATION</div>

            <div class="grid-1">
                <div class="field">
                    <label>NAME</label>
                    <div class="value">{{ request.user }}</div>
                </div>
            </div>

            <div class="grid-2">
                <div class="field">
                    <label>Position</label>
                    <div class="value">{{ request.position }}</div>
                </div>
                <div class="field">
                    <label>Department</label>
                    <div class="value">{{ request.department }}</div>
                </div>
            </div>

            <div class="grid-2">
                <div class="field">
                    <label>Address</label>
                    <div class="value">{{ request.address }}</div>
                </div>
                <div class="field">
                    <label>Contact Number</label>
                    <div class="value">{{ request.contact }}</div>
                </div>
            </div>
        </div>

        <!-- LEAVE DETAILS -->
        <div class="card">
            <div class="card-title mb-0">LEAVE DETAILS</div>

            <div class="grid-3">
                <div class="field">
                    <label>Reference No</label>
                    <div class="value">{{ request.ref_no }}</div>
                </div>
                <div class="field">
                    <label>Leave Type</label>
                    <div class="value">{{ leaveType }}</div>
                </div>
                <div class="field">
                    <label>Total Days</label>
                    <div class="value">{{ request.leave_number }}</div>
                </div>
            </div>

            <div class="grid-3">
                <div class="field">
                    <label>Date Submitted</label>
                    <div class="value">{{ formatDateTime(request.date_created) }}</div>
                </div>
                <div class="field">
                    <label>Date From</label>
                    <div class="value">{{ formatDate2(request.leave_from) }}</div>
                </div>
                <div class="field">
                    <label>Date To</label>
                    <div class="value">{{ formatDate2(request.leave_to) }}</div>
                </div>
            </div>

            <div class="grid-1 mt-3">
                <div class="field">
                    <label>Reason</label>
                    <div class="value box">{{ request.leave_reason || '-' }}</div>
                </div>
            </div>
        </div>

        <!-- APPROVAL -->
        <div class="card">
            <div class="card-title mb-0">APPROVAL</div>

            <div class="grid-3">
                <div class="field">
                    <label>Approved By</label>
                    <div class="value">{{ request.approved_by || '-' }}</div>
                </div>
                <div class="field">
                    <label>Date Approved</label>
                    <div class="value">{{ formatDateTime(request.date_approved) }}</div>
                </div>
                <div class="field">
                    <label>Status</label>
                    <div class="value">{{ request.status }}</div>
                </div>
            </div>
        </div>

        <!-- LEAVE BALANCE SUMMARY -->
        <div class="card">
            <div class="card-title mb-0">LEAVE BALANCE SUMMARY</div>

            <div class="grid-3">
                <div class="field">
                    <label>
                        Balance Before
                        <small>({{ leaveType }})</small>
                    </label>
                    <div class="value">
                        {{ balanceBefore }}
                    </div>
                </div>

                <div class="field">
                    <label>Leave Applied</label>
                    <div class="value">
                        {{ leaveApplied }}
                    </div>
                </div>

                <div class="field">
                    <label>Remaining Balance</label>
                    <div class="value" :class="{ 'text-danger': Number(balanceAfter) < 0 }">
                        {{ balanceAfter }}
                    </div>
                </div>
            </div>

            <small v-if="Number(balanceAfter) < 0" class="text-danger"
                style="font-weight:600; margin-top:6px; display:block;">
                ⚠ Excess leave subject to salary deduction
            </small>
        </div>

        <!-- LAST APPROVED LEAVE TAKEN -->
        <div class="card">
            <div class="card-title mb-0">LEAVE HISTORY</div>

            <div class="grid-2">
                <div class="field MT-3">
                    <label>Last Approved Leave Taken</label>
                    <div class="value">{{ lastApprovedLeaveTaken || '-'}}</div>
                    <!-- <div class="value">{{ formatDate2(lastApprovedLeaveTaken)  }}</div> -->
                    <!-- <small style="display:block;margin-top:6px;color:#6b7280;">
                        Based on the most recent approved leave (same leave type) that already ended.
                    </small> -->
                </div>
            </div>
        </div>

    </div>
</template>

<script>
export default {
    props: { 
        request: Object,
          lastApprovedLeaveTaken: [String, Date, null]
    },
    computed: {
        leaveType() {
            const map = { VL: "Vacation Leave", SL: "Sick Leave", EL: "Emergency Leave" };
            return map[this.request.leave_type] || this.request.leave_type;
        },

        // Leave applied (safe number)
        leaveApplied() {
            return Number(this.request.leave_number || 0);
        },

        // Remaining AFTER approval (galing DB)
        remainingAfter() {
            if (this.request.leave_type === "SL") {
                return Number(this.request.sl_remaining || 0);
            }
            // VL & EL share VL balance
            return Number(this.request.vl_remaining || 0);
        },

        // Balance After = stored remaining (AFTER approval)
        balanceAfter() {
            return this.remainingAfter;
        },

        // Balance Before = remainingAfter + leaveApplied
        balanceBefore() {
            return this.remainingAfter + this.leaveApplied;
        },

      

 
    },

    methods: {
        formatDate(d) {
            if (!d) return '-'
            const date = new Date(d)
            return date.toLocaleDateString('en-PH') // dd/mm/yyyy
        },

        formatDate2(d) {
            if (!d) return "-";

            const date = new Date(String(d).trim());
            if (isNaN(date.getTime())) return "-";

            const y = date.getUTCFullYear();
            const m = String(date.getUTCMonth() + 1).padStart(2, "0");
            const day = String(date.getUTCDate()).padStart(2, "0");

            return `${y}-${m}-${day}`;
        },


        formatDateTime(date) {
            if (!date) return '';

            // Example input:
            // "Thu, 18 Dec 2025 13:51:52 GMT"

            const parts = date.split(' ');
            const day = parts[1];
            const month = parts[2];
            const year = parts[3];
            const time = parts[4]; // 13:51:52

            return `${year}-${this.monthToNumber(month)}-${day} ${time}`;
        },

//         formatDateTime(date) {
//   if (!date) return '-';

//   const d = new Date(date);
//   if (isNaN(d.getTime())) return '-';

//   const pad = (n) => String(n).padStart(2, '0');
//   return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
// },


        monthToNumber(month) {
            const map = {
                Jan: '01', Feb: '02', Mar: '03', Apr: '04',
                May: '05', Jun: '06', Jul: '07', Aug: '08',
                Sep: '09', Oct: '10', Nov: '11', Dec: '12'
            };
            return map[month];
        },

    }
}
</script>

<style scoped>
@import url(../../assets/css/print.css);
</style>
