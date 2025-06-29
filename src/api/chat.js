// chat.js
import request from '../utils/request.js'

export function getConversations(userId) {
    return request({
        url: '/ollama/sessions?userId='+userId,
        method: 'get'
    })
}

export function sendMsg(data) {
    return request({
        url: '/ollama/chat',
        method: 'post',
        data: data
    })
}

export function createConversation(id) {
    return request({
        url: '/ollama/createSession?userId='+id,
        method: 'post'
    })
}

export function deleteSession(id) {
    return request({
        url: '/ollama/deleteSession?sessionId='+id,
        method: 'post'
    })
}

export function getConversationMessages(conversationId) {
    return request({
        url: `/ollama/conversationHistory?sessionId=`+conversationId,
        method: 'get'
    })
}

export function getPersonalityType(userId) {
    return request({
        url: '/ollama/personality?userId='+userId,
        method: 'get'
    })
}
