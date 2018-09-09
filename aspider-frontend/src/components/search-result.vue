<template>
  <div>
    <el-row :butter="20">
      <el-col :span="22" :offset="1">
        <div style="margin-top: 15px;">
          <el-input placeholder="e.g. Parkinson SLC52A3" v-model="search_text" class="input-with-select">
            <el-select v-model="search_type" slot="prepend" placeholder="请选择" style="width:100px;">
              <el-option v-for="item in search_options" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
            <el-button slot="append" icon="el-icon-search" v-on:click="search"></el-button>
          </el-input>
        </div>
      </el-col>
    </el-row>
    <el-row style="margin-top: 15px;">
      <vue-loading v-show="loading" type="bars" color="#409EFF" :size="{ width: '50px', height: '50px' }"></vue-loading>
    </el-row>
    <!-- <el-row style="margin-top: 15px;" v-show="!loading">
      <el-col :span="22" :offset="1">
        <el-row>
          <el-card>
            <el-checkbox :indeterminate="isIndeterminatePos" v-model="checkAllPos" @change="handleCheckAllPosChange">Postions</el-checkbox>
            <div style="margin: 15px 0;"></div>
            <el-checkbox-group v-model="checkedPositions" @change="handleCheckedPosChange">
              <el-checkbox v-for="p in positionOptions" :label="p" :key="p">{{p}}</el-checkbox>
            </el-checkbox-group>
            <div style="margin: 15px 0;"></div>
            <el-checkbox :indeterminate="isIndeterminateInheri" v-model="checkAllInheri" @change="handleCheckAllInheriChange">Inheritance</el-checkbox>
            <div style="margin: 15px 0;"></div>
            <el-checkbox-group v-model="checkedInheris" @change="handleCheckedInheriChange">
              <el-checkbox v-for="i in inheriOptions" :label="i" :key="i">{{i}}</el-checkbox>
            </el-checkbox-group>
          </el-card>
        </el-row>
      </el-col>
    </el-row> -->

    <el-row style="margin-top: 15px;" v-show="!loading">
      <el-col :span="22" :offset="1">
        <el-tabs v-model="activeTab" type="card">
          <el-tab-pane label="Information Summary" name="first">
            <el-card  style="margin-top: 15px;" >
              <el-checkbox :indeterminate="isIndeterminatePos" v-model="checkAllPos" @change="handleCheckAllPosChange">Postions</el-checkbox>
              <div style="margin: 15px 0;"></div>
              <el-checkbox-group v-model="checkedPositions" @change="handleCheckedPosChange">
                <el-checkbox v-for="p in positionOptions" :label="p" :key="p">{{p}}</el-checkbox>
              </el-checkbox-group>
              <div style="margin: 15px 0;"></div>
              <el-checkbox :indeterminate="isIndeterminateInheri" v-model="checkAllInheri" @change="handleCheckAllInheriChange">Inheritance</el-checkbox>
              <div style="margin: 15px 0;"></div>
              <el-checkbox-group v-model="checkedInheris" @change="handleCheckedInheriChange">
                <el-checkbox v-for="i in inheriOptions" :label="i" :key="i">{{i}}</el-checkbox>
              </el-checkbox-group>
            </el-card>
            <el-card  style="margin-top: 15px;" >
              <el-row :butter="20">
                <el-col :span="10">
                  <result-list ref="item" :listdata="listData" :posdata="posData"></result-list>
                </el-col>
                <el-col :span="13" :offset="1" style="height:1400px">

                  <router-view></router-view>

                </el-col>
              </el-row>
            </el-card>
          </el-tab-pane>
          <el-tab-pane label="数据分析" name="second">
            <el-card>
              <el-row style="margin-top:10px">
                <el-col :span=20 :offset=2>
                  <el-row :gutter="16">
                    <el-col :span="12">
                      <chart :options="echart1" auto-resize style="width: 100%;height:400px"></chart>
                    </el-col>
                    <el-col :span="12">
                      <chart :options="echart2" auto-resize style="width: 100%;height:400px"></chart>
                    </el-col>
                  </el-row>
                  <el-row>
                    <chart :options="relationChart" auto-resize style="width: 100%;height:400px"></chart>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>

          </el-tab-pane>
          <el-tab-pane label="症状信息" name="third">症状信息</el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>

  </div>
</template>

<script>
import ResultList from "./result-list";
import ResultInfo from "./result-info.vue";
import SearchBar from "./tools/search-bar.vue";
import vueLoading from "vue-loading-template";

export default {
  name: "SearchResult",
  components: {
    "result-list": ResultList,
    "result-info": ResultInfo,
    "vue-loading": vueLoading
  },
  data() {
    let data = [];
    for (let i = 0; i <= 360; i++) {
      let t = i / 180 * Math.PI;
      let r = Math.sin(2 * t) * Math.cos(2 * t);
      data.push([r, i]);
    }

    return {
      search_text: "",
      search_type: "",
      listData: [],
      posData: [],
      search_options: [
        {
          value: "gene",
          label: "Gene"
        },

        {
          value: "disease",
          label: "Disease"
        },

        {
          value: "symptom",
          label: "Symptom"
        }
      ],
      loading: true,
      value: "0",
      echart1: {
        title: {
          text: "统计分析占位图"
        },
        axisLabel: { interval: 0 },
        tooltip: {},
        radar: {
          // shape: 'circle',
          name: {
            textStyle: {
              color: "#fff",
              backgroundColor: "#999",
              borderRadius: 3,
              padding: [3, 5]
            }
          },
          indicator: [
            { name: "sales", max: 6500 },
            { name: "Administration", max: 16000 },
            { name: "Information Techology", max: 30000 },
            { name: "Customer Support", max: 38000 },
            { name: "Developmen）", max: 52000 },
            { name: "Marketing", max: 25000 }
          ]
        },
        series: [
          {
            name: "预算 vs 开销（Budget vs spending）",
            type: "radar",
            // areaStyle: {normal: {}},
            data: [
              {
                value: [4300, 10000, 28000, 35000, 50000, 19000],
                name: "预算分配（Allocated Budget）"
              }
            ]
          }
        ]
      },
      echart2: {
        title: {
          text: "统计分析占位图"
        },
        legend: {
          data: ["line"]
        },
        polar: {
          center: ["50%", "54%"]
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross"
          }
        },
        angleAxis: {
          type: "value",
          startAngle: 0
        },
        radiusAxis: {
          min: 0
        },
        series: [
          {
            coordinateSystem: "polar",
            name: "line",
            type: "line",
            showSymbol: false,
            data: data
          }
        ],
        animationDuration: 2000
      },
      relationChart: {
        title: {
          text: "NRAS基因示例"
        },
        tooltip: {},
        animationDurationUpdate: 1500,
        animationEasingUpdate: "quinticInOut",
        color: ["#83e0ff", "#45f5ce", "#b158ff"],
        legend: {
          show: true,
          data: [
            { name: "gene", textStyle: { color: "#000" } },
            { name: "disease", textStyle: { color: "#000" } },
            { name: "symptom", textStyle: { color: "#000" } }
          ]
        },
        series: [
          {
            type: "graph",
            layout: "force",
            force: {
              repulsion: 50,
              edgeLength: 20
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
                },
                formatter: "{c}"
              }
            },

            data: [
              {
                name: "NRAS",
                symbolSize: 10,
                draggable: true,
                category: 1,
                itemStyle: {
                  normal: {
                    borderColor: "#04f2a7",
                    borderWidth: 6,
                    shadowBlur: 20,
                    shadowColor: "#04f2a7",
                    color: "#001c43"
                  }
                }
              },

              {
                name: "GILLES DE LA TOURETTE SYNDROME",
                symbolSize: 8,
                draggable: true,
                category: 0,
                itemStyle: {
                  normal: {
                    borderColor: "#82dffe",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#04f2a7",
                    color: "#001c43"
                  }
                }
              },
              {
                name: "NEVUS, EPIDERMAL",
                draggable: true,
                symbolSize: 8,
                itemStyle: {
                  normal: {
                    borderColor: "#82dffe",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#04f2a7",
                    color: "#001c43"
                  }
                },
                category: 0
              },
              {
                name: "MELANOSIS, NEUROCUTANEOUS",
                symbolSize: 8,
                draggable: true,
                category: 0,
                itemStyle: {
                  normal: {
                    borderColor: "#82dffe",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#04f2a7",
                    color: "#001c43"
                  }
                }
              },

              //表型
              {
                name: "Multiple nevi:skinNailsHairSkin",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name: "Pigmented moles	:skinNailsHairSkin",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name: "Woolly hair nevus (in some patients):skinNailsHairSkin",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Hyperpigmented patches of skin (in some patients):skinNailsHairSkin",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Raised, scaly, and/or hyperkeratotic areas of skin (in some patients):	skinNailsHairSkin",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Patches of tightly curled scalp hair adjacent to straight hair (in some patients):skinNailsHairHair",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name: "Some patient may be asymptomatic:miscellaneous",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name: "Onset in first years of life:miscellaneous",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name: "Susceptibility to malignant melanoma:neoplasia",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Syringomyelia (in some patients):neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Arachnoid cysts (in some patients):neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Spinal cysts (in some patients):neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Meningioma (in some patients):neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Choroid plexus papilloma (in some patients):neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Leptomeningeal melanocytosis (in some patients):neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Hydrocephalus (in some patients):neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Seizures (in some patients):neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },

              {
                name:
                  "Delayed development (in some patients):neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Dandy-Walker malformation (in some patients):neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Parenchymal neuromelanosis:neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Giant pigmented nevi, often in lumbosacral region:skinNailsHairSkin",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name: "Numerous congenital melanocytic nevi:skinNailsHairSkin",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name: "Male:Female ratio 4:1:miscellaneous",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name: "Motor and vocal tics:neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Attention deficit hyperactivity disorder (ADHD):neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name:
                  "Obsessive-compulsive behavior:neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name: "Aggressive behavior	:neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name: "Self mutilation	:neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },

              {
                name: "Coprolalia:neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name: "Echolalia:neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              },
              {
                name: "Sleep disturbance :neurologicCentralNervousSystem",
                category: 2,
                symbolSize: 5,
                draggable: true,
                itemStyle: {
                  normal: {
                    borderColor: "#b457ff",
                    borderWidth: 4,
                    shadowBlur: 10,
                    shadowColor: "#b457ff",
                    color: "#001c43"
                  }
                }
              }
            ],
            links: [
              {
                source: "NRAS",
                target: "GILLES DE LA TOURETTE SYNDROME",
                value: "Cause"
              },
              {
                source: "NRAS",
                target: "MELANOSIS, NEUROCUTANEOUS",
                value: "Cause"
              },
              {
                source: "NRAS",
                target: "NEVUS, EPIDERMAL",
                value: "Cause"
              },

              //表型关系
              {
                source: "Sleep disturbance :neurologicCentralNervousSystem",
                target: "GILLES DE LA TOURETTE SYNDROME",
                value: "Behave"
              },
              {
                source: "Echolalia:neurologicCentralNervousSystem",
                target: "GILLES DE LA TOURETTE SYNDROME",
                value: "Behave"
              },
              {
                source: "Coprolalia:neurologicCentralNervousSystem",
                target: "GILLES DE LA TOURETTE SYNDROME",
                value: "Behave"
              },
              {
                source: "Self mutilation	:neurologicCentralNervousSystem",
                target: "GILLES DE LA TOURETTE SYNDROME",
                value: "Behave"
              },
              {
                source: "Aggressive behavior	:neurologicCentralNervousSystem",
                target: "GILLES DE LA TOURETTE SYNDROME",
                value: "Behave"
              },
              {
                source:
                  "Obsessive-compulsive behavior:neurologicCentralNervousSystem",
                target: "GILLES DE LA TOURETTE SYNDROME",
                value: "Behave"
              },
              {
                source:
                  "Attention deficit hyperactivity disorder (ADHD):neurologicCentralNervousSystem",
                target: "GILLES DE LA TOURETTE SYNDROME",
                value: "Behave"
              },
              {
                source: "Motor and vocal tics:neurologicCentralNervousSystem",
                target: "GILLES DE LA TOURETTE SYNDROME",
                value: "Behave"
              },
              {
                source: "Male:Female ratio 4:1:miscellaneous",
                target: "GILLES DE LA TOURETTE SYNDROME",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target:
                  "Numerous congenital melanocytic nevi:skinNailsHairSkin",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target:
                  "Giant pigmented nevi, often in lumbosacral region:skinNailsHairSkin",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target:
                  "Parenchymal neuromelanosis:neurologicCentralNervousSystem",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target:
                  "Dandy-Walker malformation (in some patients):neurologicCentralNervousSystem",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target:
                  "Delayed development (in some patients):neurologicCentralNervousSystem",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target:
                  "Seizures (in some patients):neurologicCentralNervousSystem",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target:
                  "Hydrocephalus (in some patients):neurologicCentralNervousSystem",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target:
                  "Leptomeningeal melanocytosis (in some patients):neurologicCentralNervousSystem",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target:
                  "Choroid plexus papilloma (in some patients):neurologicCentralNervousSystem",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target:
                  "Meningioma (in some patients):neurologicCentralNervousSystem",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target:
                  "Spinal cysts (in some patients):neurologicCentralNervousSystem",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target:
                  "Arachnoid cysts (in some patients):neurologicCentralNervousSystem",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target:
                  "Syringomyelia (in some patients):neurologicCentralNervousSystem",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target: "Susceptibility to malignant melanoma:neoplasia",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target: "Onset in first years of life:miscellaneous",
                value: "Behave"
              },
              {
                source: "MELANOSIS, NEUROCUTANEOUS",
                target: "Some patient may be asymptomatic:miscellaneous",
                value: "Behave"
              },
              {
                source: "NEVUS, EPIDERMAL",
                target: "Multiple nevi:skinNailsHairSkin",
                value: "Behave"
              },
              {
                source: "NEVUS, EPIDERMAL",
                target: "Pigmented moles	:skinNailsHairSkin",
                value: "Behave"
              },
              {
                source: "NEVUS, EPIDERMAL",
                target:
                  "Woolly hair nevus (in some patients):skinNailsHairSkin",
                value: "Behave"
              },
              {
                source: "NEVUS, EPIDERMAL",
                target:
                  "Hyperpigmented patches of skin (in some patients):skinNailsHairSkin",
                value: "Behave"
              },
              {
                source: "NEVUS, EPIDERMAL",
                target:
                  "Raised, scaly, and/or hyperkeratotic areas of skin (in some patients):	skinNailsHairSkin",
                value: "Behave"
              },
              {
                source: "NEVUS, EPIDERMAL",
                target:
                  "Patches of tightly curled scalp hair adjacent to straight hair (in some patients):skinNailsHairHair",
                value: "Behave"
              }
            ],
            lineStyle: {
              normal: {
                opacity: 0.9,
                width: 5,
                curveness: 0
              }
            },
            categories: [
              { name: "disease" },
              { name: "gene" },
              { name: "symptom" }
            ]
          }
        ]
      },
      echartData: {
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
      },
      activeTab: "first",
      searchInput: "",
      type: "",
      checkAllPos: false,
      checkAllInheri: false,
      checkedPositions: [], //positionOptions,
      checkedInheris: [], //inheriOptions,
      positionOptions: [], //positionOptions,
      inheriOptions: [], //inheriOptions,
      isIndeterminatePos: true,
      isIndeterminateInheri: true
    };
  },

  methods: {
    doSearch() {
      this.$store.state.search_text = this.search_text;
      this.$store.state.search_type = this.search_type;
      this.loading = true;
      let demo = "SLC52A3";
      let params = [];
      params.push(this.search_text);
      let url = "/" + this.search_type + "/list";
      console.log(url);
      if (this.search_type == "") {
        url = "/gene/list";
      }
      this.axios
        .post(url, {
          params: params
        })
        .then(response => {
          this.listData = response.data.list;
          this.posData = response.data.positions;
          this.positionOptions = response.data.positions;
          this.inheriOptions = response.data.inheris;
          this.checkedPositions = response.data.positions;
          this.checkedInheris = response.data.inheris;

          this.loading = false;
          // this.initData = response.data.list;
          // this.selectedData = this.initData;
          // this.totalCount = this.selectedData.length;
          // this.currentPageData = this.selectedData.slice(0, this.pageSize);
          // this.loading = false;
        })
        .catch(error => {
          this.listData = [];
          this.checkedPositions = [];
          this.checkedInheris = [];
          this.positionOptions = [];
          this.inheriOptions = [];
          this.loading = false;

          // this.selectedData = this.initData;
          // this.totalCount = this.selectedData.length;
          // this.currentPageData = this.selectedData.slice(0, this.pageSize);
          // this.loading = false;
        });
        
   
    
      this.$route.params.search_text = this.search_text;
      this.$route.params.search_type = this.search_type;
    },
    search(){
         this.$router.push(
        {
          name: 'statistics',
          params: {
            search_type: this.search_type,
            search_text: this.search_text
          }
        }
      )
    },
    handleCheckAllPosChange(val) {
      this.checkedPositions = val ? this.positionOptions : [];
      this.$refs.item.$data.posOptions = this.checkedPositions;
      this.$refs.item.setCondition();
      this.isIndeterminatePos = false;
    },
    handleCheckAllInheriChange(val) {
      this.checkedInheris = val ? this.inheriOptions : [];
      this.$refs.item.$data.inheriOptions = this.checkedInheris;
      this.$refs.item.setCondition();
      this.isIndeterminateInheri = false;
    },
    handleCheckedPosChange(value) {
      let checkedCount = value.length;
      this.checkAllPos = checkedCount === this.positionOptions.length;
      this.isIndeterminatePos =
        checkedCount > 0 && checkedCount < this.positionOptions.length;
      this.$refs.item.$data.posOptions = this.checkedPositions;

      this.$refs.item.setCondition();
    },
    handleCheckedInheriChange(value) {
      let checkedCount = value.length;
      this.checkAllInheri = checkedCount === this.inheriOptions.length;
      this.isIndeterminateInheri =
        checkedCount > 0 && checkedCount < this.inheriOptions.length;
      this.$refs.item.$data.inheriOptions = this.checkedInheris;
      this.$refs.item.setCondition();
    }
  },

  created() {
    this.search_text = this.$route.params.search_text;
    this.search_type = this.$route.params.search_type;

    this.doSearch();
  }
};
</script>

<style scoped >
.input-with-select .el-input-group__prepend {
  background-color: #fff;
}
.el-checkbox {
  margin-left: 0px;
  margin-right: 30px;
}

.input-with-select button {
  outline: none;
  border: none;
  width: 60px;
  height: 40px;
  background: #2d8cf0;
  color: white;
  font-size: 16px;
}
</style>
