import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../views/home/Home.vue'
import AdminHome from '../views/admin/adminHome'

import Login from '../views/login/Login.vue'
import Register from '../views/login/Register.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    children: [
      //账户
      { path: '/home/user/account', component: () => import('../views/home/user/account.vue') },
      { path: '/home/user/modifyAccount', component: () => import('../views/home/user/modifyAccount.vue') },
      { path: '/home/user/passwordModify', component: () => import('../views/home/user/passwordModify.vue') },

      //课程
      { path: '/home/course', component: () => import('../views/home/course/course.vue') },
    ]
  },
  {
    path: '/adminHome',
    name: 'AdminHome',
    component: AdminHome,
    children: [

      { path: '/adminHome/accountAdd', component: () => import('../views/admin/account/accountAdd.vue') },
      { path: '/adminHome/accountCheck', component: () => import('../views/admin/account/accountCheck.vue') },
      { path: '/adminHome/accountInfo', component: () => import('../views/admin/account/accountInfo.vue') },
      { path: '/adminHome/accountModify', component: () => import('../views/admin/account/accountModify.vue') },
      { path: '/adminHome/accountCancel', component: () => import('../views/admin/account/accountCancel.vue') },

    ]
  },

]


const router = new VueRouter({
  routes
})

export default router
