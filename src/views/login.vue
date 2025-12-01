<template>

  <body>
    <div class="login ">
      <div id="loginForm" class="border">
        <img alt="logo" class="mx-auto mt-4" src="../assets/images/asset_logo.png" width="45%" />
        <h2 class="title text-center">USER LOGIN</h2>
        <form @submit.prevent="btn_login" class="mt-5">
          <div class="mb-1">
            <div class="input-group">
              <span class="input-group-text"><i class="fa fa-user"></i></span>
              <input v-model="username" type="text" class="form-control" placeholder="Username">
            </div>
            <div class="invalid-feedback">Please enter your username.</div>
          </div>

          <div class="mt-3 position-relative">
            <div class="input-group">
              <span class="input-group-text"><i class="fa fa-lock"></i></span>
              <input v-model="password" :type="showPassword ? 'text' : 'password'" class="form-control"
                placeholder="Password">
              <font-awesome-icon :icon="showPassword ? ['fas', 'eye-slash'] : ['fas', 'eye']" class="eye-icon"
                @click="togglePassword" />
            </div>
          </div>

          <div class="mt-2 text-center">
            <!-- <a class="text-sm" href="#" @click.prevent="showForgotPasswordModal">Forgot Password?</a> -->
          </div>

          <div class="mt-4 d-flex justify-content-center">
            <button type="submit" class="btn btn-login w-50">LOGIN</button>
          </div>
        </form>
      </div>
      <div class="left-box">
        <!-- <img alt="Logo with a computer and gear icon" class="mx-auto" src="../assets/images/asset_logo.png" -->
        <img alt="Logo with a computer and gear icon" class="mx-auto" src="../assets/images/asset_logo_3.gif"
          width="90%" />
      </div>

    </div>
  </body>
</template>

<script>
import API_BASE from '@/utils/api_config';


export default{
  data(){
    return{
      username: "",
      password: "",
      showPassword: false
    }
  },
  methods:{
    togglePassword() {
      this.showPassword = !this.showPassword;
    },

        btn_login() {
      if (!this.username || !this.password) {
        Swal.fire({
          icon: "error",
          title: "Login Failed",
          text: "Please enter both username and password!"
        });
        return;
      }

      fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: this.username, password: this.password })
      })
        .then(response => {
          // console.log("Response:", response);
          return response.json();
        })
        .then(data => {
          if (data.first_login === 0) {
            Swal.fire({
              icon: "warning",
              title: "First Login",
              text: "You must change your password.",
              confirmButtonText: "Change Password"
            }).then(() => {
              this.isChangePasswordVisible = true;
            });
          } else if (data.user) {
            localStorage.setItem("user", JSON.stringify(data.user));
            // this.$router.push("/dashboard");
              //  console.log(data.user.department)
            if (data.user.role === 'system_admin' || data.user.job_title === 'Department Head' || data.user.role === 'admin' || data.user.department === 'SEC') {
              this.$router.push("/dashboard");
            // } else if (data.user.department === 'SEC'){
            //   this.$router.push("/forms/for_approval_forms")
            }else {
              this.$router.push("/tickets/my_tickets");
            }
          } else {
            Swal.fire({ icon: "error", title: "Login Failed", text: data.error || "Unknown error." });
          }
        })
        .catch(error => {
          console.error("Login error:", error);
          Swal.fire({ icon: "error", title: "Login Failed", text: "An error occurred. Please try again." });
        });
    },
  }
}
</script>

<style scoped>
@import url(../assets/css/buttons.css);
@import url(../../public/global.css);

.title {
  font-weight: 800;
  color: #0077b6;
  /* font-size: 28px; */
  letter-spacing: 1px;
  margin: 0;
}
.eye-icon {
  position: absolute;
  top: 50%;
  right: 15px;
  transform: translateY(-50%);
  cursor: pointer;
  color: #2b6777;
  font-size: 18px;
}

body {
  background-color: #fff;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-size: cover;
  margin: 0;
  padding: 0;
}



.left-box {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50%;
  padding: 0;
  margin: 0;
}

.login {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 55%;
  width: 55%;
  background-color: #c7d9f2;
  /* background: linear-gradient(120deg, #7ca2bc92 0%, #a5bfd0 30%, #618aa5 60%, #618aa5 100%); */
  /* border-radius: 20px; */
  /* box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px; */
  box-shadow: 0 20px 70px rgba(76, 132, 184, 0.25);
  /* border: 1px solid rgba(255, 255, 255, 0.746); */
}

.input-group-text {
  background-color: #b3d7df;
  color: #003049;
}

#loginForm {
  background-color: #fff;
  width: 50%;
  height: 100%;
  padding: 0 40px;
  display: flex;
  justify-content: top;
  flex-direction: column;
  /* border-radius: 20px; */
  /* background: rgba(255, 255, 255, 0.38); */
  /* background-color: #eaecec; */
  box-shadow: 0 20px 70px rgba(84, 194, 214, 0.25);
}

@media (max-width: 768px) {
  .login {
    flex-direction: column;
    width: 100%;
    height: auto;
    padding: 20px;
  }

  /* 
  .left-box {
    width: 100%;
    display: none;
  } */

  #loginForm {
    width: 100%;
    padding: 20px;
  }


  .btn {
    font-size: 1rem;
  }

  h2 {
    font-size: 1.5rem;
  }
}

/* Responsive Styles for Medium Screens (768px to 1024px) */
@media (max-width: 1152px) {
  .login {
    flex-direction: column;
    width: 80%;
    height: auto;
    padding: 20px;
  }

  #loginForm {
    width: 100%;
    padding: 20px;
  }

  .input-group-text {
    font-size: 1rem;
  }

  .btn {
    font-size: 1rem;
  }

  h2 {
    font-size: 1.5rem;
  }
}
</style>
