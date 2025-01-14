<template>
    <div class="fs-4 mt-4 border rounded p-3 ps-5 mb-5 w-100">
        <h1>Friend Requests Sent</h1>
        <hr>
        <div class="text-secondary text-center" v-if="friends.length === 0">
            <p>No Friend Requests Sent</p>
        </div>
        <div class="fs-4 mt-4 d-flex flex-row align-items-center gap-5 w-100" v-for="friend in displayedFriends">
            <div class="d-flex gap-5 flex-row w-100 rounded p-2 align-items-center">
                <img v-if="friend.user_profile_picture" style="width: 70px; height:70px; object-fit: cover;"
                    class="rounded-circle" :src="friend.user_profile_picture">
                <i v-if="!friend.user_profile_picture" class="bi bi-person-circle p-0"
                    style="font-size: 70px; line-height: 0"></i>
                <div class="p-2 rounded w-100">{{ friend.user_name }}</div>
            </div>
            <button type="button" class="btn btn-danger px-3 fw-semibold" style="font-size: 1.1rem; height: 2.4rem;"
                @click="unsend(friend.id)">
                Cancel
            </button>
        </div>
        <div class="d-flex gap-2 justify-content-center">
            <button type="button" class="btn btn-secondary" v-if="friendIndex > 0" @click="prevPage">Previous</button>
            <button type="button" class="btn btn-secondary" v-if="friendIndex + pageSize < friends.length"
                @click="nextPage">Next</button>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { CustomUser, Friendship } from "../../types";
import { useUserStore } from "../../stores/user";

export default defineComponent({
    props: {
        base_url: {
            type: String,
            required: true
        }
    },
    data(): { friendIndex: number, pageSize: number } {
        return { friendIndex: 0, pageSize: 5 }
    },
    methods: {
        prevPage(): void {
            this.friendIndex -= this.pageSize
        },
        nextPage(): void {
            this.friendIndex += this.pageSize
        },
        async unsend(id: number): Promise<void> {
            if (useUserStore().csrf !== '') {
                let response: Response = await fetch(`${this.base_url}/api/friendship/${id}/`, {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                        "X-CSRFToken": useUserStore().csrf
                    },
                    body: JSON.stringify(false),
                })
                if (!response.ok) {
                    confirm('Error occurred when cancelling friend request')
                    return
                }
                useUserStore().updateFriendship(id, false)
                if (this.displayedFriends.length === 0 && this.friends.length !== 0) {
                    this.friendIndex -= this.pageSize
                }
            }
        }
    },
    computed: {
        user(): CustomUser {
            return useUserStore().user
        }, friends(): Friendship[] {
            if (this.user && this.user.friends) {
                return this.user.friends.filter(friendship => friendship.status === 'Pending' && friendship.sent)
            }
            return []
        }, displayedFriends(): Friendship[] {
            return this.friends.slice(this.friendIndex, this.friendIndex + this.pageSize)
        }
    }
})
</script>

<style scoped></style>