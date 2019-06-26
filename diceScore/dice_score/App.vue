<template>
  <div id="app">
      <slot>
      </slot>
  </div>
</template>

<script>
export default {
  name: "app",
  data() {
    return {};
  },
  components: {
    
  },
  methods: {}
};
</script>

<style>
body,
h1 {
  font-family: "Raleway", sans-serif;
}
body,
html {
  height: 100%;
}
</style>
