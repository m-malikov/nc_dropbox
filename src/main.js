import Vue from "../node_modules/vue/dist/vue.js";
import LinksList from "./components/LinksList.vue";
import NewLink from "./components/NewLink.vue";
import LinkView from "./components/LinkView.vue";
import Login from "./components/Login.vue";
import VueRouter from "vue-router";

Vue.config.productionTip = false;

Vue.use(VueRouter);

const routes = {
  "/": LinksList,
  "/new": NewLink,
  "/link": LinkView,
  "/login": Login
};

new Vue({
  el: "#app",
  data: {
    currentRoute: window.location.pathname
  },
  computed: {
    ViewComponent() {
      return routes[this.currentRoute];
    }
  },
  render(h) {
    return h(this.ViewComponent);
  }
});
