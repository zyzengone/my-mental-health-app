<template>
  <div class="login-container">
    <div class="welcome-message">欢迎注册心理健康评测系统</div>
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>用户注册</span>
        </div>
      </template>
      <el-form :model="form" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" type="email"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input type="password" v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">注册</el-button>
          <div class="login-link">
            已有账号？<router-link to="/login">立即登录</router-link>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { submitRegister } from '../api/user.js'

const form = ref({
  username: '',
  email: '',
  password: ''
})

const router = useRouter()
const onSubmit = async () => {
  if (form.value.username && form.value.email && form.value.password) {
    try {
      let data = await submitRegister(form.value)
      if (data.data >= 1) {
        ElMessage.success('注册成功')
        router.push('/login')
      } else { 
        ElMessage.error('用户已存在')
      }


    } catch (error) {
      console.error(error)
      ElMessage.error('注册失败，请稍后再试')
    }
  } else {
    ElMessage.error('请填写完整信息')
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
  background-color: #FFE4C4; /* 统一浅橙色背景 */
}

.welcome-message {
  font-size: 24px;
  font-weight: bold;
  color: #FF8C00; /* 使用主色调橙色 */
  margin-bottom: 20px;
  text-align: center;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.box-card {
  width: 400px;
  padding: 20px;
  border-radius: 15px;
  background-color: rgba(255, 255, 255, 0.95);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.card-header {
  text-align: center;
  color: #FF8C00;
  font-size: 18px;
  font-weight: bold;
}

.el-form-item__label {
  color: #FF8C00;
}

.el-input__inner {
  border-radius: 10px;
  border: 1px solid #FFA07A;
}

.el-button--primary {
  border-radius: 20px;
  background-color: #FFA07A;
  border: none;
  width: 100%;
  transition: all 0.3s ease;
}

.el-button--primary:hover {
  background-color: #FF8C00;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.login-link {
  margin-top: 10px;
  text-align: center;
  color: #666;
}

.login-link a {
  color: #FF8C00;
  text-decoration: none;
  font-weight: bold;
}
</style>