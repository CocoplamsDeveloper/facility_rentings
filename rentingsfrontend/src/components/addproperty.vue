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
    
</template>


<script>
import MenuNavbar from '/src/components/menunavbar.vue';
import axios from 'axios'

export default {
    name : 'addProperties',
    components: {
      MenuNavbar
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
        columns: [
        "Unit Name/Number",
        "Unit Type",
        "Unit Rent",
        "Unit Bedrooms",
        "Unit Bathrooms",
        "Unit Size",
        "Status",
      ],
        tableData : [],
        propertiesOptions : [],
        selectedProperty: '',
        selectedUnitsCsvFile: null,
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
        unitsInputData : null
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
      }




    },
    mounted(){

      this.populatePropertiesList();
    }

}
</script>

<style scoped>
#addproperty-wrapper{
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
  margin-left: 150px;
}

.unitsheaders{
  text-align: center;
}
</style>
