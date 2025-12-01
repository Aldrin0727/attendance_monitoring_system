// // const API_BASE = process.env.VUE_APP_API_BASE_URL || "http://192.168.1.31:5000" || "http://192.168.0.101:5000";

// // for server
// const API_BASE = process.env.VUE_APP_API_BASE_URL || "http://192.168.0.101:5000";

// // for local
const API_BASE = process.env.VUE_APP_API_BASE_URL;

// let API_BASE;

// if (window.location.hostname === '192.168.0.101' || window.location.hostname === '127.0.0.1') {
//     API_BASE = process.env.VUE_APP_API_BASE_URL
// } else {
//   API_BASE = process.env.VUE_APP_API_BROADCAST_URL;  // Broadcast IP for external access

// }

// console.log(API_BASE); // Logs the URL that the frontend will use to connect to the backend

export default API_BASE;


