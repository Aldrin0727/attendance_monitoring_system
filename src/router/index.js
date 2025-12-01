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
    meta: { requiresAuth: true }
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
  