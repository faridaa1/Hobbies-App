<template>
  <div class="potential-matches">
    <h1>Users</h1>

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
        <li v-for="user in paginatedUsers" :key="user.email"
          class="list-group-item d-flex justify-content-between align-items-center">
          <div class="d-flex gap-3">
            <img v-if="user.profile_picture" :src="user.profile_picture"
              class="rounded-circle" style="width: 70px; height:70px; object-fit: cover;">
            <i v-if="!user.profile_picture" class="bi bi-person-circle p-0"
              style="font-size: 70px; line-height: 0"></i>
            <div class="d-flex flex-column gap-2 justify-content-center">
              <div><strong>{{ user.name }}</strong> ({{ user.age }} years old)</div>
              <div>Hobbies: {{ user.hobbies.length ? user.hobbies.join(', ') : "No hobbies listed" }}</div>
            </div>
          </div>
          <FriendRequestButton :otherUser="user" :base_url="base_url" />
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
import { MatchesUser } from "../../types";
import { useUserStore } from "../../stores/user";
import { mapState } from "pinia";
import FriendRequestButton from "./FriendRequestButton.vue";

export default defineComponent({
  data(): {
      users: MatchesUser[],
      minAge: number,
      maxAge: number,
      filteredUsers: MatchesUser[],
      currentPage: number,
      pageSize: number,
      base_url: string
    } {
    return {
      users: [], // All users fetched from the API
      minAge: 18, // Default minimum age
      maxAge: 100, // Default maximum age
      filteredUsers: [], // Filtered users based on age
      currentPage: 1, // Current page
      pageSize: 5, // Number of users per page
      base_url: window.location.href.includes('localhost') ? 'http://localhost:8000' : 'https://group20-web-apps-ec22476.apps.a.comp-teach.qmul.ac.uk'
    };
  },
  components: {
    FriendRequestButton
  },
  watch: {
    user(): void {
      // User undefined until pinia store is installed
      this.filteredUsers = this.removeUserFiltered();
    },
    filteredUsers(): void {
      const newFiltered = this.removeUserFiltered();
      if (newFiltered.length === this.filteredUsers.length - 1) { // Don't want endless calls when filtered changes
        this.filteredUsers = newFiltered;
      }
    }
  },
  computed: {
    ...mapState(useUserStore, ['user', 'csrf']),
    totalPages(): number {
      return Math.ceil(this.filteredUsers.length / this.pageSize);
    },
    paginatedUsers(): MatchesUser[] {
      const start: number = (this.currentPage - 1) * this.pageSize;
      const end: number = start + this.pageSize;
      return this.filteredUsers.slice(start, end);
    },
  },
  methods: {
    fetchUsers(): void {
      // Fetch users from the API
      fetch(`${this.base_url}/api/potential-matches/`,
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
          this.users = data.matches.map((user: MatchesUser) => ({
            ...user,
            hobbies: user.hobbies || [], // Ensure hobbies is an array
          }));
          this.filteredUsers = this.users; // Initialize with all users
        })
        .catch((error) => console.error("Error fetching users:", error));
    },
    applyFilter(): void {
      // Filter users by age range and remove currently logged in user
      this.filteredUsers = this.users.filter(
        (user) =>
          user.age >= this.minAge &&
          user.age <= this.maxAge &&
          user.email !== this.user.email
      );
      this.currentPage = 1; // Reset to the first page after filtering
    },
    clearFilter(): void {
      // Reset age filter and show all users
      this.minAge = 18; // Reset to default minimum age
      this.maxAge = 100; // Reset to default maximum age
      this.filteredUsers = this.users; // Show all users
      this.currentPage = 1; // Reset to the first page
    },
    prevPage(): void {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage(): void {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    removeUserFiltered(): MatchesUser[] {
      return this.filteredUsers.filter(user => user.email !== this.user.email)
    }
  },
  created(): void {
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
