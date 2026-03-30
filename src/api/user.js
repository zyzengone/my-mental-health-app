import request from '../utils/request.js'
export function submitLogin(data) {
    return request({
        url: '/user/login',
        method: 'post',
        data: data
    })
}

export function submitRegister(data) {
    return request({
        url: '/user/register',
        method: 'post',
        data: data
    })
}

export function getPersonalityType(userId) {
    return request({
        url: '/model/getPersonality?userId='+userId,
        method: 'get'
    })
}

// 恢复原有的updatePersonalityType函数
export function updatePersonalityType(userId) {
    return request({
        url: '/model/updatePersonality?userId='+userId,
        method: 'get'
    })
}

// 添加新的updateMBTIType函数用于处理MBTI人格类型更新
export function updateMBTIType(userId, mbtiType) {
    return request({
        url: '/model/savePersonality?userId='+userId+'&personality='+mbtiType,
        method: 'get'
    })
}

export function getUserWarning() {
    return request({
        url: '/model/getUserWarning',
        method: 'get'
    })
}