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
  <p>Add details and submit to assign tenants with property/units</p>
  </div>
  <form class="row g-3">
  <div class="col-4">
    <label class="form-label">Tenant</label>
    <select class="form-select" v-model="selectedTenancyTenant">
      <option disabled value="">Choose</option>
      <option v-for="tenant in tenantsOptions" :value="tenant.tenantId">{{ tenant.tenantName }}</option>
    </select>
  </div>
  <div class="col-4">
    <label class="form-label">Property</label>
    <select class="form-select" v-model="selectedTenancyProperty" @change="populateUnits">
      <option disabled value="">Choose</option>
      <option v-for="property in contractPropertiesOptions" :value="property.propertyId">{{ property.propertyName }}</option>
      <!-- <option></option> -->
    </select>
  </div>
  <div class="col-4">
    <label class="form-label">Unit</label>
    <select class="form-select" v-model="selectedTenancyUnit">
      <option v-for="unit in contractUnitsOptions" :value="unit.unitId">{{ unit.unitName }}</option>
      <option v-if="contractUnitsOptions.length === 0" disabled value="">No units for selected property</option>
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
  <div class="col-12">
    <button type='button' class="btn btn-primary" v-on:click="addTenancyRecord" :style="{marginLeft : '550px', marginTop:'10px'}">Create</button>
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
            tenantsOptions : [],
            contractPropertiesOptions : [],
            contractUnitsOptions : []
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
          let fileSize = this.contractFileDoc.size/1000

          let fileExt =  fileName.split('.')[fileName.split('.').length-1].toLowerCase();
            if((fileExt) !== 'pdf'){
              alert("please upload a pdf file, other type of file not accepted!")
              this.$refs.contractfileupload.value = null;
              this.contractFileDoc = null;
            }
            if(fileSize > 2048){
              alert("please upload a file of size upto 2 MB only")
              this.$refs.contractfileupload.value = null;
              this.contractFileDoc = null;
            }
        },

        populateTenantsProperties(){
          let queryData = {
            "userId" : localStorage.getItem('userId')
          }

          axios({
            url : "http://localhost:8000/property/tenancy/data",
            method : "GET",
            params : queryData
          }).then((response) => {
            if(response.status === 200){
              this.tenantsOptions = response.data.tenantsData;
              this.contractPropertiesOptions = response.data.propertiesData
            }
              console.log(response)
          }).catch((error) => {
            console.log(error)
          })
        },

        populateUnits(){
          
          if(this.selectedTenancyProperty === null || this.selectedTenancyProperty === ""){
            alert("Please select the property!")
            return
          }
          let queryData = {
            "userId" : localStorage.getItem('userId'),
            "propertyId" : this.selectedTenancyProperty
          }

          axios({
            url : "http://localhost:8000/property/tenancy/units",
            method : "GET",
            params : queryData
          }).then((response) => {
              if(response.status === 200){
                this.contractUnitsOptions = response.data.unitsData
              }
              console.log(response)
          }).catch((error) => {
            console.log(error)
          })
        },

      addTenancyRecord(){

        if(this.selectedTenancyTenant === null || this.selectedTenancyTenant === ''){
          alert("Please select the tenant!!");
          return;
        }
        if(this.selectedTenancyProperty === null || this.selectedTenancyProperty === ''){
          alert("Please select the Property!!");
          return
        }
        if(this.selectedTenancyUnit === null || this.selectedTenancyUnit === ''){
          alert("Please select the Unit!!");
          return
        }
        
        let tenancyStartDate = this.contractStartDate
        let tenancyEndDate = this.contractEndDate
        let currentDate = new Date()
        if(new Date(tenancyStartDate).getTime() <= currentDate.getTime()){
          alert("Please enter a valid Start Date");
          return
        }
        if(new Date(tenancyEndDate).getTime() <= currentDate.getTime()){
          alert("Please enter a valid End Date");
          return
        }

        console.log(this.contractStartDate, this.contractEndDate)

        let queryData = {
          "userId" : localStorage.getItem("userId"),
          "tenantId" : this.selectedTenancyTenant,
          "propertyId" : this.selectedTenancyProperty,
          "unitId" : this.selectedTenancyUnit,
          "rent" : this.tenantRent,
          "startDate" : this.contractStartDate,
          "endDate" : this.contractEndDate,
        }

        const formData = new FormData()
        formData.append('data', JSON.stringify(queryData))
        formData.append('contractDoc', this.contractFileDoc)

        axios({
          url : "http://localhost:8000/property/tenancy-record/create",
          method : 'POST',
          data : formData,
          headers : {'Content-type': 'multipart/form-data'}
        }).then((response) => {
          console.log(response)
        }).catch((error) => {
          alert(error.response.data.message)
        })



      }

    },
    mounted(){
      this.populateTenantsProperties();
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