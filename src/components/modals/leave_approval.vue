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
                                        v-model="leaveRequest.leave_number" readonly />
                                </div>
                                <div class="col-5">
                                    <label class="form-label label-sm">REFERENCE NUMBER</label>
                                    <input type="text" class="form-control" v-model="leaveRequest.ref_no" readonly />
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-6">
                                    <label class="form-label label-sm">Date of Leave From</label>
                                    <input type="date" class="form-control" v-model="leaveRequest.leave_from"
                                        readonly />
                                </div>
                                <div class="col-6">
                                    <label class="form-label label-sm">Date of Leave To</label>
                                    <input type="date" class="form-control" v-model="leaveRequest.leave_to" readonly />
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-12">
                                    <label class="form-label label-sm">Reason for Leave</label>
                                    <textarea class="form-control" rows="1" v-model="leaveRequest.leave_reason"
                                        readonly></textarea>
                                </div>
                            </div>
                        </div>

                        <!-- Approver Buttons for Department Head -->


                        <!-- approver -->
                        <div class="section">
                            <div class="section-title">APPROVER AND STATUS OF LEAVE</div>
                            <hr class="mt-0">
                            <div class="row mt-0">
                                <div class="col-6">
                                    <label for="approver" class="form-label label-sm">Approved by</label>
                                    <input type="text" id="approver" class="form-control" readonly />
                                </div>
                                <div class="col-3">
                                    <label for="leave_status" class="form-label label-sm">Leave Status</label>
                                    <input type="text" id="leave_status" class="form-control" readonly />
                                </div>
                                <div class="col-3">
                                    <label for="leave_status" class="form-label label-sm">Date Approved</label>
                                    <input type="text" id="leave_status" class="form-control" readonly />
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Modal Footer -->
                    <div class="modal-footer">

                        <div
                            v-if="user.job_title == 'Department Head' && leaveRequest.status == 'FOR DEPARTMENT HEAD APPROVAL'">

                            <button type="button" class="btn btn-secondary me-2" @click="approveLeaveRequest">Approve</button>
                            <button type="button" class="btn btn-danger me-2" @click="denyLeaveRequest">Deny</button>
                            <!-- <button type="button" class="btn btn-info " @click="closeModal">Close</button> -->
                        </div>

                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { getUserData } from '@/utils/get_user_data';
export default {
    props: {
        isVisible: Boolean,
        leaveRequest: Object,
    },
    data() {
        return {
            user: getUserData() || {},
        }
    },

    methods: {
        closeModal() {
            this.$emit("close");
        },

        submitForm() {
            // Add form submission logic here
            this.closeModal();
        },

        approveLeaveRequest() {
            // Logic for approving the leave request
            console.log('Leave request approved');
            this.closeModal();  // Close modal after action
        },

        denyLeaveRequest() {
            // Logic for denying the leave request
            console.log('Leave request denied');
            this.closeModal();  // Close modal after action
        }
    },

    computed: {
        formattedLeaveType() {
            const leaveTypes = {
                'EL': 'Emergency Leave',
                'VL': 'Vacation Leave',
                'SL': 'Sick Leave',
            };
            return leaveTypes[this.leaveRequest.leave_type]
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
</style>
