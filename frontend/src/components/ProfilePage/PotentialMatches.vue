<template>
    <div class="potential-matches">
      <h1>Potential Matches</h1>
  
      <!-- Age Filter -->
      <div class="filters mb-4">
        <label for="age-filter">Filter by Age:</label>
        <input
          type="number"
          v-model="minAge"
          placeholder="Min Age"
          class="me-2"
        />
        <input
          type="number"
          v-model="maxAge"
          placeholder="Max Age"
          class="me-2"
        />
        <button @click="applyFilter" class="btn btn-primary me-2">Apply Filter</button>
        <button @click="clearFilter" class="btn btn-danger">Clear Filter</button>
      </div>
  
      <!-- User List -->
      <div class="user-list">
        <ul class="list-group">
          <li
            v-for="user in paginatedUsers"
            :key="user.username"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <div>
              <p><strong>{{ user.name }}</strong> ({{ user.age }} years old)</p>
            </div>
            <button class="btn btn-success" @click="sendRequest(user.username)">
              Send Request
            </button>
          </li>
        </ul>
      </div>
  
      <!-- Pagination Controls -->
      <div class="pagination-controls mt-4 d-flex justify-content-center">
        <button
          class="btn btn-secondary me-2"
          :disabled="currentPage === 1"
          @click="prevPage"
        >
          Previous
        </button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button
          class="btn btn-secondary ms-2"
          :disabled="currentPage === totalPages"
          @click="nextPage"
        >
          Next
        </button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        users: [], // All users fetched from the API
        minAge: 18, // Default minimum age
        maxAge: 100, // Default maximum age
        filteredUsers: [], // Filtered users based on age
        currentPage: 1, // Current page
        pageSize: 5, // Number of users per page
      };
    },
    computed: {
      totalPages() {
        return Math.ceil(this.filteredUsers.length / this.pageSize);
      },
      paginatedUsers() {
        const start = (this.currentPage - 1) * this.pageSize;
        const end = start + this.pageSize;
        return this.filteredUsers.slice(start, end);
      },
    },
    methods: {
      fetchUsers() {
        // Fetch users from the API
        fetch("http://127.0.0.1:8000/api/users/")
          .then((response) => response.json())
          .then((data) => {
            this.users = data;
            this.filteredUsers = data; // Initialize with all users
          })
          .catch((error) => console.error("Error fetching users:", error));
      },
      applyFilter() {
        // Filter users by age range
        this.filteredUsers = this.users.filter(
          (user) => user.age >= this.minAge && user.age <= this.maxAge
        );
        this.currentPage = 1; // Reset to the first page after filtering
      },
      clearFilter() {
        // Reset age filter and show all users
        this.minAge = 18; // Reset to default minimum age
        this.maxAge = 100; // Reset to default maximum age
        this.filteredUsers = this.users; // Show all users
        this.currentPage = 1; // Reset to the first page
      },
      prevPage() {
        if (this.currentPage > 1) {
          this.currentPage--;
        }
      },
      nextPage() {
        if (this.currentPage < this.totalPages) {
          this.currentPage++;
        }
      },
      sendRequest(username) {
        console.log(`Friend request sent to ${username}`);
        // Add functionality to send a friend request
      },
    },
    created() {
      this.fetchUsers(); // Fetch users when the component is created
    },
  };
  </script>
  
  <style scoped>
  .potential-matches {
    padding: 20px;
  }
  .filters input {
    width: 100px;
  }
  .user-list {
    margin-top: 20px;
  }
  .list-group-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .pagination-controls {
    margin-top: 20px;
  }
  </style>
  