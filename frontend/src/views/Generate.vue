<template>
  <div class="generate-page">
    <h1>创建新文档</h1>
    
    <div class="mode-toggle">
      <button 
        :class="['toggle-btn', { active: !advancedMode }]" 
        @click="advancedMode = false"
      >
        基础模式
      </button>
      <button 
        :class="['toggle-btn', { active: advancedMode }]" 
        @click="advancedMode = true"
      >
        高级模式
      </button>
    </div>
    
    <document-form v-if="!advancedMode" @switch-mode="advancedMode = true" />
    <advanced-document-form v-else @switch-mode="advancedMode = false" />
  </div>
</template>

<script>
import DocumentForm from '../components/DocumentForm.vue';
import AdvancedDocumentForm from '../components/AdvancedDocumentForm.vue';

export default {
  name: 'Generate',
  components: {
    DocumentForm,
    AdvancedDocumentForm
  },
  data() {
    return {
      advancedMode: false
    }
  }
}
</script>

<style scoped>
.generate-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.mode-toggle {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
  background-color: #f0f0f0;
  border-radius: 8px;
  padding: 4px;
  width: 300px;
  margin-left: auto;
  margin-right: auto;
}

.toggle-btn {
  flex: 1;
  background: none;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.toggle-btn.active {
  background-color: #4CAF50;
  color: white;
}
</style> 