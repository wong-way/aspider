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
      let categories = ["disease", "symptom"];

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
        } else  {
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
        }
        nodes.push(node);
      });
      
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
            ]
          }
        ]
      };
      console.log(this.graph);
    }
  },
  created() {
    let url = "/disease/link";
     let params = [];
     params.push("146500")
     params.push("213600")
  
    this.axios
      .post(url, {
        params:params
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
