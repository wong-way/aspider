<template>
  <div id="home">

    <!-- Logo 及 搜索框 -->
    <div id="aspider">
      <center>
        <svg width="294px" height="57px" viewBox="0 0 294 57" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
          <!-- Generator: Sketch 48.2 (47327) - http://www.bohemiancoding.com/sketch -->
          <title>ASpider</title>
          <desc>Created with Sketch.</desc>
          <defs></defs>
          <g id="Artboard" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" transform="translate(-113.000000, -212.000000)" font-family="Phosphate-Solid, Phosphate" font-size="80" font-weight="normal">
            <text id="ASpider" fill="#2D8CF0">
              <tspan x="115.64" y="267">ASpider</tspan>
            </text>
          </g>
        </svg>
        <search-bar :display=true :animate=false></search-bar>
      </center>
    </div>

    <!-- 视差图像 -->
    <parallax speedFactor=0.5 sectionClass="section">
      <img src="/static/discuss.jpg">
    </parallax>

    <h1> This is a database about disease | gene | symptom</h1>
    <p> There is test text. There are test text. There are test text. There are test text. There is test text.</p>
    <br>
    <!-- 3D 卡片效果 -->
    <carousel class="carousel">
      <slide :index="0" class="slide">
        <card imgPath="/static/home-cover.jpg">
          <h1 slot="title"> Gene </h1>
          <p slot="detail"> There is test text. There are test text. There are test text. There are test text. </p>
        </card>
      </slide>
      <slide :index="1" class="slide">
        <card imgPath="/static/home-cover.jpg">
          <h1 slot="title"> Disease </h1>
          <p slot="detail"> There is test text. There are test text. There are test text. There are test text. </p>
        </card>
      </slide>

      <slide :index="2" class="slide">
        <card imgPath="/static/home-cover.jpg">
          <h1 slot="title"> Symptom </h1>
          <p slot="detail"> There is test text. There are test text. There are test text. There are test text. </p>
        </card>
      </slide>

      <slide :index="3" class="slide">
        <card imgPath="/static/home-cover.jpg">
          <h1 slot="title"> Type </h1>
          <p slot="detail"> There is test text. There are test text. There are test text. There are test text. </p>
        </card>
      </slide>

      <slide :index="4" class="slide">
        <card imgPath="/static/home-cover.jpg">
          <h1 slot="title"> Inheritence </h1>
          <p slot="detail"> There is test text. There are test text. There are test text. There are test text. </p>
        </card>
      </slide>

    </carousel>

    <br>
    <h1>Something Important</h1>
    <p> There is test text. There are test text. There are test text. There are test text. There is test text.</p>
    <br>
    <div id="intro">

      <intro-left>
        <h1 slot="title" class="title">Neo4j</h1>
        <p slot=detail class="detail">There is test text. There are test text. There are test text. There are test text. There are test text.</p>
        <img src="/static/home-cover1.jpg" slot="image" class="image">
      </intro-left>

      <intro-right>
        <h1 slot="title" class="title">Neo4j</h1>
        <p slot=detail class="detail">There is test text. There are test text. There are test text. There are test text. There are test text.</p>
        <img src="/static/home-cover3.jpg" slot="image" class="image">
      </intro-right>

      <intro-left>
        <h1 slot="title" class="title">Neo4j</h1>
        <p slot=detail class="detail">There is test text. There are test text. There are test text. There are test text. There are test text.</p>
        <img src="/static/home-cover2.jpg" slot="image" class="image">
      </intro-left>

      <intro-right>
        <h1 slot="title" class="title">Neo4j</h1>
        <p slot=detail class="detail">There is test text. There are test text. There are test text. There are test text. There are test text.</p>
        <img src="/static/home-cover4.jpg" slot="image" class="image">
      </intro-right>
    </div>

  </div>
</template>

<script>
import Card from "./tools/card.vue";
import Parallax from "vue-parallaxy";
import SearchBar from "./tools/search-bar.vue";
import IntroLeft from "./tools/intro-left.vue";
import IntroRight from "./tools/intro-right.vue";
import { Carousel3d, Slide } from "vue-carousel-3d";

export default {
  components: {
    card: Card,
    slide: Slide,
    parallax: Parallax,
    carousel: Carousel3d,
    "search-bar": SearchBar,
    "intro-left": IntroLeft,
    "intro-right": IntroRight
  },

  data() {
    return {};
  },
  methods: {}
};
</script>

<style>
#home {
  margin-top: 20px;
}

#aspider {
  margin-top: 10%;
}

svg {
  margin-bottom: 20px;
}

.title {
  font-size: 30px;
  font-weight: 400;
}

.detail {
  font-size: 16px;
  text-align: left;
  font-weight: 300;
}

.image {
  max-height: 400px;
  border-radius: 4px;
  box-shadow: 5px 5px 5px #ccc;
}

.parallax-image {
  margin-top: 50px;
  max-height: 500px;
}

.slide {
  overflow: visible !important;
  border: none;
  background: transparent !important;
}

.carousel {
  overflow: visible !important;
  padding-bottom: 30%;
}

.section {
  margin-top: 50px;
  position: relative;
  scroll-behavior: smooth;
  margin-bottom: 100px;
  max-height: 500px;
}
</style>
