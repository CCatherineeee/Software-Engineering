import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../views/home/Home.vue'
import UserAccount from '../views/home/user/account.vue'
import ModifyAccount from '../views/home/user/modifyAccount.vue'

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
      { path: '/home/user/account', name: '/home/user/account', component: UserAccount },
      { path: '/home/user/modifyAccount', name: '/home/user/modifyAccount', component: ModifyAccount },
    ]
  },

]


const router = new VueRouter({
  routes
})

export default router
