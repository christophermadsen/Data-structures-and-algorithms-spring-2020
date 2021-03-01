#include <stdlib.h>
#include <stdio.h>
#include "stack.h"

struct stack {
    int stackarr[STACK_SIZE]; // elements of stack.
    int top; // top index of the stack
    int pushes; // counter for push operations.
    int pops; // counter for pop operations.
    int max; // max size the stack reached.
};

struct stack *stack_init() {
    struct stack *s = malloc(sizeof(struct stack));

    // if pointer s is empty, return NULL, otherwise return s.
    if (s == NULL) {
        return NULL;

    } else {
        s->pushes = 0;
        s->pops = 0;
        s->max = 0;
        s->top = 0;
        return s;
    }
}

void stack_cleanup(struct stack *s) {
    fprintf(stderr, "stats %d %d %d\n", s->pushes, s->pops, s->max); // print stats.
    free(s);
}

int stack_push(struct stack *s, int e) {
    if (s == NULL) {
        return 1;

      // pushes an element to the stack if there is space.
    } else if (s->top < STACK_SIZE) {
          s->top++; // increment top index by 1.
          s->stackarr[s->top - 1] = e; // place int e on top.
          s->pushes++; // increment push counter by 1.

        // check if max stack size has increased and if so, update.
        if (s->top > s->max) {
            s->max = s->top;
        }
          return 0;

    } else {
          return 1;
    }
}

int stack_pop(struct stack *s) {
    if (s == NULL) {
        return -1;

    } else if (s->top > 0) {
        int pop_elem = s->stackarr[s->top - 1]; // element at top.
        s->top--; // decrement top index by 1.
        s->pops++; // increment pop counter by 1.
        return pop_elem; // return element at top.

    } else {
        return -1;
    }
}

int stack_peek(struct stack *s) {
    if (s == NULL) {
        return -1;

    } else if (s->top > 0) {
        return s->stackarr[s->top - 1]; // return top element.
        
    } else {
        return -1;
    }
}

int stack_empty(struct stack *s) {
    if (s == NULL) {
        return -1;

      // if the top index is 0, the stack is empty.
    } else if (s->top == 0) {
        return 1;

    } else {
        return 0;
    }
}
