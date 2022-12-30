import router from './router'
import store from './store'
import { Message } from 'element-ui'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import { getToken } from '@/utils/auth' // get token from cookie
import getPageTitle from '@/utils/get-page-title'

NProgress.configure({ showSpinner: false }) // NProgress Configuration

const whiteList = ['/login'] // no redirect whitelist

router.beforeEach(async(to, from, next) => {
  // start progress bar
  NProgress.start()

  // set page title
  document.title = getPageTitle(to.meta.title)

  // determine whether the user has logged in
  let hasToken = getToken()
  const tokenStartTime = window.localStorage.getItem('tokenStartTime')
  console.log(tokenStartTime)

  //token过期时间
  const timeOver = 1 * 24 * 60 * 60 * 1000

  // 当前时间
  let date = new Date().getTime()
  // 如果大于说明是token过期了
  if(date - tokenStartTime > timeOver) {
    hasToken = null
  }

  if (hasToken) {
    if (to.path === '/login') {
      // if is logged in, redirect to the home page
      next({ path: '/' })
      NProgress.done()
    } else {
      const hasGetUserInfo = store.getters.name
      if (hasGetUserInfo) {
        next()
      } else {
        try {
          // get user info
          await store.dispatch('user/getInfo')

          next()
        } catch (error) {
          // remove token and go to login page to re-login
          await store.dispatch('user/resetToken')
          // Message.error({message: null || "出现错误，请稍后再试"})
          next(`/login?redirect=${to.path}`)
          NProgress.done()
        }
      }
    }
  } 
  else {
    if (whiteList.indexOf(to.path) !== -1) {
      // in the free login whitelist, go directly
      next()
    } 
    else if(!hasToken){
      if (to.path == '/login') return next()
      Message.error("登录已过期，请重新登录")
      return next('/login')
      // 如果token没有过期，又是选择了登录页面就直接重定向到首页，不需要重新输入账户密码
    } 
    else if (to.path == '/login') {
      return next('/dashboard')
    }
    else {
      // other pages that do not have permission to access are redirected to the login page.
      next(`/login?redirect=${to.path}`)
      NProgress.done()
    }
  }
})

router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})
