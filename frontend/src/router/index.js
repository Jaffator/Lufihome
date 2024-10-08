import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "../views/DashboardView.vue";
import EventsView from "../views/EventsView.vue";
import SettingView from "../views/SettingView.vue";
import TempView from "../views/TempView.vue";
import LoginView from "../views/LoginView.vue";
import EditAccountView from "../views/EditAccountView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: DashboardView,
  },
  {
    path: "/editaccount",
    name: "editaccount",
    component: EditAccountView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/templog",
    name: "templog",
    component: TempView,
  },
  {
    path: "/events",
    name: "events",
    component: EventsView,
  },
  {
    path: "/setting",
    name: "setting",
    component: SettingView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
