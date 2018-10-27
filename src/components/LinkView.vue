<template>
  <div id="app">
    <Logout/>
    <h2> {{ name }}  </h2>
    <h4 id="subtext"> created at {{ datetime}}</h4>
    <FilesList :addButton="false" ref="filesList"/>
      <div @click="downloadFiles()" class="button button-md">Download all</div>
  </div>
</template>

<script>
import FilesList from "./FilesList.vue";
import Logout from "./Logout.vue";

export default {
  name: "LinkView",
  components: {
    FilesList,
    Logout
  },

  data: () => {
    return {
      name: "",
      datetime: "",
      files: []
    };
  },

  created() {
    this.fetchFiles();
  },

  methods: {
    fetchFiles() {
      var vm = this;
      var link = window.location.href.split("?id=")[1];
      fetch("http://localhost:5000/download", {
        method: "POST",
        body: JSON.stringify({
          hashes: [link],
          privKey: localStorage.getItem("password"),
          pubKey: localStorage.getItem("login")
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(response => {
          return response.json();
        })
        .then(data => {
          console.log(data, link, data[link]);
          data = JSON.parse(data[link]);
          vm.name = data.linkName;
          vm.datetime = data.datetime;
          vm.files = data.files;
          vm.$refs.filesList.getFilesFromParent(data.files);
        });
    },

    base64ToArrayBuffer(base64) {
      var binaryString = atob(base64.split("base64,")[1]);
      var binaryLen = binaryString.length;
      var bytes = new Uint8Array(binaryLen);
      for (var i = 0; i < binaryLen; i++) {
        var ascii = binaryString.charCodeAt(i);
        bytes[i] = ascii;
      }
      return bytes;
    },

    saveByteArray(name, byte) {
      var blob = new Blob([byte], { type: "application/pdf" });
      var link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      var fileName = name;
      link.download = fileName;
      link.click();
    },

    downloadFiles() {
      var vm = this;
      for (let f of vm.files) {
        fetch("http://localhost:5000/download", {
          method: "POST",
          body: JSON.stringify({
            hashes: [f.hash],
            privKey: localStorage.getItem("pasword"),
            pubKey: localStorage.getItem("login")
          }),
          headers: {
            "Content-Type": "application/json"
          }
        })
          .then(result => {
            return result.json();
          })
          .then(data => {
            var arrayBuffer = this.base64ToArrayBuffer(data[f.hash]);
            this.saveByteArray(f.name, arrayBuffer);
          });
      }
    }
  }
};
</script>

<style scoped>
#subtext {
  margin-bottom: 60px;
  font-weight: normal;
}

.button-md {
  margin-top: 60px;
}
</style>
