<template>
  <div id="app">
    <el-container>
      <el-aside >
        <ConversationList
            :conversations="conversations"
            :activeConversation="activeConversation"
            @clickConversation="clickConversation"
            @newConversation="newConversation" />
      </el-aside>
      <el-main>
        <ChatBox v-if="activeConversation" :conversation="activeConversation" />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue';
import ConversationList from '../components/ConversationList.vue';
import ChatBox from '../components/ChatBox.vue';
const conversations = ref([]);

const activeConversation = ref(null);

onMounted(()=>{
  const storedConversations = localStorage.getItem('conversionList');
  if (storedConversations) {
    conversations.value = JSON.parse(storedConversations);
  }
});
const newConversation = () => {
  let conversionList = localStorage.getItem("conversionList")
  if (conversionList){
    conversionList = JSON.parse(conversionList)
    conversations.value = conversionList
  }
  const newId = conversations.value.length + 1;
  const newConversation = { id: newId, name: `谈心${newId}` };
  conversations.value.push(newConversation);
  localStorage.setItem('conversionList', JSON.stringify(conversations.value));
  activeConversation.value = newConversation;
};
const clickConversation = (conversation) => {
  console.log(conversation)
  activeConversation.value = conversation;
}
</script>

<style scoped>
.no-conversation-selected {
  text-align: center;
  padding: 20px;
}
</style>
