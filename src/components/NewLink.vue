<template>
  <div id="app">
    <div v-if="!dataSent">
      <input class="input-lg" ref="name" placeholder="Insert name..."/>
      <h2> Files: </h2>
      <FilesList ref="files" :addButton="true"/>  
      <div>
        <h2> Your keys: </h2>
        <div class="ml">
          <input ref="alicePriv" placehoder="Insert private key..."/> <br>
          <input ref="alicePub" placeholder="Insert public key..."/> 
        </div>
        <h2> Share folder with: </h2>
        <div class="ml">
          <input ref="bobPub" placeholder="Insert public key..."/> 
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

export default {
  name: "LinkView",
  props: {},

  components: {
    FilesList: FilesList
  },

  data: () => {
    return {
      files: [],
      dataSent: false,
      link: ""
    };
  },

  methods: {
    sendFiles() {
      var vm = this;
      vm.$refs.files
        .sendFiles(
          vm.$refs.name.value,
          vm.$refs.alicePriv.value,
          vm.$refs.alicePub.value,
          vm.$refs.bobPub.value
        )
        .then(response => {
          return response.text();
        })
        .then(hash => {
          vm.link = "http://localhost:8081/link?id=" + hash;
          vm.dataSent = true;

          var links = JSON.parse(localStorage.getItem("links"));
          if (!links) {
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


