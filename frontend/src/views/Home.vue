<template>
  <div class="home">
    <div class="hero">
      <h1>AI 文档平台</h1>
      <p class="subtitle">使用人工智能快速生成专业文档</p>
      
      <div class="cta-buttons">
        <router-link to="/generate" class="btn primary">开始创建</router-link>
        <router-link to="/history" class="btn secondary">查看历史</router-link>
      </div>
    </div>
    
    <div class="features">
      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>PPT演示文稿</h3>
        <p>生成专业的演示文稿，包含结构化内容和精美排版</p>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">📝</div>
        <h3>Word文档</h3>
        <p>创建格式完善的Word文档，适用于报告、论文和其他专业文档</p>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">🚀</div>
        <h3>快速生成</h3>
        <p>只需输入主题，AI将为您完成剩余工作</p>
      </div>
    </div>
    
    <div class="how-it-works">
      <h2>使用方法</h2>
      
      <div class="steps">
        <div class="step">
          <div class="step-number">1</div>
          <div class="step-content">
            <h3>输入主题</h3>
            <p>提供您需要的文档主题和类型</p>
          </div>
        </div>
        
        <div class="step">
          <div class="step-number">2</div>
          <div class="step-content">
            <h3>AI生成</h3>
            <p>我们的AI会分析主题并生成专业内容</p>
          </div>
        </div>
        
        <div class="step">
          <div class="step-number">3</div>
          <div class="step-content">
            <h3>下载使用</h3>
            <p>下载生成的文档并根据需要进行编辑</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.hero {
  text-align: center;
  padding: 60px 20px;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 30px;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.btn {
  display: inline-block;
  padding: 12px 24px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s;
}

.primary {
  background-color: #4CAF50;
  color: white;
}

.secondary {
  background-color: #f0f0f0;
  color: #333;
}

.features {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin: 60px 0;
}

.feature-card {
  flex: 1;
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.how-it-works {
  margin: 60px 0;
}

.how-it-works h2 {
  text-align: center;
  margin-bottom: 40px;
}

.steps {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.step {
  flex: 1;
  display: flex;
  align-items: flex-start;
}

.step-number {
  background-color: #4CAF50;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 15px;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .features, .steps {
    flex-direction: column;
  }
  
  .feature-card, .step {
    margin-bottom: 20px;
  }
}
</style> 