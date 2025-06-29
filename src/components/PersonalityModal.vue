<template>
  <el-dialog
    v-model="visible"
    title="人格特征分析"
    width="500px"
    :before-close="handleClose"
  >
    <div class="personality-content">
      <h3>{{ title }}</h3>
      <p>{{ description }}</p>
      <div class="traits">
        <h4>主要特征：</h4>
        <ul>
          <li v-for="trait in traits" :key="trait">{{ trait }}</li>
        </ul>
      </div>
    </div>
    <template #footer>
      <el-button type="primary" @click="handleClose">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  personalityType: {
    type: String,
    required: true
  }
})

const visible = ref(false)

const personalityData = {
  'ISTJ': {
    title: 'ISTJ - 检查员型',
    description: '实际而务实，注重事实和细节，可靠且有责任感。',
    traits: [
      '可靠且负责任',
      '实际且注重事实',
      '喜欢秩序和组织',
      '传统且保守'
    ]
  },
  'ISFJ': {
    title: 'ISFJ - 保护者型',
    description: '温暖友善，尽责且忠诚，注重实际帮助他人。',
    traits: [
      '关心他人需求',
      '可靠且忠诚',
      '注重传统和稳定',
      '实践性强的学习者'
    ]
  },
  'INFJ': {
    title: 'INFJ - 咨询师型',
    description: '富有洞察力和同情心，追求意义和深度联系。',
    traits: [
      '深刻的思想家',
      '富有同情心',
      '重视和谐',
      '有远见和洞察力'
    ]
  },
  'INTJ': {
    title: 'INTJ - 战略家型',
    description: '独立且具有战略思维，追求知识和能力。',
    traits: [
      '独立思考',
      '战略思维',
      '追求知识和能力',
      '高度自信'
    ]
  },
  'ISTP': {
    title: 'ISTP - 巧匠型',
    description: '冷静的观察者，擅长解决实际问题。',
    traits: [
      '冷静且灵活',
      '逻辑分析能力强',
      '喜欢动手解决问题',
      '冒险精神'
    ]
  },
  'ISFP': {
    title: 'ISFP - 艺术家型',
    description: '温和敏感，注重审美和当下体验。',
    traits: [
      '敏感且友善',
      '注重审美',
      '活在当下',
      '灵活且适应性强'
    ]
  },
  'INFP': {
    title: 'INFP - 治愈者型',
    description: '理想主义且充满同情心，追求真实和自我表达。',
    traits: [
      '理想主义者',
      '富有同情心',
      '重视个人价值',
      '创造性思维'
    ]
  },
  'INTP': {
    title: 'INTP - 建筑师型',
    description: '逻辑性强，喜欢理论和抽象思考。',
    traits: [
      '逻辑分析能力强',
      '独立思考',
      '喜欢理论和抽象概念',
      '创新思维'
    ]
  },
  'ESTP': {
    title: 'ESTP - 挑战者型',
    description: '精力充沛，适应性强，注重实际行动。',
    traits: [
      '行动导向',
      '适应性强',
      '务实且现实',
      '喜欢冒险'
    ]
  },
  'ESFP': {
    title: 'ESFP - 表演者型',
    description: '外向热情，喜欢与他人分享快乐。',
    traits: [
      '热情外向',
      '喜欢社交',
      '实践性强',
      '活在当下'
    ]
  },
  'ENFP': {
    title: 'ENFP - 倡导者型',
    description: '充满热情和创造力，善于激励他人。',
    traits: [
      '热情且有创意',
      '善于社交',
      '乐观积极',
      '善于激励他人'
    ]
  },
  'ENTP': {
    title: 'ENTP - 辩论家型',
    description: '聪明且好奇，喜欢挑战和智力辩论。',
    traits: [
      '创新思维',
      '喜欢智力挑战',
      '适应性强',
      '善于辩论'
    ]
  },
  'ESTJ': {
    title: 'ESTJ - 监督者型',
    description: '实际且传统，注重效率和秩序。',
    traits: [
      '组织能力强',
      '注重效率',
      '传统且实际',
      '责任感强'
    ]
  },
  'ESFJ': {
    title: 'ESFJ - 供给者型',
    description: '温暖友善，喜欢帮助和照顾他人。',
    traits: [
      '关心他人',
      '喜欢和谐',
      '责任感强',
      '传统且有组织'
    ]
  },
  'ENFJ': {
    title: 'ENFJ - 教育家型',
    description: '富有魅力且善于交际，喜欢指导和帮助他人成长。',
    traits: [
      '善于交际',
      '富有同情心',
      '善于激励他人',
      '注重和谐'
    ]
  },
  'ENTJ': {
    title: 'ENTJ - 指挥官型',
    description: '果断且自信，天生的领导者。',
    traits: [
      '自信且果断',
      '战略思维',
      '领导能力强',
      '注重效率'
    ]
  }
}

const { title, description, traits } = computed(() => {
  return personalityData[props.personalityType] || {
    title: '未知人格类型',
    description: '系统尚未分析出您的人格类型',
    traits: []
  }
}).value

const handleClose = () => {
  visible.value = false
}

defineExpose({
  show: () => visible.value = true
})
</script>

<style scoped>
.personality-content {
  padding: 0 20px;
}
.personality-content h3 {
  color: #FF8C00;
  margin-bottom: 15px;
}
.personality-content p {
  margin-bottom: 15px;
  line-height: 1.6;
}
.traits ul {
  padding-left: 20px;
}
.traits li {
  margin-bottom: 8px;
}
</style>