<template>
  <html>

    <body>

  <div class="container">
    <div class="row">
      <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
        <div class="card card-signin my-5">
          <div class="card-body" id="loginInformation">
            <h5 class="card-title text-center">Sign In</h5>
            <div class="form-signin">
              <div class="form-label-group" >
                <input type="text" id="inputEmail" class="form-control" placeholder="Username"  v-model="user"  required autofocus>
                <label for="inputEmail">Username</label>
              </div>

              <div class="form-label-group">
                <input type="password" id="inputPassword" class="form-control" placeholder="Password" v-model="pass"   required>
                <label for="inputPassword">Password</label>
              </div>

              <div class="custom-control custom-checkbox mb-3">
                <input type="checkbox" class="custom-control-input" id="customCheck1">
                <label class="custom-control-label" for="customCheck1">Remember password</label>
              </div>
              <button class="btn btn-lg btn-primary btn-block text-uppercase" type="submit" v-on:click="saveLoginInfo()">Sign in</button>
              <router-link to="/signup">New user ? Create new account</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
    </body>
    </html>
</template>

<script>
import 'vue-notification'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import api from '../common/api.service'
    export default {
        name: "Login",
        data: function() {
           return {
                user: '',
                pass:''
           };
        },
        methods:{
                saveLoginInfo:function () {
                     let params=  {
                              data: {  
                                    username:this.user,
                                    email:this.user,
                                    password: this.pass
                                },
                              contentType: 'application/json',
                            };
                    api.post('/auth/login',params.data).then(result=>{                         
                           if(result.status===200){
                             this.$router.push({name: 'home'});
                             this.$notify({
                                        group: 'login',
                                        title: 'Successfully Logged in',
                                        text: 'Welcome to '+this.user+' !',
                                        type:'success',
                                        dir:"auto"
                                      })
                               //this.$store.dispatch('saveLogin',{username:this.user,password: this.pass,token:test.access_token}).then();

                         }
                         else{
                             this.$router.push({name: 'login'});
                             this.$notify({
                                        group: 'login',
                                        title: 'Invalid login',
                                        text: 'Username or password is invalid !',
                                        type:'error',
                                        dir:"auto"
                                      })
                         }
                    })
                },

            },

        mounted:function(){
          //jwt.destroyToken();
        },
        components:{

        }
    }
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
