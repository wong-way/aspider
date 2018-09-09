<template>
  <div>

    <el-row id="aspider">
      <center>
        <h2>Aspider</h2>
        <p>A online disease infomation analysis system</p>
        <search-bar :display=true :animate=false></search-bar>
      </center>
    </el-row>
    <el-row :gutter="20" style="margin-top:100px">
      <!-- <h1>介绍信息</h1> -->
      <el-col :span="9" :offset="4">
        <!-- <h2>介绍信息</h2> -->

        <div class="block">
          <el-carousel height="350px">
            <el-carousel-item v-for="item in 4" :key="item">
              <h3>{{ item }}</h3>
            </el-carousel-item>
          </el-carousel>
        </div>

      </el-col>
      <el-col :span="7">
        <!-- <h2>统计信息</h2> -->
        <el-card class="card" style="">
          <el-tabs activeName="first">
            <el-tab-pane label="Statistic" name="first">
              <chart :options="graph1" auto-resize style="width: 100%;height:300px"></chart>

            </el-tab-pane>
          </el-tabs>
          <el-tabs activeName="first">
            <el-tab-pane label="Statistic2" name="first">
              <chart :options="graph2" auto-resize style="width: 100%;height:450px"></chart>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>

    </el-row>
    <el-row :gutter="20" style="margin-top:100px">
      <!-- <h1>统计信息</h1> -->
      <el-col :span="4" :offset="4">
        <el-card shadow="hover" class="card">
          <center>
            <span style="font-size:36px" class="intro-card"> 308557</span><br>
            <h1 style="font-size: 22px;text-transform: uppercase;">
              Relation Record
            </h1>
          </center>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="card">
          <center>
            <span style="font-size:36px" class="intro-card"> 4188</span><br>
            <h1 style="font-size: 22px;text-transform: uppercase;">
              Disease
            </h1>
          </center>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="card">
          <center>
            <span style="font-size:36px" class="intro-card"> 4356</span><br>
            <h1 style="font-size: 22px;text-transform: uppercase;">
              Gene
            </h1>
          </center>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="card">
          <center>
            <span style="font-size:36px" class="intro-card"> 42157</span><br>
            <h1 style="font-size: 22px;text-transform: uppercase;">
              Symtopm
            </h1>
          </center>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import SearchBar from "./tools/search-bar.vue";

export default {
  data() {
    return {
      graph1: {},
      graph2: {}
    };
  },
  components: {
    "search-bar": SearchBar
  },
  created: function() {
    //todo 获取数据渲染表格
    let url = "/common/disease_info";
    this.axios
      .get(url)
      .then(response => {
        console.log(response);
        this.graph1 = {
          title: {
            text: "Top 20 Disease Count Infomation"
          },
          color: "#2d8cf0",
          tooltip: {
            trigger: "axis",
            axisPointer: {
              type: "shadow"
            }
          },
          legend: {},
          grid: {
            left: "4%",
            bottom: "3%",
            containLabel: true
          },
          yAxis: {
            type: "value"
          },
          xAxis: {
            type: "category",
            data: response.data.disease,
            axisLabel: {
              interval: 0, //横轴信息全部显示
              rotate: 60 //-30度角倾斜显示
            }
          },
          series: [
            {
              type: "bar",
              data: response.data.count
            }
          ]
        };
      })
      .catch(error => {
        console.log(error);
      });
    url = "/common/inheri_info";
    this.axios
      .get(url)
      .then(response => {
        console.log(response);
        this.graph2 = {
          title: {
            text: "Inheritance Infomation",
          },

          tooltip: {
            position: ["0%", "10%"],
            trigger: "item",
            formatter: "{a} <br/>{b}: {c} ({d}%)"
          },
          legend: {
            orient: "horizontal",
            left: "center",
            bottom: 5,
            data: response.data.inheritance
          },
         
          series: [
            {
              name: "Inheritance Statistics",
              type: "pie",
               center: ['50%', '30%'],
              radius: ["20%", "40%"],
              avoidLabelOverlap: false,
              label: {
                normal: {
                  show: false,
                  position: "center"
                }
              },
              labelLine: {
                normal: {
                  show: false
                }
              },
              data: response.data.items
            }
          ]
        };
      })
      .catch(error => {
        console.log(error);
      });
  }
};
</script>

<style scoped >
#aspider {
  padding-top: 60px !important;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
  font-family: "Open Sans", Arial, Helvetica, Sans-Serif;
}
.card {
  background-color: rgb(243, 243, 243);
}
.intro-card {
  font-family: "Open Sans", Arial, sans-serif;
  text-align: center;
}
.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
