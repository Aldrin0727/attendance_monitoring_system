<template>
    <div class="modal" v-if="isVisible">
        <div class="modal-dialog">
            <div class="modal-content">
                <!-- Modal Header -->
                <div class="modal-header py-1">
                    <font-awesome-icon :icon="['fas', 'circle-plus']" class="font-awesome-icon" />
                    <h5 class="modal-title">Request Form</h5>
                    <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
                </div>

                <!-- Form -->
                <form @submit.prevent="submitForm">
                    <div class="modal-body pb-0">
                        <!-- User Information -->
                        <div class="section">
                            <div class="section-title">User Information</div>
                            <hr class="mt-0">
                            <div class="row">
                                <div class="col-12 mb-3">
                                    <label for="user" class="form-label label-sm">USER</label>
                                    <input type="text" id="user" class="form-control" v-model="fullName" readonly />
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Position</label>
                                    <input type="text" id="user" class="form-control" v-model="user.position" readonly />
                                </div>
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Department</label>
                                    <input type="text" id="department" class="form-control" v-model="user.department_name" readonly />
                                </div>
                            </div>
                            <div class="row mb-1">
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Address</label>
                                    <input type="text" id="user" class="form-control" v-model="user.address" readonly />
                                </div>
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Contact Number</label>
                                    <input type="text" id="user" class="form-control" v-model="user.contact" readonly />
                                </div>
                            </div>
                        </div>

                        <!-- OT/OB Selection -->
                        <div class="section">
                            <div class="section-title">Select Request Type</div>
                            <hr class="mt-0 mb-2">
                            <div class="row">
                                <div class="col-12">
                                    <div>
                                        <input type="radio" id="ob" value="OB" v-model="selectedRequestType" /> 
                                        <label for="ob" class="ms-2">Official Business - OB </label>
                                        <input type="radio" id="ot" value="OT" v-model="selectedRequestType" class="ms-5" />
                                        <label for="ot" class="ms-2">Overtime - OT</label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Leave Credits / OT/OB Form -->
                        <div class="section" v-if="selectedRequestType">
                            <div class="section-title">{{ selectedRequestType === 'OT' ? 'Overtime Request' : 'Official Business Request Form' }}</div>
                            <hr class="mt-0">
                            <div class="row mb-0">
                                <div class="col-6 mb-3">
                                    <label class="form-label label-sm">Category <strong style="color: red">*</strong></label>
                                    <select v-model="ob_ot_form.selectedCategory" class="form-select" required>
                                        <option disabled value="">Select Category</option>
                                        <option value="Systems">Systems</option>
                                        <option value="Infrastructure">Infrastructure</option>
                                    </select>
                                </div>
                                 <div class="col-6">
                                    <label for="user" class="form-label label-sm">Destination<strong style="color: red">*</strong></label>
                                    <!-- <input type="text" id="user" class="form-control" v-model="ob_ot_form.destination"/> -->
                                       <select v-model="ob_ot_form.destination" class="form-select" required>
                                        <option disabled value="">Select Category</option>
                                        <option value="HO">Head Office</option>
                                        <option value="Alveo">Alveo</option>
                                        <option value="Farms">Shops</option>
                                        <option value="Shops">Farms</option>
                                    </select>
                                </div>
                            </div>

                            <div class="row mb-3">
                                <div class="col-6">
                                    <label for="date_from" class="form-label label-sm">
                                       Requested Date From <strong style="color: red">*</strong>
                                    </label>
                                    <input type="datetime-local" id="date_from" class="form-control" v-model="ob_ot_form.date_from" required />
                                </div>
                                <div class="col-6">
                                    <label for="date_to" class="form-label label-sm">
                                        Requested Date To <strong style="color: red">*</strong>
                                    </label>
                                    <input type="datetime-local" id="date_to" class="form-control" v-model="ob_ot_form.date_to" required />
                                </div>
                            </div>

                            <div class="row mb-3">
                                <div class="col-12">
                                    <label for="leave_reason" class="form-label label-sm">
                                        Reason for {{ selectedRequestType === 'OT' ? 'OT Request' : 'OB Request' }} <strong style="color: red">*</strong>
                                    </label>
                                    <textarea class="form-control" rows="1" id="leave_reason" v-model="ob_ot_form.reason" required></textarea>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-12">
                                    <label for="leave_reason" class="form-label label-sm"> Project <strong style="color: red">*</strong>
                                    </label>
                                    <textarea class="form-control" rows="1" id="leave_reason" v-model="ob_ot_form.project" required></textarea>
                                </div>
                            </div>
                        </div>

                    </div>

                    <!-- Modal Footer -->
                    <div class="modal-footer mt-4">
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
import { getUserData } from '@/utils/get_user_data';

export default {
    props: {
        isVisible: {
            type: Boolean,
            required: true
        }
    },
    data() {
        return {
            user: getUserData() || {},
            selectedRequestType: "",
            ob_ot_form: {
                destination: "",
                date_from: "",
                date_to: "",
                reason: "",
                selectedCategory: "",
                project: "",
            },
        };
    },
    computed: {
        fullName() {
            return `${this.user.first_name} ${this.user.last_name}`.trim();
        },
    },
    methods: {
        closeModal() {
            this.$emit("close");
        },

        submitForm() {
            if (!this.selectedRequestType) {
                Swal.fire("Error", "Please select OB or OT type", "error");
                return;
            }

            const formData = {
                emp_id: this.user.emp_id,
                fullName: `${this.user.first_name} ${this.user.last_name}`,
                type: this.selectedRequestType,
                category: this.ob_ot_form.selectedCategory,
                req_from: this.ob_ot_form.date_from,
                req_to: this.ob_ot_form.date_to,
                reason: this.ob_ot_form.reason,
                project: this.ob_ot_form.project,
                department: this.user.dept_code,
                destination: this.ob_ot_form.destination 
            };

            // console.log(formData)
            // Send form data to backend API
            fetch(`${API_BASE}/create_ob_ot_request`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire("Success", "Request filed successfully", "success");

                    } else {
                        Swal.fire("Error", data.error || "Failed to submit request", "error");
                    }
                })
                .catch(error => {
                    console.error("Error submitting form:", error);
                    Swal.fire("Error", "Something went wrong", "error");
                });

            // Close modal after successful submit
            this.closeModal();
        }
    }
}
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
}

#leave_reason:focus, #user:focus {
    background-color: #fff !important;
    font-size: 12px !important;
}
</style>
