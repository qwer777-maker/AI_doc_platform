<template>
  <header class="app-header">
    <div class="container">
      <div class="logo">
        <router-link to="/">
          <span>AI Doc Platform</span>
        </router-link>
      </div>
      
      <nav class="main-nav">
        <ul>
          <li><router-link to="/">首页</router-link></li>
          <li><router-link to="/generate">创建文档</router-link></li>
          <li><router-link to="/history">历史记录</router-link></li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderComponent'
}
</script>

<style scoped>
.app-header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 15px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo a {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  text-decoration: none;
}

.logo img {
  height: 40px;
}

.main-nav ul {
  display: flex;
  list-style: none;
}

.main-nav li {
  margin-left: 20px;
}

.main-nav a {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.main-nav a:hover,
.main-nav a.router-link-active {
  background-color: #f0f0f0;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
  }
  
  .logo {
    margin-bottom: 15px;
  }
  
  .main-nav ul {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .main-nav li {
    margin: 5px 10px;
  }
}
</style> 