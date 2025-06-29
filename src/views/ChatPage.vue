<template>
  <div id="app">
    <el-container>
      <!-- 移动设备上的侧边栏按钮 -->
      <el-button type="success" :icon="isSidebarOpen ? ArrowLeft : ArrowRight" :title="isSidebarOpen ? '关闭' : '展开'" v-if="isMobile" @click="toggleSidebar" class="sidebar-toggle">
        {{ isSidebarOpen ? '关闭' : '展开' }}
      </el-button>

      <!-- 侧边栏 -->
      <el-aside :class="{ 'hidden-sidebar': !isSidebarOpen }">
        <ConversationList
            :conversations="conversations"
            :activeConversation="activeConversation"
            @clickConversation="clickConversation"
            @newConversation="newConversation"
            @deleteConversation="deleteConversation"
        />
      </el-aside>

      <!-- 主内容区域 -->
      <el-main>
        <ChatBox v-if="activeConversation" :conversation="activeConversation" :messages="messages" />
        <div v-else class="no-conversation-selected">请选择一个对话或创建新对话</div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, computed } from 'vue';
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue';
import ConversationList from '../components/ConversationList.vue';
import ChatBox from '../components/ChatBox.vue';
import {getConversations, createConversation, getConversationMessages, deleteSession} from '../api/chat.js';
import {ElMessage} from "element-plus";

const conversations = ref([]);
const activeConversation = ref(null);
const messages = ref([]);
const isSidebarOpen = ref(true);
const isMobile = ref(false);

const loadConversations = async () => {
  try {
    const response = await getConversations(localStorage.getItem('userId'));
    conversations.value = response.data;
    console.log('conversionvalue',conversations.value)
  } catch (error) {
    console.error('Failed to load conversations:', error);
  }
};

const saveConversations = () => {
  localStorage.setItem('conversations', JSON.stringify(conversations.value));
};

const fetchMessages = async (conversationId) => {
  try {
    const response = await getConversationMessages(conversationId);
    console.log('messages:', response.data)
    messages.value = response.data;
  } catch (error) {
    console.error('Failed to fetch messages:', error);
  }
};

onMounted(() => {
  loadConversations();
  updateIsMobile();
  window.addEventListener('resize', updateIsMobile);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateIsMobile);
});

const newConversation = async () => {
  try {
    let userId = localStorage.getItem('userId')
    console.log('userId:', userId)
    const response = await createConversation(userId);
    const newConversation = response.data;
    console.log('conversion',newConversation)
    loadConversations()
    // saveConversations();
    activeConversation.value = newConversation;
    fetchMessages(newConversation.sessionId);
  } catch (error) {
    console.error('Failed to create conversation:', error);
  }
};

const clickConversation = (conversation) => {
  activeConversation.value = conversation;
  fetchMessages(conversation.sessionId);
};

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const updateIsMobile = () => {
  isMobile.value = window.innerWidth <= 768; // 根据需要调整断点
  console.log('Current window width:', window.innerWidth, 'isMobile:', isMobile.value);
};

const deleteConversation = (conversation) => {
  deleteSession(conversation.sessionId).then((res)=>{
    if (res.data === 1){
      ElMessage.success('删除成功');
      loadConversations();
    }
  })
};
</script>

<style scoped>
/* 默认样式 */
.el-aside {
  transition: width 0.3s ease;
}

.hidden-sidebar {
  width: 0 !important;
  overflow: hidden;
}

.sidebar-toggle {
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 1000;
  padding: 10px;
}

/* 移动设备上的样式 */
@media (max-width: 768px) {
  .el-aside {
    width: 250px;
  }

  .hidden-sidebar {
    width: 0;
  }
}

.no-conversation-selected {
  text-align: center;
  padding: 20px;
}
</style>
