<template>
    <button class="btn btn-success" @click="sendRequest(otherUser.username)"
        :disabled="userStore.getFriendship(otherUser.email) !== undefined"> <!-- Disable button if friendship exists-->
        {{ userStore.getFriendship(otherUser.email)?.status ?? 'Send Request' }}
    </button>
</template>
<script lang="ts">
import { defineComponent, PropType } from 'vue';
import { CustomUserAge } from '../../types';
import { useUserStore } from '../../stores/user';
import { mapStores } from 'pinia';

const url = 'http://localhost:8000';

export default defineComponent({
    props: {
        otherUser: {
            type: Object as PropType<CustomUserAge>,
            required: true
        },
    },
    computed: {
        ...mapStores(useUserStore),
    },
    methods: {
        async sendRequest(username: string) {
            try {
                const req = await fetch(`${url}/api/user/${this.userStore.user.id}/friendship/${username}/`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                        "X-CSRFToken": this.userStore.csrf
                    }
                });
                const response = await req.json();
                console.log(`Friend request sent to user with id${username}`);
                // Update user store - state change causes button text to change
                this.userStore.user.friends.push(response.friendship)
            } catch (error) {
                console.log(error)
            }
        },
    }
})
</script>
<style></style>