<template>
    <div class="fs-4 mt-4 border rounded p-3 ps-5 mb-5 w-100">
        <h1>My Friends</h1>
        <hr>
        <div class="fs-4 mt-4 d-flex flex-rowalign-items-center gap-5 w-100 align-items-center" v-for="(friend, index) in friends">
            <div class="d-flex gap-5 flex-row w-100 rounded p-2 align-items-center">
                <img v-if="friend.profile_picture" style="width: 70px; height:70px; object-fit: cover;" class="rounded-circle" :src="friend.profile_picture" alt="">
                <i v-if="!friend.profile_picture" class="bi bi-person-circle p-0" style="font-size: 70px; line-height: 0"></i>
                <div class="p-2 rounded w-100">{{ friend.name }}</div>
            </div>
            <button class="border-0 bg-primary text-white rounded px-3 fw-semibold" style="font-size: 1.1rem; height: 2.4rem;">
                Remove
                <!-- <i class="bi bi-trash-fill"></i> -->
            </button>
        </div>
    </div>
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";

      export default defineComponent({
          data() {
              return {
                //   title: "Other Page",
                friends: [
                    { 
                    "name": "Person McPerson",
                    "profile_picture": "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649"
                    },
                    { 
                    "name": "Alice Wonderland",
                    "profile_picture": ""
                    },
                    { 
                    "name": "Bob Builder",
                    "profile_picture": "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649"
                    },
                    { 
                    "name": "Charlie Brown",
                    "profile_picture": "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649"
                    },
                    { 
                    "name": "Daisy Duck",
                    "profile_picture": "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649"
                    },
                    { 
                    "name": "Eve Online",
                    "profile_picture": ""
                    },
                    { 
                    "name": "Frank Castle",
                    "profile_picture": "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649"
                    },
                    { 
                    "name": "Grace Hopper",
                    "profile_picture": ""
                    }
                ]
            }
        },
        async mounted() {
            let response = await fetch("http://localhost:8000/profile/", {
                credentials: 'include'
            });
            let data = await response.json();
            // this.user = data
            // const store = useUserStore()
            // store.saveUser(user_id)
          }
      })
  </script>
  
  <style scoped>
  </style>
  