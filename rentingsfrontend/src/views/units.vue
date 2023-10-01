<template>
<MenuNavbar/>
<div class="unitsPageContainer">
<div class="container" id="Unitsdata">
  <div class="unitsbutton">
  <div class="unitsheaders">
  <h2 >Add Units</h2>
  <h4 >Upload csv file with units details OR Enter data below</h4>
  </div>
    <label>Select Property</label>
      <select :style="{width: '300px'}" v-model="selectedProperty" >
        <option disabled value="">Select</option>
        <option v-for="option in propertiesOptions" :key="option.propertyId" :value="option.propertyId">{{ option.propertyName }}</option>
      </select>
  <p :style="{marginTop: '5px'}">
    -> Upload units data from a csv file
  </p>
  <button  type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#UploadUnitsCsvFileModal">Upload CSV</button>
  </div>

</div>

<button class="btn btn-secondary btn-sm" @click="addRow" :style="{marginLeft: '185px', marginTop:'20px'}">Add Row</button>
<div class="container-table">
    <table>
      <thead>
        <tr>
          <th v-for="(column, index) in columns" :key="index">{{ column }}</th>
          <th>action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rowIndex) in tableData" :key="rowIndex">
          <td v-for="(value, cellIndex) in row" :key="cellIndex" >
            <template v-if="cellIndex === 1">
              <select :id="'room' + rowIndex + '-' + cellIndex" v-model="row[cellIndex]">
                <option disabled value="">Choose</option>
                <option value="room">room</option>
                <option value="shop">shop</option>
                <option value="store">store</option>
                <option value="office">office</option>
                <option value="other">other</option>
              </select>
            </template>
            <template v-else-if="cellIndex === 3">
              <select :id="'bed' + rowIndex + '-' + cellIndex" v-model="row[cellIndex]">
                <option disabled value="">Choose</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="other">other</option>
              </select>
            </template>
            <template v-else-if="cellIndex === 4">
              <select :id="'bath' + rowIndex + '-' + cellIndex" v-model="row[cellIndex]">
                <option disabled value="">Choose</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="other">other</option>
              </select>
            </template>
            <template v-else>
              <input :id="'input' + rowIndex + '-' + cellIndex" type="text" v-model="row[cellIndex]"/>
            </template>
          </td>
          <td>
              <button @click="deleteRow(rowIndex)">Delete</button> <!-- Delete button for each row -->
          </td>
        </tr>
      </tbody>
    </table>
    <button class="btn btn-secondary" @click="sendUnitsData" :style="{marginLeft: '130px', marginTop:'20px', marginTop:'30px'}">Submit</button>

  </div>

<div class="modal fade" id="UploadUnitsCsvFileModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="exampleModalLabel">Upload Csv file</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <form>
          <div class="mb-3">
            <label for="recipient-name" class="col-form-label">Upload File</label>
            <input class="form-control" type="file" @change="handleCsvFileChange">
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" @click="handleCsvUpload">Upload</button>
      </div>
    </div>
  </div>
</div>

</div>

<div class="showUnitsTable">
  <h2 :style="{marginTop : '10px', marginBottom: '10px', textAlign:'center'}">Your Property Units</h2>
  <table>
    <thead>
      <tr>
        <td v-for="column in unitsTableColumns" >{{column}}</td>
      </tr>
      <tr>
      <td v-for="column in unitsTableColumns">

      <select v-if="column === 'Property'" v-model="propertyUnitsValue" @change="getFilteredUnits">
          <option disabled value="">Choose</option>
          <option v-for="option in propertiesOptions" :key="option.propertyId" :value="option.propertyId">{{ option.propertyName }}</option>
      </select>
      <select v-if="column === 'Unit Type'" v-model="unitsTypeValue" @change="getFilteredUnits">
        <option disabled value="">Choose</option>
        <option value="room">room</option>
        <option value="shop">shop</option>
        <option value="store">store</option>
        <option value="office">office</option>
        <option value="other">other</option>
      </select>
      <select v-if="column === 'Status'" v-model="unitsStatusValue" @change="getFilteredUnits">
          <option disabled value="">Choose</option>
          <option value="occupied">Occupied</option>
          <option value="unoccupied">Unoccupied</option>
      </select>
      <button class="btn btn-secondary" v-if="column === 'Action'" @click="clearUnitsTableFilters">Clear</button>
      </td>
      </tr>
    </thead>
    <tbody>
      <tr v-for="unit in allUnitsArray" :key="unit.unitId">
        <td>{{ unit.unitsData.unit_name }}</td>
        <td>{{ unit.unitsData.unit_type }}</td>
        <td>{{ unit.unitsData.unit_rent }}</td>
        <td>{{ unit.unitsData.unit_bedrooms }}</td>
        <td>{{ unit.unitsData.unit_bathrooms_nos }}</td>
        <td>{{ unit.unitsData.area_insqmts }}</td>
        <td>{{ unit.unitsData.unit_status }}</td>
        <td>{{ unit.propertyName }}</td>
        <td><router-link class="btn btn-info btn-sm" :to="'/update/unit/'+unit.unitId">Edit</router-link>
        <a class="btn btn-danger btn-sm" type="button" @click="deleteUnit(unit.unitId, unit.unitsData.unit_name)">Delete</a>
      </td>
      </tr>
    </tbody>

  </table>

</div>



</template>


<script>
import MenuNavbar from '/src/components/menunavbar.vue';
import axios from 'axios'

export default {
    name: 'unitsPage',
    components: {
        MenuNavbar,
    },
    data () {
        return {
        columns: [
        "Unit Name/Number",
        "Unit Type",
        "Unit Rent",
        "Unit Bedrooms",
        "Unit Bathrooms",
        "Unit Size",
        "Status",
      ],
      unitsTableColumns : [
      "Unit Name/Number",
        "Unit Type",
        "Unit Rent",
        "Unit Bedrooms",
        "Unit Bathrooms",
        "Unit Size",
        "Status",
        "Property",
        "Action"
      ],
        tableData : [],
        propertiesOptions : [],
        selectedProperty: '',
        selectedUnitsCsvFile: null,
        allUnitsArray : [],
        propertyUnitsValue : null,
        unitsStatusValue : null,
        unitsTypeValue : null,
        }

    },
    methods : {

        addRow() {
      const newRow = new Array(this.columns.length).fill(''); // Create a new row with empty values
      this.tableData.push(newRow); // Add the new row to the tableData array
    },
    deleteRow(rowIndex) {
      this.tableData.splice(rowIndex, 1); // Remove the row at the specified index
    },


    async getUnitsInputData() {
      const inputData = this.tableData.map((row) => {
        const rowData = {};
        this.columns.forEach((column, columnIndex) => {
          rowData[column] = row[columnIndex];
        });
        return rowData;
      }); // Create a deep copy of the tableData
      this.unitsInputData = inputData; // Store the input data in a component data property
      console.log(this.inputData)
    },
    data (){
      return {
        unitsInputData : null,
      }
    },

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

      async sendUnitsData(){

        if(this.selectedProperty === null || this.selectedProperty === ""){
          alert("Invalid request, Please select the property first!")
          return 
        }
        await this.getUnitsInputData();
        let data = {
          "userId" : localStorage.getItem('userId'),
          "propertyId" : this.selectedProperty,
          "unitsData" : this.unitsInputData
        }

        axios({
          url:'http://localhost:8000/property/units/add',
          method: 'POST',
          data : data
        }).then((response) => {
          alert(response.data.message)
          this.tableData = [];
          this.selectedProperty = ''
        }).catch((error) => {
          alert(error.response.data.message)

        })
      },


      handleCsvFileChange(e) {
        this.selectedUnitsCsvFile = e.target.files[0];
      },

      handleCsvUpload() {
              // Handle the file upload here (e.g., send it to the server)

        if(this.selectedProperty === null || this.selectedProperty === ""){
          alert("Invalid request, Please select the property first!")
          return 
        }

        let userData = {
          "userId" : localStorage.getItem('userId'),
          "propertyId" : this.selectedProperty,
        }

        const formData = new FormData();
        formData.append("unitscsvfile", this.selectedUnitsCsvFile)
        formData.append("data", JSON.stringify(userData))
        
        axios({
          url: "http://localhost:8000/property/units/csv-add",
          method :"POST",
          data : formData,
          headers:{'Content-Type': 'multipart/form-data'},
        }).then((response) =>  {
          alert(response.data.message)
          location.assign("http://localhost:5173/addproperty")
        }).catch((error) => {
          alert(error.response.data.message)
          location.assign("http://localhost:5173/addproperty")
        })

      // Close the modal
      },

      getPropertyUnits(){

        let queryData = {
          "userId" : localStorage.getItem("userId")
        }

        axios({
          url: "http://localhost:8000/property/allunits/get",
          method : 'GET',
          params : queryData
        }).then((response)=>{
          console.log(response)
          if(response.data.unitsData.length > 0){
          this.allUnitsArray = response.data.unitsData
          }
          else{
            alert(response.data.message)
          }
        }).catch((error) =>{
          console.log(error)
        })
      },


      getFilteredUnits(){
        let queryData = {
          "userId" :  localStorage.getItem('userId')
        }

        if(this.propertyUnitsValue !== null){
          queryData["unitPropertyFilter"] = this.propertyUnitsValue
        }
        if(this.unitsStatusValue !== null){
          queryData["unitStatusFilter"] = this.unitsStatusValue
        }
        if(this.unitsTypeValue !== null){
          queryData["unitTypeFilter"] = this.unitsTypeValue
        }

        axios({
          url : "http://localhost:8000/property/units/filter",
          method : 'POST',
          data : queryData,
        }).then((response) => {
          if(response.status == 200) {
            this.allUnitsArray =  response.data.filteredData
          }
        }).catch((error) => {
          console.log(error)
        })

      },
      clearUnitsTableFilters(){

        this.getPropertyUnits();
        this.propertyUnitsValue = null,
        this.unitsStatusValue = null,
        this.unitsTypeValue = null

      },
      deleteUnit(unitId, unitName){

        let alert_resp = confirm("Are you sure you want to delete unit "+unitName)
        let queryData = {
          "userId" : localStorage.getItem("userId"),
          "unitId" : unitId,
        }
        if(alert_resp){
          
          axios({
            url : "http://localhost:8000/property/unit/delete",
            method : 'DELETE',
            data : queryData,
          }).then((response) => {
            console.log(response)
            alert(response.data.message)
          }).catch((error) => {
            alert(error.response.data.message)
          })

        }
        else{
          return
        }


      },

},
    mounted(){
        this.populatePropertiesList();
        this.getPropertyUnits();
    },
}

</script>


<style scoped>
.unitsPageContainer{
    margin-top: 20px;
    margin-left: 160px;
}

#Unitsdata{
  margin-top:20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  table-layout: auto;
}

th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
  width:12.5%;
}

tr {
  height : 40px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 4px;
}

select {
  width: 100%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.container-table{
  max-width: 100%; /* Set a maximum width for the container */
  overflow-x: auto;
  margin-left: 100px;
}

.unitsheaders{
  text-align: center;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.data-table th, .data-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.showUnitsTable{
  max-width: 100%; /* Set a maximum width for the container */
  overflow-x: auto;
  margin-left: 190px;
  margin-top: 15px;
}
</style>