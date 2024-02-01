<template>
  <div id="app">
    <v-app>
      <v-main>
        <v-stepper v-model="step" :items="items" show-actions>
          <template v-slot:item.1>
            <HelloWorld />
            <!-- Le reste du contenu pour la première étape -->
          </template>

          <template v-slot:item.2>
            <!-- Contenu de la deuxième étape (laissez-le vide pour l'instant) -->
            <HyperParamForm v-if=" step === 2" />

          </template>

          <template v-slot:item.3>
            <!-- Contenu de la troisième étape (laissez-le vide pour l'instant) -->
          </template>
        </v-stepper>
      </v-main>
    </v-app>
  </div>
</template>

<script>
import HelloWorld from '@/components/HelloWorld.vue';
import HyperParamForm from '@/components/HyperParamForm.vue';

export default {
  components: {
    HelloWorld,
  },
  data() {
    return {
      step: 1,
      items: [
        'Choisir le dataset',
        'Selection du modèle',
        'Submit',
      ],
    };
  },

};
</script>

<style>
/* Vos styles Vuetify ou autres styles ici */
</style>