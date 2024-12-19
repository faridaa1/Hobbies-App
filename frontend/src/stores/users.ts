import { defineStore } from 'pinia'
import { CustomUser } from '../types'

export const useUsersStore = defineStore('users', {
    state: () => ({
        users: [] as CustomUser[],
    }),
    actions: {
        saveUsers(users: CustomUser[]) {
            this.users = users
        },
        addUser(user: CustomUser) {
            this.users.push(user)
        },
    }
})