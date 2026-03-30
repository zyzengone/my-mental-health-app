<template>
  <div class="profile-container">
    <el-page-header @back="goBack" content="个人中心"></el-page-header>
    
    <el-form :model="form" label-width="120px" style="margin-top: 20px;">
      <el-form-item label="年龄">
        <el-input-number v-model="form.age" :min="1" :max="120"></el-input-number>
      </el-form-item>
      
      <el-form-item label="生日">
        <el-date-picker
          v-model="form.birthday"
          type="date"
          placeholder="选择日期"
          value-format="YYYY-MM-DD"
        ></el-date-picker>
      </el-form-item>
      
      <el-form-item label="MBTI人格">
        <div class="mbti-selection">
          <div class="mbti-dimension">
            <span class="dimension-label">精力指向</span>
            <el-radio-group v-model="form.mbti.EI">
              <el-radio label="E">外向 (E)</el-radio>
              <el-radio label="I">内向 (I)</el-radio>
            </el-radio-group>
          </div>
          
          <div class="mbti-dimension">
            <span class="dimension-label">信息获取</span>
            <el-radio-group v-model="form.mbti.SN">
              <el-radio label="S">感觉 (S)</el-radio>
              <el-radio label="N">直觉 (N)</el-radio>
            </el-radio-group>
          </div>
          
          <div class="mbti-dimension">
            <span class="dimension-label">决策方式</span>
            <el-radio-group v-model="form.mbti.TF">
              <el-radio label="T">思考 (T)</el-radio>
              <el-radio label="F">情感 (F)</el-radio>
            </el-radio-group>
          </div>
          
          <div class="mbti-dimension">
            <span class="dimension-label">生活方式</span>
            <el-radio-group v-model="form.mbti.JP">
              <el-radio label="J">判断 (J)</el-radio>
              <el-radio label="P">知觉 (P)</el-radio>
            </el-radio-group>
          </div>
          
          <div class="result-display">
            <el-tag type="primary" size="large">
              当前类型: {{ computedMBTI }}
            </el-tag>
          </div>
        </div>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="submitForm">保存</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { useUserStore } from '../store/index.js'

export default {
  data() {
    return {
      form: {
        age: 25,
        birthday: '',
        mbti: {
          EI: 'E',
          SN: 'S',
          TF: 'T',
          JP: 'J'
        }
      }
    }
  },
  computed: {
    computedMBTI() {
      return this.form.mbti.EI + this.form.mbti.SN + this.form.mbti.TF + this.form.mbti.JP;
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    async submitForm() {
      try {
        const userStore = useUserStore();
        await userStore.updateMBTIType(this.computedMBTI);
        this.$message.success('保存成功');
      } catch (error) {
        console.error('保存失败:', error);
        this.$message.error('保存失败: ' + (error.message || '未知错误'));
      }
    }
  }
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.mbti-selection {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.mbti-dimension {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.dimension-label {
  font-weight: bold;
}

.result-display {
  margin-top: 10px;
}
</style>