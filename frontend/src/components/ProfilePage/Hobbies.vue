<template>
    <div class="fs-4 mt-4 border rounded p-3 ps-5 mb-5 w-100">
        <div class="d-flex justify-content-between">
            <h1>My Hobbies</h1>
            <button class="border-0 bg-white text-primary"><i class="bi bi-plus-circle-fill fs-1"></i></button>
        </div>
        <div class="fs-4 mt-4 d-flex flex-rowalign-items-center gap-5 w-100" v-for="(hobby, index) in hobbies">
            <div class="d-flex flex-column w-100">
                <div>Name</div>
                <div class="p-2 rounded w-100" style="background-color: lightgray;">{{ hobby.name }}</div>
            </div>
            <div class="d-flex flex-column w-100">
                <div>Description</div>
                <div class="p-2 rounded w-100" style="background-color: lightgray;">{{ hobby.description }}</div>
            </div>
            <button class="text-primary border-0 bg-white fs-1">
                <i class="bi bi-trash-fill"></i>
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
                hobbies: [
                    {
                    name: "Reading",
                    description: "Exploring various genres of literature, from fiction to non-fiction, to expand knowledge and imagination."
                    },
                    {
                    name: "Cycling",
                    description: "Riding a bicycle for exercise, recreation, or sport. A great way to explore the outdoors and stay fit."
                    },
                    {
                    name: "Photography",
                    description: "Capturing moments and scenes through a camera. It’s both an artistic and technical pursuit."
                    },
                    {
                    name: "Cooking",
                    description: "Preparing meals and experimenting with different cuisines. A fun way to be creative and explore new flavors."
                    },
                    {
                    name: "Gardening",
                    description: "Growing plants, flowers, or vegetables in a garden. It promotes relaxation, creativity, and sustainability."
                    },
                    {
                    name: "Painting",
                    description: "Using paints and brushes to create visual art. It allows for self-expression and development of creativity."
                    },
                    {
                    name: "Music",
                    description: "Playing musical instruments or listening to music. A form of art that brings joy, relaxation, and emotional expression."
                    },
                    {
                    name: "Traveling",
                    description: "Exploring new places, cultures, and experiences. Traveling allows you to learn, grow, and connect with the world."
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
  