<template>
    <div>

        <div class="row">
            <h4 class="col-md-10">Welcome</h4>
            <div class="">
                <label>File
                    <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
                </label>
                <button class="btn btn-success" v-on:click="submitFile()">Upload File</button>
            </div>
            <button  @click="logout()" class="col-md-1 btn btn-danger" >Logout</button>
        </div>


        <table class="table">
              <thead>
                <tr align="left">
                  <th>Name</th>
                  <th>email</th>
                  <th>Password</th>
                  <th>Mobile # </th>
                  <th>Address</th>

                </tr>
              </thead>
              <tbody>
                <tr align="left" v-bind="users" v-bind:key="emp.test" v-for="emp in users">
                  <td>{{emp.fullName}}</td>
                  <td>{{emp.email}}</td>
                  <td>{{emp.password}}</td>
                  <td>{{emp.mobileNo}}</td>
                  <td>{{emp.address}}</td>
                </tr>
              </tbody>
        </table>
    </div>
</template>

<script>
    import api from '../common/api.service'
    import axios from 'axios'
    export default {
        name: "Home",
        data:function () {
            return {
                users:[],
                files: []
            }
        },
        created:function(){

        },
        methods:{
            logout:function () {
             api.post('/auth/logout').then(res=>{
                 //let testing =res.data;

             });
             this.$router.push({name: 'login'});
          },
           submitFile()
           {
                let formData = new FormData();
                let fileData = {user_id : 4}                 
                formData.append('file', this.files[0]);
                formData.append('data',JSON.stringify(fileData))
                formData.data=fileData
                axios.post( 'http://127.0.0.1:5000/file/saveFile', formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    }).then(function(){
                    console.log('SUCCESS!!');
                })
                .catch(function(){
                    console.log('FAILURE!!');
                });
            },
      
      handleFileUpload(){
        let uploadedFiles = this.$refs.file.files;

            for( var i = 0; i < uploadedFiles.length; i++ ){
            this.files.push( uploadedFiles[i] );
            }
        }

        },
        mounted(){
            api.get('/user/').then(result=>{
                if(result && result.data){
                     this.users=result.data;
                }
            })
        },
       computed: {

        },
        components: {

       },
    }
</script>

<style scoped>

</style>
