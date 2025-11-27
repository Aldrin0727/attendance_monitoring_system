<template>
    <div>
        <nav class="d-flex justify-content-space-between" :class="['sidebar', { active: isSidebarActive }]">
            <div class="sidebar-content">
                <div class="sidebar-header">
                    <img src="../assets/images/asset_logo.png" alt="Logo" class="logo mb-4" />
                </div>

                <!-- <h4 class="pages-label mt-3">Pages</h4> -->
                <ul class="menu-list">
                    <li :class="{ active: isActive('dashboard') }">
                        <a @click.prevent="navigate('dashboard')">
                            <i class="fas fa-chart-simple"></i>
                            <span v-show="!isSidebarActive">Dashboard</span>
                        </a>
                    </li>
                  <li :class="{ active: isActive('parameters') }">
                        <a @click.prevent="toggleDropdown('parameters')">
                            <i class="fas fa-sliders"></i>
                            <span v-show="!isSidebarActive">Parameters</span>
                            <i class="fas fa-chevron-down dropdown-icon" :class="{ open: dropdowns.parameters }"></i>
                        </a>

                        <ul v-show="dropdowns.parameters" class="submenu">
                            <li :class="{ active: isActive('user_list') }"
                                @click="navigate('user_list')">
                                Users
                            </li>
                        </ul>

                    </li>

                    <li :class="{ active: isActive('attendance') }">
                        <a @click.prevent="navigate('attendance')">
                            <i class="fas fa-computer"></i>
                            <span v-show="!isSidebarActive">Attendance</span>
                        </a>
                    </li>

                    <li :class="{ active: isActive('ob_ot') }">
                        <a @click.prevent="navigate('ob_ot')">
                            <i class="fas fa-window-restore"></i>
                            <span v-show="!isSidebarActive">OB/OT</span>
                        </a>
                    </li>
                    <li :class="{ active: isActive('reports') }">
                        <a @click.prevent="navigate('reports')">
                            <i class="fas fa-chart-line"></i>
                            <span v-show="!isSidebarActive">Reports</span>
                        </a>
                    </li>
                    
                </ul>



            </div>


            <div class="sidebar-footer">
                <ul class="menu-list mb-0">
                    <li>
                        <a @click.prevent=signOut>
                            <i class="fas fa-right-from-bracket"></i>
                            <span v-show="!isSidebarActive">Sign Out</span>
                        </a>
                    </li>
                </ul>
            </div>
        </nav>


    </div>
</template>

<script>

export default {
      name: "Sidenav",
        props: {
    isSidebarActive: {
      type: Boolean,
      default: false
    }
  },
    data(){
        return{
            dropdowns: {
                assignments: false,
                parameters: false,
            },
        }
    },
    methods: {
        navigate(view) {
            // let hardwareSubmenus = ['list_of_hardware'];
            let parametersSubmenus = ['employee_list','user_list'];
            // let softwareSubmenus = ['list_of_software'];
            let assignmentsSubmenus = ['employee_assets', 'assign_asset', 'return_transfer_asset'];



            if (assignmentsSubmenus.includes(view)) {
                this.$router.push({ path: `/assignments/${view}` });
            } else if (parametersSubmenus.includes(view)) {
                this.$router.push({ path: `/parameters/${view}` });
            } else {
                this.$router.push({ path: `/${view}` });
            }
        },
        isActive(view) {
            return (
                this.$route.path === `/${view}` ||
                this.$route.path.startsWith(`/parameters/${view}`) ||
                this.$route.path.startsWith(`/assignments/${view}`)
            );
        },
        toggleDropdown(menu) {
            this.dropdowns[menu] = !this.dropdowns[menu];
        },
    }
}
</script>

<style>
/* @import url(../assets/css/cards.css);
@import url(../assets/css/inputbox.css);
@import url(../assets/css/dataTable.css); */
@import url(../assets/css/navbar.css);




.font-awesome-icon {
    color: #73a9b8 !important;
    width: 30px;
    height: 45px;
    margin-right: 10px;
}





</style>
