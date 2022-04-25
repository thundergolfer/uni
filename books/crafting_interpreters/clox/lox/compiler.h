#ifndef clox_compiler_h
#define clox_compiler_h

#include "object.h"
#include "vm.h"
#include "chunk.h"

bool compile(const char* source, Chunk* chunk);

#endif
