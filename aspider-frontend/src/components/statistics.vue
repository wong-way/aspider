<template>
  <div>

    <el-row>
      <vue-loading v-show="loading" type="bars" color="#409EFF" :size="{ width: '50px', height: '50px' }"></vue-loading>

    </el-row>
    <el-row>

      <chart :options="echartData" auto-resize style="width: 100%;height:500px"></chart>

    </el-row>
    <el-row>

      <chart :options="pie" auto-resize style="width: 100%;height:500px"></chart>

    </el-row>
  </div>

</template>

<script>
import vueLoading from "vue-loading-template";
export default {
  data() {
    return {
      search_text: "demo",

      search_type: "",
      loading: true,
      echartData: {},
      pie: {}
    };
  },
  components: { "vue-loading": vueLoading },
  watch: {
    search_text1(val) {
      this.search_text = val;
      this.setPie(val);
    },
    search_type1(val){
      this.search_type =val;
    }
  },
  methods: {
    setPie: function(val) {
      console.log("set pie");
      let url = "/" + this.search_type + "/statistics";
      if (this.search_type == "") {
        url = "/gene/statistics";
      }
      console.log("pie:"+url)

      let demo = val;
      let params = [];
      let value11;
      let value22;

      params.push(demo);
      this.axios
        .post(url, {
          params: params
        })
        .then(response => {
          this.loading = false;
          value11 = response.data.inheris.ar;
          value22 = response.data.inheris.ad;
      
          this.pie = {
            title: {
              text: "遗传方式统计信息"
            },
            tooltip: {
              trigger: "item",
              formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
              orient: "vertical",
              left: "right",
              data: ["Autosomal recessive", "Autosomal dominant"]
            },
            series: [
              {
                name: "遗传方式",
                type: "pie",
                radius: "55%",
                center: ["50%", "60%"],
                data: [
                  { value: value11, name: "Autosomal recessive" },
                  { value: value22, name: "Autosomal dominant" }
                ],
                itemStyle: {
                  emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: "rgba(0, 0, 0, 0.5)"
                  }
                }
              }
            ]
          };
        })
        .catch(error => {
          this.loading = false;
          console.log(error);
        });
    }
  },
  created() {
    this.echartData = {
      title: {
        text: "疾病数量统计"
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
      xAxis: {
        type: "value",
        boundaryGap: [0, 0.01],
        axisLabel: {
          interval: 0, //横轴信息全部显示
          rotate: -30 //-30度角倾斜显示
        }
      },
      yAxis: {
        type: "category",
        data: [
          "疾病1",
          "疾病2",
          "疾病3",
          "疾病4",
          "疾病5",
          "疾病6",
          "疾病7",
          "疾病8",
          "疾病9",
          "疾病10",
          "疾病11",
          "疾病12",
          "疾病1",
          "疾病2",
          "疾病3",
          "疾病4",
          "疾病5",
          "疾病6",
          "疾病7",
          "疾病8",
          "疾病9",
          "疾病10",
          "疾病11",
          "疾病12"
        ]
      },
      series: [
        {
          type: "bar",
          data: [
            18203,
            23489,
            29034,
            10497,
            13174,
            63023,
            15023,
            32520,
            62485,
            31581,
            45230,
            26895,
            18203,
            23489,
            29034,
            10497,
            13174,
            63023,
            15023,
            32520,
            62485,
            31581,
            45230,
            26895
          ]
        }
      ]
    };
   
    this.search_text = this.$route.params.search_text;
    this.search_type = this.$route.params.search_type;
    this.setPie(this.search_text );
  },
  computed: {
    search_text1() {
      return this.$store.state.search_text;
    },
    search_type1() {
      return this.$store.state.search_type;
    }
  }
};
</script>

<style scoped >
</style>
