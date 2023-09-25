import { createRouter, createWebHistory } from 'vue-router'
import adminLogin from './views/adminlogin.vue'
import Dashboard from './views/dashboard.vue'
import PropertyPage from './views/properties.vue'
import addProperties from './components/addproperty.vue'
import TenantPage from './views/Tenants.vue'


const routes = [

  {
    path: '/home',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/login',
    name: 'adminLogin',
    component: adminLogin
  },
  {
    path: '/properties',
    name: 'PropertyPage',
    component: PropertyPage
  },
  {
    path: '/addproperty',
    name: 'addProperties',
    component: addProperties
  },
  {
    path: '/tenants',
    name: 'TenantPage',
    component: TenantPage
  },

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// router.beforeEach((to, from, next) => {
//   if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
//     next({ name: 'LogIn', query: { to: to.path } });
//   } else {
//     next()
//   }
// })

export default router