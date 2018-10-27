<template>
  <div id="logout">
    <b> {{ login }} </b> <div class="button button-sm" @click="logout"> log out </div>
  </div>
</template>

<script>
export default {
  name: "Logout",

  data: () => {
    return {
      login: "",
      password: ""
    };
  },

  created() {
    this.login = localStorage.getItem("login");
    this.password = localStorage.getItem("password");

    if (!this.login) {
      window.location.href = "/login";
    }
  },

  methods: {
    logout() {
      localStorage.setItem("login", null);
      localStorage.setItem("password", null);
      window.location.href = "/login";
    }
  }
};
</script>

<style scoped>
#logout {
  position: absolute;
  top: 0px;
  right: 60px;
  margin-top: 110px;
  margin-right: 30px;
}

.button-sm {
  display: inline-block;
  margin-left: 20px;
}
</style>
