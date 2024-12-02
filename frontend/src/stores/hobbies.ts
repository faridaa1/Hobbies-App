import { defineStore } from 'pinia'
import { Hobby } from '../types'

export const useUserStore = defineStore('hobbies', {
    state: () => ({
        hobbies: [] as Hobby[] 
    }),
    actions: {
        addHobby(hobby: Hobby) {
            this.hobbies.push(hobby)
        }
    }
})