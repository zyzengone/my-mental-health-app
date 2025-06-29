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
      
      <el-form-item label="人格特质">
        <el-checkbox-group v-model="form.personality">
          <el-checkbox label="外向" name="type"></el-checkbox>
          <el-checkbox label="内向" name="type"></el-checkbox>
          <el-checkbox label="敏感" name="type"></el-checkbox>
          <el-checkbox label="理性" name="type"></el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="submitForm">保存</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        age: 25,
        birthday: '',
        personality: []
      }
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    submitForm() {
      this.$message.success('保存成功');
    }
  }
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
}
</style>