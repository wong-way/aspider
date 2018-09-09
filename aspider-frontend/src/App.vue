<template>
  <div id="app">
      <el-menu mode="horizontal" :default-active="active" @select="handleSelect">
        <img src="/static/logo.png" class="logo">
        <el-menu-item index="Home">Home</el-menu-item>
        <el-menu-item index="Gene">Gene</el-menu-item>
        <el-menu-item index="Disease">Disease</el-menu-item>
        <el-menu-item index="Symptom">Symptom</el-menu-item>
        <!-- 封装的搜索框 -->
        <search-bar class="nav-search" v-if="!this.if_home"></search-bar>
      </el-menu>
    <router-view></router-view>
    <div class="footer">
      Copyright© belongs to original authors
      <br>
      Programmed By : Huang Wei, Jiang Jiahao, Lai Lingxin
      <br>
      ASpider - Disease Data Network
    </div>
  </div>
</template>

<script>
import SearchBar from './components/tools/search-bar.vue'
export default {
  name: 'app',
  components: {
    'search-bar': SearchBar
  },

  data () {
    return {
      active: 'Home',
      if_home: true
    }
  },
  methods: {
    handleSelect (name) {
      if (name === 'Home') {
        this.if_home = true
        this.$router.push('/')
      } else {
        this.if_home = false
        this.$router.push({name: 'details'})
      }
    }
  }
}
</script>

<style>
#app {
  font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
}

.nav-item{
  float: right;
  margin-right: 50px;
}

.title{
  float: left;
  margin-left: 10px;
  font-size: 25px;
  font-weight: 300;
}

.logo{
  margin-top: 5px;
  margin-left: 20px;
  width: 50px;
  height: 50px;
}

.nav-search {
  float: right;
  margin-right: 20px;
}

.logo {
  float: left;
  margin-right: 20px;
}

.footer {
  border-top: 1px solid #e3e8ee;
  margin-top: 5%;
  margin-bottom: 1%;
  text-align: center;
  padding-top: 10px;
}

</style>
