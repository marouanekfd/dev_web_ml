<template>
  <v-container class="hyperparam-form">
    <v-form @submit.prevent="submitForm">
      <v-row>
        <v-col cols="12">
          <v-label for="n_clusters">Nombre de clusters (K) :</v-label>
          <v-text-field id="n_clusters" v-model.number="params.n_clusters" type="number" min="1"></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-label for="init">Initiation des centroids :</v-label>
          <v-select id="init" v-model="params.init" :items="['k-means++', 'random']"></v-select>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-label for="max_iter">Nombre maximal d'itérations :</v-label>
          <v-text-field id="max_iter" v-model.number="params.max_iter" type="number" min="1"></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-label for="tol">Tolérance pour la convergence :</v-label>
          <v-text-field id="tol" v-model.number="params.tol" type="number" min="0"></v-text-field>
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
        <v-select
          label="Sélectionner un dataset"
          :items="dataFiles"
          v-model="selectedDataset"
          @change="loadDataFiles"
        ></v-select>
      </v-col>
    </v-row>

    <!-- Nouveau : Bouton pour sélectionner la colonne cible -->
    <v-row v-if="selectedDataset">
      <v-col cols="12">
        <v-btn @click="selectTargetColumn">
          Sélectionner la colonne cible
        </v-btn>
      </v-col>
    </v-row>
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
        n_clusters: 3,
        init: 'k-means++',
        max_iter: 300,
        tol: 1
      },
      split: {
        train_size: 70, // Valeur initiale de 70% pour l'entraînement
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
      // Ici, tu peux ouvrir un dialogue ou une nouvelle vue pour sélectionner la colonne cible
      // Pour l'instant, je vais simplement logger le dataset sélectionné
      console.log("Dataset sélectionné:", this.selectedDataset);
      // Tu devras implémenter la logique pour sélectionner la colonne cible
    },
  
    async loadDataFiles() {
      // Utilise l'objet `options` pour configurer la méthode `POST` et les headers si nécessaire
      const options = {
        method: 'POST',
        headers: {
          // Ajoute des headers si ton API en a besoin, par exemple un Content-Type ou des tokens d'authentification
          'Content-Type': 'application/json'
        },
        // Si ton endpoint attend un corps de requête, ajoute-le ici
        // body: JSON.stringify({ someData: 'yourValue' })
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
      console.log('Hyperparamètres KMeans soumis:', this.params);
      console.log('Fractionnement Train/Test:', this.split.train_size);
      console.log(this.filename)
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
  /* Limite la largeur du formulaire */
  margin: auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.slider-container {
  margin: 20px 0;
}

.slider {
  width: 100%;
  /* Pleine largeur à l'intérieur du container */
  height: 25px;
  /* Hauteur du slider */
  background: #efefef;
  /* Couleur de fond du slider */
  outline: none;
  /* Supprime l'outline pour un look plus net */
  opacity: 0.7;
  /* Transparence légère */
  -webkit-transition: .2s;
  /* Transition pour l'effet de survol */
  transition: opacity .2s;
}

.slider:hover {
  opacity: 1;
  /* Opacité totale lors du survol */
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