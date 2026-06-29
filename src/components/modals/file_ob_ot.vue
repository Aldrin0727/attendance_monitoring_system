<template>
  <div class="modal" v-if="isVisible">
    <div class="modal-dialog">
      <div class="modal-content">
        <!-- Modal Header -->
        <div class="modal-header py-1">
          <font-awesome-icon :icon="['fas', 'circle-plus']" class="font-awesome-icon" />
          <h5 class="modal-title">Request Form</h5>
          <button type="button" class="btn-close" @click="closeModal" aria-label="Close" :disabled="submitting"></button>
        </div>

        <!-- Form -->
        <form @submit.prevent="submitForm">
          <div class="modal-body pb-0">
            <!-- User Information -->
            <div class="section">
              <div class="section-title">User Information</div>
              <hr class="mt-0" />
              <div class="row">
                <div class="col-12 mb-3">
                  <label for="user" class="form-label label-sm">USER</label>
                  <input type="text" id="user" class="form-control" v-model="fullName" readonly />
                </div>
              </div>
              <div class="row mb-3">
                <div class="col-6">
                  <label for="position" class="form-label label-sm">Position</label>
                  <input type="text" id="position" class="form-control" v-model="user.position" readonly />
                </div>
                <div class="col-6">
                  <label for="department" class="form-label label-sm">Department</label>
                  <input type="text" id="department" class="form-control" v-model="user.department_name" readonly />
                </div>
              </div>
              <div class="row mb-1">
                <div class="col-6">
                  <label for="address" class="form-label label-sm">Address</label>
                  <input type="text" id="address" class="form-control" v-model="user.address" readonly />
                </div>
                <div class="col-6">
                  <label for="contact" class="form-label label-sm">Contact Number</label>
                  <input type="text" id="contact" class="form-control" v-model="user.contact" readonly />
                </div>
              </div>
            </div>

            <!-- OT/OB Selection -->
            <div class="section">
              <div class="section-title">Select Request Type</div>
              <hr class="mt-0 mb-2" />
              <div class="row">
                <div class="col-12">
                  <div>
                    <input type="radio" id="ob" value="OB" v-model="selectedRequestType" :disabled="submitting" />
                    <label for="ob" class="ms-2">Official Business - OB</label>

                    <input type="radio" id="ot" value="OT" v-model="selectedRequestType" class="ms-5" :disabled="submitting" />
                    <label for="ot" class="ms-2">Overtime - OT</label>
                  </div>
                </div>
              </div>
            </div>

            <!-- OT/OB Form -->
            <div class="section" v-if="selectedRequestType">
              <div class="section-title">
                {{ selectedRequestType === 'OT' ? 'Overtime Request' : 'Official Business Request Form' }}
              </div>
              <hr class="mt-0" />

              <div class="row mb-0">
                <div class="col-6 mb-3">
                  <label class="form-label label-sm">
                    Category <strong style="color: red">*</strong>
                  </label>
                  <select v-model="ob_ot_form.selectedCategory" class="form-select" required :disabled="submitting">
                    <option disabled value="">Select Category</option>
                    <option value="Systems">Systems</option>
                    <option value="Infrastructure">Infrastructure</option>
                  </select>
                </div>

                <div class="col-6">
                  <label class="form-label label-sm">
                    Destination <strong style="color: red">*</strong>
                  </label>
                  <select v-model="ob_ot_form.destination" class="form-select" required :disabled="submitting">
                    <option disabled value="">Select Destination</option>
                    <option value="HO">Head Office</option>
                    <option value="Alveo">Alveo</option>
                    <option value="Shops">Shops</option>
                    <option value="Farms">Farms</option>
                    <option value="WSP">Workshop</option>
                  </select>
                </div>
              </div>

              <!-- Shops checklist -->
              <div class="row mt-2" v-if="ob_ot_form.destination === 'Shops'">
                <div class="col-12">
                  <div class="d-flex justify-content-between">
                    <label class="form-label label-sm">
                      Select Shop(s) <strong style="color:red">*</strong>
                    </label>
                    <i>
                      <small class="text-muted d-block mt-1 form-label label-sm">(Choose at least 1 shop)</small>
                    </i>
                  </div>

                  <div class="shops-grid">
                    <label class="shop-item" v-for="s in sortedShops" :key="s">
                      <input
                        type="checkbox"
                        :value="s"
                        v-model="ob_ot_form.selectedShops"
                        :disabled="submitting"
                      />
                      <span class="ms-2">{{ s }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <div class="row mb-3 mt-3">
                <div class="col-6">
                  <label for="date_from" class="form-label label-sm">
                    Requested Date From <strong style="color: red">*</strong>
                  </label>
                  <input
                    type="datetime-local"
                    id="date_from"
                    class="form-control"
                    v-model="ob_ot_form.date_from"
                    required
                    :disabled="submitting"
                  />
                </div>
                <div class="col-6">
                  <label for="date_to" class="form-label label-sm">
                    Requested Date To <strong style="color: red">*</strong>
                  </label>
                  <input
                    type="datetime-local"
                    id="date_to"
                    class="form-control"
                    v-model="ob_ot_form.date_to"
                    required
                    :disabled="submitting"
                  />
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-12">
                  <label for="project" class="form-label label-sm">
                    Project <strong style="color: red">*</strong>
                  </label>
                  <textarea
                    class="form-control"
                    rows="1"
                    id="project"
                    v-model="ob_ot_form.project"
                    required
                    :disabled="submitting"
                  ></textarea>
                </div>
              </div>

              <div class="row">
                <div class="col-12">
                  <label for="reason" class="form-label label-sm">
                    Reason for {{ selectedRequestType === 'OT' ? 'OT Request' : 'OB Request' }}
                    <strong style="color: red">*</strong>
                  </label>
                  <textarea
                    class="form-control"
                    rows="1"
                    id="reason"
                    v-model="ob_ot_form.reason"
                    required
                    :disabled="submitting"
                  ></textarea>
                </div>
              </div>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer mt-4">
            <button type="submit" class="btn btn-success" :disabled="submitting">
              <span v-if="submitting">Submitting...</span>
              <span v-else>Submit</span>
            </button>

            <button type="button" class="btn btn-info" @click="closeModal" :disabled="submitting">
              Close
            </button>
          </div>
        </form>
      </div>

      <!-- ✅ Processing overlay (same pattern as leave modal) -->
      <div v-if="submitting" class="screen-loader" role="dialog" aria-modal="true">
        <div class="loader-card">
          <div class="spinner-border" aria-hidden="true"></div>
          <div class="loader-title">
            Submitting {{ selectedRequestType === 'OT' ? 'Overtime' : 'Official Business' }}
          </div>
          <div class="loader-subtitle">
            Please wait while we submit your request and notify your Department Head thru email.
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import API_BASE from "@/utils/api_config";
import { getUserData } from "@/utils/get_user_data";

export default {
  props: {
    isVisible: { type: Boolean, required: true },
  },
  data() {
    return {
      user: getUserData() || {},
      selectedRequestType: "",
      existingRequests: [],
      submitting: false, // ✅ added

      ob_ot_form: {
        destination: "",
        date_from: "",
        date_to: "",
        reason: "",
        selectedCategory: "",
        project: "",
        selectedShops: [],
      },

      shops: [
        "Aurea G2",
        "Aurea NGH",
        "RET ACC",
        "RET ATC",
        "RET BAY",
        "RET G4",
        "RET GB5",
        "RET MCIA",
        "RET MEGAMALL",
        "RET MOA",
        "RET MPS",
        "RET NAIA T3",
        "RET NUSTAR",
        "RET POD",
        "RET ROC",
        "RET SM Aura",
        "RET SPM",
        "RET STF",
        "RET Trinoma",
        "V! ATC",
        "V! Cloverleaf",
        "V! Eastwood",
        "V! Glorietta",
        "V! JMall",
        "V! Lucky Chinatown",
        "V! MEGAMALL",
        "V! MOA",
        "V! New Greenhills",
        "V! One Ayala",
        "V! Robinsons Ermita",
        "V! Robinsons Galleria",
        "V! Rockwell",
        "V! Shangrila",
        "V! SM North",
        "V! Trinoma",
        "V! Uptown Mall",
      ],
    };
  },
  computed: {
    fullName() {
      return `${this.user.first_name} ${this.user.last_name}`.trim();
    },
    sortedShops() {
      return [...this.shops].sort((a, b) => a.localeCompare(b));
    },
  },
  watch: {
    "ob_ot_form.destination"(val) {
      if (val !== "Shops") this.ob_ot_form.selectedShops = [];
    },
  },
  mounted() {
    this.fetchExistingOTOB();
  },
  methods: {
    closeModal() {
      if (this.submitting) return;

      // reset fields
      this.selectedRequestType = "";
      this.ob_ot_form = {
        destination: "",
        date_from: "",
        date_to: "",
        reason: "",
        selectedCategory: "",
        project: "",
        selectedShops: [],
      };

      this.$emit("close");
    },

    fetchExistingOTOB() {
      fetch(`${API_BASE}/get_otob_for_approval_request_date`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ emp_id: this.user.emp_id }),
      })
        .then((res) => res.json())
        .then((data) => {
          this.existingRequests = data.alldates || [];
        });
    },

    // hasOTOBConflict(from, to) {
    //   const newFrom = new Date(from);
    //   const newTo = new Date(to);

    //   return this.existingRequests.some((req) => {
    //     const oldFrom = new Date(req.req_from || req.leave_from);
    //     const oldTo = new Date(req.req_to || req.leave_to);
    //     return newFrom <= oldTo && newTo >= oldFrom;
    //   });
    // },

    submitForm() {
      if (this.submitting) return;

      if (!this.selectedRequestType) {
        Swal.fire("Error", "Please select OB or OT type", "error"); 
        return;
      }

      if (this.ob_ot_form.destination === "Shops" && this.ob_ot_form.selectedShops.length === 0) {
        Swal.fire("Error", "Please select at least one shop.", "error");
        return;
      }

      // if (this.hasOTOBConflict(this.ob_ot_form.date_from, this.ob_ot_form.date_to)) {
      //   Swal.fire("Not Allowed", "This request overlaps with an existing OB/OT request.", "warning");
      //   return;
      // }

      const formData = {
        emp_id: this.user.emp_id,
        fullName: this.fullName,
        type: this.selectedRequestType,
        category: this.ob_ot_form.selectedCategory,
        req_from: this.ob_ot_form.date_from,
        req_to: this.ob_ot_form.date_to,
        reason: this.ob_ot_form.reason,
        project: this.ob_ot_form.project,
        department: this.user.dept_code,
        destination: this.ob_ot_form.destination,
        shops: this.ob_ot_form.destination === "Shops" ? this.ob_ot_form.selectedShops : [],
      };

      this.submitting = true;

      fetch(`${API_BASE}/create_ob_ot_request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })
        .then((response) => response.json())
        .then((data) => {
          this.submitting = false;

          if (data.success) {
            Swal.fire("Success", "Request filed successfully. Your Department Head has been notified.", "success");
            this.$emit("updateDataTable");
            this.closeModal();
          } else {
            Swal.fire("Error", data.error || "Failed to submit request", "error");
          }
        })
        .catch((error) => {
          this.submitting = false;
          console.error("Error submitting form:", error);
          Swal.fire("Error", "Something went wrong", "error");
        });
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
  color: #699dc8;
}

.form-control,
.form-select {
  color: #333 !important;
  background-color: #e9ecef !important;
}

#reason:focus,
#user:focus,
#project:focus {
  background-color: #fff !important;
  font-size: 12px !important;
}

/* ✅ Shops grid layout */
.shops-grid {
  display: grid;
  gap: 8px 16px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 12px;
}

@media (max-width: 992px) {
  .shops-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 576px) {
  .shops-grid {
    grid-template-columns: 1fr;
  }
}

.shop-item {
  display: flex;
  align-items: center;
  font-size: 13px;
}

/* ✅ loader overlay (same as leave modal) */
.screen-loader {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
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
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.18);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.loader-title {
  margin-top: 12px;
  font-weight: 700;
  font-size: 16px;
  color: #df7a8a;
}

.loader-subtitle {
  margin-top: 6px;
  font-size: 13px;
  color: #475569;
  line-height: 1.4;
}
</style>
