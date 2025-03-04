import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8001/api/v1';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
});

// 添加响应拦截器，用于调试
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response || error.message);
    return Promise.reject(error);
  }
);

export default {
  // 创建新文档
  createDocument(documentData) {
    return apiClient.post('/documents/', documentData);
  },
  
  // 获取文档状态
  getDocumentStatus(documentId) {
    return apiClient.get(`/documents/${documentId}/status`);
  },
  
  // 获取文档详情
  getDocument(documentId) {
    return apiClient.get(`/documents/${documentId}`);
  },
  
  // 获取文档列表
  getDocuments() {
    return apiClient.get('/documents/');
  }
}; 