import { defineStore } from 'pinia'
import { CustomUser, Friendship, UserHobby } from '../types'

export const useUserStore = defineStore('user', {
    state: (): { user: CustomUser, hobbies: { user_hobbies: UserHobby[] }, csrf: string} => ({
        user: {} as CustomUser,
        hobbies: { user_hobbies: [] },
        csrf: ''
    }),
    actions: {
        saveUser(user: CustomUser) {
            this.user = user
        },
        saveHobbies(hobbies: { user_hobbies: UserHobby[] }) {
            this.hobbies = hobbies
        },
        addHobby(hobby: UserHobby) {
            this.hobbies.user_hobbies.push(hobby)
        },
        deleteHobby(hobby : UserHobby) {
            this.hobbies.user_hobbies = this.hobbies.user_hobbies.filter(myHobby => myHobby.hobby.hobby_id !== hobby.hobby.hobby_id)
        },
        updateFriendship(id: number, isAccepted: boolean) {
            // Accept or delete friendship
            let friendship: Friendship | undefined = this.user.friends.find(fs => fs.id === id) 
            if (friendship) {
                if (isAccepted) {
                    friendship.status = 'Accepted'
                } else {
                    this.user.friends = this.user.friends.filter(fs => fs.id !== id)
                }
            } 
        }
    },
    getters: {
        getFriendship: (state) => {
            return (email: string) => state.user.friends?.find(friendship => friendship.user_email === email)
        },
    }
})