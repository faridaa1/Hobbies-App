import { defineStore } from 'pinia'
import { CustomUser } from '../types'

export const useUserStore = defineStore('user', {
    state: () => ({
        user: null as CustomUser | null
    }),
    actions: {
        saveUser(user: CustomUser) {
            this.user = user
        }
    }
})