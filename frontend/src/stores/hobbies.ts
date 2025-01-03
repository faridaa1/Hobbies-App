import { defineStore } from 'pinia'
import { Hobby } from '../types'

export const useHobbiesStore = defineStore('hobbies', {
    state: (): { hobbies: Hobby[] } => ({
        hobbies: []
    }),
    actions: {
        addHobby(hobby: Hobby) {
            this.hobbies.push(hobby)
        }, 
        setHobbies(hobbies: Hobby[]) {
            this.hobbies = hobbies;
        }
    }
})