<template>
  <div id="app">
    <input ref="priv" placeholder="Insert private key..." @input="fetchFiles()"/> <br>
    <input ref="pub" placeholder="Insert public key..." @input="fetchFiles()"/> 
    <h2> {{ name }}  </h2>
    <h4 id="subtext"> created at {{ datetime}}</h4>
    <FilesList :addButton="false" ref="filesList"/>
      <div @click="downloadFiles()" class="button button-md">Download all</div>
  </div>
</template>

<script>
import FilesList from "./FilesList.vue";

export default {
  name: "LinkView",
  components: {
    FilesList: FilesList
  },

  data: () => {
    return {
      name: "",
      datetime: "",
      files: []
    };
  },

  methods: {
    fetchFiles() {
      var vm = this;
      var link = window.location.href.split("?id=")[1];
      fetch("http://localhost:5000/download", {
        method: "POST",
        body: JSON.stringify({
          hashes: [link],
          privKey: vm.$refs.priv.value,
          pubKey: vm.$refs.pub.value
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(response => {
          return response.json();
        })
        .then(data => {
          data = JSON.parse(data[link]);
          vm.name = data.linkName;
          vm.datetime = data.datetime;
          vm.files = data.files;
          vm.$refs.filesList.getFilesFromParent(data.files);
        });
    },

    base64ToArrayBuffer(base64) {
      var binaryString = window.atob(base64);
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
            privKey: vm.$refs.priv.value,
            pubKey: vm.$refs.pub.value
          }),
          headers: {
            "Content-Type": "application/json"
          }
        })
          .then(result => {
            return result.json();
          })
          .then(data => {
            var arrrayBuffer = base64ToArrayBuffer(data[f.hash]);
            saveByteArray(f.name, arrayBuffer);
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
