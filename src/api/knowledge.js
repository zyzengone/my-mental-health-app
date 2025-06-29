import request from '../utils/request.js'

//示例以application/json格式传参
export function getAllDisease() {
    return request({
        url: '/node/getAll',
        method: 'get'
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
