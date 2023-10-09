<template>
  <div class="container-sm" :style="{marginTop : '100px'}">
  <main class="form-signin w-50 m-auto">
  <form>
    <h1 class="h3 mb-3 fw-normal">Please sign in</h1>

    <div class="form-floating">
      <input type="email" class="form-control" placeholder="name@example.com" v-model="ldEmail">
      <label for="floatingInput">Email address</label>
    </div>
    <div class="form-floating">
      <input type="password" class="form-control" v-model="ldPassword" placeholder="Password">
      <label for="floatingPassword">Password</label>
    </div>

    <div class="form-check text-start my-3">
      <input class="form-check-input" type="checkbox" value="remember-me" id="flexCheckDefault">
      <label class="form-check-label" for="flexCheckDefault">
        Remember me
      </label>
    </div>
    <button class="btn btn-primary w-100 py-2" type="button" v-on:click="landlordLogin()">Sign in</button>
    <p class="mt-5 mb-3 text-body-secondary">&copy; 2017–2023</p>
  </form>
</main>
</div>
    
</template>


<script>
import axios from 'axios'

export default {
    name :'adminLogin',
    data() {
      return {
        ldEmail : '',
        ldPassword : ''
      }
    },
    methods:{
        landlordLogin(){
          let data = {
            userEmail : this.ldEmail,
            userPassword : this.ldPassword,
        }
        axios({
            url: "http://127.0.0.1:8000/property/user/login",
            method : "post",
            data: data
            }).then((response)=>{
            console.log(response)
            if(response.status === 200){
                alert(response.data.message)
                localStorage.setItem("userId", response.data.userId)
                this.$router.push({name:"Dashboard"})
            }
            
        }).catch((error) => {
            console.log(error)
        })
        }
    }
}
</script>


<style scoped>

</style>