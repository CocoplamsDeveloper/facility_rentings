<template>
<MenuNavbar/>
<div class="container" id="addtenant-wrapper">
<div class="container" id="addtenantform">
<h2 :style="{textAlign : 'center'}">Add Tenant</h2>
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
  <!-- <div class="col-md-4">
    <label class="form-label">Tenant Rent</label>
    <input class="form-control" v-model="tenantRent">
  </div> -->
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
  <input class="form-control" type="file" ref="tenantfileupload" @change="handleTenantDoc">
  </div>

  <div class="col-12">
    <button type='button' class="btn btn-primary" v-on:click="addTenant">Submit</button>
  </div>
</form>
</div>

<div class="tenantPropertyAttachment">
  <div class="text-div">
  <h2>Create Tenancy Record</h2>
  <p>Click on below button to assign tenants with property/units</p>
  </div>
  <form class="row g-3">
  <div class="col-4">
    <label class="form-label">Tenant</label>
    <select class="form-select" v-model="selectedTenancyTenant">
      <option disabled value="">Choose</option>
    </select>
  </div>
  <div class="col-4">
    <label class="form-label">Property</label>
    <select class="form-select" v-model="selectedTenancyProperty">
      <option disabled value="">Choose</option>
      <!-- <option></option> -->
    </select>
  </div>
  <div class="col-4">
    <label class="form-label">Unit</label>
    <select class="form-select" v-model="selectedTenancyUnit">
      <option disabled value="">Choose</option>
    </select>
  </div>
  <div class="col-4">
    <label class="form-label">Rent</label>
    <input type="text" class="form-control" v-model="tenantRent">
  </div>
  <div class="col-4">
    <label class="form-label">Start date</label>
    <input type="date" class="form-control" v-model="contractStartDate">
  </div>
  <div class="col-4">
    <label class="form-label">End date</label>
    <input type="date" class="form-control" v-model="contractEndDate">
  </div>
  <div class="col-md-4">
  <label for="formFile" class="form-label">Contract document</label>
  <input class="form-control" type="file" ref="contractfileupload" @change="handleContractDoc">
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
            selectedTenancyProperty : null,
            selectedTenancyTenant : null,
            selectedTenancyUnit : null,
            contractStartDate : '',
            contractEndDate : '',
            contractFileDoc : null,
        }
    },
    methods:{

        handleTenantDoc(e){
            this.tenantDoc = e.target.files[0]
            let fileName = this.tenantDoc.name
            let fileExt =  fileName.split('.')[fileName.split('.').length-1].toLowerCase();
            let fileSize = this.tenantDoc.size/1000
            if((fileExt) !== 'pdf'){
              alert("please upload a pdf file, other type of file not accepted!")
              this.$refs.tenantfileupload.value = null;
              this.tenantDoc = null;
            }
            if(fileSize > 2048){
              alert("please upload a file of size upto 2 MB only")
              this.$refs.tenantfileupload.value = null;
              this.tenantDoc = null;
            }

        },

        addTenant(){

            let tenantsData = {
                "userId" : localStorage.getItem("userId"),
                "userFirstname" : this.tenantFirstName,
                "userLastname" : this.tenantLastName,
                "contactNumber" :  this.tenantContactNumber,
                "userNationality" : this.tenantNationality,
                "userStatus" : this.tenantStatus,
                "userEmail" :  this.tenantEmail,
                "previousAddress" :  this.tenantPreviousAddress,
            }


            const formData = new FormData();
            formData.append('tenantDocFile', this.tenantDoc)
            formData.append('data', JSON.stringify(tenantsData))

            axios({
                url : "http://localhost:8000/property/tenant/add",
                method: "POST",
                data : formData,
                headers : {'Content-type': 'multipart/form-data'}
            }).then((response) =>{
                console.log(response)
                alert(response.data.message)
            }).catch((error) =>{
              alert(error.response.data.message)
                console.log(error.response.data.message)
            })
        },
        handleContractDoc(e){
          this.contractFileDoc = e.target.files[0]
          let fileName = this.contractFileDoc.name
          let fileSize = this.contractFileDoc.size
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

#addtenantform{
  margin-top: 20px;
}

.tenantPropertyAttachment{
  margin-top: 20px;
}
.text-div{
  text-align: center;
}
</style>