<template>

  <div class="files-grid">
    <div v-for="(f, i) in files" :key="i" >
        <a :href="f.url">
            <img :src="resolveImage(f.name)" class="icon"/>
        </a>
        <a :href="f.url">
            {{ f.name }}
        </a>
    </div>
    <div v-if="addButton">
       <div class="button button-lg" @click="triggerFileInput()">Add...</div>
       <input type="file" multiple id="file-input" ref="fileInput" @change="addFiles($event)"/>
    </div>
  </div>
</template>

<script>
export default {
  name: "FilesList",
  props: {
    addButton: Boolean
  },
  data: () => {
    return {
      files: []
    };
  },
  methods: {
    resolveImage: function(filename) {
      if (filename.endsWith(".pdf")) {
        return require("../assets/pdf.svg");
      } else if (filename.endsWith(".py")) {
        return require("../assets/py.svg");
      } else if (filename.endsWith(".doc") || filename.endsWith(".docx")) {
        return require("../assets/word.svg");
      } else {
        return require("../assets/file.svg");
      }
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    addFiles(event) {
      var vm = this;
      var files = event.target.files;
      for (let file of files) {
        let reader = new FileReader();
        reader.onloadend = function() {
          vm.files.push({
            name: file.name,
            bytes: reader.result
          });
        };
        reader.readAsDataURL(file);
      }
    },

    sendFiles(linkName, alicePriv, alicePub, bobPub) {
      return fetch("http://localhost:5000/upload", {
        method: "POST",
        body: JSON.stringify({
          linkName,
          alicePriv: localStorage.getItem("password"),
          alicePub: localStorage.getItem("login"),
          bobPub,
          datetime: new Date().toString(),
          files: this.files
        }),
        headers: {
          "Content-Type": "application/json"
        }
      });
    },

    getFilesFromParent(files) {
      this.files = files;
    }
  }
};
</script>

<style scoped>
.files-grid {
  margin-top: 40px;
  margin-bottom: 100px;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  grid-row-gap: 50px;
  text-align: center;
}

.icon {
  max-height: 50px;
  max-width: 50px;
  display: block;
  margin: auto;
  margin-bottom: 10px;
}

#file-input {
  position: fixed;
  top: -100em;
}
</style>
