<template>
  <el-card :body-style="{ padding: '0px' }">
    <img :src="imgPath" class="card-image">
    <div style="padding: 14px;">
      <span><slot name="title"></slot></span>
      <div class="bottom clearfix">
        <slot name="detail"></slot>
      </div>
    </div>
  </el-card>
</template>

<script>
export default {
  name: 'Card',
  props: {
    imgPath: {
      type: String,
      default: '../../../static/home-cover1.jpg'
    }
  }

}
</script>

<style>

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.card-image {
  width: 100%;
  display: block;
}

.clearfix:before,
.clearfix:after {
    display: table;
    content: "";
}

.clearfix:after {
    clear: both
}

</style>
