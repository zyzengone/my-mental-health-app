<template>
  <el-menu default-active="1" class="el-menu-vertical-demo custom-menu">
    <el-menu-item index="new-conversation" @click="createNewConversation">
      <i class="el-icon-plus"></i>
      创建新会话
    </el-menu-item>
    <el-menu-item
        v-for="conversation in conversations"
        :key="conversation.sessionId"
        :index="conversation.sessionId"
        @click="selectConversation(conversation)"
        @mouseover="showDeleteIcon = true"
        @mouseleave="showDeleteIcon = false"
    >
      {{ '谈心'+conversation.id }}
      <el-button type="danger" class="icon-delete" circle :icon="Delete"  @click.stop="deleteConversation(conversation)"/>
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';
import {CircleClose, Delete} from "@element-plus/icons-vue";

const props = defineProps({
  conversations: Array,
  activeConversation: Object
});
const emit = defineEmits(['newConversation', 'clickConversation', 'deleteConversation']);

const showDeleteIcon = ref(false);

const createNewConversation = () => {
  emit('newConversation');
};

const selectConversation = conversation => {
  console.log('clickConversation', conversation);
  emit('clickConversation', conversation);
};

const deleteConversation = conversation => {
  console.log('deleteConversation', conversation);
  emit('deleteConversation', conversation);
};

</script>

<style scoped>

.el-menu-item {
  color: #333; /* 设置文字颜色为深灰色 */
  font-size: 16px; /* 设置字体大小 */
  position: relative; /* 使删除图标相对定位 */
}

.el-menu-item .icon-delete {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
}
:deep(.el-menu-item [class^=el-icon]){
  font-size: 18px;
  margin-right: 0!important;
  text-align: center;
  vertical-align: middle;
  width: var(--el-menu-icon-width);
}

.el-menu {
  border-right: none;
}

.el-menu-item {
  transition: all 0.3s ease;
  margin: 4px 8px;
  border-radius: 8px;
}

.el-menu-item:hover {
  background-color: #FFE4C4 !important;
}

.el-menu-item.is-active {
  background-color: #FFDAB9 !important;
  font-weight: bold;
}
</style>
