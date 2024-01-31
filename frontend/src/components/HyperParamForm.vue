<template>
    <div>
      <h2>Configuration du modèle KMeans</h2>
      <form @submit.prevent="submitForm">
        <div>
          <label for="n_clusters">Nombre de clusters (K) :</label>
          <input type="number" id="n_clusters" v-model.number="params.n_clusters" min="1">
        </div>
  
        <div>
          <label for="init">Initiation des centroids :</label>
          <select id="init" v-model="params.init">
            <option value="k-means++">k-means++</option>
            <option value="random">Aléatoire</option>
          </select>
        </div>
  
        <div>
          <label for="max_iter">Nombre maximal d'itérations :</label>
          <input type="number" id="max_iter" v-model.number="params.max_iter" min="1">
        </div>
  
        <div>
          <label for="tol">Tolérance pour la convergence :</label>
          <input type="number" id="tol" v-model.number="params.tol" min="0">
        </div>

        <div>
        <label for="trainSizeSlider">Pourcentage pour l'ensemble d'entraînement: {{ split.train_size }}%</label>
        <input type="range" id="trainSizeSlider" v-model="split.train_size" min="0" max="100">
      </div>

      <button type="submit">Configurer le modèle et le fractionnement</button>
    </form>
  </div>
</template>


  <script>
  export default {
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
      }
    };
  },
  methods: {
  async submitForm() {
    console.log('Hyperparamètres KMeans soumis:', this.params);
    console.log('Fractionnement Train/Test:', this.split.train_size);

    try {
      const response = await fetch('/api/submit-kmeans-params', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          params: this.params,
          split: this.split
        })
      });

      const responseData = await response.json();
      console.log(responseData);
    } catch (error) {
      console.error('Erreur lors de l\'envoi des données:', error);
    }
  }
}
};
</script>


<style scoped>
.hyperparam-form {
  max-width: 500px; /* Limite la largeur du formulaire */
  margin: auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.slider-container {
  margin: 20px 0;
}

.slider {
  width: 100%; /* Pleine largeur à l'intérieur du container */
  height: 25px; /* Hauteur du slider */
  background: #efefef; /* Couleur de fond du slider */
  outline: none; /* Supprime l'outline pour un look plus net */
  opacity: 0.7; /* Transparence légère */
  -webkit-transition: .2s; /* Transition pour l'effet de survol */
  transition: opacity .2s;
}

.slider:hover {
  opacity: 1; /* Opacité totale lors du survol */
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