import { defineStore } from 'pinia'
import { CustomUser, Friendship, UserHobbies, UserHobby } from '../types'

export const useUserStore = defineStore('user', {
    state: () => ({
        user: {} as CustomUser,
        hobbies: {} as UserHobbies,
        csrf: '' as string
    }),
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
            this.hobbies.user_hobbies = this.hobbies.user_hobbies.filter(myHobby => myHobby.hobby.hobby_id !== hobby.hobby.hobby_id)
        },
        updateFriendship(id: number, isAccepted: boolean) {
            let friendship: Friendship | undefined = this.user.friends.find(fs => fs.id === id) 
            if (friendship) {
                if (isAccepted) {
                    friendship.status = 'Accepted'
                } else {
                    this.user.friends = this.user.friends.filter(fs => fs.id !== id)
                }
            } 
        }
    }
})