<template>
    <div>
        <ul class="nav nav-tabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="personal-details-tab" data-bs-toggle="tab" data-bs-target="#personal-details-tab-pane" type="button" role="tab" aria-controls="personal-details-tab-pane" aria-selected="true">
                    Personal Details
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="hobbies-tab" data-bs-toggle="tab" data-bs-target="#hobbies-tab-pane" type="button" role="tab" aria-controls="hobbies-tab-pane" aria-selected="true">
                    Hobbies
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="friends-tab" data-bs-toggle="tab" data-bs-target="#friends-tab-pane" type="button" role="tab" aria-controls="friends-tab-pane" aria-selected="true">
                    Friends
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="friend-requests-sent-tab" data-bs-toggle="tab" data-bs-target="#friend-requests-sent-tab-pane" type="button" role="tab" aria-controls="friend-requests-sent-tab-pane" aria-selected="true">
                    Friend Requests Sent
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="friend-requests-received-tab" data-bs-toggle="tab" data-bs-target="#friend-requests-received-tab-pane" type="button" role="tab" aria-controls="friend-requests-received-tab-pane" aria-selected="true">
                    Friend Requests Received
                </button>
            </li>
        </ul>
        <div class="tab-content" id="myTabContent">
            <div class="tab-pane fade show active" id="personal-details-tab-pane" role="tabpanel" aria-labelledby="personal-details-tab" tabindex="0">
                <PersonalDetails />
            </div>
            <div class="tab-pane fade" id="hobbies-tab-pane" role="tabpanel" aria-labelledby="hobbies-tab" tabindex="1">
            </div>
            <div class="tab-pane fade" id="friends-tab-pane" role="tabpanel" aria-labelledby="friends-tab" tabindex="2">
            </div>
            <div class="tab-pane fade" id="friend-requests-sent-tab-pane" role="tabpanel" aria-labelledby="friend-requests-sent-tab" tabindex="3">
            </div>
            <div class="tab-pane fade" id="friend-requests-received-tab-pane" role="tabpanel" aria-labelledby="friend-requests-received-tab" tabindex="4">
            </div>
        </div>
    </div>
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";
      import PersonalDetails from "../components/ProfilePage/PersonalDetails.vue";
  
      export default defineComponent({
          data() {
              return {
                  title: "Profile",
              }
          }
      })
  </script>
  
  <style scoped>
  </style>
  