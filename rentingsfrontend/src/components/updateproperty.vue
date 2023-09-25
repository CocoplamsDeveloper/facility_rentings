<template>
<MenuNavbar/>
<div class="container" id="updateproperty-wrapper">
<div class="container" id="updatePropertyform">
<h2>Update Property</h2>
<form class="row g-3">
  <div class="col-4">
    <label class="form-label">Property Name</label>
    <input type="text" class="form-control" v-model="propertyNameUpdate">
  </div>
  <div class="col-4">
    <label class="form-label">Governate</label>
    <input class="form-control" v-model="propertyGovernateUpdate">
  </div>
  <div class="col-4">
    <label class="form-label">City</label>
    <input class="form-control" v-model="propertyCityUpdate">
  </div>
  <div class="col-4">
    <label class="form-label">Street</label>
    <input class="form-control" v-model="propertyStreetUpdate">
  </div>
  <div class="col-4">
    <label class="form-label">Block</label>
    <input type="text" class="form-control" placeholder="" v-model="propertyBlockUpdate">
  </div>
  <div class="col-md-4">
    <label class="form-label">Property number</label>
    <input class="form-control" v-model="propertyNumberUpdate">
  </div>
  <div class="col-md-4">
    <label class="form-label">Property civil ID</label>
    <input class="form-control" v-model="propertyCivilUpdate">
  </div>
  <div class="col-4">
    <label class="form-label">Description</label>
    <input type="text" class="form-control" placeholder="" v-model="propertyDescriptionUpdate">
  </div>
  <div class="col-md-4">
    <label class="form-label">Property Size(sq.mtrs)</label>
    <input class="form-control" v-model="propertySizeUpdate">
  </div>
  <div class="col-md-4">
    <label for="inputCity" class="form-label">Year Built</label>
    <input type="text" class="form-control" v-model="propertyBuiltYearUpdate">
  </div>
  <div class="col-md-4">
    <label for="inputState" class="form-label">Property Type</label>
    <select id="inputState" class="form-select" v-model="propertyTypeUpdate">
      <option disabled value="">Choose</option>
      <option>Commercial</option>
      <option>Residential</option>
      <option>Both</option>
    </select>
  </div>
  <div class="col-md-4">
    <label for="inputState" class="form-label">Status</label>
    <select class="form-select" v-model="propertyStatusUpdate">
      <option disabled value="">Choose</option>
      <option>Active</option>
      <option>Inactive</option>
    </select>
  </div>
  <div class="col-md-4">
    <div class="card" :style="{width: '18rem', height: '18rem'}">
        <img :src="'http://localhost:8000/'+this.propertyCurrentImage" alt=".." :style="{width: '18rem', height: '18rem'}">
    </div>
  <label for="formFile" class="form-label">Property Image</label>
  <input class="form-control" type="file" @change="imageUpload">
  </div>
  <div class="col-4">
    <label class="form-label">Property Booking Value</label>
    <input type="text" class="form-control" v-model="propertyBuyValueUpdate">
  </div>
  <div class="col-4">
    <label class="form-label">Property Estimated Value</label>
    <input type="text" class="form-control" v-model="propertySaleValueUpdate">
  </div>
  <div class="col-12">
    <button type='button' class="btn btn-primary" v-on:click="">Update</button>
  </div>
</form>
</div>
</div>

</template>


<script>
import MenuNavbar from '/src/components/menunavbar.vue';
import axios from 'axios';

export default {
    name : 'updateProperty',
    components: {
        MenuNavbar
    },
    data (){
        return {
            propertyNameUpdate : '',
            propertyGovernateUpdate : '',
            propertyCityUpdate: '',
            propertyStreetUpdate : '',
            propertyBlockUpdate: '',
            propertyNumberUpdate : '',
            propertyCivilUpdate: '',
            propertyDescriptionUpdate : '',
            propertySizeUpdate : '',
            propertyBuiltYearUpdate : '',
            propertyTypeUpdate : '',
            propertyStatusUpdate : '',
            propertyBuyValueUpdate : '',
            propertySaleValueUpdate : '',
            propertyCurrentImage : '',
        }
    },
    methods : {

        populatePropertyForm(propertyData){
            console.log(propertyData)
            let data =  propertyData[0].fields
            this.propertyNameUpdate = data.property_name,
            this.propertyGovernateUpdate = data.governate,
            this.propertyCityUpdate = data.City,
            this.propertyStreetUpdate = data.Street,
            this.propertyBlockUpdate = data.Block,
            this.propertyNumberUpdate = data.property_number,
            this.propertyCivilUpdate = data.propert_civil_id,
            this.propertyDescriptionUpdate = data.property_description,
            this.propertySizeUpdate = data.area_insqmtrs,
            this.propertyBuiltYearUpdate = data.built_year,
            this.propertyTypeUpdate = data.property_type,
            this.propertyStatusUpdate = data.property_status,
            this.propertyBuyValueUpdate = data.buying_price,
            this.propertySaleValueUpdate = data.selling_price,
            this.propertyCurrentImage = data.property_image
        },
    
        getPerProperty(){
            let propId = this.$route.params.id
            console.log(propId)
            let userData  = {
                'userId' : localStorage.getItem('userId')
            }

            axios({
                url : 'http://localhost:8000/property/property/'+propId,
                method : 'GET',
                params : userData,
            }).then((response)=>{
                this.populatePropertyForm(response.data.property_data)
            }).catch((error) => {
                alert(error.response.data.message)
            })
        }
    },
    mounted(){
        this.getPerProperty();
    },

}

</script>

<style scoped>
#updateproperty-wrapper{
    margin-top: 20px;
    margin-left: 160px;
}
</style>