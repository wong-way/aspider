<template>
  <el-row :gutter="20" justify="center" type="flex" align="middle" class="intro">
    <el-col :span=10 class="intro-text">
      <el-row type="flex" justify="center">
        <slot name="title"></slot>
      </el-row>

      <el-row type="flex" justify="center">
        <slot name="detail"></slot>
      </el-row>
    </el-col>

    <el-col :span=14>
      <slot name="image" ></slot>
    </el-col>
  </el-row>

</template>

<script>
export default {
  name: 'IntroLeft'
}
</script>

<style>

.intro {
  margin-top: 5%;
}
.intro-text {
  margin-left: 5%;
  margin-right: 5%;
}

</style>
