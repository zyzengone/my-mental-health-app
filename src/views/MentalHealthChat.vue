<template>
  <el-container class="chat-container">
    <el-aside width="200px" class="sidebar">
      <!-- 侧边栏内容，如好友列表 -->
    </el-aside>
    <el-main class="chat-main">
      <el-card class="chat-box">
        <!-- 消息列表 -->
        <div class="message" v-for="(message, index) in messages" :key="index">
          <el-avatar :src="message.avatar" />
          <div class="content">{{ message.text }}</div>
        </div>
      </el-card>
      <el-input
          type="textarea"
          v-model="inputMessage"
          placeholder="输入消息..."
          class="input-message"
          @keyup.enter="sendMessage"
      />
      <el-button type="primary" @click="sendMessage">发送</el-button>
    </el-main>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      messages: [],
      inputMessage: '',
    };
  },
  methods: {
    sendMessage() {
      if (this.inputMessage.trim() === '') return;
      this.messages.push({
        text: this.inputMessage,
        avatar: 'your-avatar-url',
      });
      this.inputMessage = '';
    },
  },
};
</script>

<style scoped>
.chat-container {
  height: 100vh;
  display: flex;
}
.sidebar {
  background-color: #f5f5f5;
}
.chat-main {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
.chat-box {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
}
.input-message {
  margin-top: 20px;
}
</style>
