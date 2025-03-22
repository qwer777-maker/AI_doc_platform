import api from '@/services/api'

export default {
  namespaced: true,
  
  state: {
    documents: [],
    loading: false,
    error: null
  },
  
  mutations: {
    SET_DOCUMENTS(state, documents) {
      state.documents = documents
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    ADD_DOCUMENT(state, document) {
      state.documents.unshift(document)
    },
    UPDATE_DOCUMENT(state, updatedDocument) {
      const index = state.documents.findIndex(doc => doc.id === updatedDocument.id)
      if (index !== -1) {
        state.documents.splice(index, 1, updatedDocument)
      }
    }
  },
  
  actions: {
    async fetchDocuments({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.getDocuments()
        commit('SET_DOCUMENTS', response.data)
        commit('SET_ERROR', null)
      } catch (error) {
        commit('SET_ERROR', '获取文档列表失败')
        console.error(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async createDocument({ commit }, documentData) {
      try {
        const response = await api.createDocument(documentData)
        return response.data
      } catch (error) {
        console.error(error)
        throw error
      }
    },
    
    async createAdvancedDocument({ commit }, documentData) {
      try {
        const response = await api.createAdvancedDocument(documentData)
        return response.data
      } catch (error) {
        console.error(error)
        throw error
      }
    },
    
    async getDocument({ commit }, documentId) {
      try {
        const response = await api.getDocument(documentId)
        return response.data
      } catch (error) {
        console.error(error)
        throw error
      }
    },
    
    async getDocumentStatus({ commit }, documentId) {
      try {
        const response = await api.getDocumentStatus(documentId)
        return response.data
      } catch (error) {
        console.error(error)
        throw error
      }
    }
  },
  
  getters: {
    getDocumentById: (state) => (id) => {
      return state.documents.find(doc => doc.id === id)
    }
  }
} 