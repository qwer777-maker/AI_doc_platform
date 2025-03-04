<template>
  <div class="document-form">
    <h2>创建新文档</h2>
    
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="topic">文档主题</label>
        <input 
          id="topic" 
          v-model="topic" 
          type="text" 
          required 
          placeholder="输入文档主题"
        />
      </div>
      
      <div class="form-group">
        <label for="docType">文档类型</label>
        <select id="docType" v-model="docType" required>
          <option value="ppt">PPT演示文稿</option>
          <option value="word">Word文档</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="additionalInfo">额外信息 (可选)</label>
        <textarea 
          id="additionalInfo" 
          v-model="additionalInfo" 
          placeholder="输入任何额外的要求或信息"
          rows="4"
        ></textarea>
      </div>
      
      <div class="form-group">
        <label for="template">选择模板 (可选)</label>
        <select id="template" v-model="templateId">
          <option value="default">默认模板</option>
          <option v-for="template in templates" :key="template.id" :value="template.id">
            {{ template.name }}
          </option>
        </select>
      </div>
      
      <button type="submit" :disabled="submitting">
        {{ submitting ? '生成中...' : '生成文档' }}
      </button>
    </form>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'DocumentForm',
  data() {
    return {
      topic: '',
      docType: 'ppt',
      additionalInfo: '',
      templateId: 'default',
      submitting: false,
      error: null,
      templates: [
        { id: 'business', name: '商务模板' },
        { id: 'academic', name: '学术模板' },
        { id: 'creative', name: '创意模板' }
      ]
    };
  },
  methods: {
    ...mapActions('documents', ['createDocument']),
    
    async submitForm() {
      if (!this.topic) {
        this.error = '请输入文档主题';
        return;
      }
      
      this.submitting = true;
      this.error = null;
      
      try {
        const documentData = {
          topic: this.topic,
          doc_type: this.docType,
          additional_info: this.additionalInfo,
          template_id: this.templateId
        };
        
        const response = await this.createDocument(documentData);
        console.log('Document created, full response:', response);
        
        // 确保存储完整的响应对象
        localStorage.setItem('currentDocument', JSON.stringify(response));
        
        // 确保使用正确的 ID
        this.$router.push(`/results/${response.id}`);
      } catch (error) {
        this.error = '创建文档时出错，请重试';
        console.error('Submit error:', error);
      } finally {
        this.submitting = false;
      }
    }
  }
};
</script>

<style scoped>
.document-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input, select, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style> 