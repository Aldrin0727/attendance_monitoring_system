import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Login",
    component: () => import("../views/login.vue"),
    meta: { hideSideNav: true, hideTopNav: true },
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: () => import("../views/dashboard.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/leave_requests",
    name: "LeaveRequests",
    component: () => import("../views/leave_requests.vue"),
    meta: { requiresAuth: true },
    props: (route) => ({
      status: route.query.status,
      job_title: route.query.job_title,
    }),
  },
   {
    path: "/attendance",
    name: "Attendance",
    component: () => import("../views/attendance.vue"),
    meta: { requiresAuth: true },
  },
   {
    path: "/ob_ot",
    name: "OB_OT",
    component: () => import("../views/ob_ot.vue"),
    meta: { requiresAuth: true },
     props: (route) => ({
      status: route.query.status,
      job_title: route.query.job_title,
    }),
  },


];


const router = createRouter({
  history: createWebHistory(), // Palitan ito
  routes
});

// Navigation Guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem("user");

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/"); // Redirect to login if not authenticated
  } else {
    next();
  }
});
export default router
  