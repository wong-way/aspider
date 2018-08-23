<template>
  <div id="details">
    {{this.search_type}}
    <SearchResult></SearchResult>
  </div>
</template>

<script>
import SearchResult from "./search-result.vue";
export default {
  data() {
    return {
      search_text: "",
      search_type: ""
    };
  },
  components: {
    SearchResult
  },
  created() {
    this.search_text = this.$route.params.search_text;
    this.search_type = this.$route.params.search_type;
    
  }
};
</script>

<style>
</style>
