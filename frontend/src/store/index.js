import Vue from 'vue'
import Vuex from 'vuex'
import documentsModule from './modules/documents'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    documents: documentsModule
  }
}) 