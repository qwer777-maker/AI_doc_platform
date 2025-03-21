import axios from 'axios';

// 根据当前URL选择合适的API路径
const currentPort = window.location.port;
const API_URL = currentPort === '3000' 
  ? 'http://localhost:8001/api/v1'  // 前端在3000端口时直接访问后端
  : '/api/v1';                      // 其他情况使用相对路径

console.log('使用API URL:', API_URL, '当前端口:', currentPort);

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// 添加响应拦截器，用于调试
apiClient.interceptors.response.use(
  response => {
    console.log('API 响应成功:', response);
    return response;
  },
  error => {
    console.error('API Error:', error.response || error.message);
    return Promise.reject(error);
  }
);

// 添加请求拦截器，用于调试
apiClient.interceptors.request.use(
  config => {
    console.log('API 请求:', config.method.toUpperCase(), config.url, config.data || {});
    return config;
  },
  error => {
    console.error('请求配置错误:', error);
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