import { defineStore } from 'pinia'
import { CustomUser } from '../types'

export const useUsersStore = defineStore('users', {
    state: (): {users: CustomUser[] } => ({
        users: [],
    }),
    actions: {
        saveUsers(users: CustomUser[]): void {
            this.users = users
        },
        addUser(user: CustomUser): void {
            this.users.push(user)
        },
    }
})