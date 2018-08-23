<template>
  <div>
    <el-row>
      <el-col style="height:1400px">
        <el-scrollbar style="height:100%">
          <el-card v-for="item in currentPageData" style="margin-bottom:15px ;" shadow="always">
            <div slot="header">
              <span>#{{item.mimnumber }}</span>
            </div>
            <div style="margin-bottom:10px">
              <i class="el-icon-edit"></i>
              <strong>Disease: {{item.preferredTitle }}{{item.shorteningTitle=='null'?'':'('+item.shorteningTitle+')'}}</strong>
              <br>
              <i class="el-icon-edit-outline"></i>
              <strong class="result-title">inheritance:</strong> {{item.inheritance }}
              <br>
              <i class="el-icon-view"></i>
              <strong class="result-title">symptom count:</strong> {{item.symptomCount}}
              <br>
              <i class="el-icon-tickets"></i>
              <strong class="result-title">main site of disease:</strong>
              <el-tag size="small" color="white" :hit="true" v-for="(p,index) in item.position">{{p}}</el-tag>
            </div>
            <el-button type="primary" size="small" icon="el-icon-edit" @click="showDetail(item.mimnumber)">View</el-button>
            <el-button type="primary" size="small" icon="el-icon-share">Relation</el-button>
          </el-card>
        </el-scrollbar>
      </el-col>
    </el-row>
    <el-row style="margin-top:20px">
      <el-pagination @current-change="handleCurrentChange" :current-page.sync="currentPage" :page-size="pageSize" small layout="total,prev, pager, next, jumper" :total="totalCount">
      </el-pagination>
    </el-row>

  </div>
</template>

<script>
export default {
  name: "ResultItem",
  data() {
    return {
      currentPage: 1,
      pageSize: 5,
      totalCount: "",
      selectedData: [],
      currentPageData: [],
      initData: [],
      demoData: [
        {
          mimnumber: "210900",
          preferredTitle: "BLOOM SYNDROME",
          shorteningTitle: "BLM",
          inheritance: "Autosomal recessive",
          symptomCount: "42",
          position: ["growthHeight", "growthOther", "headAndNeckHead"]
        },
        {
          mimnumber: "210900",
          preferredTitle: "BLOOM SYNDROME",
          shorteningTitle: "BLM",
          inheritance: "Autosomal dominant",
          symptomCount: "42",
          position: ["growthHeight", "growthOther", "headAndNeckHead"]
        },
        {
          mimnumber: "211400",
          preferredTitle:
            "BRONCHIECTASIS WITH OR WITHOUT ELEVATED SWEAT CHLORIDE 1",
          shorteningTitle: "BESC1",
          inheritance: "Autosomal recessive",
          symptomCount: "5",
          position: [
            "respiratoryLung",
            "laboratoryAbnormalities",
            "headAndNeckFace"
          ]
        },
        {
          mimnumber: "211400",
          preferredTitle:
            "BRONCHIECTASIS WITH OR WITHOUT ELEVATED SWEAT CHLORIDE 1",
          shorteningTitle: "BESC1",
          inheritance: "Autosomal dominant",
          symptomCount: "5",
          position: [
            "respiratoryLung",
            "laboratoryAbnormalities",
            "headAndNeckFace"
          ]
        },
        {
          mimnumber: "211400",
          preferredTitle:
            "BRONCHIECTASIS WITH OR WITHOUT ELEVATED SWEAT CHLORIDE 1",
          shorteningTitle: "BESC1",
          inheritance: "Autosomal dominant",
          symptomCount: "5",
          position: [
            "respiratoryLung",
            "laboratoryAbnormalities",
            "headAndNeckFace"
          ]
        },
        {
          mimnumber: "210900",
          preferredTitle: "BLOOM SYNDROME",
          shorteningTitle: "BLM",
          inheritance: "Autosomal recessive",
          symptomCount: "42",
          position: ["growthHeight", "growthOther", "headAndNeckHead"]
        },
        {
          mimnumber: "210900",
          preferredTitle: "BLOOM SYNDROME",
          shorteningTitle: "BLM",
          inheritance: "Autosomal dominant",
          symptomCount: "42",
          position: ["growthHeight", "growthOther", "headAndNeckHead"]
        },
        {
          mimnumber: "211400",
          preferredTitle:
            "BRONCHIECTASIS WITH OR WITHOUT ELEVATED SWEAT CHLORIDE 1",
          shorteningTitle: "BESC1",
          inheritance: "Autosomal recessive",
          symptomCount: "5",
          position: [
            "respiratoryLung",
            "laboratoryAbnormalities",
            "headAndNeckFace"
          ]
        },
        {
          mimnumber: "211400",
          preferredTitle:
            "BRONCHIECTASIS WITH OR WITHOUT ELEVATED SWEAT CHLORIDE 1",
          shorteningTitle: "BESC1",
          inheritance: "Autosomal dominant",
          symptomCount: "5",
          position: [
            "respiratoryLung",
            "laboratoryAbnormalities",
            "headAndNeckFace"
          ]
        },
        {
          mimnumber: "211433",
          preferredTitle:
            "BRONCHIECTASIS WITH OR WITHOUT ELEVATED SWEAT CHLORIDE 1",
          shorteningTitle: "BESC1",
          inheritance: "Autosomal dominant",
          symptomCount: "5",
          position: [
            "respiratoryLung",
            "laboratoryAbnormalities",
            "headAndNeckFace"
          ]
        }
      ],

      inheriOptions: ["Autosomal recessive", "Autosomal dominant"],
      posOptions: [
        "growthHeight",
        "growthOther",
        "headAndNeckHead",
        "respiratoryLung",
        "laboratoryAbnormalities",
        "headAndNeckFace"
      ]
    };
  },
  created: function() {},
  watch: {
    listdata: function() {
      this.initData = this.listdata;
      this.posOptions = this.posdata;
      this.selectedData = this.initData;
      this.totalCount = this.selectedData.length;
      this.currentPageData = this.selectedData.slice(0, this.pageSize);
    }
  },
  props: ["listdata","posdata"],
  methods: {
    showDetail: function(mim) {
      this.$router.push({
        name: "resultDetail",
        params: {
          mimnumber: mim
        }
      });
    },
    setCondition: function(event) {
      this.selectedData = [];
      let temp = [];
      this.initData.forEach(element => {
        if (this.inheriOptions.indexOf(element.inheritance) >= 0)
          temp.push(element);
      });
      console.log(temp.length);
      temp.forEach(element => {
        let intersection = element.position.filter(v => this.posOptions.includes(v))
        if (intersection.length>0) {
          this.selectedData.push(element);
        }else{
          console.log(element)
        }
      });

      console.log(this.selectedData.length);
      this.currentPageData = this.selectedData.slice(0, 5);
      this.totalCount = this.selectedData.length;
    },
 
    
    handleCurrentChange(val) {
      this.currentPageData = this.selectedData.slice(
        (this.currentPage - 1) * this.pageSize,
        this.currentPage * this.pageSize
      );
    }
  },
  components: {}
};
</script>
<style>
.el-scrollbar__wrap {
  overflow-x: hidden;
}

.result-number {
  height: 150px;
  line-height: 100px;
  text-align: center;
  margin: auto;
}
.result-detail h6 {
  color: #555;
}
.result-title {
  color: #555;
}
</style>
