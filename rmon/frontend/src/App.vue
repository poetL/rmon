<template>
  <div id="app">
    <div class="col-sm-3 col-md-2 sidebar">
      <ul class="nav nav-sidebar">
        <li v-for="(host, index) in hosts" v-if="index < 6" v-bind:class="{active: isActive(host.name)}">
          <a href="#">
            {{ host.name }} 
            <div class="pull-right handle-group">
            <i class="fa fa-times"></i>
            <i class="fa fa-pencil-square-o"></i>
            </div>
          </a>
        </li>
      </ul>
    </div>

    <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
      <div class="row">
        <img src="data:image/gif;base64,R0lGODlhAQABAIAAAHd3dwAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==" width="200" height="200" class="img-responsive" alt="Generic placeholder thumbnail">
        <h4>Label</h4>
        <span class="text-muted">Something else</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      currentHost: '测试服务器',
      hosts: [
        {name: '测试服务器'},
        {name: '生产服务器'}
      ],
      msg: 'Welcome to Your Vue.js App'
    }
  },

  methods: {
    isActive:  function (hostName) {
      console.log(hostName)
      return this.currentHost == hostName
    }
  }
}
</script>

<style>

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 60px;
}

.sidebar a {
  color: #34495e;
}

.sidebar .active a {
  color: #42b983;
}

.handle-group {
  line-height: inherit;
}


@media (min-width: 768px) {
  .sidebar{
    position: fixed;
  }
}

</style>
