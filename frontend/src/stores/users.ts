import { defineStore } from 'pinia'
import { CustomUser } from '../types'

export const useUsersStore = defineStore('users', {
    state: (): {users: CustomUser[] } => ({
        users: [],
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