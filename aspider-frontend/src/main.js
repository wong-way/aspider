// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

import axios from 'axios'
import Vuex from 'vuex'
import store from './vuex/store'


import ECharts from 'vue-echarts/components/ECharts.vue'
import 'echarts/lib/chart/radar'
import 'echarts/lib/chart/bar'
import 'echarts/lib/chart/pie'
import 'echarts/lib/chart/graph'
import 'echarts/lib/chart/line'

import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/title'
import 'echarts/lib/component/legend'
import 'echarts/lib/component/polar'
Vue.use(ElementUI)
Vue.use(Vuex)
Vue.component('chart', ECharts)

Vue.prototype.axios = axios
Vue.config.productionTip = false

// 开发用，local dev server 接口
axios.defaults.baseURL = 'http://127.0.0.1:5000/'

// 部署用，remote server 接口
// axios.defaults.baseURL = 'http://############/'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
