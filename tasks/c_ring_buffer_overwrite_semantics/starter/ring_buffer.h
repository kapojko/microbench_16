#ifndef RING_BUFFER_H
#define RING_BUFFER_H

#include <stdbool.h>
#include <stddef.h>

typedef struct {
    int *data;
    size_t capacity;
    size_t len;
    size_t head;
} ring_buffer_t;

void rb_init(ring_buffer_t *rb, int *storage, size_t capacity);
size_t rb_len(const ring_buffer_t *rb);
void rb_push(ring_buffer_t *rb, int value);
bool rb_pop_oldest(ring_buffer_t *rb, int *out);
bool rb_peek_oldest(const ring_buffer_t *rb, int *out);
bool rb_peek_newest(const ring_buffer_t *rb, int *out);

#endif
