<template>
  <div class="warning-list">
    <el-card shadow="hover" class="warning-card">
      <template #header>
        <div class="card-header">
          <h3>心理健康预警</h3>
          <el-button type="primary" @click="refreshWarnings" circle>
            <el-icon><Refresh /></el-icon>
          </el-button>
        </div>
      </template>

      <el-table :data="warnings" style="width: 100%" border>
        <el-table-column prop="userId" label="用户id" width="120" />
        <el-table-column prop="warningTime" label="触发时间" width="180" />
        <el-table-column prop="type" label="预警类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getTagType(row.type)">
              {{ row.type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="预警内容" />
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button size="small" @click="handleDetail(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getUserWarning } from '../api/user'

const warnings = ref([])
const loading = ref(false)

onMounted(() => {
  fetchWarnings()
})

const fetchWarnings = async () => {
  try {
    loading.value = true
    const res = await getUserWarning()
    warnings.value = res.data || []
    console.log(res.data)
  } catch (error) {
    ElMessage.error('获取预警列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const getTagType = (type) => {
  const typeMap = {
    '抑郁': 'danger',
    '焦虑': 'warning',
    '自杀': 'error'
  }
  return typeMap[type] || ''
}

const refreshWarnings = () => {
  fetchWarnings()
  ElMessage.success('已刷新预警列表')
}

const handleDetail = (row) => {
  // TODO: 显示预警详情
  console.log('查看详情:', row)
}
</script>

<style scoped>
.warning-list {
  padding: 20px;
}

.warning-card {
  border-radius: 8px;
  border: 1px solid #FFA07A;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.el-button {
  background-color: #FFA07A;
  border: none;
}

.el-button:hover {
  background-color: #FF8C00;
}

.el-table {
  margin-top: 10px;
}

.el-tag {
  border-radius: 12px;
}
</style>