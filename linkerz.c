 #include <stdio.h>
#include <stdlib.h>

typedef struct Noderz node;

typedef struct Noderz {
  int num;
  node *next;
 } node; 

node head = NULL; 

node alloc_node(int data, node *head){
  node new = malloc(sizeof(node));
  if (!new) {
    printf("error allocating memory")
    return;
  }
  new.num = data;
  new.next = &head;
  return new;
  
  
