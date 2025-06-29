<template>
  <div class="home-container">
    <el-row :gutter="20" type="flex" justify="center">
      <el-col :span="8">
        <el-card
            class="card card-2"
            :body-style="{ padding: '20px', textAlign: 'center' }"
            @click.native="navigateTo('/chat')"
        >
          <div class="card-title">心理健康评测与聊天</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card
            class="card card-3"
            :body-style="{ padding: '20px', textAlign: 'center' }"
            @click.native="navigateTo('/knowledge-graph')"
        >
          <div class="card-title">医疗知识图谱</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  methods: {
    navigateTo(path) {
      this.$router.push(path);
    },
  },
};
</script>

<style scoped>
.home-container {
  display: flex;
  justify-content: center;
  padding: 20px;
}

.card {
  cursor: pointer;
  height: 100px;
  margin-bottom: 200px;
  display: flex;
  padding: 100px;
  align-items: center;
  justify-content: center;
}

.card-1 {
  background-color: #409eff;
  color: white;
}

.card-2 {
  background-color: #67c23a;
  color: white;
}

.card-3 {
  background-color: #e6a23c;
  color: white;
}
</style>
