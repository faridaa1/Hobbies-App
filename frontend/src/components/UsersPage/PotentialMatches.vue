<template>
  <div class="potential-matches">
    <h1>Potential Matches</h1>

    <!-- Age Filter -->
    <div class="filters mb-4">
      <label for="age-filter">Filter by Age</label>
      <FilterButton :min="minAge" :max="maxAge" class="my-5" @changeMinAge="changeMinAge" @changeMaxAge="changeMaxAge"/>
      <button @click="clearFilter" class="btn btn-danger">Clear Filter</button>
    </div>

    <!-- User List -->
    <div class="user-list">
      <ul class="list-group">
        <li v-for="user in paginatedUsers" :key="user.email"
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
import { MatchesUser } from "../../types";
import { useUserStore } from "../../stores/user";
import { mapState } from "pinia";
import FriendRequestButton from "./FriendRequestButton.vue";
import FilterButton from "./FilterButton.vue";

export default defineComponent({
  data() {
    return {
      users: [] as MatchesUser[], // All users fetched from the API
      minAge: 0, // Default minimum age
      maxAge: 100, // Default maximum age
      filteredUsers: [] as MatchesUser[], // Filtered users based on age
      currentPage: 1, // Current page
      pageSize: 5, // Number of users per page
    };
  },
  components: {
    FriendRequestButton, FilterButton
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
    changeMinAge(newMin: number): void {
      this.minAge += newMin
    },
    changeMaxAge(newMax: number): void {
      this.maxAge += newMax
    },
    fetchUsers(): void {
      // Fetch users from the API
      fetch("/api/potential-matches/",
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
