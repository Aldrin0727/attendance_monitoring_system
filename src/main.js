window.__VUE_PROD_HYDRATION_MISMATCH_DETAILS__ = true;

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import $ from 'jquery';

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import all solid icons */
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'

import './assets/css/buttons.css'
import './assets/css/inputbox.css'
import './assets/css/cards.css'
import './assets/css/modal.css'
import './assets/css/dataTable.css'
import '../public/global.css'

import 'datatables.net-bs5';
import 'datatables.net-bs5/css/dataTables.bootstrap5.min.css';

import DataTable from 'datatables.net-vue3';
import DataTablesLib from 'datatables.net';


DataTable.use(DataTablesLib);

/* add all solid icons to the library */
library.add(fas, far, fab)

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)

app.use(router).mount('#app')


window.$ = window.jQuery = $; // Make jQuery available globally

// new Vue({
//   render: h => h(App),
// }).$mount('#app');

