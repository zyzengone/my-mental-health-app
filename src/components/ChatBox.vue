<template>
  <div class="chat-box">
    <div class="messages">
      <!-- 动态渲染消息列表 -->
      <div class="message" v-for="msg in messages" :key="msg.id" :class="{ 'my-message': msg.isMine }">
        <img :src="msg.isMine ? myAvatar : robotAvatar" :hidden="msg.isMine" alt="头像" class="avatar" />
        <div class="bubble" :class="{ 'align-left': !msg.isMine, 'align-right': msg.isMine }">
          <div class="content">
            {{ msg.text }}
          </div>
        </div>
        <img :src="msg.isMine ? myAvatar : robotAvatar" :hidden="!msg.isMine" alt="头像" class="avatar" />
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
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { sendMsg } from "../api/chat.js";
import robot from '../assets/1.png'
import people from '../assets/2.png'
// 假设的头像图片路径
const myAvatar = people;
const robotAvatar = robot;
const messages = ref([]);
const inputText = ref('');
let conversationId = ref(1);

const props = defineProps({
  conversation: Object
});

// 从 localStorage 读取消息
onMounted(() => {
  const storedMessages = localStorage.getItem('messages');
  if (storedMessages) {
    messages.value = JSON.parse(storedMessages);
  } else {
    messages.value = [
      { id: 1, text: '你好呀，我是你的心理健康知心姐姐！', isMine: false }
    ];
    saveMessagesToLocalStorage()
  }
});

watch(props, (newVal) => {
  if (newVal.conversation) {
    conversationId.value = newVal.conversation.id;
    console.log('newVal.conversation', newVal.conversation)
    const storedMessages = localStorage.getItem('messages');
    if (storedMessages) {
      console.log('storedMessages', storedMessages)
      let storedMessagesObj = JSON.parse(storedMessages)
      console.log('storedMessagesObj', storedMessagesObj)
      console.log('storedMessagesObj[conversationId.value]', storedMessagesObj[conversationId.value])
      if (storedMessagesObj[conversationId.value]){
        messages.value = storedMessagesObj[conversationId.value];
      } else {
        messages.value = [
          { id: 1, text: '你好呀，我是你的心理健康知心姐姐小玲！', isMine: false }
        ];
        saveMessagesToLocalStorage()
      }
    } else {
      messages.value = [
        { id: 1, text: '你好呀，我是你的心理健康知心姐姐！', isMine: false }
      ];
    }
  }
});

const sendMessage = () => {
  if (inputText.value.trim()) {
    const newMessage = {
      id: messages.value.length + 1,
      text: inputText.value,
      isMine: true,
    };
    messages.value.push(newMessage);
    saveMessagesToLocalStorage();

    let data = { 'message': inputText.value };
    sendMsg(data).then(res => {
      const botMessage = {
        id: messages.value.length + 1,
        text: res,
        isMine: false,
      };
      messages.value.push(botMessage);
      saveMessagesToLocalStorage();
    });

    inputText.value = '';
  }
};

const saveMessagesToLocalStorage = () => {
  let currentMessages = getMessagesFromLocalStorage()||{};
  console.log('saveId', currentMessages)
  currentMessages[conversationId.value] = messages.value
  console.log('currentMessages', currentMessages)
  localStorage.setItem('messages', JSON.stringify(currentMessages));
};
const getMessagesFromLocalStorage = () => {
  return JSON.parse(localStorage.getItem('messages'));
};
</script>

<style scoped>
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
  background-color: #fff;
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
  background-color: #e2e2e2;
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

.input-area {
  display: flex;
  padding: 10px;
  align-items: center;
  background-color: #fff;
}
</style>
