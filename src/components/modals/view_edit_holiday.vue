<template>
    <div class="modal" v-if="isVisible">
        <div class="modal-dialog">
            <div class="modal-content">

                <div class="modal-header py-1">
                    <font-awesome-icon :icon="['fas', mode === 'edit' ? 'pen-to-square' : 'eye']"
                        class="font-awesome-icon" />
                    <h5 class="modal-title">
                        {{ mode === "edit" ? "Edit Holiday" : "View Holiday" }}
                    </h5>
                    <button type="button" class="btn-close" @click="close"></button>
                </div>

                <form @submit.prevent="save" v-if="form">
                    <div class="modal-body">

                        <div class="row mb-3">
                            <div class="col-12">
                                <label class="form-label label-sm">Holiday Name <span style="color:red">*</span></label>
                                <input type="text" class="form-control" v-model="form.holiday_name" :readonly="isView"
                                    required />
                            </div>
                        </div>

                        <div class="row mb-1">
                            <div class="col-6">
                                <label class="form-label label-sm">Holiday Date <span style="color:red">*</span></label>

                                <div class="date-wrap">
                                    <!-- Display only -->
                                    <input type="text" class="form-control fake-date" :value="holidayDateNoYear"
                                        placeholder="Select date" readonly />

                                    <span class="date-suffix">MM-DD</span>

                                    <span class="date-icon">
                                        <i class="fas fa-calendar-alt"></i>
                                    </span>

                                    <!-- real date input only enabled in edit mode -->
                                    <input v-if="!isView" type="date" class="real-date" v-model="form.holiday_date_full"
                                        required />
                                </div>

                                <small v-if="!isView && holidayDateExists" class="text-danger"
                                    style="font-size:12px; display:block; margin-top:4px;">
                                    Holiday already exists on this date.
                                </small>
                            </div>

                            <div class="col-6">
                                <label class="form-label label-sm">Status <span style="color:red">*</span></label>
                                <select class="form-select" v-model="form.status" :disabled="isView">
                                    <option value="ACTIVE">ACTIVE</option>
                                    <option value="INACTIVE">INACTIVE</option>
                                </select>
                            </div>
                        </div>

                    </div>

                    <div class="modal-footer d-flex justify-content-end gap-2">
                        <!-- Close button: VIEW only -->
                        <button v-if="isView" type="button" class="btn btn-secondary" @click="close">
                            Close
                        </button>

                        <!-- Save button: EDIT only -->
                        <button v-if="!isView" type="submit" class="btn btn-success"
                            :disabled="saving || holidayDateExists">
                            <span v-if="saving">
                                <i class="fas fa-spinner fa-spin"></i>&nbsp;Saving...
                            </span>
                            <span v-else>Save</span>
                        </button>
                    </div>


                </form>

            </div>
        </div>
    </div>
</template>

<script>
import API_BASE from "@/utils/api_config";

export default {
    name: "holiday_modal",
    props: {
        isVisible: { type: Boolean, required: true },
        user: { type: Object, required: true },
        holiday: { type: Object, default: null }, // selected row
        mode: { type: String, default: "view" },  // "view" | "edit"
        holidaySet: { type: [Object, Array], default: () => new Set() }
    },
    data() {
        return {
            saving: false,
            form: null
        };
    },
    computed: {
        isView() {
            return this.mode === "view";
        },

        // show MM-DD only (no year)
        holidayDateNoYear() {
            if (!this.form?.holiday_date_full) return "";
            const d = new Date(this.form.holiday_date_full);
            if (isNaN(d.getTime())) return "";

            const mm = String(d.getMonth() + 1).padStart(2, "0");
            const dd = String(d.getDate()).padStart(2, "0");
            return `${mm}-${dd}`;
        },

        // block duplicates (except itself)
        holidayDateExists() {
            if (!this.form?.holiday_date_full) return false;

            const mmdd = this.toMMDD(this.form.holiday_date_full);
            const selfOld = this.toMMDD(this.form._original_date_full);

            // if same as original (editing existing), allow
            if (mmdd && selfOld && mmdd === selfOld) return false;

            if (this.holidaySet && typeof this.holidaySet.has === "function") {
                return this.holidaySet.has(mmdd);
            }
            if (Array.isArray(this.holidaySet)) {
                return this.holidaySet.includes(mmdd);
            }
            return false;
        }
    },
    watch: {
        isVisible(val) {
            if (val) this.loadForm();
        },
        holiday: {
            deep: true,
            handler() {
                if (this.isVisible) this.loadForm();
            }
        }
    },
    methods: {
        toMMDD(dateStr) {
            if (!dateStr) return "";
            const d = new Date(dateStr);
            if (isNaN(d.getTime())) return "";
            const mm = String(d.getMonth() + 1).padStart(2, "0");
            const dd = String(d.getDate()).padStart(2, "0");
            return `${mm}-${dd}`;
        },

        mmddToFullDate(mmdd) {
            if (!mmdd) return "";
            const [mm, dd] = String(mmdd).split("-");
            if (!mm || !dd) return "";
            const y = new Date().getFullYear(); // just for picker
            return `${y}-${mm.padStart(2, "0")}-${dd.padStart(2, "0")}`;
        },

        loadForm() {
            if (!this.holiday) {
                this.form = null;
                return;
            }

            const full = this.mmddToFullDate(this.holiday.holiday_date);

            this.form = {
                id: this.holiday.id,
                holiday_name: this.holiday.holiday_name || "",
                status: this.holiday.status || "ACTIVE",
                holiday_date_full: full,          // for date picker
                _original_date_full: full         // for duplicate check
            };
        },

        close() {
            this.$emit("close");
        },

        save() {
            if (this.isView) return;

            if (!this.form.holiday_name || !this.form.holiday_date_full) {
                Swal.fire("Invalid", "Holiday name and date are required.", "warning");
                return;
            }

            if (this.holidayDateExists) {
                Swal.fire("Duplicate", "Holiday already exists on that date.", "warning");
                return;
            }

            // submit as MM-DD only (no year)
            const holiday_date = this.toMMDD(this.form.holiday_date_full);

            Swal.fire({
                title: "Are you sure?",
                html: `
      You are about to update this holiday:<br><br>
      <div style="text-align:left; font-size:13px;">
        <b>Name:</b> ${this.form.holiday_name}<br>
        <b>Date:</b> ${holiday_date} <span style="color:#6b7280">(MM-DD)</span><br>
        <b>Status:</b> ${this.form.status}<br>
      </div>
    `,
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "Yes, update",
                cancelButtonText: "Cancel",
                confirmButtonColor: "#28a745",
            }).then((result) => {
                if (!result.isConfirmed) return;

                this.saving = true;

                fetch(`${API_BASE}/update_holiday`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        id: this.form.id,
                        holiday_name: this.form.holiday_name,
                        holiday_date: holiday_date, // MM-DD
                        status: this.form.status,
                        updated_by: `${this.user.first_name} ${this.user.last_name}`.trim(),
                    }),
                })
                    .then((res) => res.json())
                    .then((data) => {
                        if (!data.success) throw new Error(data.error || "Update failed");

                        Swal.fire("Success", "Holiday updated successfully.", "success");
                        this.$emit("saved");
                    })
                    .catch((err) => {
                        Swal.fire("Error", err.message || "Something went wrong", "error");
                    })
                    .finally(() => {
                        this.saving = false;
                    });
            });
        }

    }
};
</script>

<style scoped>
@import url(../../assets/css/modal.css);
@import url(../../assets/css/buttons.css);
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

.date-wrap {
    position: relative;
}

.fake-date {
    padding-right: 38px;
    cursor: pointer;
    pointer-events: none;
}

.date-icon {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 3;
    color: #6c757d;
    pointer-events: none;
    font-size: 14px;
}

.date-suffix {
    position: absolute;
    right: 42px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 3;
    color: #9ca3af;
    font-size: 12px;
    pointer-events: none;
}

/* only shown in edit mode via v-if */
.real-date {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    z-index: 4;
    cursor: pointer;
}
</style>
