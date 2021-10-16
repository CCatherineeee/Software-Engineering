import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import VueAxios from 'vue-axios'
// import { createApp } from 'vue'
//+引入组件库及相关样式
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'


// const app = createApp(App)

Vue.use(VueAxios, axios)
    //让Vue使用ElementUI
Vue.use(ElementUI)

Vue.config.productionTip = false

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')