import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import HelloWorld from '@/components/HelloWorld'
import Signup from '@/components/Signup'
import api from './common/api.service'
Vue.use(Router)

export const router = new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      component: Login
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/home',
      name: 'home',
      component: Home
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup
    },
    {
      path: '/hello',
      name: 'HelloWorld',
      component: HelloWorld
    },
    // { path: '*', component: 'NotFound' }
  ]
})


router.beforeEach((to, from, next) => {

  if(to.path.toLowerCase()==='/signup')
    return next();

  else if(to.path.toLocaleLowerCase()!=='/home'){
      next()
  }
   if(from.path.toLowerCase()!=='/' ){
       if(from.path.toLowerCase()!=='/login'){
           api.get('/auth/checkAuth').then(response=>{
            },error=>{
            if(error.response.status===401){
           next('/login')
       }
     });
      }
   }

  next();
});

export default router
