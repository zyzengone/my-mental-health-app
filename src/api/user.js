import request from '../utils/request.js'
export function submitLogin(data) {
    return request({
        url: '/user/login',
        method: 'post',
        data: data
    })
}

export function getPersonalityType(userId) {
    return request({
        url: '/ollama/getPersonality?userId='+userId,
        method: 'get'
    })
}

export function updatePersonalityType(userId) {
    return request({
        url: '/ollama/updatePersonality?userId='+userId,
        method: 'get'
    })
}

export function getUserWarning() {
    return request({
        url: '/ollama/getUserWarning',
        method: 'get'
    })
}