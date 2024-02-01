<template>
  <div id="app">
    <v-app>
      <v-main>
        <v-stepper v-model="step" :items="items" show-actions>
          <template v-slot:item.1>
            <HelloWorld v-on:dataInfo="setDataInfo" v-on:target="setTarget" v-on:filename="setFilename" />
          </template>

          <template v-slot:item.2>
            <HyperParamForm v-if=" step === 2"  :filename="filename"/>

          </template>

          <template v-slot:item.3>
            <PredictForm v-if=" step === 3" v-bind:dataInfo="dataInfo"  :target="target"/>
          </template>
        </v-stepper>
      </v-main>
    </v-app>
  </div>
</template>

<script>
import HelloWorld from '@/components/HelloWorld.vue';
import HyperParamForm from '@/components/HyperParamForm.vue';
import PredictForm from './components/PredictForm.vue';

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
      dataInfo: null,
      target:null, 
      filename: null
    };
   }, // Add a closing brace here
  methods:{
    setDataInfo(dataInfo){
      this.dataInfo = dataInfo;
      console.log('fichier', dataInfo)
    },
    setTarget(target){
      this.target = target;
      console.log('setTarget',this.target)
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