<!-- App.vue -->
<template>
  <div class="layout">
    <Sidenav v-if="!hideSideNav" class="sidenav" />
    <div class="main-content" :class="{'no-margin': isLoginRoute}">
      <!-- <TopNav v-if="!hideTopNav" /> -->
      <main class="content">
        <router-view :key="$route.fullPath" />
      </main>
    </div>
  </div>
</template>

<script>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import Sidenav from './components/sidenav.vue'


export default {
  name: 'App',
  components: { Sidenav },
  setup() {
    const route = useRoute()
    const isLoginRoute = computed(() => route.name === 'Login')
    const hideSideNav  = computed(() => route.meta?.hideSideNav === true)
    const hideTopNav   = computed(() => route.meta?.hideTopNav === true)

    const isSidebarActive = ref(!hideSideNav.value)
    watch(hideSideNav, (hidden) => { isSidebarActive.value = !hidden }, { immediate: true })

    return { isLoginRoute, hideSideNav, hideTopNav, isSidebarActive }
  }
}

</script>

<style scoped>
.layout {
  display: flex;
  width: 100%;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 250px; 
  /* margin-top: 60px;   */
}


.content{
  flex-grow:1;
  padding: 20px
}
.main-content.no-margin {
  margin-left: 0 !important;
  margin-top: 0 !important;
}
</style>

