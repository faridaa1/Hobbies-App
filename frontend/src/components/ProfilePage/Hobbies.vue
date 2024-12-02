<template>
    <div class="fs-4 mt-4 border rounded p-3 ps-5 mb-5 w-100">
        <div class="d-flex justify-content-between">
            <h1>My Hobbies</h1>
            <button class="border-0 bg-white text-primary"><i class="bi bi-plus-circle-fill fs-1"></i></button>
        </div>
        <div class="fs-4 mt-4 d-flex flex-rowalign-items-center gap-5 w-100" v-for="(hobby, index) in hobbies">
            <div class="d-flex flex-column w-100">
                <div>Name</div>
                <div class="p-2 rounded w-100" style="background-color: lightgray;">{{ hobby.hobby_name }}</div>
            </div>
            <div class="d-flex flex-column w-100">
                <div>Description</div>
                <div class="p-2 rounded w-100" style="background-color: lightgray;">{{ hobby.hobby_description }}</div>
            </div>
            <button class="text-primary border-0 bg-white fs-1">
                <i class="bi bi-trash-fill"></i>
            </button>
        </div>
    </div>
  </template>
  
  <script lang="ts">
    import { defineComponent } from "vue";
    import { useHobbiesStore } from "../../stores/hobbies";
    import { Hobby } from "../../types";

    export default defineComponent({
        computed: {
            hobbies(): Hobby[] {
                const hobbiesStore = useHobbiesStore()
                return hobbiesStore.hobbies;
            }
        }
    })
</script>
  
<style scoped>
</style>
