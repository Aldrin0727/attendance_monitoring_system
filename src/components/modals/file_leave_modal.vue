<template>
    <div class="modal" v-if="isVisible">
        <div class="modal-dialog">
            <div class="modal-content">
                <!-- Modal Header -->
                <div class="modal-header py-1">
                    <font-awesome-icon :icon="['fas', 'circle-plus']" class="font-awesome-icon" />
                    <h5 class="modal-title">Leave Request Form</h5>
                    <button type="button" class="btn-close" @click="$emit('close')" aria-label="Close"></button>
                </div>

                <!-- Form -->
                <form @submit.prevent="submitForm">
                    <div class="modal-body">
                        <!-- Personal Information Section -->
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
                                    <label for="user" class="form-label label-sm">Position</label>
                                    <input type="text" id="user" class="form-control" readonly />
                                </div>
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">department</label>
                                    <input type="text" id="user" class="form-control" readonly />
                                </div>
                            </div>
                            <div class="row mb-1">
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Address</label>
                                    <input type="text" id="user" class="form-control" readonly />
                                </div>
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Contact Number</label>
                                    <input type="text" id="user" class="form-control" readonly />
                                </div>
                            </div>
                        </div>

                        <!-- Personal Information Section -->
                        <div class="section">
                            <div class="section-title">Leave Credits</div>
                            <hr class="mt-0">
                            <div class="row">
                                <div class="col-6 mb-3">
                                    <label for="user" class="form-label label-sm">Type of Leave</label>
                                    <select id="system_type" v-model="selectedTypeofLeave" class="form-select">
                                        <option disabled value="">Select Type of Leave</option>
                                        <option value="SL">Sick Leave</option>
                                        <option value="VL">Vacation Leave</option>
                                        <option value="EL">Emergency Leave</option>
                                    </select>

                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Position</label>
                                    <input type="text" id="user" class="form-control" readonly />
                                </div>
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">department</label>
                                    <input type="text" id="user" class="form-control" readonly />
                                </div>
                            </div>
                            <div class="row mb-1">
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Address</label>
                                    <input type="text" id="user" class="form-control" readonly />
                                </div>
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Contact Number</label>
                                    <input type="text" id="user" class="form-control" readonly />
                                </div>
                            </div>
                        </div>


                    </div>

                    <!-- Modal Footer -->
                    <div class="modal-footer mt-2">
                        <!-- <button type="submit" class="btn btn-success">Submit</button> -->

                        <span>
                            Submit
                        </span>

                        <button type="button" class="btn btn-info" @click="$emit('close')">Close</button>
                    </div>
                </form>


            </div>
        </div>
    </div>
</template>

<script>
import API_BASE from '@/utils/api_config';


export default {
    props: {
        isVisible: {
            type: Boolean,
            required: true
        }
    },
    data() {
        return {
            selectedTypeofLeave: "",
        }

    },
    watch: {

    },
    mounted() {
        this.fetchUserDetails();
    },
    methods: {
        fetchUserDetails() {
            fetch(`${API_BASE}/leave_details`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({})
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Failed to fetch departments");
                    }
                    return response.json();
                })
                .then(data => {
                    // this.leave_details = data;
                    console.log(data)
                })
                .catch(error => {
                    console.error("Error fetching departments:", error);
                    alert("Failed to fetch departments.");
                });
        },
    },
    computed: {

    }
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
</style>
