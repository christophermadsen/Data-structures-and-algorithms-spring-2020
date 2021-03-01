#include "list.h"

/*
 * TODO: A lot of code missing here. You will need to add implementations for
 * all the functions described in list.h here.
 *
 * Start by adding the definitions for the list and node structs. You may
 * implement any of the Linked List versions discussed in the lecture, which
 * have some different trade-offs for the functions you will need to write.
 *
 * Note: The function prototypes in list.h assume the most basic Singly Linked
 * List. If you build some other version, you may not need all of the function
 * arguments for all of the described functions. This will produce a warning,
 * which you can suppress by adding a simple if-statement to check the value
 * of the unused parameter.
 *
 * Also, do not forget to add any required includes at the top of your file.
 */

struct node {
    int value;
    struct node *next;
    struct node *prev;
};

// Doubly-linkd list
struct list {
    struct node *head;
    struct node *tail;
};

struct list *list_init(void) {
    struct list *l = malloc(sizeof(struct list));
    if (l) {
        l->head = NULL;
        l->tail = NULL;
        return l;
    } else {
        return NULL;
    }
}

struct node *list_new_node(int num) {
    struct node *n = malloc(sizeof(struct node));
    if (n) {
        n->value = num;
        n->next = NULL;
        n->prev = NULL;
        return n;
    } else {
        return NULL;
    }
}

struct node *list_head(struct list *l) {
    if (l) {
        return l->head;
    } else {
        return NULL;
    }
}

struct node *list_next(struct node *n) {
    if (n) {
        return n->next;
    } else {
        return NULL;
    }
}

int list_add_front(struct list *l, struct node *n) {
    if (l == NULL) {
        return 1;

    // Case where list already has an element.
    } else if (l->head) {
        l->head->prev = n;
        n->next = l->head;
        n->prev = NULL;
        l->head = n;
        return 0;

    // Case where the list is empty.
    } else {
        l->head = n;
        l->tail = n;
        n->next = NULL;
        n->prev = NULL;
        return 0;
    }
}

struct node *list_tail(struct list *l) {
    if (l) {
        return l->tail;
    } else {
        return NULL;
    }
}

struct node *list_prev(struct list *l, struct node *n) {
    // Returns NULL if list is empty or n is the first element.
    if (l->head == n || l->head == NULL) {
        return NULL;

    // Iterates through the list, returns element if previous of n.
    } else {
        struct node *current = l->head;
        while (current) {
            if (current->next == n) {
                return current;
            }
            current = current->next;
        }
        // If node wasn't in the list.
        return NULL;
    }
}

int list_add_back(struct list *l, struct node *n) {
    if (l == NULL || n == NULL) {
        return 1;

    // Case where list already has an element.
    } else if (l->tail) {
        l->tail->next = n;
        n->prev = l->tail;
        n->next = NULL;
        l->tail = n;
        return 0;

    // Case where the list is empty.
    } else {
        l->head = n;
        l->tail = n;
        n->next = NULL;
        n->prev = NULL;
        return 0;
    }
}

int list_node_value(struct node *n) {
    if (n) {
        return n->value;
    } else {
        return 0;
    }
}

int list_unlink_node(struct list *l, struct node *n) {
    if (l && n && list_node_present(l, n)) {
        // Case with list length of 1.
        if (l->head == n && l->tail == n) {
            l->head = NULL;
            l->tail = NULL;

        // Case where node is the tail of the list.
        } else if (l->tail == n) {
            n->prev->next = NULL;
            l->tail = n->prev;

        // Case where node is the head of the list.
        } else if (l->head == n) {
            n->next->prev = NULL;
            l->head = n->next;

        // Case where node is in the middle of the list.
        } else {
            n->prev->next = n->next;
            n->next->prev = n->prev;
        }

        n->next = NULL;
        n->prev = NULL;
        return 0;

    } else {
        return 1;
    }
}

void list_free_node(struct node *n) {
    free(n);
}

int list_cleanup(struct list *l) {
    // Frees each node before freeing list struct.
    if (l) {
        struct node *current = l->head;
        while (current) {
            struct node *next = current->next;
            list_free_node(current);
            current = next;
        }
        free(l);
        return 0;

    } else {
        return 1;
    }
}

int list_node_present(struct list *l, struct node *n) {
    // Iterates over each node in list and checks presence.
    if (l && n) {
        struct node *current = l->head;
        while (current) {
            if (current == n) {
                return 1;
            }
            current = current->next;
        }
    }
    return 0;
}

int list_insert_after(struct list *l, struct node *n, struct node *m) {
    // If n is already present or m is not in the list.
    if (list_node_present(l, n) || !list_node_present(l, m)) {
        return 1;

    } else if (l && n && m) {
        // If m is the tail of the list.
        if (m == l->tail) {
            m->next = n;
            n->prev = m;
            n->next = NULL;
            l->tail = n;
            return 0;

        // If m is in the list.
        } else {
            n->next = m->next;
            n->prev = m;
            m->next->prev = n;
            m->next = n;
            return 0;
        }

    } else {
        return 1;
    }
}

int list_insert_before(struct list *l, struct node *n, struct node *m) {
    // If n is already present or m is not in the list.
    if (list_node_present(l, n) || !list_node_present(l, m)) {
        return 1;

    } else if (l && n && m) {
        // If m is the head of the list.
        if (m == l->head) {
            m->prev = n;
            n->next = m;
            n->prev = NULL;
            l->head = n;
            return 0;

        // If m is in the list.
        } else {
            m->prev->next = n;
            n->prev = m->prev;
            m->prev = n;
            n->next = m;
            return 0;
        }

    } else {
        return 1;
    }
}

size_t list_length(struct list *l) {
    // Iterates through a list and increments a counter for each element.
    if (l) {
        size_t len = 0;
        struct node *current = l->head;
        while (current) {
            len++;
            current = current->next;
        }
        return len;
    } else {
        return 0;
    }
}

struct node *list_get_ith(struct list *l, size_t i) {
    if (l && (list_length(l) > i)) {
        struct node *current = l->head;

        if (i == 0) {
            return current;
        }

        while (i) {
            current = current->next;
            i--;
        }

        return current;

    } else {
        return NULL;
    }


    // Gets the next node i times, starting from list head.
    // if (l && (list_length(l) > i)) {
    //     struct node *current = l->head;
    //     for (size_t j = 0; j == i; j++) {
    //         current = current->next;
    //     }
    //     return current;
    // } else {
    //     return NULL;
    // }
}

struct list *list_cut_after(struct list *l, struct node *n) {
    if (l && n) {
        // If the node is the tail of the list, treat as fail.
        if (n == l->tail) {
            return NULL;

        //
        } else {
            struct list *lr = list_init();
            lr->head = n->next;
            lr->tail = l->tail;
            lr->head->prev = NULL;
            l->tail = n;
            n->next = NULL;
            return lr;
        }

    } else {
        return NULL;
    }
}
