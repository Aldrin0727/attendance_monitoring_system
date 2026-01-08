<template>
    <div class="modal" v-if="isVisible">
        <div class="modal-dialog">
            <div class="modal-content">

                <div class="modal-header py-1">
                    <font-awesome-icon :icon="['fas', 'circle-plus']" class="font-awesome-icon" />
                    <h5 class="modal-title">Add Holiday</h5>
                    <button type="button" class="btn-close" @click="close"></button>
                </div>

                <form @submit.prevent="submitHoliday">
                    <div class="modal-body">

                        <div class="row mb-3">
                            <div class="col-12">
                                <label class="form-label label-sm">
                                    Holiday Name <span style="color:red">*</span>
                                </label>
                                <input type="text" class="form-control" v-model="form.holiday_name" required />
                            </div>
                        </div>

                        <div class="row mb-1">
                            <div class="col-6">
                                <label class="form-label label-sm">
                                    Holiday Date <span style="color:red">*</span>
                                </label>

                                <div class="date-wrap">
                                    <!-- Display only -->
                                    <input type="text" class="form-control fake-date" :value="holidayDateNoYear"
                                        placeholder="Select date" readonly />

                                    <!-- MM-DD muted suffix -->
                                    <span class="date-suffix">MM-DD</span>

                                    <!-- Calendar icon -->
                                    <span class="date-icon">
                                        <i class="fas fa-calendar-alt"></i>
                                    </span>

                                    <!-- REAL date input (clickable) -->
                                    <input type="date" class="real-date" v-model="form.holiday_date" required />
                                </div>

                                <small v-if="holidayDateExists" class="text-danger"
                                    style="font-size:12px; display:block; margin-top:4px;">
                                    Holiday already exists on this date.
                                </small>
                            </div>

                            <div class="col-6">
                                <label class="form-label label-sm">Status <span style="color:red">*</span></label>
                                <select class="form-select" v-model="form.status">
                                    <option value="ACTIVE">ACTIVE</option>
                                    <option value="INACTIVE">INACTIVE</option>
                                </select>
                            </div>
                        </div>


                    </div>

                    <div class="modal-footer d-flex justify-content-end">
                        <!-- <button type="button" class="btn btn-secondary" @click="close" :disabled="saving">
                            Close
                        </button> -->

                        <button type="submit" class="btn btn-success" :disabled="saving || holidayDateExists">
                            <span v-if="saving">
                                <i class="fas fa-spinner fa-spin"></i>&nbsp;Adding...
                            </span>
                            <span v-else>Add</span>
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
    name: "add_holiday_modal",
    props: {
        isVisible: { type: Boolean, required: true },

        // pass user object from parent para may created_by
        user: { type: Object, required: true },

        // pass Set (or Array) of existing holiday dates para ma-block duplicates
        holidaySet: { type: [Object, Array], default: () => new Set() }
    },
    data() {
        return {
            saving: false,
            form: {
                holiday_name: "",
                holiday_date: "",
                holiday_mmdd: "",   // MM-DD (for saving/checking)
                status: "ACTIVE"
            }
        };
    },
    watch: {
        isVisible(val) {
            if (val) this.resetForm();
        },
        "form.holiday_date"(val) {
            this.form.holiday_mmdd = val ? val.slice(5) : ""; // => "01-08"
        }
    },
    computed: {
        holidayDateNoYear() {
            return this.form.holiday_mmdd || "";
        },

        holidayDateExists() {
            if (!this.form.holiday_mmdd) return false;

            // ✅ check using MM-DD
            if (this.holidaySet && typeof this.holidaySet.has === "function") {
                return this.holidaySet.has(this.form.holiday_mmdd);
            }
            if (Array.isArray(this.holidaySet)) {
                return this.holidaySet.includes(this.form.holiday_mmdd);
            }
            return false;
        }
    },
    methods: {
        openNativePicker() {
            const el = this.$refs.holidayDate;
            if (!el) return;

            // modern browsers
            if (el.showPicker) el.showPicker();
            else el.focus();
        },
        resetForm() {
            this.saving = false;
            this.form = {
                holiday_name: "",
                holiday_date: "",
                status: "ACTIVE"
            };
        },

        close() {
            this.$emit("close");
        },

        submitHoliday() {
            console.log( this.form.holiday_mmdd)
            if (!this.form.holiday_name || !this.form.holiday_mmdd) {
                Swal.fire("Invalid", "Holiday name and date are required.", "warning");
                return;
            }

            if (this.holidayDateExists) {
                Swal.fire("Duplicate", "Holiday already exists on that date.", "warning");
                return;
            }

            this.saving = true;

            fetch(`${API_BASE}/add_holiday`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    holiday_name: this.form.holiday_name,
                    holiday_date: this.form.holiday_mmdd,
                    status: this.form.status,
                    created_by: `${this.user.first_name} ${this.user.last_name}`.trim()
                })
            })
                .then((res) => res.json())
                .then((data) => {
                    if (!data.success) throw new Error(data.error || "Failed to create holiday");

                    Swal.fire("Success", "Holiday added successfully.", "success");

                    // inform parent to refresh
                    this.$emit("saved");
                    this.$emit("close");
                })
                .catch((err) => {
                    Swal.fire("Error", err.message || "Something went wrong", "error");
                })
                .finally(() => {
                    this.saving = false;
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
    cursor: pointer;
    z-index: 3;
    color: #6c757d;
    pointer-events: none;
    font-size: 14px;
}

.date-suffix {
    position: absolute;
    right: 42px;
    /* left of the calendar icon */
    top: 50%;
    transform: translateY(-50%);
    z-index: 3;
    color: #9ca3af;
    /* muted */
    font-size: 12px;
    pointer-events: none;
}


/* REAL date input (clickable but invisible) */
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
