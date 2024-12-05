import { defineStore } from 'pinia'
import { CustomUser } from '../types'

export const useUserStore = defineStore('user', {
    state: () => ({
        user: {} as CustomUser,
    }),
    actions: {
        saveUser(user: CustomUser) {
            this.user = user
        },
        async getUser() {
            // should probably check that user is signed in before doing this
            const result = await fetch('http://localhost:8000/api/user/')
            const data = await result.json()
            this.saveUser(data)
        }
    }
})