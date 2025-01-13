<template>
    <button name="status" v-if="friendship" :class="buttonClass" disabled>
        {{ buttonText }}
    </button>
    <button name="send-request" v-else @click="sendRequest(otherUser.username)" class="btn btn-success">
        Send Request
    </button>
</template>
<script lang="ts">
import { defineComponent, PropType } from 'vue';
import { MatchesUser } from '../../types';
import { useUserStore } from '../../stores/user';
import { mapStores } from 'pinia';

export default defineComponent({
    props: {
        otherUser: {
            type: Object as PropType<MatchesUser>,
            required: true
        },
    },
    computed: {
        ...mapStores(useUserStore),
        friendship() {
            return this.userStore.getFriendship(this.otherUser.email);
        },
        userSentRequest() {
            return this.friendship?.sent;
        },
        buttonClass() {
            return `btn ${this.friendship?.status === 'Accepted' ? 'btn-primary' : 'btn-success'}`;
        },
        buttonText() {
            if (this.friendship?.status === 'Accepted') {
                return 'Accepted'
            } else if (!this.friendship?.sent) {
                return 'Check Profile'
            } else {
                return 'Request Sent'
            }
        },
    },
    methods: {
        async sendRequest(username: string) {
            try {
                const req = await fetch(`/api/user/${this.userStore.user.id}/friendship/${username}/`, {
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
        }
    }
})
</script>
<style></style>