import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../views/home/Home.vue'
import AdminHome from '../views/admin/adminHome'

import Login from '../views/login/Login.vue'
import AdminLogin from '../views/login/AdminLogin.vue'
import Register from '../views/login/Register.vue'

import ConcreteCourse from '../views/home/course/concreteCourse.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/AdminLogin',
    name: '/AdminLogin',
    component: AdminLogin,
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
      //学生账户
      { path: '/home/student/account', component: () => import('../views/home/student/account.vue') },
      { path: '/home/student/modifyAccount', component: () => import('../views/home/student/modifyAccount.vue') },
      { path: '/home/student/passwordModify', component: () => import('../views/home/student/passwordModify.vue') },

      //课程
      { path: '/home/course', component: () => import('../views/home/course/course.vue') },
      { path: '/home/test', component: () => import('../views/home/course/test.vue') },
      {
        path: '/home/concreteCourse', component: ConcreteCourse, children: [
          { path: '/home/concreteCourse/Ann', component: () => import('../views/home/course/courseDetail/courseAnnounce.vue') },
          { path: '/home/concreteCourse/Exper', component: () => import('../views/home/course/courseDetail/courseExperiment.vue') },
          { path: '/home/concreteCourse/Peo', component: () => import('../views/home/course/courseDetail/coursePeople.vue') },
        ]
      },


      //通知
      { path: '/home/announce', component: () => import('../views/home/announce/announce.vue') },
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
