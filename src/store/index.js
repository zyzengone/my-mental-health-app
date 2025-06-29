// src/store/index.js
import { createPinia, defineStore } from 'pinia'
import { submitLogin } from "../api/user.js";
import { updatePersonalityType } from "../api/user.js";
import { getPersonalityType } from "../api/user.js";

export const useUserStore = defineStore('user', {
    state: () => ({
        isAuthenticated: false,
        conversationCount: 0,
        personalityType: null
    }),
    actions: {
        async login(form) {
            try {
                const response = await submitLogin(form);
                // 假设登录成功后，后端返回的数据中包含一个token字段
                const data = response.data;
                console.log(data)
                if (data === '-1') {
                    throw new Error('用户名或密码错误');
                }
                // 将token保存到localStorage
                localStorage.setItem('token', data.token);
                localStorage.setItem('userId', data.userId);
                // 更新状态
                this.token = data.token;
                this.isAuthenticated = true;
                localStorage.setItem('isAuthenticated', 'true');
            } catch (error) {
                console.error('登录失败:', error);
                throw error; // 抛出错误以便在组件中处理
            }
        },
        logout() {
            this.isAuthenticated = false
            localStorage.removeItem('token')
            localStorage.removeItem('isAuthenticated')
        },
        incrementConversationCount() {
            console.log('每3次对话后获取人格类型')
            this.conversationCount++
            if (this.conversationCount % 1 === 0) {
                this.updatePersonalityType()
                console.log('每3次对话后获取人格类型')
            }
        },
        async updatePersonalityType() {
            try {
                const userId = localStorage.getItem('userId')
                const response = await updatePersonalityType(userId)
                this.personalityType = response.data
            } catch (error) {
                console.error('获取人格类型失败:', error)
            }
        },
        async fetchPersonalityType() {
            try {
                const userId = localStorage.getItem('userId')
                const response = await getPersonalityType(userId)
                this.personalityType = response.data.trim()
                console.log('获取人格类型成功:', this.personalityType)
            } catch (error) {
                console.error('获取人格类型失败:', error)
            }
        }

    }
})

const pinia = createPinia()
export default pinia
