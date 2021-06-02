#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

/**
 * ⚠️ I am garbage at C code. Haven't written it in years. This is likely awful.
**/

const int ALPHABET_LEN = 26;

typedef struct Node Node;  // declare 'struct Node' as 'Node'

struct Node {
    int terminal;
    Node* children[ALPHABET_LEN];
};

typedef struct {
    Node* root;
} Trie;

Node* create_new_trie_node() {
    Node* node = (Node*)malloc (sizeof(Node));
    node->terminal = false;

    for (int i = 0; i < ALPHABET_LEN; i++) {
        node->children[i] = NULL;
    }
    return node;
}

void insert(Trie* trie, char* word) {
    Node* curr;

    curr = trie->root;

    while (*word) {
        if (curr->children[*word - 'a'] == NULL) {
            curr->children[*word - 'a'] = create_new_trie_node();
        }
        curr = curr->children[*word - 'a'];
        word++;
    }
    curr->terminal = true;
}

int main(int argc, char *argv[]) {
    printf("Testing trie implementation\n");

    Trie *t;

    t = malloc (sizeof (Trie));
    t->root = create_new_trie_node();

    char word[] = "apple";

    insert(t, word);

    // TODO(Jonathon): Implement search/includes/delete

    return 0;
}
