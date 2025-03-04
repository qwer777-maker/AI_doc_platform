<template>
  <div class="generate-page">
    <h1>创建新文档</h1>
    <document-form />
  </div>
</template>

<script>
import DocumentForm from '../components/DocumentForm.vue';

export default {
  name: 'Generate',
  components: {
    DocumentForm
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
  margin-bottom: 30px;
}
</style> 