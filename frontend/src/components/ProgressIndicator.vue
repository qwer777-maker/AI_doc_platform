<template>
  <div class="progress-container">
    <div class="progress-bar">
      <div 
        class="progress-fill" 
        :style="{ width: `${progress * 100}%` }"
        :class="{ 'completed': status === 'completed', 'failed': status === 'failed' }"
      ></div>
    </div>
    
    <div class="progress-info">
      <div class="progress-status">
        <span class="status-label">状态:</span>
        <span class="status-value" :class="statusClass">{{ statusText }}</span>
      </div>
      
      <div class="progress-percentage">{{ Math.round(progress * 100) }}%</div>
    </div>
    
    <div v-if="message" class="progress-message">
      {{ message }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProgressIndicator',
  props: {
    status: {
      type: String,
      required: true,
      validator: value => ['queued', 'processing', 'completed', 'failed'].includes(value)
    },
    progress: {
      type: Number,
      required: true,
      validator: value => value >= 0 && value <= 1
    },
    message: {
      type: String,
      default: ''
    }
  },
  computed: {
    statusText() {
      const statusMap = {
        'queued': '排队中',
        'processing': '处理中',
        'completed': '已完成',
        'failed': '失败'
      };
      return statusMap[this.status] || this.status;
    },
    statusClass() {
      return `status-${this.status}`;
    }
  }
};
</script>

<style scoped>
.progress-container {
  margin: 20px 0;
}

.progress-bar {
  height: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-fill {
  height: 100%;
  background-color: #4CAF50;
  transition: width 0.3s ease;
}

.progress-fill.completed {
  background-color: #4CAF50;
}

.progress-fill.failed {
  background-color: #f44336;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.status-label {
  font-weight: bold;
  margin-right: 5px;
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

.progress-message {
  font-style: italic;
  color: #666;
}
</style> 