<template>
  <footer class="app-footer">
    <div class="container">
      <p>&copy; {{ currentYear }} AI Doc Platform. 保留所有权利。</p>
      <div class="footer-links">
        <a href="#">关于我们</a>
        <a href="#">使用条款</a>
        <a href="#">隐私政策</a>
        <a href="#">联系我们</a>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterComponent',
  computed: {
    currentYear() {
      return new Date().getFullYear();
    }
  }
}
</script>

<style scoped>
.app-footer {
  background-color: #f9f9f9;
  padding: 20px 0;
  margin-top: 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-links {
  display: flex;
  gap: 20px;
}

.footer-links a {
  color: #666;
  text-decoration: none;
}

.footer-links a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
    text-align: center;
  }
  
  p {
    margin-bottom: 15px;
  }
  
  .footer-links {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style> 