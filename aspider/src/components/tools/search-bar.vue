<template>
  <div id="search-bar" class="search" v-bind:class="{show:display}">
      <el-row justify="end" type="flex" align="middle">
        <transition name="slide">
          <div id="search-input" v-show="display">
            <el-col :span="8">
              <div class="select">
                <el-select v-model="search_type" placeholder="Type" size="mini">
                  <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
              </div>
            </el-col>
            <el-col :span=15 style="padding-top:4px;">
              <input placeholder="Enter your search term..." v-model="search_text">
            </el-col>
          </div>
        </transition>
        <el-col :span=3.5>
          <button v-on:click="search"><i class="el-icon-search"></i></i></button>
        </el-col>
      </el-row>
  </div>

</template>

<script>
export default {
  name: 'SearchBar',
  data () {
    return {
      options: [
        {
          value: 'gene',
          label: 'Gene'
        },

        {
          value: 'disease',
          label: 'Disease'
        },

        {
          value: 'symptom',
          label: 'Symptom'
        }
      ],
      search_text: '',
      search_type: ''
    }
  },

  props: {
    display: {
      type: Boolean,
      default: false
    },

    animate: {
      type: Boolean,
      default: false
    }
  },

  methods: {
    search () {
      // 启用动画
      if (!this.animate) {
        if (!this.display) {
          this.display = true
        } else if (this.display && this.search_text === '') {
          this.display = false
        } else {
          this.push()
        }
      } else {
        this.push()
      }
    },

    push () {
      this.$router.push(
        {
          name: 'statistics',
          params: {
            search_type: this.search_type,
            search_text: this.search_text
          }
        }
      )
    }
  }
}
</script>

<style>

.search {
  border: none;
  width: 400px;
}

.search input {
  background: none;
  padding-left: 10px;
  border: none;
  color:#606266;
  font-size: 14px;

}

.search input:focus {
  outline: none;
}

.search button {
  outline: none;
  border: none;
  width: 60px;
  height: 50px;
  background: #2d8cf0;
  color: white;
  font-size: 16px;
}

.select {
  border-right: solid 1px;
  border-right-color: #d2d5dc;
}

.show {
  border: solid 1px;
  border-color: #dddee1;
  text-align: left;
  background: white;
}

.slide-enter-active {
  animation: slide .5s;
}

.slide-leave-active {
  animation: slide .5s reverse;
}

@keyframes slide {
  from {
    -webkit-transform: translate3d(100%, 0, 0);
    transform: translate3d(100%, 0, 0);
    visibility: visible;
  }

  to {
    -webkit-transform: translate3d(0, 0, 0);
    transform: translate3d(0, 0, 0);
  }
}

</style>
