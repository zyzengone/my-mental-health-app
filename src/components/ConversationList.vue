<template>
  <el-menu default-active="1" class="el-menu-vertical-demo">
    <el-menu-item index="new-conversation" @click="createNewConversation">
      <i class="el-icon-plus"></i>
      创建新会话
    </el-menu-item>
    <el-menu-item
        v-for="conversation in conversations"
        :key="conversation.id"
        :index="conversation.id.toString()"
        @click="selectConversation(conversation)"
    >
      {{ conversation.name }}
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  conversations: Array,
  activeConversation: Object
});
const emit = defineEmits(['newConversation','clickConversation']);

const createNewConversation = () => {
  emit('newConversation');
};

const selectConversation = conversation => {
  console.log('clickConversation', conversation)
  emit('clickConversation', conversation)
};
</script>
