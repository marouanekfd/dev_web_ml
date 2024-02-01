<template>

        <v-container class="hyperparam-form">
            <v-col>
              
              
                <v-form @submit.prevent="submitForm">
                  <v-col >
                <v-text-field v-model="values['token']" >Token: </v-text-field>
                    </v-col>
                    <v-col v-for="(item, index) in dataInfo.data" :key="item">
                        <v-text-field v-if="item !== target" :label="item" v-model="values[item]"></v-text-field>
                    </v-col>
                    <v-btn type="submit" color="primary">Envoyer</v-btn>
                </v-form>
            </v-col>
        </v-container>
        

  </template>

  <script>
  export default {
    props:['dataInfo', 'target', 'filename'],
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
        columns : this.dataInfo.data,
        values: {},
        json_predict: null
  
  
      };
    },
    methods: {
      async submitForm() {
    const formData = new FormData();
    console.log(this.values)
    // Ajoutez les données au formulaire
    formData.append('dataInfo', JSON.stringify(this.dataInfo.data));
    formData.append('values', JSON.stringify(str(this.values)));

    
    console.log(formData)

    

    try {
      const response = await fetch("/api/predict", { method: 'POST', body: formData });
      const data = await response.json();

      this.json_predict = data.valeurs;

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
  }}
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