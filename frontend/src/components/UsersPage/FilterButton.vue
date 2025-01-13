<template>
    <div>
        <div class="main_bar">
            <div class="bar"></div>
            <div id="min_age" class="min_age" @mousedown="(event) => getMousePosition(event, 'min')">
                <p class="age">{{ min }}</p>
            </div>
            <div id="max_age" class="max_age" @mousedown="(event) => getMousePosition(event, 'max')" @mouseup="dragMax=false">
                <p class="age">{{ max }}</p>
            </div>
        </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    emits: ['changeMinAge', 'changeMaxAge'],
    data(): {currentMinMousePosition: number, 
        currentMaxMousePosition: number, 
        dragMin: boolean, 
        dragMax: boolean,
        minMouseMoveHandler: (event: MouseEvent) => void,
        minMouseUpHandler: () => void,
        maxMouseMoveHandler: (event: MouseEvent) => void
        maxMouseUpHandler: () => void,
    } { 
        return {
            currentMinMousePosition: 0,
            currentMaxMousePosition: 0,
            dragMin: false,
            dragMax: false,
            minMouseMoveHandler: (event: MouseEvent) => this.changeAge(event, 'min'),
            minMouseUpHandler: () => this.mouseUp('min'),
            maxMouseUpHandler: () => this.mouseUp('max'),
            maxMouseMoveHandler: (event: MouseEvent) => this.changeAge(event, 'max')
        }
    },
    props: {
        min: Number,
        max: Number
    },
    methods: {
        mouseUp(range: string): void {
            if (range === 'min') {
                this.dragMin = false
                window.removeEventListener('mousemove', this.minMouseMoveHandler)
                window.removeEventListener('mouseup', this.minMouseUpHandler)
            } else {
              this.dragMax = false
              window.removeEventListener('mousemove', this.maxMouseMoveHandler)
              window.removeEventListener('mouseup', this.maxMouseUpHandler)
            }
        },
        getMousePosition(event: MouseEvent, range: string): void {
            if (range === 'min') {
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
                if (element) {
                    let elementVal = range === 'min' ? element.style.left : element.style.right
                    let currentPos: number = parseFloat(elementVal.replace("pxrem","")) || 0
                    let mousePos = range === 'min' ? this.currentMinMousePosition : this.currentMaxMousePosition
                    if (mousePos < event.clientX) {
                        if (this.min && this.max && this.min === this.max) return
                        if (range === 'min') {
                            element.style.left = (currentPos + 0.125)+"rem"
                        } else {
                            if (this.max && this.max < 100) {
                                element.style.right = (currentPos - 0.125)+"rem"
                            } else {
                                return
                            }
                        }
                        this.$emit(range === 'min' ? 'changeMinAge' : 'changeMaxAge', 1)
                    } else if (this.currentMinMousePosition > event.clientX){
                        if (range === 'min') {
                            if (this.min && this.min > 0) {
                                element.style.left = (currentPos - 0.125)+"rem"
                            } else {
                                return
                            }
                        } else {
                            element.style.right = (currentPos + 0.125)+"rem"
                        }
                        this.$emit(range === 'min' ? 'changeMinAge' : 'changeMaxAge', -1)
                    }
                } 
                if (range === 'min') {
                    this.currentMinMousePosition = event.clientX
                } else {
                    this.currentMaxMousePosition = event.clientX
                }                  
            }
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
    }

    .age {
        position: absolute;
        margin-top: 1.7rem;
    }

</style>
  