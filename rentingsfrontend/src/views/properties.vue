<template>
    <MenuNavbar/>
    <div class="container" id="propertypagecontainer">
        <h1 id="proppageheading">Properties</h1>
        <br/>
        <div class="addPropertydiv">
        <a type="button" class="btn btn-primary" :style="{Position:'fixed'}" href="/addproperty" >Add Property</a>
        </div>
        <div class="property-table">
            <table class="table table-striped-columns">
            <thead>
                <tr>
                <th scope="col">#</th>
                <th scope="col">First</th>
                <th scope="col">Last</th>
                <th scope="col">Handle</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                <th scope="row">1</th>
                <td>Mark</td>
                <td>Otto</td>
                <td>@mdo</td>
                </tr>
                <tr>
                <th scope="row">2</th>
                <td>Jacob</td>
                <td>Thornton</td>
                <td>@fat</td>
                </tr>
                <tr>
                <th scope="row">3</th>
                <td colspan="2">Larry the Bird</td>
                <td>@twitter</td>
                </tr>
            </tbody>
        </table>

    </div>

    </div>
    
    
</template>


<script>
import MenuNavbar from '/src/components/menunavbar.vue';

export default {
    name : 'PropertyPage',
    components:{
        MenuNavbar
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
