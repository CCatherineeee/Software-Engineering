import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../views/home/Home.vue'
import AdminHome from '../views/admin/adminHome'
import TeacherHome from '../views/teacher/teacherHome.vue'

import Login from '../views/login/Login.vue'
import AdminLogin from '../views/login/AdminLogin.vue'
import Register from '../views/login/Register.vue'

import StuConcreteCourse from '../views/home/course/concreteCourse.vue'
import TeaConcreteCourse from '../views/teacher/course/concreteCourse.vue'



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
    //学生界面
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
        path: '/home/concreteCourse', component: StuConcreteCourse, children: [
          { path: '/home/concreteCourse/Ann', component: () => import('../views/home/course/courseDetail/courseAnnounce.vue') },
          { path: '/home/concreteCourse/Exper', component: () => import('../views/home/course/courseDetail/courseExperiment.vue') },
          { path: '/home/concreteCourse/Peo', component: () => import('../views/home/course/courseDetail/coursePeople.vue') },
          { path: '/home/concreteCourse/Perform', component: () => import('../views/home/course/courseDetail/coursePerformance.vue') },
          { path: '/home/concreteCourse/ConExper', component: () => import('../views/home/course/experiment/experiment.vue') },
          { path: '/home/concreteCourse/FillExper', component: () => import('../views/home/course/experiment/experimentFill.vue') },
          { path: '/home/concreteCourse/File', component: () => import('../views/home/course/courseDetail/courseFile.vue') },


        ]
      },

      //通知
      { path: '/home/announce', component: () => import('../views/home/announce/announce.vue') },
    ]
  },
  {
    //管理员界面
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
  {
    //老师界面
    path: '/teacherHome',
    name: 'TeacherHome',
    component: TeacherHome,
    children: [
      //账户
      { path: '/teacherHome/teacher/account', component: () => import('../views/teacher/account/account.vue') },
      { path: '/teacherHome/teacher/modifyAccount', component: () => import('../views/teacher/account/modifyAccount.vue') },
      { path: '/teacherHome/teacher/passwordModify', component: () => import('../views/teacher/account/passwordModify.vue') },

      //课程
      { path: '/teacherHome/course', component: () => import('../views/teacher/course/course.vue') },
      { path: '/teacherHome/manageCourse', component: () => import('../views/teacher/course/manageCourse.vue') },
      { path: '/teacherHome/courseClass', component: () => import('../views/teacher/course/courseManage/courseClass.vue') },
      {
        path: '/teacherHome/concreteCourse', component: TeaConcreteCourse, children: [
          { path: '/teacherHome/concreteCourse/Ann', component: () => import('../views/teacher/course/courseDetail/courseAnnounce.vue') },
          { path: '/teacherHome/concreteCourse/Peo', component: () => import('../views/teacher/course/courseDetail/coursePeople.vue') },
          { path: '/teacherHome/concreteCourse/Perform', component: () => import('../views/teacher/course/courseDetail/coursePerformance.vue') },
          { path: '/teacherHome/concreteCourse/File', component: () => import('../views/teacher/course/courseDetail/courseFile.vue') },
          { path: '/teacherHome/concreteCourse/Exper', component: () => import('../views/teacher/course/courseDetail/courseExperiment.vue') },

          { path: '/teacherHome/concreteCourse/stuExper', component: () => import('../views/teacher/course/experiment/stuExper.vue') },
          { path: '/teacherHome/concreteCourse/stuExperList', component: () => import('../views/teacher/course/experiment/stuExperList.vue') },
          { path: '/teacherHome/concreteCourse/PreviewExper', component: () => import('../views/teacher/course/experiment/previewExper.vue') },
          { path: '/teacherHome/concreteCourse/addExper', component: () => import('../views/teacher/course/experiment/addExperiment.vue') },




        ]
      },
    ]
  },

]


const router = new VueRouter({
  routes
})

export default router
