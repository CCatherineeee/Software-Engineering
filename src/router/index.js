import Vue from 'vue'
import VueRouter from 'vue-router'

import StudentHome from '../views/student/studentHome.vue'
import AdminHome from '../views/admin/adminHome.vue'
import TeacherHome from '../views/teacher/teacherHome.vue'
import AssistHome from '../views/assist/assistHome.vue'

import Login from '../views/login/Login.vue'
import AdminLogin from '../views/login/AdminLogin.vue'
import Register from '../views/login/Register.vue'


import StuConcreteCourse from '../views/student/course/concreteCourse.vue'
import TeaConcreteCourse from '../views/teacher/course/concreteCourse.vue'
import AssistConcreteCourse from '../views/assist/course/concreteCourse.vue'


Vue.use(VueRouter)

const routes = [

  {
    path: '/',
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
    path: '/studentome',
    name: 'StudentHome',
    component: StudentHome,
    children: [
      //学生账户
      { path: '/studentHome/control', component: () => import('../views/student/Control.vue') },
      { path: '/studentHome/account', component: () => import('../views/student/account/account.vue') },
      { path: '/studentHome/modifyAccount', component: () => import('../views/student/account/modifyAccount.vue') },
      { path: '/studentHome/modifyPassword', component: () => import('../views/student/account/passwordModify.vue') },

      //课程
      { path: '/studentHome/course', component: () => import('../views/student/course/course.vue') },
      {
        path: '/studentHome/concreteCourse', component: StuConcreteCourse, children: [
          { path: '/studentHome/concreteCourse/Ann', component: () => import('../views/student/course/courseDetail/courseAnnounce.vue') },
          { path: '/studentHome/concreteCourse/Exper', component: () => import('../views/student/course/courseDetail/courseExperiment.vue') },
          { path: '/studentHome/concreteCourse/Peo', component: () => import('../views/student/course/courseDetail/coursePeople.vue') },
          { path: '/studentHome/concreteCourse/Perform', component: () => import('../views/student/course/courseDetail/coursePerformance.vue') },
          { path: '/studentHome/concreteCourse/ConExper', component: () => import('../views/student/course/experiment/experiment.vue') },
          { path: '/studentHome/concreteCourse/FillExper', component: () => import('../views/student/course/experiment/experimentFill.vue') },
          { path: '/studentHome/concreteCourse/File', component: () => import('../views/student/course/courseDetail/courseFile.vue') },
          { path: '/studentHome/concreteCourse/onlineExp', component: () => import('../views/student/course/experiment/onlineExperiment.vue') },
          { path: '/studentHome/concreteCourse/examHome/checkExam', component: () => import('../views/student/Exam/checkExam.vue') },
          { path: '/studentHome/concreteCourse/examHome/exam', component: () => import('../views/student/Exam/checkQuestion.vue') },
          { path: '/studentHome/concreteCourse/examHome/closeExam', component: () => import('../views/student/Exam/closeExam.vue') },
          { path: '/studentHome/concreteCourse/examHome/submit', component: () => import('../views/student/Exam/submit.vue') },


        ]
      },
      { path: '/studentHome/accounce', component: () => import('../views/announce/announce.vue') },
    ]
  },
  {
    //管理员界面
    path: '/adminHome',
    name: 'AdminHome',
    component: AdminHome,
    children: [
      //账户
      { path: '/adminHome/account', component: () => import('../views/admin/account/account.vue') },
      { path: '/adminHome/modifyAccount', component: () => import('../views/admin/account/modifyAccount.vue') },
      { path: '/adminHome/modifyPassword', component: () => import('../views/admin/account/passwordModify.vue') },
      //公告
      { path: '/adminHome/annManage', component: () => import('../views/admin/annManage/annManage.vue') },
      //课程
      {
        path: '/adminHome/courseManage',
        name: 'AdminCourseManage',
        component: () => import('../views/admin/courseManage/courseManageHome.vue'),
        children: [
          { path: '/adminHome/courseManage/courseType', component: () => import('../views/admin/courseManage/courseType.vue') },
          { path: '/adminHome/courseManage/courseTea', component: () => import('../views/admin/courseManage/courseTea.vue') },
        ]
      },
      //用户
      {
        path: '/adminHome/userManage',
        name: 'AdminUserManage',
        component: () => import('../views/admin/userManage/accountManageHome.vue'),
        children: [
          { path: '/adminHome/userManage/accountAdd', component: () => import('../views/admin/userManage/accountAdd.vue') },
          { path: '/adminHome/userManage/accountCheck', component: () => import('../views/admin/userManage/accountCheck.vue') },
          { path: '/adminHome/userManage/accountInfo', component: () => import('../views/admin/userManage/accountInfo.vue') },
          { path: '/adminHome/userManage/accountModify', component: () => import('../views/admin/userManage/accountModify.vue') },
          { path: '/adminHome/userManage/accountCancel', component: () => import('../views/admin/userManage/accountCancel.vue') },
        ]
      },


    ]
  },
  {
    //老师界面
    path: '/teacherHome',
    name: 'TeacherHome',
    component: TeacherHome,
    children: [
      { path: '/teacherHome/control', component: () => import('../views/teacher/Control.vue') },
      //账户
      { path: '/teacherHome/account', component: () => import('../views/teacher/account/account.vue') },
      { path: '/teacherHome/modifyAccount', component: () => import('../views/teacher/account/modifyAccount.vue') },
      { path: '/teacherHome/modifyPassword', component: () => import('../views/teacher/account/passwordModify.vue') },

      //课程
      { path: '/teacherHome/myClass', component: () => import('../views/teacher/course/myClass.vue') },
      { path: '/teacherHome/manageCourse', component: () => import('../views/teacher/course/manageCourse.vue') },
      { path: '/teacherHome/courseClass', component: () => import('../views/teacher/course/courseManage/courseClass.vue') },
      { path: '/teacherHome/manageExperiment', component: () => import('../views/teacher/course/courseManage/manageExperiment.vue') },
      {
        path: '/teacherHome/concreteCourse', component: TeaConcreteCourse, children: [
          { path: '/teacherHome/concreteCourse/Ann', component: () => import('../views/teacher/course/courseDetail/courseAnnounce.vue') },
          { path: '/teacherHome/concreteCourse/Peo', component: () => import('../views/teacher/course/courseDetail/coursePeople.vue') },
          { path: '/teacherHome/concreteCourse/Perform', component: () => import('../views/teacher/course/courseDetail/coursePerformance.vue') },
          { path: '/teacherHome/concreteCourse/Score', component: () => import('../views/teacher/course/courseDetail/courseScore.vue') },
          { path: '/teacherHome/concreteCourse/File', component: () => import('../views/teacher/course/courseDetail/courseFile.vue') },
          { path: '/teacherHome/concreteCourse/Exper', component: () => import('../views/teacher/course/courseDetail/courseExperiment.vue') },

          { path: '/teacherHome/concreteCourse/ConExper', component: () => import('../views/teacher/course/experiment/experiment.vue') },
          { path: '/teacherHome/concreteCourse/stuExper', component: () => import('../views/teacher/course/experiment/stuExper.vue') },

          { path: '/teacherHome/concreteCourse/stuExperList', component: () => import('../views/teacher/course/experiment/stuExperList.vue') },


        ]
      },
      { path: '/teacherHome/concreteCourse/stuExperOnline', component: () => import('../views/teacher/course/experiment/stuExperOnline.vue') },
      {
        path: '/teacherHome/duty-course', component: () => import('../views/teacher/Exam/examHome.vue'), children: [
          { path: '/teacherHome/duty-course/exam/checkExam', component: () => import('../views/teacher/Exam/checkExam.vue') },
          { path: '/teacherHome/duty-course/exam/addExam', component: () => import('../views/teacher/Exam/AddExam.vue') },
          { path: '/teacherHome/duty-course/exam/analysisExam', component: () => import('../views/teacher/Exam/AnalysisExam.vue') },
          { path: '/teacherHome/duty-course/courseInfo', component: () => import('../views/teacher/Exam/CourseInfo.vue') },
          { path: '/teacherHome/duty-course/manageClass', component: () => import('../views/teacher/Exam/ManageClass.vue') },
          { path: '/teacherHome/duty-course/manageEx', component: () => import('../views/teacher/Exam/experiment.vue') },

        ]
      },
      { path: '/teacherHome/concreteCourse/exam', component: () => import('../views/teacher/Exam/checkQuestion.vue') },
      { path: '/teacherHome/accounce', component: () => import('../views/announce/announce.vue') },
    ]
  },

  {
    //助教界面
    path: '/assistHome',
    name: 'AssistHome',
    component: AssistHome,
    children: [
      { path: '/assistHome/control', component: () => import('../views/assist/Control') },
      //账户
      { path: '/assistHome/account', component: () => import('../views/assist/account/account.vue') },
      { path: '/assistHome/modifyAccount', component: () => import('../views/assist/account/modifyAccount.vue') },
      { path: '/assistHome/modifyPassword', component: () => import('../views/assist/account/passwordModify.vue') },

      //课程
      { path: '/assistHome/myClass', component: () => import('../views/assist/course/myClass.vue') },
      {
        path: '/assistHome/concreteCourse', component: AssistConcreteCourse, children: [
          { path: '/assistHome/concreteCourse/Ann', component: () => import('../views/assist/course/courseDetail/courseAnnounce.vue') },
          { path: '/assistHome/concreteCourse/Exper', component: () => import('../views/assist/course/courseDetail/courseExperiment.vue') },
          { path: '/assistHome/concreteCourse/ConExper', component: () => import('../views/assist/course/experiment/experiment.vue') },
          { path: '/assistHome/concreteCourse/stuExperList', component: () => import('../views/assist/course/experiment/stuExperList.vue') },
          { path: '/assistHome/concreteCourse/stuExper', component: () => import('../views/assist/course/experiment/stuExper.vue') },
          { path: '/assistHome/concreteCourse/Score', component: () => import('../views/assist/course/courseDetail/courseScore.vue') },

          { path: '/assistHome/concreteCourse/Peo', component: () => import('../views/assist/course/courseDetail/coursePeople.vue') },
          { path: '/assistHome/concreteCourse/File', component: () => import('../views/assist/course/courseDetail/courseFile.vue') },

        ]
      },
      { path: '/assistHome/concreteCourse/stuExperOnline', component: () => import('../views/assist/course/experiment/stuExperOnline.vue') },
      { path: '/assistHome/accounce', component: () => import('../views/announce/announce.vue') },
    ]
  },

]


const router = new VueRouter({
  routes
})

export default router
