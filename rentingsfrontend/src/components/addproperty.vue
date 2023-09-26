<template>
<MenuNavbar/>
<div class="container" id="addproperty-wrapper">
<div class="container" id="addPropertyform">
<h2>Add Property</h2>
<form class="row g-3">
  <div class="col-4">
    <label class="form-label">Property Name</label>
    <input type="text" class="form-control" v-model="propertyName">
  </div>
  <div class="col-4">
    <label class="form-label">Governate</label>
    <input class="form-control" v-model="propertyGovernate">
  </div>
  <div class="col-4">
    <label class="form-label">City</label>
    <input class="form-control" v-model="propertyCity">
  </div>
  <div class="col-4">
    <label class="form-label">Street</label>
    <input class="form-control" v-model="propertyStreet">
  </div>
  <div class="col-4">
    <label class="form-label">Block</label>
    <input type="text" class="form-control" placeholder="" v-model="propertyBlock">
  </div>
  <div class="col-md-4">
    <label class="form-label">Property number</label>
    <input class="form-control" v-model="propertyNumber">
  </div>
  <div class="col-md-4">
    <label class="form-label">Property civil ID</label>
    <input class="form-control" v-model="propertyCivil">
  </div>
  <div class="col-4">
    <label class="form-label">Description</label>
    <input type="text" class="form-control" placeholder="" v-model="propertyDescription">
  </div>
  <div class="col-md-4">
    <label class="form-label">Property Size(sq.mtrs)</label>
    <input class="form-control" v-model="propertySize">
  </div>
  <div class="col-md-4">
    <label for="inputCity" class="form-label">Year Built</label>
    <input type="text" class="form-control" v-model="propertyBuiltYear">
  </div>
  <div class="col-md-4">
    <label for="inputState" class="form-label">Property Type</label>
    <select id="inputState" class="form-select" v-model="propertyType">
      <option disabled value="">Choose</option>
      <option>Commercial</option>
      <option>Residential</option>
      <option>Both</option>
    </select>
  </div>
  <div class="col-md-4">
    <label for="inputState" class="form-label">Status</label>
    <select class="form-select" v-model="propertyStatus">
      <option disabled value="">Choose</option>
      <option>Active</option>
      <option>Inactive</option>
    </select>
  </div>
  <div class="col-md-4">
  <label for="formFile" class="form-label">Property Image</label>
  <input class="form-control" type="file" @change="imageUpload">
  </div>
  <div class="col-4">
    <label class="form-label">Property Booking Value</label>
    <input type="text" class="form-control" v-model="propertyBuyValue">
  </div>
  <div class="col-4">
    <label class="form-label">Property Estimated Value</label>
    <input type="text" class="form-control" v-model="propertySaleValue">
  </div>
  <div class="col-12">
    <button type='button' class="btn btn-primary" v-on:click="addPropertyFunc()">Submit</button>
  </div>
</form>
</div>
</div>
    
</template>


<script>
import MenuNavbar from '/src/components/menunavbar.vue';
import axios from 'axios'

export default {
    name : 'addProperties',
    components: {
      MenuNavbar,
    },
    data (){
      return {
        propertyName:'',
        propertyGovernate:'',
        propertyCity:'',
        propertyStreet:'',
        propertyBlock:'',
        propertyNumber:'',
        propertyCivil:'',
        propertyDescription:'',
        propertyBuiltYear:'',
        propertySaleValue:'',
        propertyType: '',
        propertyStatus: '',
        propertyBuyValue: '',
        propertySaleValue : '',
        imageFile: null,
        propertySize : '',

      }
    },
    methods:{

      imageUpload(e){
          this.imageFile = e.target.files[0]
      },

      addPropertyFunc(){
        let propertywisedata = {
          "userId" : localStorage.getItem("userId"),
          "propertyName":this.propertyName,
          "governateName" : this.propertyGovernate,
          "propertyCity" : this.propertyCity,
          "propertyStreet" : this.propertyStreet,
          "propertyBlock" : this.propertyBlock,
          "propertyNumber" : this.propertyNumber,
          "propertyCivil" : this.propertyCivil,
          "propertyDescription" : this.propertyDescription,
          "propertyBuiltYear" : this.propertyBuiltYear,
          "propertySaleValue" : this.propertySaleValue,
          "propertyType" : this.propertyType,
          "propertyStatus" : this.propertyStatus,
          "propertyBuyValue" : this.propertyBuyValue,
          "propertySize" :  this.propertySize
        }
        console.log(propertywisedata)
        const formData = new FormData();
        formData.append("image", this.imageFile);
        formData.append('data', JSON.stringify(propertywisedata))

        axios.post('http://127.0.0.1:8000/property/add',formData,{
          headers: {'Content-type': 'multipart/form-data'}

        }).then((response) => {
          alert(response.data.message)
        }).catch((error) => {
          alert(error.response.data.message)

        })

      },

 




    },
    mounted(){

    }

}
</script>

<style scoped>
#addproperty-wrapper{
    margin-top: 20px;
    margin-left: 160px;
}

</style>
