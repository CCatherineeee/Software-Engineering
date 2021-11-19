import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import VueAxios from 'vue-axios'
//+引入组件库及相关样式
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import vuetify from './plugins/vuetify'
//图标
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import vueToPdf from 'vue-to-pdf'
import htmlToPdf from '@/components/Utils/htmlToPdf'

Vue.use(VueAxios, axios)
//让Vue使用ElementUI
Vue.use(ElementUI)
Vue.use(vuetify)
Vue.use(vueToPdf);
Vue.use(htmlToPdf)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
