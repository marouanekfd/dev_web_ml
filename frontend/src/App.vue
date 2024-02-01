<template>
  <div id="app">
    <v-app>
      <v-main>
        <v-stepper v-model="step" :items="items" show-actions>
          <template v-slot:item.1>
            <HelloWorld v-on:target="setTarget" v-on:filename="setFilename" />
            <!-- Le reste du contenu pour la première étape -->
          </template>

          <template v-slot:item.2>
            <!-- Contenu de la deuxième étape (laissez-le vide pour l'instant) -->
            <HyperParamForm v-if=" step === 2" :target="target" :filename="filename"/>

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
        'Prédire',
      ],
      dataInfo:null,
      target: null, 
      filename: null,

    };
  },
  methods:{
    setDataInfo(dataInfo){
      this.dataInfo = dataInfo;
    },
    setTarget(target){
      this.target = target
      console.log("setTarget", this.target)
    },
    setFilename(filename){
      this.filename = filename;
      console.log('setFilename',this.filename)
    }
  }

};
</script>

<style>
/* Vos styles Vuetify ou autres styles ici */
</style>