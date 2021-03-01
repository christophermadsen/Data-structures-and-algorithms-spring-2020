#include <stdlib.h>
#include <stdio.h>

#include "array.h"

struct array {
    int *elements; // The integer elements of the array.
    unsigned long tail; // The index AFTER the last array element.
    unsigned long capacity; // The memory capacity of the array.
};

struct array *array_init(unsigned long initial_capacity) {
    struct array *a = malloc(sizeof(struct array));
    a->elements = malloc(initial_capacity * sizeof(int));
    a->capacity = initial_capacity;
    a->tail = 0;
    if (a == NULL || a->elements == NULL) {
        return NULL;
    }
    return a;
}

void array_cleanup(struct array *a) {
    free(a->elements);
    free(a);
}

int array_get(struct array *a, unsigned long index) {
    if (a == NULL) {
        return -1;
    }
    // Case where index is out of bounds or array is empty.
    if (a->tail <= index || a->tail == 0) {
        return -1;
    }
    return a->elements[index];
}

/* Note: Although this operation might require the array to be resized and
 * copied, in order to make room for the added element, it is possible to do
 * this in such a way that the amortized complexity is still O(1).
 * Make sure your code is implemented in such a way to guarantee this. */
int array_append(struct array *a, int elem) {
    if (a == NULL) {
        return 1;

    // Case where array is full.
    } else if (a->tail == a->capacity) {
        a->capacity++;
        a->elements = realloc(a->elements, a->capacity * sizeof(int));
    }

    a->tail++;
    a->elements[a->tail - 1] = elem;
    return 0;
}

unsigned long array_size(struct array *a) {
    return a->tail;
}
