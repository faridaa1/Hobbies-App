<template>
  <div class="potential-matches">
    <h1>Potential Matches</h1>

    <!-- Age Filter -->
    <div class="filters mb-4">
      <label for="age-filter">Filter by Age:</label>
      <div class="age-range d-flex align-items-center mb-3">
        <span class="me-2">Min: </span>
        <input type="number" v-model="minAge" placeholder="Min Age" class="me-2" />
        <span class="me-2">Max: </span>
        <input type="number" v-model="maxAge" placeholder="Max Age" class="me-2" />
      </div>
      <button @click="applyFilter" class="btn btn-primary me-2">Apply Filter</button>
      <button @click="clearFilter" class="btn btn-danger">Clear Filter</button>
    </div>

    <!-- User List -->
    <div class="user-list">
      <ul class="list-group">
        <li v-for="user in paginatedUsers" :key="user.username"
          class="list-group-item d-flex justify-content-between align-items-center">
          <div>
            <p><strong>{{ user.name }}</strong> ({{ user.age }} years old)</p>
            <p>Hobbies: {{ user.hobbies.length ? user.hobbies.join(', ') : "No hobbies listed" }}</p>
          </div>
          <FriendRequestButton :otherUser="user" />
        </li>
      </ul>
    </div>

    <!-- Pagination Controls -->
    <div class="pagination-controls mt-4 d-flex justify-content-center">
      <button class="btn btn-secondary me-2" :disabled="currentPage === 1" @click="prevPage">
        Previous
      </button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button class="btn btn-secondary ms-2" :disabled="currentPage === totalPages" @click="nextPage">
        Next
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { CustomUserAge } from "../../types";
import { useUserStore } from "../../stores/user";
import { mapState } from "pinia";
import FriendRequestButton from "./FriendRequestButton.vue";

export default defineComponent({
  data() {
    return {
      users: [] as CustomUserAge[], // All users fetched from the API
      minAge: 18, // Default minimum age
      maxAge: 100, // Default maximum age
      filteredUsers: [] as CustomUserAge[], // Filtered users based on age
      currentPage: 1, // Current page
      pageSize: 5, // Number of users per page
    };
  },
  components: {
    FriendRequestButton,
  },
  computed: {
    ...mapState(useUserStore, ["user", "csrf"]),
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
      fetch("http://localhost:8000/api/potential-matches",
        {
          method: 'GET',
          headers: {
            "X-CSRFToken": this.csrf,
          },
          credentials: 'include'
        }
      )
        .then((response) => response.json())
        .then((data) => {
          console.log(data)
          this.users = data.matches.map((user) => ({
            ...user,
            hobbies: user.hobbies || [], // Ensure hobbies is an array
          }));
          this.filteredUsers = this.users; // Initialize with all users
        })
        .catch((error) => console.error("Error fetching users:", error));
    },
    applyFilter() {
      // Filter users by age range and remove currently logged in user
      this.filteredUsers = this.users.filter(
        (user) =>
          user.age >= this.minAge &&
          user.age <= this.maxAge &&
          user.email !== this.user.email
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
  },
  created() {
    this.fetchUsers(); // Fetch users when the component is created
  },
});
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
  margin-top: 90px;
}
</style>
