<template>
    <div>
        <ul class="nav nav-tabs mt-4" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="personal-details-tab" data-bs-toggle="tab"
                    data-bs-target="#personal-details-tab-pane" type="button" role="tab"
                    aria-controls="personal-details-tab-pane" aria-selected="true">
                    Personal Details
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button name="hobbies" class="nav-link" id="hobbies-tab" data-bs-toggle="tab"
                    data-bs-target="#hobbies-tab-pane" type="button" role="tab" aria-controls="hobbies-tab-pane"
                    aria-selected="true">
                    Hobbies
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="friends-tab" data-bs-toggle="tab" data-bs-target="#friends-tab-pane"
                    type="button" role="tab" aria-controls="friends-tab-pane" aria-selected="true">
                    Friends
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="friend-requests-sent-tab" data-bs-toggle="tab"
                    data-bs-target="#friend-requests-sent-tab-pane" type="button" role="tab"
                    aria-controls="friend-requests-sent-tab-pane" aria-selected="true">
                    Friend Requests Sent
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="friend-requests-received-tab" data-bs-toggle="tab"
                    data-bs-target="#friend-requests-received-tab-pane" type="button" role="tab"
                    aria-controls="friend-requests-received-tab-pane" aria-selected="true">
                    Friend Requests Received
                </button>
            </li>
        </ul>
        <div class="tab-content" id="myTabContent">
            <div class="tab-pane fade show active" id="personal-details-tab-pane" role="tabpanel"
                aria-labelledby="personal-details-tab" tabindex="0">
                <PersonalDetails :today="today()" :base_url="base_url" />
            </div>
            <div class="tab-pane fade" id="hobbies-tab-pane" role="tabpanel" aria-labelledby="hobbies-tab" tabindex="1">
                <Hobbies :today="today()" :base_url="base_url" />
            </div>
            <div class="tab-pane fade" id="friends-tab-pane" role="tabpanel" aria-labelledby="friends-tab" tabindex="2">
                <Friends :base_url="base_url" />
            </div>
            <div class="tab-pane fade" id="friend-requests-sent-tab-pane" role="tabpanel"
                aria-labelledby="friend-requests-sent-tab" tabindex="3">
                <FriendRequestsSent :base_url="base_url" />
            </div>
            <div class="tab-pane fade" id="friend-requests-received-tab-pane" role="tabpanel"
                aria-labelledby="friend-requests-received-tab" tabindex="4">
                <FriendRequestsReceived :base_url="base_url" />
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import PersonalDetails from "../components/ProfilePage/PersonalDetails.vue";
import Hobbies from "../components/ProfilePage/Hobbies.vue";
import Friends from "../components/ProfilePage/Friends.vue";
import FriendRequestsSent from "../components/ProfilePage/FriendRequestsSent.vue";
import FriendRequestsReceived from "../components/ProfilePage/FriendRequestsReceived.vue";

export default defineComponent({
    data(): { title: String, base_url: string } {
        return {
            title: "Profile",
            base_url: window.location.href.includes('localhost') ? 'http://localhost:8000' : 'https://group20-web-apps-ec22476.apps.a.comp-teach.qmul.ac.uk'
        }
    },
    components: {
        PersonalDetails,
        Hobbies,
        Friends,
        FriendRequestsSent,
        FriendRequestsReceived,
    },
    methods: {
        today(): string {
            const today: Date = new Date();
            const year: number = today.getFullYear();
            const month: string = (today.getMonth() + 1).toString().padStart(2, '0')
            const day: string = today.getDate().toString().padStart(2, '0')
            return `${year}-${month}-${day}`;
        }
    }
})
</script>

<style scoped></style>