import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import VueAxios from 'vue-axios'
//+引入组件库及相关样式
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Vuetify from './plugins/vuetify.js'
//图标
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import 'vuetify/dist/vuetify.min.css'
import vueToPdf from 'vue-to-pdf'
import htmlToPdf from '@/components/Utils/htmlToPdf'
import Base64 from '../js/base64.js'

import VueQuillEditor from 'vue-quill-editor'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'







Vue.use(VueAxios, axios)
//让Vue使用ElementUI
Vue.use(ElementUI)
Vue.use(Vuetify)
Vue.use(vueToPdf);
Vue.use(htmlToPdf)
Vue.use(VueQuillEditor)

Vue.config.productionTip = false
Vue.prototype.$Base64 = Base64;


new Vue({
  router,
  store,
  Vuetify,
  render: h => h(App)
}).$mount('#app')
