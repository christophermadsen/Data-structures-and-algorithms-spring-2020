#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <math.h>

#include "list.h"
#define BUF_SIZE 1024

static char buf[BUF_SIZE];

struct config {
    // You can ignore these options until you implement the
    // extra command-line arguments.

    // Set to 1 if -u is specified, 0 otherwise.
    int unique_values;

    // Set to 1 if -d is specified, 0 otherwise.
    int descending_order;

    // Set to 1 if -i is specified, 0 otherwise.
    int insert_intermediate;

    // Set to 1 if -z is specified, 0 otherwise.
    int zip_alternating;
};

int parse_options(struct config *cfg, int argc, char *argv[]) {
    memset(cfg, 0, sizeof(struct config));
    int c;
    while ((c = getopt (argc, argv, "udiz")) != -1) {
        switch (c) {
            case 'u': cfg->unique_values = 1; break;
            case 'd': cfg->descending_order = 1; break;
            case 'i': cfg->insert_intermediate = 1; break;
            case 'z': cfg->zip_alternating = 1; break;
            default:
                      fprintf(stderr, "invalid option: -%c\n", optopt);
                      return 1;
        }
    }
    return 0;
}

// Function makes sure that each token is only an integer.
int validate_token(char *token) {
    size_t len = strlen(token);
    int check;
    for (size_t i = 0; i < len; i++) {
        check = (int)(token[i]);
        if ((check > 47 && check < 58) || check == 10) {
            continue;
        } else {
            return 0;
        }
    }
    return 1;
}

// Performs the insertion sort algorithm on a linked list.
int insertion_sort(struct list *l, int descending_order) {
    if (!list_head(l)){
        list_cleanup(l);
        return 0;
    }

    size_t len = list_length(l);
    for (size_t i = 0; i < len; i++) {
        struct node *n = list_get_ith(l, i);
        struct node *temp = list_prev(l, n);
        while (temp) {

            // Sort descending.
            if (descending_order) {
                if (list_node_value(temp) < list_node_value(n)) {
                    temp = list_prev(l, temp);
                } else {
                    break;
                }

            // Sort ascending.
            } else {
                if (list_node_value(temp) > list_node_value(n)) {
                    temp = list_prev(l, temp);
                } else {
                    break;
                }
            }
        }

        list_unlink_node(l, n);
        if (!temp) {
            list_add_front(l, n);
        } else {
            list_insert_after(l, n, temp);
        }

    }
    return 1;
}

// Compares each nodes value with the values of the rest and removes if equal.
void list_remove_duplicates(struct list *l) {
    struct node *n = list_head(l);
    struct node *check;
    struct node *duplicate;

    while (n && list_next(n)) {
        check = n;

        while (list_next(check)) {
            if (list_node_value(n) == list_node_value(list_next(check))) {
                duplicate = list_next(check);
                list_unlink_node(l, duplicate);
                list_free_node(duplicate);
            } else {
                check = list_next(check);
            }
        }
        n = list_next(n);
    }
}

// Inserts an interpolated value between each adjacent element.
void intermediate_insertion(struct list *l) {
    struct node *n = list_head(l);
    struct node *next;
    float intermediate;
    while (list_next(n)) {
        next = list_next(n);
        intermediate = (float)list_node_value(next) + (float)list_node_value(n);
        intermediate /= 2;
        list_insert_after(l, list_new_node((int)round(intermediate)), n);
        n = next;
    }
}

// Splits into 2 lists, then alternates between elements 1-by-1 in the first list.
void zip_alternation(struct list *l) {
    size_t half = (size_t)round((float)list_length(l)/2);
    struct list *lr = list_cut_after(l, list_get_ith(l, half - 1));

    struct node *n = list_head(lr);
    struct node *index = list_head(l);
    struct node *next, *nexti;
    while (n) {
        next = list_next(n);
        nexti = list_next(index);
        list_unlink_node(lr, n);
        list_insert_after(l, n, index);
        n = next;
        index = nexti;
    }
    list_cleanup(lr);
}

//////////////////////////
// I misundertood certain parts and made these functions, which were not needed.
/////////////////////////

// Reverses a list by unlinking and adding each element to the front.
// void reverse_list(struct list *l) {
//     struct node *n = list_head(l);
//     struct node *next;
//     while (n) {
//         next = list_next(n);
//         list_unlink_node(l, n);
//         list_add_front(l, n);
//         n = next;
//     }
// }

// Checks if input only consists of whitespace.
// int only_whitespace(char *buf) {
//     size_t len = strlen(buf);
//     size_t i = 0;
//     for (; i < len; i++) {
//         if (buf[i] == ' ' || buf[i] == 10) {
//             continue;
//         } else {
//             break;
//         }
//     }
//
//     if (i == len) {
//         return 1;
//     }
//
//     return 0;
// }

/////////////////////////

int main(int argc, char *argv[]) {
    struct config cfg;
    if (parse_options(&cfg, argc, argv) != 0) {
        return 1;
    }

    struct list *l = list_init();
    while (fgets(buf, BUF_SIZE, stdin)) {
        char *token = strtok(buf, " ");
        while(token != NULL && (int)(*token) != 10) {
            int check = validate_token(token);
            if (check) {
                list_add_back(l, list_new_node(atoi(token)));

            } else {
                list_cleanup(l);
                return 1;
            }
            token = strtok(NULL, " ");
        }
    }
    // case 'u'
    if (cfg.unique_values) {
        list_remove_duplicates(l);
    }

    // Also includes case 'd'
    if (!insertion_sort(l, cfg.descending_order)) {
        return 1;
    }

    // case 'i'
    if (cfg.insert_intermediate) {
        intermediate_insertion(l);
    }

    // case 'z'
    if (cfg.zip_alternating) {
        zip_alternation(l);
    }

    // Printing the list.
    struct node *n = list_head(l);
    while(n) {
        fprintf(stdout, "%d\n", list_node_value(n));
        n = list_next(n);
    }

    list_cleanup(l);
    return 0;
}
