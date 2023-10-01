<template>
<MenuNavbar/>
<div class="container" id="addtenant-wrapper">
<div class="container" id="addtenantform">
<h2>Add Tenant</h2>
<form class="row g-3">
  <div class="col-4">
    <label class="form-label">Tenant First Name</label>
    <input type="text" class="form-control" v-model="tenantFirstName">
  </div>
  <div class="col-4">
    <label class="form-label">Tenant Last Name</label>
    <input class="form-control" v-model="tenantLastName">
  </div>
  <div class="col-4">
    <label class="form-label">Contact Number</label>
    <input class="form-control" v-model="tenantContactNumber">
  </div>
  <div class="col-4">
    <label class="form-label">Tenant Email</label>
    <input class="form-control" v-model="tenantEmail">
  </div>
  <div class="col-4">
    <label class="form-label">Nationality</label>
    <input type="text" class="form-control" placeholder="" v-model="tenantNationality">
  </div>
  <div class="col-md-4">
    <label class="form-label">Tenant Rent</label>
    <input class="form-control" v-model="tenantRent">
  </div>
  <div class="col-4">
    <label class="form-label">Previous address</label>
    <input type="text" class="form-control" placeholder="" v-model="tenantPreviousAddress">
  </div>
  <!-- <div class="col-md-4">
    <label for="inputState" class="form-label">Property Type</label>
    <select id="inputState" class="form-select" v-model="propertyType">
      <option disabled value="">Choose</option>
      <option>Commercial</option>
      <option>Residential</option>
      <option>Both</option>
    </select>
  </div> -->
  <div class="col-md-4">
    <label for="inputState" class="form-label">Tenant Status</label>
    <select class="form-select" v-model="tenantStatus">
      <option disabled value="">Choose</option>
      <option value="active">Active</option>
      <option value="Inactive">Inactive</option>
    </select>
  </div>
  <div class="col-md-4">
  <label for="formFile" class="form-label">Tenant document</label>
  <input class="form-control" type="file" @change="handleTenantDoc">
  </div>

  <div class="col-12">
    <button type='button' class="btn btn-primary" v-on:click="addTenant">Submit</button>
  </div>
</form>
</div>
</div>
    

</template>


<script>
import MenuNavbar from '/src/components/menunavbar.vue';
import axios from 'axios'

export default {
    name : 'addTenant',
    components: {
        MenuNavbar
    },
    data (){
        return{
            tenantFirstName : '',
            tenantLastName : '',
            tenantContactNumber : '',
            tenantEmail : '',
            tenantNationality : '',
            tenantPreviousAddress : '',
            tenantRent : '',
            tenantStatus : '',
            tenantDoc : null,
        }
    },
    methods:{

        handleTenantDoc(e){
            this.tenantDoc = e.target.files[0]
        },

        addTenant(){

            let tenantsData = {
                "userFirstname" : this.tenantFirstName,
                "userLastname" : this.tenantLastName,
                "contactNumber" :  this.tenantContactNumber,
                "userNationality" : this.tenantNationality,
                "userStatus" : this.tenantStatus,
                "userEmail" :  this.tenantEmail,
                "tenantRent" : this.tenantRent,
                "previousAddress" :  this.tenantPreviousAddress,
            }
            let queryData = {
                "userId" : localStorage.getItem("userId"),
                "userRole" : 3,
                "userData" : tenantsData
            }

            const formData = new FormData();
            formData.append('tenantDocFile', this.tenantDoc)
            formData.append('data', JSON.stringify(queryData))

            axios({
                url : "http://localhost:8000/property/users/create",
                method: "POST",
                data : formData,
            }).then((response) =>{
                console.log(response)
            }).catch((error) =>{
                console.log(error.response.data.message)
            })
        }

    },
    mounted(){

    }
    
}

</script>

<style scoped>
#addtenant-wrapper{
    margin-top: 20px;
    margin-left: 160px;
}
</style>