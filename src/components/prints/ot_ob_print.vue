<template>
    <div class="pdf-wrapper">

        <!-- HEADER -->
        <div class="header">
            <h2>{{ request.type }} REQUEST FORM</h2>
            <p class="subtitle">For HR Record</p>
        </div>

        <!-- USER INFORMATION -->
        <div class="card">
            <div class="card-title">USER INFORMATION</div>

            <div class="grid-1">
                <div class="field">
                    <label>NAME</label>
                    <div class="value">{{ request.fullName }}</div>
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

        <!-- OT REQUEST -->
        <div class="card">
            <div class="card-title">{{ request.type }} REQUEST DETAILS</div>

            <div class="grid-3">
                <div class="field">
                    <label>Reference Number</label>
                    <div class="value">{{ request.ref_number }}</div>
                </div>
                <div class="field">
                    <label>Type</label>
                    <div class="value">{{ request.type }}</div>
                </div>
                <div class="field">
                    <label>Category</label>
                    <div class="value">{{ request.category }}</div>
                </div>
            </div>

            <div class="grid-3 mt-3">
                <div class="field">
                    <label>Destination</label>
                    <div class="value">{{ request.destination }}</div>
                </div>
                <div class="field">
                    <label>Requested Date From</label>
                    <div class="value">{{ format(request.req_from) }}</div>
                </div>
                <div class="field">
                    <label>Requested Date To</label>
                    <div class="value">{{ format(request.req_to) }}</div>
                </div>
            </div>

            <div class="grid-2 mt-3">
                <div class="field">
                    <label>Reason</label>
                    <div class="value box">{{ request.reason || '-' }}</div>
                </div>
                <div class="field">
                    <label>Project</label>
                    <div class="value box">{{ request.project || '-' }}</div>
                </div>
            </div>
        </div>

        <!-- APPROVER -->
        <div class="card">
            <div class="card-title">Actual {{ request.type }} Execution</div>

            <div class="grid-3">
                <div class="field">
                    <label>Actual Start Date & Time</label>
                    <div class="value">{{ format(request.actual_from) }}</div>
                </div>
                <div class="field">
                    <label>Actual End Date & Time</label>
                    <div class="value">{{ format(request.actual_to) }}</div>
                </div>
                <div class="field">
                    <label>Hours</label>
                    <div class="value">{{ request.actual_hours }}</div>
                </div>
            </div>
        </div>

        <!-- APPROVER -->
        <div class="card">
            <div class="card-title">APPROVER</div>

            <div class="grid-2">
                <div class="field">
                    <label>Approved By</label>
                    <div class="value">{{ request.approved_by }}</div>
                </div>
                <div class="field">
                    <label>Date Approved</label>
                    <div class="value">{{ format(request.date_approved) }}</div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
export default {
    props: {
        request: Object
    },
    methods: {
        format(value) {
            if (!value) return '-';

            // Case 1: MySQL datetime
            if (typeof value === 'string' && value.includes('-') && value.includes(':')) {
                return value.replace('T', ' ').replace(' GMT', '').slice(0, 16);
            }

            // Case 2: JS Date string (Fri, 12 Dec 2025 13:39:00 GMT)
            const d = new Date(value);
            
            const year = d.getUTCFullYear();
            const month = String(d.getUTCMonth() + 1).padStart(2, '0');
            const day = String(d.getUTCDate()).padStart(2, '0');
            const hours = String(d.getUTCHours()).padStart(2, '0');
            const minutes = String(d.getUTCMinutes()).padStart(2, '0');


            return `${year}-${month}-${day} ${hours}:${minutes}`;
        }

    }
};
</script>

<style scoped>
.pdf-wrapper {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    color: #222;
}

/* HEADER */
.header {
    text-align: center;
    margin-bottom: 22px;
}

.header h2 {
    margin: 0;
    font-size: 24px;
    letter-spacing: 0.6px;
    font-weight: bold;
    color: #66bcb4;
}

.subtitle {
    font-size: 12px;
    color: #666;
    margin-top: 4px;
}

.header-divider {
    margin: 12px auto 0;
    width: 80%;
    border-bottom: 1px solid #ddd;
}


/* CARD */
.card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 16px;
    background-color: #fafbfc;
}

.card-title {
    font-size: 12px;
    font-weight: 700;
    color: #6b7280;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: 6px;
}

/* GRID SYSTEM */
.grid-1 {
    display: grid;
    grid-template-columns: 1fr;
    gap: 10px;
}

.grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-top: 10px;
}

.grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 10px;
}

/* FIELD */
.field label {
    font-size: 10px;
    font-weight: 700;
    color: #2b6777;
    text-transform: uppercase;
    margin-bottom: 4px;
    display: block;
}

.value {
    background: #f1f3f5;
    border-radius: 4px;
    padding: 8px 10px;
    font-size: 12px;
}

.value.box {
    min-height: 40px;
}
</style>
