<template>
  <div class="d-flex align-items-center">
   <i class="fa-regular fa-clock fa-lg fa-spin fa-spin-reverse"></i>
    <p class="mb-0" style="font-size: 15px; margin-left: 12px;">
      {{ currentDateTime }}
      <!-- sadadsad -->
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentDateTime: ''
    };
  },
  mounted() {
    this.updateDateTime();
    setInterval(this.updateDateTime, 1000); 
  },
  methods: {
    updateDateTime() {
      const options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true };
      const now = new Date().toLocaleString('en-US', options);
      this.currentDateTime = now;
    }
  }
};
</script>

<style scoped>
.fa-clock {
  color: #699dc8;
}

</style>
