#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#include "stack.h"

// checks if character is an operator
bool isOp(int c) {
    // +, -, *, /, ^, ~, (
    if (c == 43 || c == 45 || c == 42 ||
        c == 47 || c == 94 || c == 126) {

        return true;
    } else {
        return false;
    }
}

// returns the precedence of an operator
int getPrecedence(int op) {
    // +, -
    if (op == 43 || op == 45) {
        return 2;

    // *, /
    } else if ( op == 42 || op == 47) {
        return 3;

    // ^
    } else if (op == 94) {
        return 4;

    // ~
    } else if (op == 126) {
        return 5;

    } else {
        return 0;
    }
}

// returns true if operator 1 has precedence over operator 2, or is the same.
bool comparePrecedence(int operator1, int operator2) {
    int p1 = getPrecedence(operator1);
    int p2 = getPrecedence(operator2);

    // Making sure ^ is right associative.
    if (operator1 == 94 && operator2 == 94) {
        return true;

    } else if (p2 < p1) {
        return true;

    } else {
        return false;
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("usage: %s \"infix_expr\"\n", argv[0]);
        return 1;
    }

    char *input = argv[1];
    struct stack *s = stack_init();
    unsigned long len = strlen(input);
    unsigned long i = 0;
    int stackedOp;

    // iterating while loop over the characters in the input string.
    while (i < len) {
        int token = (int)(input[i]);
        int prev = token;

        if (i > 0) {
            prev = (int)(input[i - 1]);
        }

        // if operator, push to stack in compliance with precedence.
        if (isOp(token)) {

            // push if stack is already empty
            if (stack_empty(s)) {
                stack_push(s, token);
                if (i != 0) {
                    fprintf(stdout, " ");
                }

            } else {

                // while stack is not empty.
                while (!stack_empty(s)) {
                    // pop and print if operator in stack has higher precedence.
                    if (!comparePrecedence(token, stack_peek(s))) {
                        stackedOp = stack_pop(s);
                        fprintf(stdout, " %c", stackedOp);

                        // case where no other operator had lower precedence.
                        if (stack_empty(s)) {
                            stack_push(s, token);
                            fprintf(stdout, " ");
                            break;
                        }

                    // push if operator has highest precedence in the stack.
                    } else {
                        stack_push(s, token);
                        if (!isOp(prev)) {
                            fprintf(stdout, " ");
                        }
                        break;
                    }
                }
            }
            i++;

        // if digit, print immediately.
        } else if (isdigit(token)) {
            fprintf(stdout, "%c", token);
            i++;

        // ignore white space.
        } else if (token == 32) {
            i++;

        // if '(' add to stack and continue
        } else if (token == 40) {
            stack_push(s, token);
            i++;

        // if a ')' then print everything in stack until '(' is encountered.
        } else if (token == 41) {
            bool insideBracket = true;
            while (insideBracket) {
                stackedOp = stack_pop(s);

                if (stackedOp == 40) {
                    insideBracket = false;

                // error code 1 if mismatched closing bracket is present.
                } else if (stack_empty(s)) {
                    return 1;

                } else {
                    fprintf(stdout, " %c", stackedOp);
                }
            }
            i++;

        // error code 1 if an invalid char is encountered.
        } else {
            return 1;
        }
    }

    while (!stack_empty(s)) {
        fprintf(stdout, " %c", stack_peek(s));
        stackedOp = stack_pop(s);

        // error code 1 if mismatched opening bracket present.
        if (stackedOp == 40) {
            return 1;
        }
    }

    printf("\n");
    stack_cleanup(s);
    return 0;
}
