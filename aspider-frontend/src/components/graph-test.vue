<template>
  <div>
    <el-row :gutter="16">
      <el-col :offset="8">
        <chart :options="graph" auto-resize></chart>
      </el-col>

    </el-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      graph: {}
    };
  },
  components: {},
  methods: {
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
            category: 2,
            itemStyle: {
              normal: {
                color: "#2f4554"
              }
            }
          };
        } else if (element.value == "gene") {
          node = {
            name: element.name,
            category: 1,
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
            category: 4,
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
            category: 3,
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
      // data.forEach(element => {
      //   let disease = {
      //     name: element[0].preferredTitle,
      //     symbolSize: 25,
      //     draggable: true,
      //     category: 0,
      //     tooltip: {
      //       trigger: "item",
      //       //   formatter: "{a} <br/>{b}: {c} ({d}%)"
      //       formatter: function(params) {
      //         return categories[params.data.category] + "<br/>" + params.name;
      //       }
      //     },
      //     itemStyle: {
      //       normal: {
      //         color: "#c23531"
      //       }
      //     }
      //   };
      //   let symptom = {
      //     name: element[1].symptom,
      //     symbolSize: 15,
      //     draggable: true,
      //     category: 2,
      //     tooltip: {
      //       trigger: "item",
      //       //   formatter: "{a} <br/>{b}: {c} ({d}%)"
      //       formatter: function(params) {
      //         return categories[params.data.category] + "<br/>" + params.name;
      //       }
      //     },
      //     itemStyle: {
      //       normal: {
      //         color: "#2f4554"
      //       }
      //     }
      //   };
      //   let gene = {
      //     name: element[3].number,
      //     category: 1,
      //     symbolSize: 10,
      //     draggable: true,
      //     tooltip: {
      //       trigger: "item",
      //       //   formatter: "{a} <br/>{b}: {c} ({d}%)"
      //       formatter: function(params) {
      //         return categories[params.data.category] + "<br/>" + params.name;
      //       }
      //     },
      //     itemStyle: {
      //       normal: {
      //         color: "#61a0a8"
      //       }
      //     }
      //   };
      //   let type = {
      //     name: element[2].name,
      //     category: 4,
      //     symbolSize: 10,
      //     draggable: true,
      //     tooltip: {
      //       trigger: "item",
      //       //   formatter: "{a} <br/>{b}: {c} ({d}%)"
      //       formatter: function(params) {
      //         return categories[params.data.category] + "<br/>" + params.name;
      //       }
      //     },
      //     itemStyle: {
      //       normal: {
      //         color: "#d48265"
      //       }
      //     }
      //   };
      //   let inheri = {
      //     name: element[4].name,
      //     category: 3,
      //     symbolSize: 10,
      //     draggable: true,
      //     tooltip: {
      //       trigger: "item",
      //       //   formatter: "{a} <br/>{b}: {c} ({d}%)"
      //       formatter: function(params) {
      //         return categories[params.data.category] + "<br/>" + params.name;
      //       }
      //     },
      //     itemStyle: {
      //       normal: {
      //         color: "#91c7ae"
      //       }
      //     }
      //   };
      //   // 添加节点
      //   if (!nodeMap.has(disease.name)) nodeMap.set(disease.name, disease);
      //   if (!nodeMap.has(symptom.name)) nodeMap.set(symptom.name, symptom);
      //   if (!nodeMap.has(gene.name)) nodeMap.set(gene.name, gene);
      //   if (!nodeMap.has(type.name)) nodeMap.set(type.name, type);
      //   if (!nodeMap.has(inheri.name)) nodeMap.set(inheri.name, inheri);
      //   let link1 = {
      //     source: disease.name,
      //     target: symptom.name,
      //     value: "Behave"
      //   };
      //   let link2 = {
      //     source: symptom.name,
      //     target: type.name,
      //     value: "Belong"
      //   };
      //   let link3 = {
      //     source: disease.name,
      //     target: gene.name,
      //     value: "Cause"
      //   };
      //   let link4 = {
      //     source: disease.name,
      //     target: inheri.name,
      //     value: "Observe"
      //   };
      //   links.add(link1);
      //   links.add(link2);
      //   links.add(link3);
      //   links.add(link4);
      // });

      // let nodes = [];
      // nodeMap.forEach(function(value, key, map) {
      //   nodes.push(value);
      // });
      this.graph = {
        title: {
          text: "Graph demo"
        },
        tooltip: {
          position: ["0%", "0%"],
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
      console.log(this.graph);
    }
  },
  created() {
    let url = "/disease/graph";
    this.axios
      .post(url, {
        params: "614172"
      })
      .then(response => {
        this.setGraph(response.data);
      })
      .catch(error => {
        console.log(error);
      });
  }
};
</script>

<style scoped >
</style>
