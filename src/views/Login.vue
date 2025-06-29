<template>
  <div class="login-container">
    <div class="welcome-message">欢迎使用心理健康评测系统</div>
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>用户登录</span>
        </div>
      </template>
      <el-form :model="form" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input type="password" v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { useUserStore} from "../store/index.js";

const form = ref({
  username: '',
  password: ''
})

const router = useRouter()
const userStore = useUserStore()
const onSubmit = async () => {
  if (form.value.username && form.value.password) {
    try {
      await userStore.login(form.value);
      ElMessage.success('登录成功');
      router.push('/chat');
    } catch (error) {
      console.error(error);
      ElMessage.error('登录失败，请检查用户名和密码');
    }
  } else {
    ElMessage.error('请输入用户名和密码');
  }
}

</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #deedcb, #6490d3); /* 温馨渐变背景色 */
}

.welcome-message {
  font-size: 24px;
  font-weight: bold;
  color: #333; /* 根据背景调整颜色 */
  margin-bottom: 20px;
  text-align: center;
}

.box-card {
  width: 400px;
  padding: 20px;
  border-radius: 15px; /* 添加圆角 */
  background-color: rgba(255, 255, 255, 0.9); /* 半透明背景色，与背景融合 */
}

.card-header {
  text-align: center;
  color: #333; /* 根据背景调整颜色 */
}

.el-form-item__label {
  color: #333; /* 根据背景调整颜色 */
}

.el-input__inner {
  border-radius: 10px; /* 输入框圆角 */
}

.el-button--primary {
  border-radius: 10px; /* 按钮圆角 */
}
</style>

