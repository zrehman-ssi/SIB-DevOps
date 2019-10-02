<template>
    <div class="container">
     <div class="row">
      <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
        <div class="card card-signin my-5">
          <div class="card-body" id="loginInformation">
            <h5 class="card-title text-center">Sign up</h5>
            <div class="form-signin">
               <div class="form-label-group" >
                <input type="text" id="fullName" class="form-control" placeholder="Full Name"  v-model="fullName"  required autofocus>
                   <label for="inputEmail"></label>
              </div>

              <div class="form-label-group" >
                <input type="text" id="address" class="form-control" placeholder="Address"  v-model="address"  required autofocus>
                   <label for="inputEmail"></label>
              </div>

             <div class="form-label-group" >
                <input type="text" id="mobilNo" class="form-control" placeholder="Mobile #"  v-model="mobileNo"  required autofocus>
                   <label for="inputEmail"></label>
             </div>

              <div class="form-label-group" >
                <input type="text" id="inputEmail" class="form-control" placeholder="Username"  v-model="toUsername"  required autofocus>
                   <label for="inputEmail"></label>
              </div>

              <div class="form-label-group">
                <input type="password" id="inputPassword" class="form-control" placeholder="Password" v-model="toPassword"   required>
                   <label for="inputEmail"></label>
              </div>

              <button class="btn btn-lg btn-primary btn-block text-uppercase" type="submit" v-on:click="saveLoginInfo()">Register</button>
                <router-link to="/login">Already Registered ?</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
</div>
</template>

<script>
    import api from '@/common/api.service'
    export default {
        name: "signup",
        data:function () {
            return{
                toUsername:'',
                toPassword:'',
                mobileNo:'',
                address:'',
                fullName:''
            }
        },
         methods:{
                saveLoginInfo:function () {
                    let params=  {
                              url:'/register',
                              data: {username:this.toUsername,password: this.toPassword ,mobileNo: this.mobileNo,address:this.address,fullName: this.fullName},
                              contentType: 'application/json',
                            };

                    api.post(params.url,params.data).then(res=>{
                        let test=res.data;
                         if(test.isCreated==true){
                             this.$router.push({name: 'login'});
                              this.$notify({
                                        group: 'login',
                                        title: 'Successfully Signup',
                                        text: test.message,
                                        type:'success',
                                        dir:"auto"
                                      })
                         }
                         else{
                             this.$router.push({name: 'signup'});
                             this.$notify({
                                        group: 'login',
                                        title: 'Username already exists',
                                        text: test.message,
                                        type:'error',
                                        dir:"auto"
                                      })
                         }
                    });
                },
            },
    }
</script>

<style scoped>

</style>
