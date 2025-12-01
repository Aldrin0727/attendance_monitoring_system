<template>
    <div>
        <nav class="d-flex justify-content-space-between" :class="['sidebar', { active: isSidebarActive }]">
            <div class="sidebar-content">
                <div class="sidebar-header mb-3">
                    <!-- User panel -->
                    <div class="user-panel" v-if="user">
                        <!-- Bilog na pic / initials -->
                        <div class="avatar-wrapper" :title="user.fullName">
                            <img v-if="user.avatar" :src="user.avatar" alt="User photo" class="avatar" />
                            <div v-else class="avatar avatar-initials">
                                <span>{{ userInitials }}</span>
                            </div>
                        </div>

                        <!-- Name + Dept (itatago pag collapsed yung sidebar) -->
                        <div class="user-text" v-show="!isSidebarActive">
                            <div class="user-name">
                                {{ user.fullName }}
                            </div>
                            <div class="user-dept">
                                {{ user.department }}
                            </div>
                        </div>
                    </div>
                </div>

                <ul class="menu-list mt-2">
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
                            <li :class="{ active: isActive('user_list') }" @click="navigate('user_list')">
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
                        <a @click.prevent="signOut">
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
    data() {
        return {
            dropdowns: {
                assignments: false,
                parameters: false,
            },
            user: null, 
        };
    },
    computed: {
  userInitials() {
            const u = this.user || {};
            let fullName = "";

            if (u.fullName) {
                fullName = u.fullName;
            } else if (u.first_name || u.last_name) {
                fullName = [u.first_name, u.last_name].filter(Boolean).join(" ");
            }

            fullName = String(fullName).trim();
            if (!fullName) return "";

            const parts = fullName.split(/\s+/);
            const first = parts[0]?.[0] || "";
            const last = parts.length > 1 ? parts[parts.length - 1]?.[0] : "";

            return (first + last).toUpperCase();
        }
    },
    mounted() {
        const stored = localStorage.getItem("user");
        if (stored) {
            const u = JSON.parse(stored);
            this.user = {
                fullName: `${u.first_name} ${u.last_name}`,
                department: u.department,
                avatar: u.avatar || null, // kung may profile pic ka
            };
        }
    },
    methods: {
        navigate(view) {
            let parametersSubmenus = ['employee_list', 'user_list'];
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
        signOut() {
            Swal.fire({
                title: "Are you sure?",
                text: "You will be logged out of your account.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#28a745",
                cancelButtonColor: "#E5394B",
                confirmButtonText: "Yes, sign out"
            }).then((result) => {
                if (result.isConfirmed) {
                    localStorage.removeItem("user");
                    sessionStorage.clear();

                    this.$router.push("/").then(() => {
                        window.history.pushState(null, "", "/");
                    });


                    // Show success message
                    Swal.fire("Signed Out", "You have been signed out.", "success");

                    this.user = {};
                }
            });
        }
    }
};
</script>

<style scoped>
@import url(../assets/css/navbar.css);
@import url(../assets/css/swal.css);
@import url(../assets/css/buttons.css);
@import url(../../public/global.css);


.font-awesome-icon {
    color: #73a9b8 !important;
    width: 30px;
    height: 45px;
    margin-right: 10px;
}

.user-panel {
    display: flex;
    align-items: center;
    /* padding: 14px; */
    padding: 14px 0 14px 0;
}

.avatar-wrapper {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
}

.avatar {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-initials {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #df7a8a;
    color: #fff;
    font-weight: 600;
    font-size: 18px;
}

.user-text {
    margin-left: 10px;
    flex: 1;
    min-width: 0;
}

.user-name {
    font-size: 14px;
    font-weight: 500;
    line-height: 1.2;
    white-space: nowrap;
    /* overflow: hidden; */
    /* text-overflow: ellipsis; */
    display: block;
}

.user-dept {
    font-size: 11px;
    opacity: 0.8;
    margin-top: 2px;
}

.btn-secondary{
      background-color: #4a8fe7;
   border-radius: 9999px;
   font-weight: 700;
   letter-spacing: .06em;
}

</style>
