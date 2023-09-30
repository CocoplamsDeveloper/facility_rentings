<template>
<MenuNavbar/>
<div class="container" id="updateunits-wrapper">
<div class="container" id="updateUnitsform">
<h2>Update Units</h2>
<form class="row g-3">
  <div class="col-4">
    <label class="form-label">Unit Name/Number</label>
    <input type="text" class="form-control" v-model="propertyNameUpdate">
  </div>
  <div class="col-4">
    <label class="form-label">Unit Type</label>
    <input class="form-control" v-model="propertyGovernateUpdate">
  </div>
  <div class="col-4">
    <label class="form-label">City</label>
    <input class="form-control" v-model="propertyCityUpdate">
  </div>
  <div class="col-4">
    <label class="form-label">Unit Rent</label>
    <input class="form-control" v-model="propertyStreetUpdate">
  </div>
  <div class="col-4">
    <label class="form-label">Unit Bedrooms</label>
    <input type="text" class="form-control" placeholder="" v-model="propertyBlockUpdate">
  </div>
  <div class="col-md-4">
    <label class="form-label">Unit Bathrooms</label>
    <input class="form-control" v-model="propertyNumberUpdate">
  </div>
  <div class="col-md-4">
    <label class="form-label">Unit Size</label>
    <input class="form-control" v-model="propertyCivilUpdate">
  </div>
  <div class="col-md-4">
    <label for="inputState" class="form-label">Unit Status</label>
    <select id="inputState" class="form-select" v-model="propertyTypeUpdate">
      <option disabled value="">Choose</option>
      <option>Commercial</option>
      <option>Residential</option>
      <option>Both</option>
    </select>
  </div>
  <div class="col-md-4">
    <label for="inputState" class="form-label">Unit Property</label>
    <select class="form-select" v-model="propertyStatusUpdate">
      <option disabled value="">Choose</option>
      <option>Active</option>
      <option>Inactive</option>
    </select>
  </div>
  <div class="col-12">
    <button type='button' class="btn btn-primary" v-on:click="updatePropertyFunc" :style="{marginLeft : '550px', marginTop:'20px'}">Update</button>
  </div>
</form>
</div>
</div>


</template>

<script>
import MenuNavbar from '/src/components/menunavbar.vue';
import axios from 'axios'

export default {
    name : 'updateUnits',
    components : {
        MenuNavbar,
    },
    data (){
        return {

        }
    },
    methods : {

    }
}

</script>


<style scoped>
</style>