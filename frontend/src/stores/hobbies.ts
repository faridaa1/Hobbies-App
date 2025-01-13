import { defineStore } from 'pinia'
import { Hobby } from '../types'

export const useHobbiesStore = defineStore('hobbies', {
    state: (): { hobbies: Hobby[] } => ({
        hobbies: []
    }),
    actions: {
        addHobby(hobby: Hobby): void {
            this.hobbies.push(hobby)
        }, 
        setHobbies(hobbies: Hobby[]): void {
            this.hobbies = hobbies;
        }
    }
})