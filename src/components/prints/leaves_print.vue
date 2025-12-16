<template>
    <div class="pdf-wrapper">

        <!-- HEADER -->
        <div class="header">
            <h2>LEAVE REQUEST FORM</h2>
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

            <div class="grid-2">
                <div class="field">
                    <label>Date From</label>
                    <div class="value">{{ formatDate(request.leave_from) }}</div>
                </div>
                <div class="field">
                    <label>Date To</label>
                    <div class="value">{{ formatDate(request.leave_to) }}</div>
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
                    <div class="value">{{ formatDate(request.date_approved) }}</div>
                </div>
                <div class="field">
                    <label>Status</label>
                    <div class="value">{{ request.status }}</div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
export default {
    props: { request: Object },
    computed: {
        leaveType() {
            const map = {
                VL: 'Vacation Leave',
                SL: 'Sick Leave',
                EL: 'Emergency Leave'
            }
            return map[this.request.leave_type] || this.request.leave_type
        }
    },
    methods: {
        formatDate(d) {
            if (!d) return '-'
            const date = new Date(d)
            return date.toLocaleDateString('en-GB') // dd/mm/yyyy
        }
    }
}
</script>

<style scoped>
@import url(../../assets/css/print.css);
</style>
