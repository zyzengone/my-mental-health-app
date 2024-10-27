import request from '../utils/request.js'

//示例以application/json格式传参
export function sendMsg(data) {
    return request({
        url: '/ollama/chat',
        method: 'post',
        data: data
    })
}

//示例在url后面拼接参数传参
export function test(params) {
    return request({
        url: '/admin/login',
        method: 'post',
        params: params
    })
}
