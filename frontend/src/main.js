import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Notifications from 'vue-notification'
import ApiService from './common/api.service'

Vue.config.productionTip = false
Vue.use(Notifications)
ApiService.init();

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
