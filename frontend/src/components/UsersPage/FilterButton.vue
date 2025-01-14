<template>
    <div class="d-flex flex-column gap-5">
        <div class="main_bar">
            <div class="bar"></div>
            <div id="min_age" class="min_age" @mousedown="(event) => getMousePosition(event, 'min')">
                <p class="age">{{ min }}</p>
            </div>
            <div id="max_age" class="max_age" @mousedown="(event) => getMousePosition(event, 'max')">
                <p class="age">{{ max }}</p>
            </div>
        </div>
        <div class="d-flex gap-2">
            <button @click="$emit('applyFilter')" class="btn btn-primary">Apply Filter</button>
            <button @click="clearFilter" class="btn btn-danger">Clear Filter</button>
      </div>  
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    emits: ['changeMinAge', 'changeMaxAge', 'applyFilter', 'clearFilter'],
    props: {
        minAge: {
            type: Number,
            required: true
        }, maxAge: {
            type: Number,
            required: true
        }
    },
    data(): {currentMinMousePosition: number, 
        currentMaxMousePosition: number, 
        min: number,
        max: number,
        dragMin: boolean, 
        dragMax: boolean,
        minMouseMoveHandler: (event: MouseEvent) => void,
        minMouseUpHandler: () => void,
        maxMouseMoveHandler: (event: MouseEvent) => void
        maxMouseUpHandler: () => void,
        minimumAge: number,
        maximumAge: number,
        scaleFactor: number,
    } { 
        return {
            currentMinMousePosition: 0,
            currentMaxMousePosition: 0,
            dragMin: false,
            dragMax: false,
            minMouseMoveHandler: (event: MouseEvent) => this.changeAge(event, 'min'),
            minMouseUpHandler: () => this.mouseUp('min'),
            maxMouseUpHandler: () => this.mouseUp('max'),
            maxMouseMoveHandler: (event: MouseEvent) => this.changeAge(event, 'max'),
            min: this.minAge,
            max: this.maxAge,
            minimumAge: this.minAge,
            maximumAge: this.maxAge,
            scaleFactor: 13.3/(this.maxAge-this.minAge)
        }
    },
    methods: {
        clearFilter(): void {
            this.min = this.minimumAge
            this.max = this.maxAge
            let min_element: HTMLElement | null = document.getElementById('min_age')
            let max_element: HTMLElement | null = document.getElementById('max_age')
            if (max_element && min_element) {
                min_element.style.left = '0rem'
                max_element.style.right = '0rem'
            }
            this.$emit('clearFilter')
        },
        mouseUp(range: string): void {
            let element: HTMLElement | null = document.getElementById(range === 'min' ? 'min_age' : 'max_age')
            if (range === 'min') {
                this.dragMin = false
                window.removeEventListener('mousemove', this.minMouseMoveHandler)
                window.removeEventListener('mouseup', this.minMouseUpHandler)
            } else {
                this.dragMax = false
                window.removeEventListener('mousemove', this.maxMouseMoveHandler)
                window.removeEventListener('mouseup', this.maxMouseUpHandler)
            }
            if (element) {
                element.style.backgroundColor = 'rgb(0, 123, 255)'
            }
        },
        getMousePosition(event: MouseEvent, range: string): void {
            let element: HTMLElement | null = document.getElementById(range === 'min' ? 'min_age' : 'max_age')
            if (range === 'min' && element) {
                this.currentMinMousePosition = event.clientX
                this.dragMin = true
                window.addEventListener('mousemove', this.minMouseMoveHandler)
                window.addEventListener('mouseup', this.minMouseUpHandler)
            } else {
                this.currentMaxMousePosition = event.clientX
                this.dragMax = true
                window.addEventListener('mousemove', this.maxMouseMoveHandler)
                window.addEventListener('mouseup', this.maxMouseUpHandler)
            }
        },
        changeAge(event: MouseEvent, range: string): void {
            if (this.dragMin || this.dragMax) {
                let element: HTMLElement | null = document.getElementById(range === 'min' ? 'min_age' : 'max_age')
                let elementB: HTMLElement | null = document.getElementById(range === 'min' ? 'max_age' : 'min_age')
                if (element && elementB) {
                    element.style.backgroundColor = 'darkblue'
                    let elementVal: string = range === 'min' ? element.style.left : element.style.right
                    let currentPos: number = parseFloat(elementVal.replace("pxrem","")) || 0
                    let startMousePosition: number = range === 'min' ? this.currentMinMousePosition : this.currentMaxMousePosition
                    if (startMousePosition < event.clientX) {
                        if (range === 'min' && this.min < this.max) {
                            element.style.left = (currentPos + this.scaleFactor)+"rem"
                            this.min += 1
                            if (this.min === this.max && this.min === this.maxAge) {
                                elementB.style.zIndex = '1'
                                element.style.zIndex = '2'
                            } 
                        } else if (range === 'max' && this.max < this.maxAge) {
                            element.style.right = (currentPos - this.scaleFactor)+"rem"
                            this.max += 1
                        } else return
                        this.$emit(range === 'min' ? 'changeMinAge' : 'changeMaxAge', range === 'min' ? this.min+1 : this.max+1)
                    } else if (startMousePosition > event.clientX){
                        if (range === 'min' && this.min > this.minAge) {
                            element.style.left = (currentPos - this.scaleFactor)+"rem"
                            this.min -= 1
                        } else if (range === 'max' && this.max > this.min) {
                            element.style.right = (currentPos + this.scaleFactor)+"rem"
                            this.max -= 1
                            if (this.min === this.max && this.max === this.minAge) {
                                elementB.style.zIndex = '1'
                                element.style.zIndex = '2'
                            } 
                        } else return
                        this.$emit(range === 'min' ? 'changeMinAge' : 'changeMaxAge', range === 'min' ? this.min-1 : this.min+1)
                    }
                } 
                if (range === 'min') {
                    this.currentMinMousePosition = event.clientX
                } else {
                    this.currentMaxMousePosition = event.clientX
                }                  
            }
        }
    }, watch: {
        minAge(newMinAge) {
            this.minimumAge = newMinAge
            this.min = newMinAge
            this.scaleFactor = 13.3/(this.maxAge-this.minAge)
        }, maxAge(newMaxAge) {
            this.maximumAge = newMaxAge
            this.max = newMaxAge
            this.scaleFactor = 13.3/(this.maxAge-this.minAge)
        }
    }
});
</script>

<style scoped>
    .main_bar {
        height: 0.5rem;
        width: 15rem;
        background-color: lightgray;
        position: relative;
        border-radius: 1rem;
    }

    .bar {
        position: absolute;
        height: 0.5rem;
        width: 15rem;
        background-color: rgb(0, 123, 255);
        border-radius: 1rem;
    }

    .min_age {
        position: absolute;
        background-color: rgb(0, 123, 255);
        height: 1.7rem;
        width: 1.7rem;
        top: 50%;
        transform: translateY(-50%);
        border-radius: 50%;
        display: flex;
        justify-content: center;
    }

    .max_age {
        position: absolute;
        background-color: rgb(0, 123, 255);
        height: 1.7rem;
        width: 1.7rem;
        top: 50%;
        right: 0;
        transform: translateY(-50%);
        border-radius: 50%;
        display: flex;
        justify-content: center;
    }

    .age {
        position: absolute;
        margin-top: 1.7rem;
    }
</style>
  