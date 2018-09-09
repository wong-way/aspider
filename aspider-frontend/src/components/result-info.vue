<template>
  <div style="text-align:left">
    <vue-loading v-show="loading" type="bars" color="#409EFF" :size="{ width: '50px', height: '50px' }"></vue-loading>
    <div style="height:1400px">
      <el-scrollbar style="height:100%">
        <el-card shadow="always" v-show="!loading">
          <el-row>
            <el-col :span="22" :offset="0.5">
              <el-row>
                <h3>#mimnumber </h3>
                <p>{{mimnumber}}</p>
              </el-row>
              <el-row>
                <h3>#Disease</h3>
                <p>
                  {{data.preferredTitle }}({{data.shorteningTitle}})
                </p>
              </el-row>
              <el-row>
                <h3>#inheritance</h3>
                <p>
                  {{data.inheritance}}
                </p>
              </el-row>
              <el-row>
                <h3>#Symptom</h3>

                <div>
                  <el-collapse v-model="value" accordion>
                    <el-collapse-item :title=item.type v-for="item in data.symptoms">
                      <li v-for="s in item.symptom">
                        {{s}}
                      </li>
                    </el-collapse-item>
                  </el-collapse>
                </div>

              </el-row>
            </el-col>
          </el-row>
          <el-row style="margin-top:10px">
            <el-col :span=20 :offset=2>
              <el-row :gutter="16">
                <chart :options="pie" auto-resize style="width: 100%;height:400px"></chart>
              </el-row>

              <el-row>
                <chart :options="graph" auto-resize style="width: 100%;height:400px"></chart>
              </el-row>
            </el-col>
          </el-row>

        </el-card>
      </el-scrollbar>
    </div>

  </div>
</template>

<script>
import vueLoading from "vue-loading-template";
export default {
  name: "ResultInfo",
  data() {
    let data = [];
    for (let i = 0; i <= 360; i++) {
      let t = i / 180 * Math.PI;
      let r = Math.sin(2 * t) * Math.cos(2 * t);
      data.push([r, i]);
    }

    return {
      seriesData: [],
      loading: "true",
      value: "0",
      mimnumber: "",
      disease: {
        mimnumber: "210900",
        preferredTitle: "BLOOM SYNDROME",
        shorteningTitle: "BLM",
        inheritance: "Autosomal recessive",
        symtomCount: "42",
        position: ["growthHeight", "growthOther", "headAndNeckHead"]
      },
      symptoms: [
        {
          position: "growthHeight",
          symptom: [
            "Average adult male height 151cm",
            "Average adult female height 144cm"
          ]
        },
        {
          position: "growthOther",
          symptom: ["Prenatal onset growth retardation", "Growth failure"]
        },
        {
          position: "headAndNeckHead",
          symptom: ["Dolichocephaly", "Microcephaly"]
        },
        {
          position: "headAndNeckFace",
          symptom: ["Narrow", "Malar hypoplasia"]
        },
        {
          position: "headAndNeckEars",
          symptom: ["Prominent ears"]
        }
      ],
      data: {},
      pie: {},

      graph: {}
    };
  },
  components: {
    "vue-loading": vueLoading
  },
  created() {
    this.mimnumber = this.$route.params.mimnumber;
  },
  methods: {
    setPie: function(data, label) {
      this.pie = {
        title: {
          text: "Disease parts statistics",
          x: "center"
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
          orient: "horizontal",
          left: "center",
          bottom: 5,
          data: label
        },
        series: [
          {
            center:["50%","40%"],
            name: "part",
            type: "pie",
            radius: ["20%", "30%"],
            data: data
          }
        ]
      };
    },
    setGraph: function(data) {
      let categories = ["disease", "symptom", "gene", "type", "inheritance"];
      let links = data.links;
      let nodes = [];
      data.nodes.forEach(element => {
        let node = {};
        if (element.value == "disease") {
          node = {
            name: element.name,
            symbolSize: 25,
            draggable: true,
            category: 0,
            itemStyle: {
              normal: {
                color: "#c23531"
              }
            }
          };
        } else if (element.value == "symptom") {
          node = {
            name: element.name,
            symbolSize: 15,
            draggable: true,
            category: 1,
            itemStyle: {
              normal: {
                color: "#2f4554"
              }
            }
          };
        } else if (element.value == "gene") {
          node = {
            name: element.name,
            category: 2,
            symbolSize: 10,
            draggable: true,
            itemStyle: {
              normal: {
                color: "#61a0a8"
              }
            }
          };
        } else if (element.value == "type") {
          node = {
            name: element.name,
            category: 3,
            symbolSize: 10,
            draggable: true,
            itemStyle: {
              normal: {
                color: "#d48265"
              }
            }
          };
        } else {
          node = {
            name: element.name,
            category: 4,
            symbolSize: 10,
            draggable: true,
            itemStyle: {
              normal: {
                color: "#91c7ae"
              }
            }
          };
        }
        nodes.push(node);
      });
      this.graph = {
        title: {
          text: "Disease Network Graph",
          x: "center"
        },
        tooltip: {
          position: ["0%", "10%"],
          formatter: function(params) {
            if (params.data.source) {
              //注意判断，else是将节点的文字也初始化成想要的格式
              return params.data.value;
            } else {
              return categories[params.data.category] + "<br/>" + params.name;
            }
          }
        },
        animationDurationUpdate: 1500,
        animationEasingUpdate: "quinticInOut",
        color: ["#c23531", "#2f4554", "#61a0a8", "#d48265", "#91c7ae"],
        legend: {
          bottom: 5,
          show: true,
          data: [
            { name: "disease" },
            { name: "symptom" },
            { name: "gene" },
            { name: "type" },
            { name: "inheritance" }
          ]
        },
        series: [
          {
            type: "graph",
            layout: "force",
            force: {
              repulsion: 100,
              edgeLength: 30
            },
            symbolSize: 5,
            roam: true,

            label: {
              normal: {
                show: false
              }
            },
            edgeSymbolSize: [1, 3],
            edgeLabel: {
              normal: {
                show: false,
                textStyle: {
                  fontSize: 13
                }
                // formatter: "{c}"
              }
            },

            data: nodes,
            links: links,
            categories: [
              { name: "disease" },
              { name: "symptom" },
              { name: "gene" },
              { name: "type" },
              { name: "inheritance" }
            ]
          }
        ]
      };
  
    }
  },
  watch: {
    $route: function() {
      this.mimnumber = this.$route.params.mimnumber;
    },
    mimnumber: function() {
      let params = this.mimnumber;
      let url = "/disease/detail";
      this.axios
        .post(url, {
          params: params
        })
        .then(response => {
          let tempSeries = [];
          let tempLabel = [];
          this.data = response.data;
          for (let i = 0; i < response.data.symptoms.length; i++) {
            tempLabel.push(response.data.symptoms[i].type);
            tempSeries.push({
              name: response.data.symptoms[i].type,
              value: response.data.symptoms[i].symptom.length
            });
          }
          this.setPie(tempSeries, tempLabel);
          // console.log(this.seriesData);
          this.loading = false;
        })
        .catch(error => {
          this.loading = false;
        });
      url = "/disease/graph";
      this.axios
        .post(url, {
          params: params
        })
        .then(response => {
          this.setGraph(response.data);
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
};
</script>

<style scoped >
.el-scrollbar__wrap {
  overflow-x: hidden;
}
</style>
