import Vue from 'vue'
import Router from 'vue-router'
import home from '@/components/home'
import details from '@/components/details'
import ResultDetail from '@/components/result-detail'
import SearchResult from '@/components/search-result'
import Statistics from '@/components/statistics'
import graph from '@/components/graph-test'

Vue.use(Router)

export default new Router({
  routes: [{
      path: '/',
      name: 'home',
      component: home
    },{
      path: '/graph',
      name: 'graph',
      component: graph
    },

    {
      path: '/details',
      name: 'details',
      component: SearchResult,
      children: [{
          path: "",
          name: "statistics",
          component: Statistics,
        },
        {
          path: ':mimnumber',
          name: 'resultDetail',
          component: ResultDetail
        }
      ]
    }
  ]
})
