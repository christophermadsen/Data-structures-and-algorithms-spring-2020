#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "array.h"
#include "hash_table.h"

struct table {
    // The (simple) array used to index the table
    struct node **array;
    // The function used for computing the hash values in this table
    unsigned long (*hash_func)(unsigned char *);

    // Maximum load factor after which the table array should be resized
    double max_load;
    // Capacity of the array used to index the table
    unsigned long capacity;
    // Current number of elements stored in the table
    unsigned long load;
};

/* Note: This struct should be a *strong* hint to a specific type of hash table
 * You may implement other options, if you can build them in such a way they
 * pass all tests. However, the other options are generally harder to code. */
struct node {
    // The string of characters that is the key for this node
    char *key;
    // A resizing array, containing the all the integer values for this key
    struct array *value;

    // Next pointer
    struct node *next;
};

// ... SOME CODE MISSING HERE ...

// Function to initialize a node struct.
struct node *node_init(unsigned long initial_capacity, char *key) {
    struct node *n = malloc(sizeof(struct node));
    struct array *a = array_init(initial_capacity);

    if (n == NULL || a == NULL) {
        return NULL;
    }

    n->key = key;
    n->next = NULL;
    n->value = a;
    return n;
}

struct table *table_init(unsigned long capacity,
                         double max_load,
                         unsigned long (*hash_func)(unsigned char *)) {

    // Init table, exit with NULL if it fails.
    struct table *t = malloc(sizeof(struct table));
    if (t == NULL) {
        return NULL;
    }

    // Init node array, exit with NULL if it fails.
    t->array = calloc(capacity, sizeof(struct node));
    if (t->array == NULL) {
        return NULL;
    }

    // Init values and hash function in table struct, then return table.
    t->capacity = capacity;
    t->max_load = max_load;
    t->hash_func = hash_func;
    t->load = 0;
    return t;
}

int table_insert(struct table *t, char *key, int value) {
    if (t == NULL) {
        return 1;
    }

    // Applies hash function and translates it (with modulor)
    unsigned long hash = t->hash_func((unsigned char *)(key)) % t->capacity;

    // Allocating memory for the node
    // struct node *n = malloc(sizeof(struct node));
    struct node *n = node_init(1, key);
    if (n == NULL) {
        return 1;
    }

    // Append value to node/key.
    array_append(n->value, value);

    // Case where node needs to be linked.
    if (t->array[hash]) {
        struct node *link = t->array[hash];

        if (link == NULL) {
            return 1;
        }

        while (link->next) {
            if (strcmp(key, link->key) == 0) {
                free(n);
                array_append(link->value, value);
                return 0;
            }
            link = link->next;
        }
        link->next = n;

    // Case where hash is empty.
    } else {
        t->array[hash] = n;
    }
    t->load++;
    return 0;
}

struct array *table_lookup(struct table *t, char *key) {
    // ... SOME CODE MISSING HERE ...
    if (t == NULL) {
        return NULL;
    }

    unsigned long hash = t->hash_func((unsigned char *)(key)) % t->capacity;
    if (t->array[hash]) {
        struct node *link = t->array[hash];
        while (link->next) {
            if (strcmp(key, link->key) == 0) {
                return link->value;
            }
            link = link->next;
        }
        return t->array[hash]->value;
    }
    return NULL;
}


int table_delete(struct table *t, char *key) {
    // ... SOME CODE MISSING HERE ...
}

void table_cleanup(struct table *t) {
    unsigned long check = 0;
    while (check < t->capacity) {
        if (t->array[check]) {
            struct node *current = t->array[check];
            while (current) {
                struct node *next = current->next;
                free(current->value);
                free(current);
                current = next;
         }
     }
        check++;
    }
    free(t->array);
    free(t);
}
