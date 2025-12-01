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
          <div class="modal-body">
            <!-- User Information -->
            <div class="section">
              <div class="section-title">User Information</div>
              <hr class="mt-0">
              <div class="row">
                <div class="col-12 mb-3">
                  <label for="user" class="form-label label-sm">USER</label>
                  <input type="text" id="user" class="form-control" readonly />
                </div>
              </div>
              <div class="row mb-3">
                <div class="col-6">
                  <label class="form-label label-sm">Position</label>
                  <input type="text" class="form-control" readonly />
                </div>
                <div class="col-6">
                  <label class="form-label label-sm">Department</label>
                  <input type="text" class="form-control" readonly />
                </div>
              </div>
              <div class="row mb-1">
                <div class="col-6">
                  <label class="form-label label-sm">Address</label>
                  <input type="text" class="form-control" readonly />
                </div>
                <div class="col-6">
                  <label class="form-label label-sm">Contact Number</label>
                  <input type="text" class="form-control" readonly />
                </div>
              </div>
            </div>

            <!-- Leave Credits -->
            <div class="section">
              <div class="section-title">Leave Credits</div>
              <hr class="mt-0">

              <div class="row">
                <div class="col-6 mb-3">
                  <label class="form-label label-sm">
                    Type of Leave <strong style="color: red">*</strong>
                  </label>
                  <select v-model="selectedTypeofLeave" class="form-select" required>
                    <option disabled value="">Select Type of Leave</option>
                    <option value="SL">Sick Leave</option>
                    <option value="VL">Vacation Leave</option>
                    <option value="EL">Emergency Leave</option>
                  </select>
                </div>
                <div class="col-6">
                  <label class="form-label label-sm">Total Leave Days</label>
                  <input
                    type="text"
                    class="form-control leave_days"
                    :value="leaveForm.total_leave_days"
                    readonly
                  />
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-6">
                  <label for="date_from" class="form-label label-sm">
                    Date of Leave From <strong style="color: red">*</strong>
                  </label>
                  <input
                    type="datetime-local"
                    id="date_from"
                    class="form-control"
                    v-model="leaveForm.date_from"
                    required
                  />
                </div>
                <div class="col-6">
                  <label for="date_to" class="form-label label-sm">
                    Date of Leave To <strong style="color: red">*</strong>
                  </label>
                  <input
                    type="datetime-local"
                    id="date_to"
                    class="form-control"
                    v-model="leaveForm.date_to"
                    required
                  />
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-12">
                  <label for="leave_reason" class="form-label label-sm">
                    Reason for leave <strong style="color: red">*</strong>
                  </label>
                  <textarea
                    class="form-control"
                    rows="2"
                    id="leave_reason"
                    v-model="leave_reason"
                    required
                  ></textarea>
                </div>
              </div>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer mt-2">
            <button type="submit" class="btn btn-success">Submit</button>
            <button type="button" class="btn btn-info" @click="closeModal">Close</button>
          </div>
        </form>

      </div>
    </div>
  </div>
</template>


<script>
import API_BASE from '@/utils/api_config';

export default {
  name: 'file_leave_modal',
  props: {
    isVisible: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      selectedTypeofLeave: "",
      leaveForm: {
        date_from: "",
        date_to: "",
        total_leave_days: "", // optional, for future compute
      },
      leave_reason: "",
    };
  },
  methods: {
    closeModal() {
      // reset fields
      this.selectedTypeofLeave = "";
      this.leaveForm.date_from = "";
      this.leaveForm.date_to = "";
      this.leaveForm.total_leave_days = "";
      this.leave_reason = "";

      // notify parent to hide modal
      this.$emit("close");
    },

    submitForm() {
      // dito mo ilalagay yung submit logic later
      // for now pwedeng simple:
      console.log({
        type: this.selectedTypeofLeave,
        ...this.leaveForm,
        reason: this.leave_reason,
      });

      // after successful submit, close modal
      this.closeModal();
    },
  },
};
</script>




<style scoped>
@import url(../../assets/css/modal.css);
@import url(../../assets/css/buttons.css);

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

.form-control, .form-select{
    color:#333 !important;
    background-color: #e9ecef !important;
}

.leave_days{
    background-color: #b3cadc !important;
    border: #fff !important;

}

#leave_reason:focus{
    background-color: #fff !important;
    font-size: 12px !important;
}
</style>
