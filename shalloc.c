#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

#define HEAP_SIZE 4096

typedef struct Chunk {
  size_t size;
  bool free = 1;
  Chunk *next; 
} Chunk; 

char heaperz[HEAP_SIZE];

Chunk *free_head = heaperz;

