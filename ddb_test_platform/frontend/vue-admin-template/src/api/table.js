import request from '@/utils/request'

export function getServerResults(pflag,p,v,ps) {
  return request({
    url: '/server/list/',
    method: 'get',
    params:{'pflag':pflag,'p':p,'v':v,'page_size':ps}
  })
}

export function getServerInfo(id) {
  return request({
    url: '/server/list/getinfo',
    method: 'get',
    params:{'id':id}
  })
}

// export function refreshServerResults(params) {
//   return request({
//     url: '/server/list/refresh',
//     method: 'get',
//     params
//   })
// }

export function getPluginResults(pflag,p,v,ps) {
  return request({
    url: '/plugin/list/',
    method: 'get',
    params:{'pflag':pflag,'p':p,'v':v,'page_size':ps}
  })
}

export function getPluginInfo(id) {
  return request({
    url: '/plugin/list/getinfo',
    method: 'get',
    params:{'id':id}
  })
}

export function getApiCppResults(pflag, sv, av) {
  return request({
    url: '/cpp/list/',
    method: 'get',
    params:{'pflag':pflag,'sv':sv,'av':av}
  })
}

export function getApiCppInfo(build_number) {
  return request({
    url: '/cpp/list/getinfo',
    method: 'get',
    params:{'build_number':build_number}
  })
}


export function getApiJavaResults(av) {
  return request({
    url: '/java/list/',
    method: 'get',
    params:{'av':av}
  })
}

export function getApiJavaInfo(build_number) {
  return request({
    url: '/java/list/getinfo',
    method: 'get',
    params:{'build_number':build_number}
  })
}

export function getApiJsResults(av) {
  return request({
    url: '/js/list/',
    method: 'get',
    params:{'av':av}
  })
}

export function getApiJsInfo(build_number) {
  return request({
    url: '/js/list/getinfo',
    method: 'get',
    params:{'build_number':build_number}
  })
}

// export function getList(params) {
//   return request({
//     url: '/api/books',
//     method: 'get',
//     params
//   })
// }

// export function insertList(name, author) {
//   return request({
//     url: '/api/books/insert/',
//     method: 'post',
//     params: {name,author}
//   })
// }

// export function updateList(origin_name,name,author) {
//   return request({
//     url: '/api/books/update/',
//     method: 'post',
//     params: {origin_name,name,author}
//   })
// }

// export function deleteList(name, author) {
//   return request({
//     url: '/api/books/delete/',
//     method: 'post',
//     params: {name, author}
//   })
// }