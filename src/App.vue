<template>
  <div id="app">
    <LinkView username="salamantos" name="Mega Secret Files" datetime="21:04 01.02.03"/>
  </div>
</template>

<script>
import LinksList from "./components/LinksList.vue";
import NewLink from "./components/NewLink.vue";
import LinkView from "./components/LinkView.vue";

export default {
  name: "app",
  components: {
    LinksList,
    NewLink,
    LinkView
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  color: #111;
  padding-top: 60px;
  max-width: 1000px;
  margin: auto;
}

h2 {
  margin-top: 50px;
}

.button {
  font-weight: bold;
  margin-top: 20px;
  margin-bottom: 20px;
  color: #1e65f3;
  cursor: pointer;
}

.button-sm {
  font-size: 1em;
}

.button-md {
  font-size: 1.5em;
}

.button-lg {
  font-size: 2em;
}

.button:hover {
  color: #314773;
}

.ml {
  margin-left: 50px;
}

</style>
