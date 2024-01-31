<script setup>
import axios from 'axios';
</script>
<template>
  <v-container>
    <v-row>
      <v-col>
        <v-file-input label="Fichier" @change="filePicked" ref="fileInput" required></v-file-input>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-btn @click="sendFile" color="primary">Importer</v-btn>
      </v-col>
    </v-row>

    <v-row v-if="columns.length > 0">
      <v-col>
        <v-select
          v-model="selectedColumns"
          :items="columns"
          label="Choisir des colonnes"
          
        ></v-select>
      </v-col>

      <v-col>
        <v-btn @click="downloadSelectedColumns" color="success">Prédire</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      packages: [],
      devmode: undefined,
      file: '',
      columns: [],
      selectedColumns: []
    }
  },
  methods: {
    filePicked(event) {
      this.file = event.target.files[0];
    },
    sendFile() {
      if (this.file) {
        const formData = new FormData();
        formData.append('file', this.file);

        fetch("/api/upload", {method:'POST', body: formData})
                .then(res => res.json()).then(data => {
                this.columns = data.data;
                console.log(this.columns)
            });
      }
    },
    downloadSelectedColumns() {
    if (this.columns && this.selectedColumns.length > 0) {
      const formData = new FormData();
      formData.append('file', this.file.name);
      formData.append('target', this.selectedColumns);
      axios.post("/api/predire", formData)
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }
  },
  created() {
    fetch("/api/mode").then(res => res.json()).then(data => {
      this.devmode = data.devmode;
      
    });
  },
}};

</script>
