<template>
    <MenuNavbar/>
    <div class="container" id="propertypagecontainer">
        <h1 id="proppageheading">Properties</h1>
        <br/>
        <div class="addPropertydiv">
        <a type="button" class="btn btn-primary" :style="{Position:'fixed'}" href="/addproperty" >Add Property</a>
        </div>
        <div class="property-table">
            <h3 :style="{textAlign : 'center', marginBottom:'10px'}">Your Properties</h3>
            <table class="table table-striped-columns">
            <thead>
                <tr>
                <th scope="col">#No</th>
                <th scope="col">Property Name</th>
                <th scope="col">Property Type</th>
                <th scope="col">Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(prop, index) in userProperties" :key="index">
                <th scope="row">{{ prop.propertyId }}</th>
                <td>{{ prop.propertyName }}</td>
                <td>{{ prop.propertyType }}</td>
                <td><router-link class="btn btn-info" :to="'/update/property/'+prop.propertyId" >Update</router-link>
                    <button class="btn btn-danger" v-on:click="deleteProperty(prop.propertyId)" :style="{marginLeft: '5px'}">Delete</button>
                </td>
                </tr>
            </tbody>
        </table>

    </div>

    </div>
    
    
</template>


<script>
import MenuNavbar from '/src/components/menunavbar.vue';
import axios from 'axios';

export default {
    name : 'PropertyPage',
    components:{
        MenuNavbar
    },
    data (){
        return {
            userProperties : [],
        }
    },
    methods : {

        getUserProperties(){
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
              this.userProperties = response.data.propertiesData
            }
          }).catch((error) => {
            console.log(error)
            alert(error.response.data.message)
          })
        },

        deleteProperty(propId){
            console.log(propId)

        }
    },
    mounted(){
        this.getUserProperties();
    }

}
</script>

<style scoped>

#propertypagecontainer{
    display : flex;
    float: right;
    margin-left: 100px;
}
#proppageheading{
    margin-top: 20px;
    margin-left:450px;
}
.addPropertydiv{
    margin-top: 150px;
    margin-left :-550px;
}
.property-table{
    width : 100%;
    margin-top:250px;
}

</style>
