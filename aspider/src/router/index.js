import Vue from 'vue'
import Router from 'vue-router'
import home from '@/components/home'
import details from '@/components/details'
import ResultInfo from '@/components/result-info'
import SearchResult from '@/components/search-result'
import Statistics from '@/components/statistics'
import graph from '@/components/graph-test'
import link from '@/components/link-test'
import NewHome from '@/components/new-home'
import ResultRelation from '@/components/result-relation'
Vue.use(Router)

export default new Router({
  routes: [{
      path: '/',
      name: 'home',
      // component: home
      component:NewHome
    },{
      path: '/graph',
      name: 'graph',
      component: graph
    },
    {
      path: '/link',
      name: 'link',
      component: link
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
          path: 'info/:mimnumber',
          name: 'resultInfo',
          component: ResultInfo
        },
        {
          path: 'relation/:mimnumber',
          name: 'resultRelation',
          component: ResultRelation
        }
      ]
    }
  ]
})
