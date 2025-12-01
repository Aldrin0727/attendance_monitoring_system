<template>
    <div class="modal" v-if="isVisible">
        <div class="modal-dialog">
            <div class="modal-content">
                <!-- Modal Header -->
                <div class="modal-header py-1">
                    <font-awesome-icon :icon="['fas', 'circle-plus']" class="font-awesome-icon" />
                    <h5 class="modal-title">File a Leave</h5>
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
                                    <input type="text" id="user" v-model="fullName" class="form-control" readonly />
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Position</label>
                                    <input type="text" id="user" v-model="fullName" class="form-control" readonly />
                                </div>
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">department</label>
                                    <input type="text" id="user" v-model="fullName" class="form-control" readonly />
                                </div>
                            </div>
                            <div class="row mb-1">
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Address</label>
                                    <input type="text" id="user" v-model="fullName" class="form-control" readonly />
                                </div>
                                <div class="col-6">
                                    <label for="user" class="form-label label-sm">Contact Number</label>
                                    <input type="text" id="user" v-model="fullName" class="form-control" readonly />
                                </div>
                            </div>
                        </div>


                    </div>

                    <!-- Modal Footer -->
                    <div class="modal-footer mt-2">
                        <!-- <button type="submit" class="btn btn-success">Submit</button> -->
                        <button type="submit" class="btn btn-secondary" :disabled="loading">
                            <span v-if="loading">
                                <i class="fas fa-spinner fa-spin me-2"></i>Submitting...
                            </span>
                            <span v-else>
                                Submit
                            </span>
                        </button>
                        <button type="button" class="btn btn-info" @click="$emit('close')">Close</button>
                    </div>
                </form>


            </div>
        </div>
    </div>
</template>

<script>


export default {
    props: {
        isVisible: {
            type: Boolean,
            required: true
        }
    },
    data() {
        return {
        }

    },
    watch: {

    },
    mounted() {

    },
    methods: {

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

.modal-title{
    color: #699dc8
}
</style>
