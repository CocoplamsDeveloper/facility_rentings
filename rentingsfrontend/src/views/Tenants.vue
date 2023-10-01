<template>
    <MenuNavbar/>
    <div class="container" id="tenantpagecontainer">
        <h1 id="tenantpageheading">Tenants</h1>
        <br/>
        <div class="addTenantdiv">
        <a type="button" class="btn btn-primary" :style="{Position:'fixed'}" href="/addtenant" >Add Tenant</a>
        </div>
        <div class="tenants-table">
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
    name : 'TenantsPage',
    components:{
        MenuNavbar
    }

}
</script>

<style scoped>

#tenantpagecontainer{
    display : flex;
    float: right;
    margin-left: 350px;
}
#tenantpageheading{
    margin-top: 20px;
    margin-left:450px;
}
.addTenantdiv{
    margin-top: 150px;
    margin-left :-550px;
}
.tenants-table{
    width : 100%;
    margin-top:250px;
}

</style>
