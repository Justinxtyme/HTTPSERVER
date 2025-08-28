#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

#define HEAP_SIZE 4096

typedef struct Chunk {
  size_t size;
  bool free = true;
  Chunk *next; 
} Chunk; 

