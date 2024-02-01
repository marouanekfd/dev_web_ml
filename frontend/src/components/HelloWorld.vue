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
          label="Choississez votre target"
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
      selectedColumns: [],
      target:''
    }
  },
  methods: {

    goToNextStep() {
      this.$emit('next-step', this.selectedColumns);
    },

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
                this.$emit('dataInfo', data);
            });
      }
    },
    downloadSelectedColumns() {
    if (this.file && this.selectedColumns.length > 0) {
        const formData = new FormData();
        formData.append('file', this.file);

        // Envoie également la colonne sélectionnée au backend
        formData.append('targetColumn', this.selectedColumns);
        this.$emit('target', this.selectedColumns);
        console.log(this.selectedColumns);
    }
},
  created() {
    fetch("/api/mode").then(res => res.json()).then(data => {
      this.devmode = data.devmode;

    });
  },
}};

</script>