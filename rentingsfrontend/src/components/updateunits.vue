<template>
<MenuNavbar/>
<div class="container" id="updateunits-wrapper">
<div class="container" id="updateUnitsform">
<h2>Update Units</h2>
<form class="row g-3">
  <div class="col-4">
    <label class="form-label">Unit Name/Number</label>
    <input type="text" class="form-control" v-model="unitNameUpdate">
  </div>
  <div class="col-4">
    <label class="form-label">Unit Type</label>
    <select id="inputState" class="form-select" v-model="unitTypeUpdate">
      <option disabled value="">Choose</option>
      <option value="room">room</option>
      <option value="shop">shop</option>
      <option value="store">store</option>
      <option value="office">office</option>
      <option value="other">other</option>
    </select>
  </div>
  <div class="col-4">
    <label class="form-label">Unit Rent</label>
    <input class="form-control" v-model="unitRentUpdate">
  </div>
  <div class="col-4">
    <label class="form-label">Unit Bedrooms</label>
    <input type="text" class="form-control" placeholder="" v-model="unitBedroomsUpdate">
  </div>
  <div class="col-md-4">
    <label class="form-label">Unit Bathrooms</label>
    <input class="form-control" v-model="unitBathroomsUpdate">
  </div>
  <div class="col-md-4">
    <label class="form-label">Unit Size</label>
    <input class="form-control" v-model="unitSizeUpdate">
  </div>
  <div class="col-md-4">
    <label for="inputState" class="form-label">Unit Status</label>
    <select id="inputState" class="form-select" v-model="unitStatusUpdate">
      <option disabled value="">Choose</option>
      <option value="occupied">occupied</option>
      <option value="unoccupied">unoccupied</option>
    </select>
  </div>
  <div class="col-md-4">
    <label for="inputState" class="form-label">Unit Property</label>
    <input class="form-control" v-model="unitPropertyUpdate" readonly>
  </div>
  <div class="col-12">
    <button type='button' class="btn btn-primary" v-on:click="updateUnits" :style="{marginLeft : '550px', marginTop:'20px'}">Update</button>
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
          unitNameUpdate : '',
          unitRentUpdate: '',
          unitSizeUpdate : '',
          unitBathroomsUpdate : '',
          unitBedroomsUpdate : '',
          unitTypeUpdate : '',
          unitStatusUpdate : '',
          unitPropertyUpdate : '',
          propertiesOptions : []
        }
    },
    methods : {

      populatePropertiesList(){
          let queryData =  {
            "userId" : localStorage.getItem('userId')
          }

          axios({
            url:'http://localhost:8000/property/landlord-prop/get',
            params: queryData,
            method:"GET",
          }).then((response) => {
            if (response.status === 200){
              console.log(response)
              this.propertiesOptions = response.data.propertiesData
            }
          }).catch((error) => {
            console.log(error)
            alert(error.response.data.message)
          })
      },

      getSingleUnit(){

        let unitId = this.$route.params.id
            console.log(unitId)
            let userData  = {
                'userId' : localStorage.getItem('userId')
            }

            axios({
                url : 'http://localhost:8000/property/units/'+unitId,
                method : 'GET',
                params : userData,
            }).then((response)=>{
                console.log(response)
                this.populateUnitsForm(response.data.unitData)
            }).catch((error) => {
                alert(error.response.data.message)
            })
      },

      populateUnitsForm(units){
        this.unitNameUpdate = units[0].unit_name,
        this.unitRentUpdate = units[0].unit_rent,
        this.unitSizeUpdate = units[0].area_insqmts,
        this.unitBathroomsUpdate = units[0].unit_bathrooms_nos,
        this.unitBedroomsUpdate = units[0].unit_bedrooms,
        this.unitTypeUpdate = units[0].unit_type,
        this.unitStatusUpdate = units[0].unit_status,
        this.propertiesOptions.forEach((prop) => {
          if(prop.propertyId === units[0].unit_property_id){
            this.unitPropertyUpdate = prop.propertyName
          }
        })
      },

      updateUnits(){

        let updatedData = {
          "unitId" : this.$route.params.id,
          "unitName/Number" : this.unitNameUpdate,
          "unitType" : this.unitTypeUpdate,
          "unitBedrooms" : this.unitBedroomsUpdate,
          "unitBathrooms" :  this.unitBathroomsUpdate,
          "unitSize"  : this.unitSizeUpdate,
          "unitStatus" : this.unitStatusUpdate,
          "unitRent" : this.unitRentUpdate,
        }

        let data = {
          "userId" : localStorage.getItem("userId"),
          "updatedData" : updatedData
        }

        axios({
          url : "http://localhost:8000/property/units/update",
          method : "POST",
          data : data,
        }).then((response)=>{
          alert(response.data.message)
          this.$router.push({name : "unitsPage"})
        }).catch((error) =>{
          alert(error.response.data.message)
        })
      }

    },
    mounted (){
      this.populatePropertiesList();
      this.getSingleUnit();
    }
}

</script>


<style scoped>

#updateproperty-wrapper{
    margin-top: 20px;
    margin-left: 160px;
}
</style>