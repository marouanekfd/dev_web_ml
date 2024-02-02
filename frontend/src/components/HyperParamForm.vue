<template>
  <v-container class="hyperparam-form">
    <v-form @submit.prevent="submitForm">
      <v-row>
        <v-col cols="12">
          <v-label for="model">Modèle :</v-label>
          <v-select id="model" v-model="params.model" :items="['RandomForestClassifier', 'RandomForestRegressor' ]"></v-select>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-label for="n_estimators">N-estimators :</v-label>
          <v-text-field id="n_estimators" v-model.number="params.n_estimators" type="number" min="100"></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-label for="criterion">Initiation du criterion :</v-label>
          <v-select id="criterion" v-model="params.criterion" :items="['gini', 'entropy','log_loss' ]"></v-select>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-label for="max_depth">Profondeur maximal :</v-label>
          <v-text-field id="max_depth" v-model.number="params.max_depth" type="number" min="1"></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-label for="min_samples_split">Min_samples_split :</v-label>
          <v-text-field id="min_samples_split" v-model.number="params.min_samples_split" type="number" min="2"></v-text-field>
        </v-col>
      </v-row>

      <v-row class="slider-container">
        <v-col cols="12">
          <v-label for="trainSizeSlider">Pourcentage pour l'ensemble d'entraînement: {{ split.train_size }}%</v-label>
          <v-slider id="trainSizeSlider" v-model="split.train_size" min="0" max="100" :step="1"></v-slider>
        </v-col>
      </v-row>
      <!-- Nouveau : Sélecteur de dataset -->
    
      <v-row>
        <v-col cols="12">
          <v-btn type="submit" color="primary">Configurer le modèle et le fractionnement</v-btn>
        </v-col>
      </v-row>

    </v-form>
    <v-row v-if="apiResponse">
      <v-col>
        <h3>Réponse reçue du serveur :</h3>
        <pre>{{ apiResponse }}</pre>
      </v-col>

      <v-col cols="12">
        <!-- Bouton pour afficher le token -->
        <v-btn @click="showToken" color="secondary">Afficher le Token</v-btn>

        <!-- Bouton pour supprimer le modèle -->
        <v-btn @click="deleteModel" color="error">Supprimer mon modèle</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>


<script>
export default {
  props: ['target', 'filename'],
  data() {
    return {
      params: {
        n_estimators: 100,
        criterion: 'gini',
        max_depth: 2,
        min_samples_split: 2,
        model : 'RandomForestClassifier'
      },
      split: {
        train_size: 70,
      },
      apiResponse: null,
      dataFiles: [],
      selectedDataFile: null,
      targetColumn: null,


    };
  },
  mounted() {
    this.loadDataFiles();
  },
  methods: {
    selectTargetColumn() {
      console.log("Dataset sélectionné:", this.selectedDataset);
    },
    async loadDataFiles() {
      const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
      };

      try {
        const response = await fetch('/api/data-files', options);
        if (response.ok) {
          const files = await response.json();
          this.dataFiles = files;
        } else {
          console.error('Erreur lors du chargement des fichiers de données:', response.statusText);
        }
      } catch (error) {
        console.error('Erreur lors de la connexion au serveur:', error);
      }
    },
    async submitForm() {
      try {
        const response = await fetch('/api/train', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            params: this.params,
            split: this.split,
            filename: this.filename,
            target: this.target
          })
        });

        const responseData = await response.json();
        this.apiResponse = responseData;
      } catch (error) {
        console.error('Erreur lors de l\'envoi des données:', error);
      }
    },

    showToken() {
      if (this.apiResponse && this.apiResponse.token) {
        alert(`Token: ${this.apiResponse.token}`);
      } else {
        alert("Aucun token disponible.");
      }
    },

    async deleteModel() {
      if (!this.apiResponse || !this.apiResponse.token) {
        alert("Token non disponible pour la suppression du modèle.");
        return;
      }

      try {
        const response = await fetch('/api/delete-model', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ token: this.apiResponse.token })
        });
        const responseData = await response.json();
        alert("Modèle supprimé avec succès.");
      } catch (error) {
        console.error('Erreur lors de la suppression du modèle:', error);
        alert("Erreur lors de la suppression du modèle.");
      }
    }
  }
};
</script>


<style scoped>
.hyperparam-form {
  max-width: 500px;
  margin: auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.slider-container {
  margin: 20px 0;
}

.slider {
  width: 100%;
  height: 25px;
  background: #efefef;
  outline: none;
  opacity: 0.7;
  -webkit-transition: .2s;
  transition: opacity .2s;
}

.slider:hover {
  opacity: 1;
}


button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>