import { defineStore } from 'pinia'
import { CustomUser } from '../types'

export const useUserStore = defineStore('user', {
    state: () => ({
        user: {} as CustomUser 
    }),
    actions: {
        saveUser(user: CustomUser) {
            this.user = user
        }
    }
})