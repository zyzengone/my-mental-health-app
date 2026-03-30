<template>
  <div class="chat-box">
    <div class="messages">
      <!-- 动态渲染消息列表 -->
      <div class="message" v-for="msg in messages" :key="msg.id || msg.timestamp" :class="{ 'my-message': msg.role === 'user' }">
        <img :src="msg.role === 'user' ? myAvatar : robotAvatar" :hidden="msg.role === 'user'" alt="头像" class="avatar" />
        <div class="bubble" :class="{ 'align-left': msg.role === 'assistant', 'align-right': msg.role === 'user' }">
          <div class="content">
            <template v-if="msg.content && msg.content.startsWith('http')">
              <img :src="msg.content" alt="图片消息" class="image-message" width="100px" height="100px"/>
            </template>
            <template v-else>
              <div v-html="renderMarkdown(msg.content)"></div>
            </template>
          </div>
        </div>
        <img :src="msg.role === 'user' ? myAvatar : robotAvatar" :hidden="msg.role === 'assistant'" alt="头像" class="avatar" />
      </div>
    </div>
    <div class="quick-prompts" v-if="showPrompts && messages.length === 0">
      <div
        class="prompt"
        v-for="(prompt, index) in prompts"
        :key="index"
        @click="selectPrompt(prompt)"
      >
        {{ prompt }}
      </div>
    </div>
    <div class="input-area">
      <el-input
          type="textarea"
          v-model="inputText"
          placeholder="请输入消息"
          @keyup.enter="sendMessage"
      />
      <el-button @click="sendMessage">发送</el-button>
      <el-upload
          action="http://localhost:8080/model/uploadImage"
          :headers="headers"
          :data="uploadData"
          :show-file-list="false"
          :on-success="handleImageUploadSuccess"
          :before-upload="beforeImageUpload"
      >
      </el-upload>
    </div>
  </div>
</template>


<script setup>
import { ref, watch, onMounted } from 'vue';
import robot from '../assets/1.png'
import people from '../assets/2.png'
import { fetchEventSource } from "@microsoft/fetch-event-source";
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import {getConversationMessages} from "../api/chat.js";
import { useUserStore } from "../store/index.js";

// 假设的头像图片路径
const myAvatar = people;
const url =  import.meta.env.VITE_API_URL || 'http://localhost:8080';
const robotAvatar = robot;
const messages = ref([]);
const inputText = ref('');
const selectedModel = ref('deepseek');
let conversationId = ref(null);
const userStore = useUserStore();
const props = defineProps({
  conversation: Object,
});

// 从 localStorage 读取消息
onMounted(() => {
});

const showPrompts = ref(true);
const prompts = ref([
  '有什么方法能缓解焦虑呢',
  '晚上天天失眠怎么办',
  '最近压力很大怎么办',
  '如何改善情绪低落'
]);

const selectPrompt = (prompt) => {
  inputText.value = prompt;
  showPrompts.value = false;
  sendMessage();
};

const fetchMessages = async (sessionId) => {
  try {
    const response = await getConversationMessages(sessionId);
    console.log('messages:', response.data)
    if (response.data && response.data.length > 0) {
      messages.value = response.data;
    }
    // 如果没有历史消息，显示提示
    if (messages.value.length === 0) {
      showPrompts.value = true;
    }
  } catch (error) {
    console.error('Failed to fetch messages:', error);
  }
};

watch(props, (newVal) => {
  if (newVal.conversation && newVal.conversation.sessionId) {
    // 切换会话时先清空旧消息，避免残留
    messages.value = [];
    conversationId.value = newVal.conversation.sessionId
    fetchMessages(newVal.conversation.sessionId)
  }
},{ immediate: true});

const sendMessage = () => {
  if (inputText.value.trim() && conversationId.value) {
    const newMessage = {
      userId: localStorage.getItem('userId'),
      message: inputText.value,
      sessionId: conversationId.value,
      timestamp: Date.now(),
      userFlag: 1,
    };
    messages.value.push({
      id: 'temp-' + Date.now(),
      role: 'user',
      content: inputText.value,
      timestamp: Date.now()
    });
    showPrompts.value = false;
    const BaseUrl = url+"/model/chatStream";
    const botMessage = {
      id: 'temp-ai-' + Date.now(),
      userId: localStorage.getItem('userId'),
      role: 'assistant',
      content: '',
      timestamp: Date.now(),
    };
    let token = localStorage.getItem('token');
    messages.value.push(botMessage);
    userStore.incrementConversationCount();
    fetchEventSource(BaseUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": token
      },
      body: JSON.stringify(newMessage),
      onmessage: (message)=>{
        console.log(message);
        if (message.data && message.data !== '[DONE]') {
          messages.value[messages.value.length-1].content = messages.value[messages.value.length-1].content + message.data;
        }
      },
      onerror: (err) => {
        console.log('Connection error', err);
        if (messages.value.length > 0) {
          messages.value[messages.value.length-1].content = 'AI服务暂时不可用，请稍后再试。';
        }
      },
      onclose:()=> {
        console.log('Connection closed');
      },
    });

    inputText.value = '';
  }
};

// 处理图片上传成功后的逻辑
const handleImageUploadSuccess = (response, file, fileList) => {
  if (!conversationId.value) return;
  
  const newMessage = {
    id: 'temp-' + Date.now(),
    userId: localStorage.getItem('userId'),
    message: url+'/uploads/'+response.data,
    sessionId: conversationId.value,
    timestamp: Date.now(),
    role: 'user',
    type: 'image'
  };
  messages.value.push(newMessage);
  sendImageMessage(newMessage);
};

// 发送图片消息
const sendImageMessage = (newMessage) => {
  const BaseUrl = url+"/model/chatImage";
  const botMessage = {
    id: 'temp-ai-' + Date.now(),
    userId: localStorage.getItem('userId'),
    role: 'assistant',
    content: '',
    timestamp: Date.now(),
  };
  let token = localStorage.getItem('token');
  messages.value.push(botMessage);
  fetchEventSource(BaseUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": token
    },
    body: JSON.stringify({
      sessionId: conversationId.value,
      userId: localStorage.getItem('userId'),
      message: newMessage.message
    }),
    onmessage: (message)=>{
      console.log(message);
      if (message.data && message.data !== '[DONE]') {
        messages.value[messages.value.length-1].content = messages.value[messages.value.length-1].content + message.data;
      }
    },
    onerror: (err) => {
      console.log('Connection error', err);
      if (messages.value.length > 0) {
        messages.value[messages.value.length-1].content = 'AI服务暂时不可用，请稍后再试。';
      }
    },
    onclose:()=> {
      console.log('Connection closed');
    },
  });
};

// 上传图片前的验证逻辑
const beforeImageUpload = (file) => {
  const isLt2M = file.size / 1024 / 1024 < 2;
  if (!isLt2M) {
    ElMessage.error('上传图片大小不能超过 2MB!');
  }
  return isLt2M;
};

// 设置请求头
const headers = {
  Authorization: localStorage.getItem('token')
};

// 设置上传数据
const uploadData = {
  userId: localStorage.getItem('userId'),
  sessionId: conversationId.value
};


// 渲染Markdown并净化HTML
const renderMarkdown = (text) => {
  if (!text) return '';
  const html = marked.parse(text);
  return DOMPurify.sanitize(html);
};

// 清空消息（当切换会话时）
const clearMessages = () => {
  messages.value = [];
  showPrompts.value = true;
};

// 暴露方法给父组件
defineExpose({
  clearMessages
});
</script>

<style scoped>
.model-selector {
  padding: 8px 15px;
  background-color: #FFF5F5;
  border-bottom: 1px solid #E0FFE0;
}

.model-selector :deep(.el-select) {
  width: 150px;
}

.model-selector :deep(.el-input__inner) {
  border-radius: 15px;
  border: 1px solid #FFB6C1;
  background-color: #FFF9F9;
  height: 32px;
  line-height: 32px;
}

.model-selector :deep(.el-input__inner:focus) {
  border-color: #FF8C00;
}
.chat-box {
  display: flex;
  flex-direction: column;
  height: 90vh;
  background-color: #f5f5f5;
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
  padding: 10px;
  background-color: #FFF5F5;
}

.message {
  display: flex;
  margin-bottom: 10px;
}

.my-message {
  justify-content: flex-end;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 4px 8px;
}

.bubble {
  max-width: 60%;
  padding: 8px 12px;
  border-radius: 12px;
  background-color: #ffffff;
  word-wrap: break-word;
}

.my-message .bubble {
  background-color: #dcf8c6;
}

.align-left {
  margin-left: 5px;
}

.align-right {
  margin-right: 5px;
}

.quick-prompts {
  display: flex;
  height: 40px;
  gap: 8px;
  padding: 8px 12px;
  background-color: #FFF5F5;
  overflow-x: auto;
  border-bottom: 1px solid #E0FFE0;
}

.prompt {
  color: #555;
  padding: 4px 10px;
  font-size: 12px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
  border-radius: 12px;
  background-color: rgba(144, 238, 144, 0.3);
}

.prompt:hover {
  background-color: rgba(144, 238, 144, 0.5);
  color: #333;
}

.input-area {
  display: flex;
  padding: 15px;
  align-items: center;
  background-color: #FFF5F5;
  gap: 10px;
}

.input-area :deep(.el-textarea__inner) {
  border-radius: 20px;
  border: 1px solid #FFB6C1;
  background-color: #FFF9F9;
  padding: 12px 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.input-area :deep(.el-button) {
  background-color: #FF8C00;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 12px 24px;
  transition: all 0.3s ease;
}

.input-area :deep(.el-button:hover) {
  background-color: #FF6B00;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Markdown内容样式 */
.content :deep(p) {
  margin: 8px 0;
  line-height: 1.5;
}

.content :deep(a) {
  color: #1890ff;
  text-decoration: none;
}

.content :deep(a:hover) {
  text-decoration: underline;
}

.content :deep(code) {
  background-color: #f0f0f0;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: monospace;
}

.content :deep(pre) {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}

.content :deep(blockquote) {
  border-left: 3px solid #ddd;
  padding-left: 10px;
  color: #666;
  margin-left: 0;
}

.content :deep(ul),
.content :deep(ol) {
  padding-left: 20px;
}

.content :deep(h1),
.content :deep(h2),
.content :deep(h3),
.content :deep(h4),
.content :deep(h5),
.content :deep(h6) {
  margin: 16px 0 8px;
  font-weight: bold;
}
</style>
