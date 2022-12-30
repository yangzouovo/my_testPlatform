import request from '@/utils/request'

// export function login(data) {
//   return request({
//     url: '/vue-admin-template/user/login',
//     method: 'post',
//     data
//   })
// }

// export function getInfo(token) {
//   return request({
//     url: '/vue-admin-template/user/info',
//     method: 'get',
//     params: { token }
//   })
// }

// export function logout() {
//   return request({
//     url: '/vue-admin-template/user/logout',
//     method: 'post'
//   })
// }


export function login(data) {
  return request({
    url: '/user_auth/user/login',
    method: 'post',
    data
  })
}

export function getInfo(username) {
  return request({
    url: '/user_auth/user/info/',
    method: 'get',
    params: { 'username':username }
  })
}

export function logout() {
  return request({
    url: '/user_auth/user/logout',
    method: 'post'
  })
}