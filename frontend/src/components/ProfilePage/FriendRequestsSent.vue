<template>
    <div class="fs-4 mt-4 border rounded p-3 ps-5 mb-5 w-100">
      <h1>Friend Requests Sent</h1>
      <hr>
      <div
        class="fs-4 mt-4 d-flex flex-row align-items-center gap-5 w-100"
        v-for="(friend, index) in paginatedFriends"
        :key="index"
      >
        <div class="d-flex gap-5 flex-row w-100 rounded p-2 align-items-center">
          <img
            v-if="friend.profile_picture"
            style="width: 70px; height:70px; object-fit: cover;"
            class="rounded-circle"
            :src="friend.profile_picture"
            alt=""
          />
          <i
            v-if="!friend.profile_picture"
            class="bi bi-person-circle p-0"
            style="font-size: 70px; line-height: 0"
          ></i>
          <div class="p-2 rounded w-100">{{ friend.name }}</div>
        </div>
        <button
          type="button"
          class="btn btn-danger px-3 fw-semibold"
          style="font-size: 1.1rem; height: 2.4rem;"
        >
          Cancel
        </button>
      </div>
  
      <!-- Pagination Controls -->
      <div class="d-flex justify-content-center mt-4">
        <button
          type="button"
          class="btn btn-secondary me-2"
          :disabled="currentPage === 1"
          @click="prevPage"
        >
          Previous
        </button>
        <button
          type="button"
          class="btn btn-secondary"
          :disabled="currentPage === totalPages"
          @click="nextPage"
        >
          Next
        </button>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  
  export default defineComponent({
    data() {
      return {
        friends: [
          {
            name: "Person McPerson",
            profile_picture:
              "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649",
          },
          { name: "Alice Wonderland", profile_picture: "" },
          {
            name: "Bob Builder",
            profile_picture:
              "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649",
          },
          {
            name: "Charlie Brown",
            profile_picture:
              "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649",
          },
          {
            name: "Daisy Duck",
            profile_picture:
              "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649",
          },
          { name: "Eve Online", profile_picture: "" },
          {
            name: "Frank Castle",
            profile_picture:
              "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649",
          },
          { name: "Grace Hopper", profile_picture: "" },
        ],
        currentPage: 1,
        pageSize: 5, // Number of items per page
      };
    },
    computed: {
      paginatedFriends() {
        const start = (this.currentPage - 1) * this.pageSize;
        const end = start + this.pageSize;
        return this.friends.slice(start, end);
      },
      totalPages() {
        return Math.ceil(this.friends.length / this.pageSize);
      },
    },
    methods: {
      nextPage() {
        if (this.currentPage < this.totalPages) {
          this.currentPage++;
        }
      },
      prevPage() {
        if (this.currentPage > 1) {
          this.currentPage--;
        }
      },
    },
  });
  </script>
  
  <style scoped></style>
  