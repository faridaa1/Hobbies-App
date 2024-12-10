import { defineStore } from 'pinia'
import { CustomUser, UserHobby } from '../types'

export const useUserStore = defineStore('user', {
    state: () => ({
        user: {} as CustomUser,
        hobbies: [] as UserHobby[]
    }),
    getters: {
        getHobbies: (state) => {
            return state.hobbies;
        },
    },
    actions: {
        saveUser(user: CustomUser) {
            this.user = user
        },
        saveHobbies(hobbies: UserHobby[]) {
            this.hobbies = hobbies
        },
        addHobby(hobby: UserHobby) {
            this.hobbies.push(hobby)
        },
        deleteHobby(hobby : UserHobby) {
            this.hobbies = this.hobbies.filter(myHobby => myHobby !== hobby)
        },
    }
})