<template>
  <div id="app">
    <!-- 导航栏，使用 router-link 进行导航 -->
    <nav>
      <router-link to="/">首页</router-link> |
      <router-link to="/chat">心理健康测评与聊天</router-link> |
      <router-link to="/knowledge-graph">医疗知识图谱</router-link>
    </nav>

    <!-- router-view 是路由出口，路由匹配到的组件将在这里渲染 -->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
/* 全局样式 */
body {
  font-family: Arial, sans-serif;
}

nav {
  padding: 1rem;
  background-color: #eee;
  display: flex;
  justify-content: center;
}

nav a {
  margin: 0 1rem;
  text-decoration: none;
  color: #42b983;
}

nav a.router-link-active {
  font-weight: bold;
}
</style>
