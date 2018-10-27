<template>
  <div id="app">
    <h2> Please login to continue </h2>
    <input v-model="login" placeholder="Login"/> <br>
    <input v-model="password" type="password" placeholder="Password"/> <br>
    <div class="button button-md" @click="tryLogin"> Login </div>
    <img src="https://i.gifer.com/3o6O.gif" title="animation" />
    <img style="position:absolute; float:right;" src="../assets/cloud.jpg" title="animation" />
    <svg ref="svg">
    </svg>
  </div>
</template>

<script>
export default {
  name: "Login",

  data: () => {
    return {
      login: "",
      password: ""
    };
  },

  methods: {
    tryLogin() {
      localStorage.setItem("login", this.login);
      localStorage.setItem("password", this.password);
      window.location.href = "/";
    }
  }
};
</script>

<style scoped>
input {
  margin-bottom: 30px;
}
html {
  background-image: linear-gradient(45deg, #1e65f3 0%, #108adc 100%);
  height: 100%;
}
</style>
