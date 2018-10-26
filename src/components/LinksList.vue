<template>
  <div id="app">
    <input ref="priv" placeholder="Insert private key..." @input="fetchLinks()"/> <br>
    <input ref="pub" placeholder="Insert public key..." @input="fetchLinks()"/> 
    <h2> Links shared by you </h2>
    <table class="ml">
      <tr v-for="(l, i) in links" :key=i> 
        <td> <div class="button button-sm" @click="relocate(l.url)">  {{ l.name }} </div> </td>
        <td> {{ l.datetime }} </td>
        <td> <div class="button button-sm">  Copy link </div> </td>
      </tr>
    </table>
    <div class="button button-md" id="add" @click="relocate('new')"> Add new </div>
  </div>
</template>

<script>
export default {
  name: "LinksList",

  data: () => {
    return {
      username: "salamantos",
      links: []
    };
  },

  methods: {
    relocate(url) {
      window.location = url;
    },

    fetchLinks() {
      var vm = this;
      var links = JSON.parse(localStorage.getItem("links"));
      fetch("http://localhost:5000/download", {
        method: "POST",
        body: JSON.stringify({
          hashes: links,
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
          for (let i in data) {
            data[i] = JSON.parse(data[i]);
            vm.links.push({
              name: data[i].linkName,
              datetime: data[i].datetime,
              url: "http://localhost:8081/link?id=" + i
            });
          }
        });
    }
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
  margin-bottom: 50px;
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

input {
  font-size: 1.5em;
  border-top: none;
  border-right: none;
  border-left: none;
  color: #111;
  outline: none;
  margin-bottom: 20px;
}

.input-lg {
  font-size: 1.5em;
  font-weight: bold;
}
</style>

<style scoped>
table {
  width: 90%;
}

tr {
  height: 3em;
}

#add {
  margin-top: 40px;
}

a {
  color: #1e65f3;
}
</style>
