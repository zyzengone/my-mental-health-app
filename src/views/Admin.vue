<template>
  <div class="admin-container">
    <div class="admin-sidebar">
      <el-menu
        default-active="1"
        class="el-menu-vertical"
        background-color="#FFE4C4"
        text-color="#333"
        active-text-color="#FF8C00"
      >
        <el-menu-item index="1" @click="activeTab = 'warnings'">
          <el-icon><Warning /></el-icon>
          <span>预警查看</span>
        </el-menu-item>
      </el-menu>
    </div>
    <div class="admin-content">
      <WarningList v-if="activeTab === 'warnings'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Warning } from '@element-plus/icons-vue'
import WarningList from '../components/WarningList.vue'

const activeTab = ref('warnings')
</script>

<style scoped>
.admin-container {
  display: flex;
  height: calc(100vh - 60px);
}

.admin-sidebar {
  width: 200px;
  background-color: #FFE4C4;
}

.admin-content {
  flex: 1;
  padding: 20px;
  background-color: #fff;
}

.el-menu-vertical {
  border-right: none;
}

.el-menu-item {
  transition: all 0.3s;
}

.el-menu-item:hover {
  background-color: #FFA07A !important;
  color: white !important;
}

.el-menu-item.is-active {
  background-color: #FF8C00 !important;
  color: white !important;
}
</style>