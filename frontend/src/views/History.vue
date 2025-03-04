<template>
  <div class="history-page">
    <h1>文档历史记录</h1>
    
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="fetchDocuments">重试</button>
    </div>
    
    <div v-else-if="documents.length === 0" class="empty-state">
      <p>您还没有生成任何文档</p>
      <router-link to="/generate" class="btn primary">创建第一个文档</router-link>
    </div>
    
    <div v-else class="document-list">
      <div 
        v-for="doc in documents" 
        :key="doc.id" 
        class="document-card"
        :class="{ 'completed': doc.status === 'completed', 'failed': doc.status === 'failed' }"
      >
        <div class="document-info">
          <h3>{{ doc.topic }}</h3>
          <p class="document-type">{{ getDocTypeName(doc.doc_type) }}</p>
          <p class="document-date">{{ formatDate(doc.created_at) }}</p>
          <p class="document-status" :class="`status-${doc.status}`">
            {{ getStatusText(doc.status) }}
          </p>
        </div>
        
        <div class="document-actions">
          <router-link :to="`/results/${doc.id}`" class="btn view">
            查看详情
          </router-link>
          <a 
            v-if="doc.status === 'completed' && doc.download_url" 
            :href="doc.download_url" 
            class="btn download"
          >
            下载
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'History',
  computed: {
    ...mapState('documents', ['documents', 'loading', 'error'])
  },
  created() {
    this.fetchDocuments();
  },
  methods: {
    ...mapActions('documents', ['fetchDocuments']),
    
    getDocTypeName(docType) {
      const docTypes = {
        'ppt': 'PPT演示文稿',
        'word': 'Word文档',
        'pdf': 'PDF文档'
      };
      return docTypes[docType] || docType;
    },
    
    getStatusText(status) {
      const statusMap = {
        'queued': '排队中',
        'processing': '处理中',
        'completed': '已完成',
        'failed': '失败'
      };
      return statusMap[status] || status;
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleString();
    }
  }
};
</script>

<style scoped>
.history-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.loading, .error, .empty-state {
  text-align: center;
  margin: 40px 0;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  text-align: center;
}

.primary {
  background-color: #4CAF50;
  color: white;
}

.document-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.document-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-left: 4px solid #ccc;
}

.document-card.completed {
  border-left-color: #4CAF50;
}

.document-card.failed {
  border-left-color: #f44336;
}

.document-info {
  flex: 1;
}

.document-info h3 {
  margin-bottom: 10px;
}

.document-type, .document-date {
  color: #666;
  margin-bottom: 5px;
}

.document-status {
  font-weight: bold;
  margin-top: 10px;
}

.status-queued {
  color: #9e9e9e;
}

.status-processing {
  color: #2196F3;
}

.status-completed {
  color: #4CAF50;
}

.status-failed {
  color: #f44336;
}

.document-actions {
  display: flex;
  gap: 10px;
}

.view {
  background-color: #2196F3;
  color: white;
}

.download {
  background-color: #4CAF50;
  color: white;
}

@media (max-width: 768px) {
  .document-card {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .document-actions {
    margin-top: 15px;
    width: 100%;
  }
  
  .document-actions .btn {
    flex: 1;
    text-align: center;
  }
}
</style> 