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
                    <label>Date Created</label>
                    <div class="value">{{ formatApproved(request.date_created) }}</div>
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

          <!-- SHOPS (only if destination is Shops) -->
            <div class="mt-3" v-if="request.destination === 'Shops' && shopList.length">
                <div class="field">
                    <label>Shop(s)</label>
                    <div class="chips-wrap">
                        <span class="chip" v-for="s in shopList" :key="s">{{ s }}</span>
                    </div>
                </div>
            </div>

            <div class="grid-2 mt-3">
                <div class="field">
                    <label>Reason</label>
                    <div class="value box">{{ request.request_reason || '-' }}</div>
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
            <div class="card-title">APPROVAL</div>

            <div class="grid-3">
                <div class="field">
                    <label>Approved By</label>
                    <div class="value">{{ request.approved_by }}</div>
                </div>
               <div class="field">
                    <label>Date Approved</label>
                    <div class="value">{{ formatApproved(request.date_approved) }}</div>
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
    props: {
        request: Object
    },
     computed: {
    shopList() {
      const raw = this.request?.shop_location || "";
      return raw.split(",").map(s => s.trim()).filter(Boolean);
    }
  },
  methods: {
  monthToNumber(mon) {
    const m = {
      Jan: "01", Feb: "02", Mar: "03", Apr: "04",
      May: "05", Jun: "06", Jul: "07", Aug: "08",
      Sep: "09", Oct: "10", Nov: "11", Dec: "12"
    };
    return m[mon] || "01";
  },

  // returns "YYYY-MM-DD HH:MM:SS" (no timezone conversion)
  toMySQLDateTime(value) {
    if (!value) return "";

    const s = String(value).trim();

    // MySQL: "YYYY-MM-DD HH:MM:SS" or "YYYY-MM-DD HH:MM"
    if (/^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}/.test(s)) {
      return s.length >= 19 ? s.slice(0, 19) : (s + ":00").slice(0, 19);
    }

    // ISO: "YYYY-MM-DDTHH:MM:SS" or "YYYY-MM-DDTHH:MM"
    if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(s)) {
      const base = s.replace("T", " ");
      return base.length >= 19 ? base.slice(0, 19) : (base + ":00").slice(0, 19);
    }

    // RFC: "Wed, 12 Feb 2026 14:47:00 GMT" (NO timezone conversion)
    const rfc = s.match(
      /^[A-Za-z]{3},\s(\d{1,2})\s([A-Za-z]{3})\s(\d{4})\s(\d{2}):(\d{2})(?::(\d{2}))?/
    );
    if (rfc) {
      const dd = String(rfc[1]).padStart(2, "0");
      const mm = this.monthToNumber(rfc[2]);
      const yyyy = rfc[3];
      const HH = rfc[4];
      const MM = rfc[5];
      const SS = rfc[6] || "00";
      return `${yyyy}-${mm}-${dd} ${HH}:${MM}:${SS}`;
    }

    return s; // fallback para makita mo pa rin raw format
  },

// outputs: "YYYY-MM-DD HH:MM:SS"  ✅ SAME as approval
format(value) {
  if (!value) return "-";
  const dt = this.toMySQLDateTime(value);
  if (!dt) return "-";
  return dt.slice(0, 19); // YYYY-MM-DD HH:MM:SS
},

  // Used for date_created/date_approved in PDF (military with seconds)
  // outputs: "YYYY-MM-DD HH:MM:SS"
  formatApproved(dt) {
    if (!dt) return "";
    const out = this.toMySQLDateTime(dt);
    return out || "";
  }
}

};
</script>

<style scoped>
@import url(../../assets/css/print.css);
</style>
