<template>
  <div id="app">
    <Logout/>
    <div v-if="!dataSent">
      <input class="input-lg" v-model="name" placeholder="Insert folder name..."/>
      <h2> Files: </h2>
      <FilesList ref="files" :addButton="true"/>  
      <div>
        <h2> Share folder with: </h2>
        <div class="ml">
          <input v-model="bobLogin" placeholder="Insert login..."/> 
        </div>
      </div>
      <div class="button button-lg" @click="sendFiles()"> Create </div>
    </div>
    <div v-if="dataSent">
      <h2> Your link: </h2>
      <div class="button button-sm" @click="locateToLink()"> {{ link }} </div>
    </div>
  </div>
</template>

<script>
import FilesList from "./FilesList.vue";
import Logout from "./Logout";
export default {
  name: "LinkView",
  props: {},

  components: {
    FilesList,
    Logout
  },

  data: () => {
    return {
      files: [],
      dataSent: false,
      link: "",
      name: "",
      bobLogin: ""
    };
  },

  methods: {
    sendFiles() {
      var vm = this;
      vm.$refs.files
        .sendFiles(vm.name, vm.login, vm.password, vm.bobLogin)
        .then(response => {
          return response.text();
        })
        .then(hash => {
          vm.link = "http://localhost:8081/link?id=" + hash;
          vm.dataSent = true;

          var links = localStorage.getItem("links");
          if (links) {
            links = JSON.parse(links);
          } else {
            links = [];
          }
          links.push(hash);
          localStorage.setItem("links", JSON.stringify(links));
        });
    },

    locateToLink() {
      window.location.href = this.link;
    }
  }
};
</script>

<style scoped>
#app {
  margin-top: 110px;
}
</style>
