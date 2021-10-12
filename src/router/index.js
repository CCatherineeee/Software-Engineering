import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../views/home/Home.vue'
import UserAccount from '../views/home/user/account.vue'

import Login from '../views/login/Login.vue'
import Register from '../views/login/Register.vue'


import Test from '../views/test.vue'
import Test1 from '../views/test1.vue'

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
      { path: '/home/user/account', name: '/home/user/account', component: UserAccount },
    ]
  },



  {
    path: '/test',
    name: 'Test',
    component: Test,
  },
  {
    path: '/test1',
    name: 'Test1',
    component: Test1,
  },
]


const router = new VueRouter({
  routes
})

export default router
