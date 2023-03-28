import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

import {
  Message
} from 'element-ui'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes test_reports mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: 'Dashboard', icon: 'dashboard' }
    }]
  },

  // {
  //   path: '/example',
  //   component: Layout,
  //   redirect: '/example/table',
  //   name: 'Example',
  //   meta: { title: 'Example', icon: 'el-icon-s-help' },
  //   children: [
  //     {
  //       path: 'table',
  //       name: 'Table',
  //       component: () => import('@/views/table/index'),
  //       meta: { title: 'Table', icon: 'table' }
  //     },
  //     {
  //       path: 'tree',
  //       name: 'Tree',
  //       component: () => import('@/views/tree/index'),
  //       meta: { title: 'Tree', icon: 'tree' }
  //     }
  //   ]
  // },

  // {
  //   path: '/form',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'index',
  //       name: 'Form',
  //       component: () => import('@/views/form/index'),
  //       meta: { title: 'Form', icon: 'form' }
  //     }
  //   ]
  // },

  {
    path: '/test_reports',
    component: Layout,
    // redirect: '/test_reports/server',
    name: 'TestReports',
    meta: {
      title: '测试报告',
      icon: 'form'
    },
    children: [
      {
        path: 'server',
        component: () => import('@/views/test_reports/server/index'), // Parent router-view
        name: 'Server',
        meta: { title: 'Server' },
        children: [
          {
            path: 'release130',
            component: () => import('@/views/test_reports/server/release130'),
            name: 'release130',
            meta: { title: 'release130' }
          },
          {
            path: 'release200',
            component: () => import('@/views/test_reports/server/release200'),
            name: 'release200',
            meta: { title: 'release200' }
          }
        ]
      },
      {
        path: 'plugin',
        component: () => import('@/views/test_reports/plugin/index'), // Parent router-view
        name: 'Plugin',
        meta: { title: 'Plugin' },
        children: [
          {
            path: 'release130',
            component: () => import('@/views/test_reports/plugin/release130'),
            name: 'release130',
            meta: { title: 'release130' }
          },
          {
            path: 'release200',
            component: () => import('@/views/test_reports/plugin/release200'),
            name: 'release200',
            meta: { title: 'release200' }
          }
        ]
      },
      {
        path: 'api',
        component: () => import('@/views/test_reports/api/index'),
        name: 'Api',
        meta: { title: 'Api' },
        children: [
          {
            path: 'cpp',
            component: () => import('@/views/test_reports/api/cpp/index'),
            name: 'C++',
            meta: { title: 'C++' },
            children: [
              {
                path: 'release130',
                component: () => import('@/views/test_reports/api/cpp/release130'),
                name: 'release130',
                meta: { title: 'release130' },
                children: [
                  {
                    path: 'ssl102',
                    component: () => import('@/views/test_reports/api/cpp/release130/ssl102'),
                    name: 'ssl102',
                    meta: { title: 'ssl102'}
                  },
                  {
                    path: 'ssl110',
                    component: () => import('@/views/test_reports/api/cpp/release130/ssl110'),
                    name: 'ssl110',
                    meta: { title: 'ssl110' }
                  },
                ]
              },
              
              // {
              //   path: 'release200',
              //   component: () => import('@/views/test_reports/api/cpp/release200'),
              //   name: 'release200',
              //   meta: { title: 'release200' }
              // }
            ]
          },
          {
            path: 'java',
            component: () => import('@/views/test_reports/api/java'),
            name: 'Java',
            meta: { title: 'Java' },
            children: [
              {
                path: 'release130',
                component: () => import('@/views/test_reports/api/java/release130'),
                name: 'release130',
                meta: { title: 'release130' },
                children:[]
              },
              // {
              //   path: 'release200',
              //   component: () => import('@/views/test_reports/api/java/release200'),
              //   name: 'release200',
              //   meta: { title: 'release200' }
              // },
            ]
          },
          {
            path: 'js',
            component: () => import('@/views/test_reports/api/js'),
            name: 'JavaScript',
            meta: { title: 'JavaScript' },
            children: [
              {
                path: 'master',
                component: () => import('@/views/test_reports/api/js/master'),
                name: 'master',
                meta: { title: 'master' },
                children:[]
              },
            ]
          },
        ]
      }
    ]
  },

  {
    path: 'DolphinDB.cn',
    component: Layout,
    children: [
      {
        path: 'https://dolphindb.cn',
        meta: { title: 'DolphinDB.cn', icon: 'link' }
      }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
