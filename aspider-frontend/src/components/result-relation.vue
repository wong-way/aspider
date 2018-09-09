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
                <el-table :data="page_disease_info" style="width:100%" :fit=true>
                  <el-table-column prop="source" label="disease" min-width="100">
                    <template slot-scope="scope">

                      <el-popover trigger="hover" placement="top">
                        <p>mimnumber: {{ scope.row.source.mimnumber }}</p>
                        <p>preferredTitle: {{ scope.row.source.preferredTitle }}</p>
                        <p>shorteningTitle:{{scope.row.source.shorteningTitle}}</p>
                        <div slot="reference" class="name-wrapper">
                          <el-tag size="medium">{{ scope.row.source.mimnumber}}</el-tag>
                        </div>
                      </el-popover>
                    </template>
                  </el-table-column>
                  <el-table-column prop="target" label="target" min-width="100">
                    <template slot-scope="scope">
                      <el-popover trigger="hover" placement="top">
                        <p>mimnumber: {{ scope.row.target.mimnumber }}</p>
                        <p>preferredTitle: {{ scope.row.target.preferredTitle }}</p>
                        <p>shorteningTitle:{{scope.row.target.shorteningTitle}}</p>
                        <div slot="reference" class="name-wrapper">
                          <el-tag size="medium">{{ scope.row.target.mimnumber}}</el-tag>
                        </div>
                      </el-popover>
                    </template>
                  </el-table-column>
                  <el-table-column prop="path" label="path" min-width="100">
                  </el-table-column>
                  <el-table-column label="operation" min-width="200">
                    <template slot-scope="scope">
                      <el-button size="mini" type="primary" @click="handleView(scope.$index, scope.row)">View</el-button>
                      <el-button size="mini" type="info" @click="handleAdd(scope.$index, scope.row)">Add</el-button>
                      <el-button size="mini" type="danger" @click="handleRemove(scope.$index, scope.row)">remove</el-button>
                    </template>
                  </el-table-column>
                </el-table>
                <el-pagination @current-change="handleCurrentChange" :current-page.sync="currentPage" :page-size="pageSize" small layout="total,prev, pager, next, jumper" :total="totalCount">
                </el-pagination>
              </el-row>
            </el-col>
          </el-row>
          <el-row style="margin-top:10px">
            <el-button size="mini" type="danger" @click="handleRemoveAll()">Reset</el-button>

            <chart :options="graph" auto-resize style="width: 100%;height:600px"></chart>
          </el-row>
        </el-card>
      </el-scrollbar>
    </div>

  </div>
</template>

<script>
import vueLoading from "vue-loading-template";
export default {
  data() {
    return {
      loading: true,
      mimnumber: "",
      disease_info: [],
      page_disease_info: [],
      view_disease: {},
      graph: {},

      request_params: [],
      currentPage: 1,
      pageSize: 5,
      totalCount: ""
    };
  },
  components: { "vue-loading": vueLoading },
  created() {
    this.mimnumber = this.$route.params.mimnumber;
  },
  watch: {
    $route: function() {
      this.mimnumber = this.$route.params.mimnumber;
    },
    mimnumber: function() {
      let params = this.mimnumber;
      let url = "/disease/top5item";
      this.axios
        .post(url, {
          params: params
        })
        .then(response => {
          this.disease_info = response.data;
          this.page_disease_info = this.disease_info.slice(0, 5);
          this.totalCount = response.data.length;
          this.loading = false;
        })
        .catch(error => {
          this.loading = false;
        });
    }
  },
  methods: {
    handleView(index, row) {
      this.request_params = [];
      let url = "/disease/link";
      this.request_params.push(row.source.mimnumber);
      this.request_params.push(row.target.mimnumber);
      this.axios
        .post(url, {
          params: this.request_params
        })
        .then(response => {
          this.setGraph(response.data.nodes, response.data.links);
        })
        .catch(error => {
          console.log(error);
        });
    },
    handleAdd(index, row) {
      let url = "/disease/link";
      if (this.request_params.indexOf(row.source.mimnumber) == -1)
        this.request_params.push(row.source.mimnumber);
      if (this.request_params.indexOf(row.target.mimnumber) == -1)
        this.request_params.push(row.target.mimnumber);
      this.axios
        .post(url, {
          params: this.request_params
        })
        .then(response => {
          this.setGraph(response.data.nodes, response.data.links);
        })
        .catch(error => {
          console.log(error);
        });
    },

    handleRemove(index, row) {
      let url = "/disease/link";

      let i = this.request_params.indexOf(row.target.mimnumber);
      if (i != -1) this.request_params.splice(i, 1);

      this.axios
        .post(url, {
          params: this.request_params
        })
        .then(response => {
          this.setGraph(response.data.nodes, response.data.links);
        })
        .catch(error => {
          console.log(error);
        });
    },
    handleRemoveAll() {
      this.graph = {};
      this.request_params = [];
    },

    setGraph: function(nodes, links) {
      let categories = ["disease", "symptom"];

      let tmpLinks = links;
      let tmpNodes = [];
      nodes.forEach(element => {
        let node = {};
        if (element.name.indexOf(this.mimnumber) != -1) {
          node = {
            name: element.name,
            symbolSize: 25,
            draggable: true,
            category: 0,
            force: {
              gravity: 1
            },
         
            itemStyle: {
              normal: {
                color: "#c23531"
              }
            }
          };
        } else {
          if (element.value == "disease") {
            node = {
              name: element.name,
              symbolSize: 25,
              draggable: true,
              category: 0,
              force: {
                gravity: 0.5
              },
              itemStyle: {
                normal: {
                  color: "#c23531"
                }
              }
            };
          } else {
            node = {
              name: element.name,
              symbolSize: 15,
              draggable: true,
              category: 1,
              force: {
                gravity: 0.5
              },
              itemStyle: {
                normal: {
                  color: "#2f4554"
                }
              }
            };
          }
        }

        tmpNodes.push(node);
      });

      this.graph = {
        title: {
          text: "RelationShip",
          left: "right"
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
          data: [{ name: "disease" }, { name: "symptom" }]
        },
        series: [
          {
            type: "graph",
            layout: "force",
            force: {
              repulsion: 200,
              edgeLength: [100, 300]
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

            data: tmpNodes,
            links: tmpLinks,
            categories: [{ name: "disease" }, { name: "symptom" }]
          }
        ]
      };
    },
    handleCurrentChange(val) {
      this.page_disease_info = this.disease_info.slice(
        (this.currentPage - 1) * this.pageSize,
        this.currentPage * this.pageSize
      );
    }
  }
};
</script>

<style scoped >
</style>
