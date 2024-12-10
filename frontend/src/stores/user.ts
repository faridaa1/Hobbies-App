import { defineStore } from 'pinia'
import { CustomUser, UserHobbies, UserHobby } from '../types'

export const useUserStore = defineStore('user', {
    state: () => ({
        user: {} as CustomUser,
        hobbies: {} as UserHobbies
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
        saveHobbies(hobbies: UserHobbies) {
            this.hobbies = hobbies
        },
        addHobby(hobby: UserHobby) {
            this.hobbies.user_hobbies.push(hobby)
        },
        deleteHobby(hobby : UserHobby) {
            this.hobbies.user_hobbies = this.hobbies.user_hobbies.filter(myHobby => myHobby !== hobby)
        },
    }
})