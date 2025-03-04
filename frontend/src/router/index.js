import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Generate from '../views/Generate.vue';
import Results from '../views/Results.vue';
import History from '../views/History.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/generate',
    name: 'Generate',
    component: Generate
  },
  {
    path: '/results/:id',
    name: 'Results',
    component: Results
  },
  {
    path: '/history',
    name: 'History',
    component: History
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router; 