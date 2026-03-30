// chat.js
import request from '../utils/request.js'

export function getConversations(userId) {
    return request({
        url: '/model/sessions?userId='+userId,
        method: 'get'
    })
}

export function sendMsg(data) {
    return request({
        url: '/model/chat',
        method: 'post',
        data: data
    })
}

export function createConversation(id) {
    return request({
        url: '/model/createSession?userId='+id,
        method: 'post'
    })
}

export function deleteSession(id) {
    return request({
        url: '/model/deleteSession?sessionId='+id,
        method: 'post'
    })
}

export function getConversationMessages(conversationId) {
    return request({
        url: `/model/conversationHistory?sessionId=`+conversationId,
        method: 'get'
    })
}

export function getPersonalityType(userId) {
    return request({
        url: '/model/personality?userId='+userId,
        method: 'get'
    })
}
