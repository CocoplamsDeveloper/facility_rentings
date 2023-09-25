<template>
<div class="flex-shrink-0 p-3" style="width: 150px;" id="sidebarmenu">
    <a href="/" class="d-flex align-items-center pb-3 mb-3 link-body-emphasis text-decoration-none border-bottom">
      <span class="fs-5 fw-semibold">Smart Facility management</span>
    </a>
    <ul class="list-unstyled ps-0">
      <li class="mb-1">
        <a class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed"  href="/home">
          Dashboard
        </a>
        <!-- <div class="collapse show" id="home-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 La">
            <li><a href="#" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Overview</a></li>
            <li><a href="#" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Updates</a></li>
            <li><a href="#" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Reports</a></li>
          </ul>
        </div> -->
      </li>
      <li class="mb-1">
        <a class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" href="/properties">
          Properties
        </a>
        <!-- <div class="collapse" id="dashboard-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="#" class="link-body-emphasis d-inline-flex text-decoration-none rounded">All Properties</a></li>
            <li><a href="#" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Add Properties</a></li>
            <li><a href="#" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Manage</a></li>
          </ul>
        </div> -->
      </li>
      <li class="mb-1">
        <a class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" href="/tenants">
          Tenants
        </a>
        <!-- <div class="collapse" id="orders-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="#" class="link-body-emphasis d-inline-flex text-decoration-none rounded">All Tenants</a></li>
            <li><a href="#" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Add Tenants</a></li>
            <li><a href="#" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Manage</a></li>
          </ul>
        </div> -->
      </li>
      <li class="border-top my-3"></li>
      <li class="mb-1">
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#account-collapse" aria-expanded="false">
          Account
        </button>
        <div class="collapse" id="account-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 large">
            <li><a href="#" class="link-body-emphasis d-inline-flex text-decoration-none rounded">New...</a></li>
            <li><a href="#" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Profile</a></li>
            <li><a href="#" class="link-body-emphasis d-inline-flex text-decoration-none rounded">Settings</a></li>
            <li><a href="#" type="button" class="link-body-emphasis d-inline-flex text-decoration-none rounded" v-on:click="landlordLogout()">Log out</a></li>
          </ul>
        </div>
      </li>
    </ul>
  </div>
</template>


<script>
import axios from 'axios'

export default {
    name :'MenuNavbar',
    data (){
      return {

      }
    },
    methods:{
      landlordLogout(){
        let data = {
          userId : localStorage.getItem("userId")
        }

        axios({
          url: "http://127.0.0.1:8000/property/ld-logout",
          method : "get",
          params : data
        }).then((response) => {
          if (response.status === 200){
            localStorage.removeItem("userId");
            this.$router.push('/login');
          }
      }).catch((error) => {
        console.log(error)
      })

      }

    }
}
</script>


<style scoped>
#sidebarmenu{
  position: fixed;
  float:left;
}

</style>
