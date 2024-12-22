<template>
    <div class="fs-4 mt-4 border rounded p-3 ps-5 mb-5 w-100">
        <h1>My Friends</h1>
        <hr>
        <div class="fs-4 mt-4 d-flex flex-row align-items-center gap-5 w-100 align-items-center" v-for="friend in friends">
            <div class="d-flex gap-5 flex-row w-100 rounded p-2 align-items-center">
                <img v-if="friend.user_profile_picture" style="width: 70px; height:70px; object-fit: cover;" class="rounded-circle" :src="friend.user_profile_picture">
                <i v-if="!friend.user_profile_picture" class="bi bi-person-circle p-0" style="font-size: 70px; line-height: 0"></i>
                <div class="p-2 rounded w-100">{{ friend.user_name }}</div>
            </div>
            <button type="button" class="btn btn-primary px-3 fw-semibold" style="font-size: 1.1rem; height: 2.4rem;" @click="removeFriend(friend.id)">
                Remove
            </button>
        </div>
    </div>
  </template>
  
  <script lang="ts">
    import { defineComponent } from "vue";
    import { CustomUser, Friendship, } from "../../types";
    import { useUserStore } from "../../stores/user";

    export default defineComponent({
        methods: {
            async removeFriend(id: number): Promise<void> {
                if (useUserStore().csrf !== '') {
                    let response: Response = await fetch(`http://localhost:8000/api/user/friendship/${id}/`, {
                        method:'POST', 
                        credentials: 'include', 
                        headers: { 
                            'Content-Type': 'application/json',
                            "X-CSRFToken": useUserStore().csrf
                        },
                        body: JSON.stringify(false),
                    }) 
                    if (!response.ok) {
                        confirm('Error occurred when removing friend')
                        return
                    }
                    useUserStore().updateFriendship(id, false)
                }
            }
        },
        computed: {
            user(): CustomUser {
                return useUserStore().user
            }, friends(): Friendship[] {
                if (this.user && this.user.friends) {
                    return this.user.friends.filter(friendship => friendship.status === 'Accepted')
                }
                return []
            }, 
        }
    })
  </script>
  
  <style scoped>
  </style>
  