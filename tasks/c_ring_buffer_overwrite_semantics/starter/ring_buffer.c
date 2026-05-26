#include "ring_buffer.h"

void rb_init(ring_buffer_t *rb, int *storage, size_t capacity) {
    rb->data = storage;
    rb->capacity = capacity;
    rb->len = 0;
    rb->head = 0;
}

size_t rb_len(const ring_buffer_t *rb) {
    return rb->len;
}

void rb_push(ring_buffer_t *rb, int value) {
    if (rb->capacity == 0) {
        return;
    }

    size_t tail = (rb->head + rb->len) % rb->capacity;
    rb->data[tail] = value;

    if (rb->len == rb->capacity) {
        // BUG: overwriting the oldest element should advance head, not grow len.
        rb->len += 1;
    } else {
        rb->len += 1;
    }
}

bool rb_pop_oldest(ring_buffer_t *rb, int *out) {
    if (rb->len == 0) {
        return false;
    }
    *out = rb->data[rb->head];
    rb->head = (rb->head + 1) % rb->capacity;
    rb->len -= 1;
    return true;
}

bool rb_peek_oldest(const ring_buffer_t *rb, int *out) {
    if (rb->len == 0) {
        return false;
    }
    *out = rb->data[rb->head];
    return true;
}

bool rb_peek_newest(const ring_buffer_t *rb, int *out) {
    if (rb->len == 0) {
        return false;
    }
    size_t newest = (rb->head + rb->len) % rb->capacity;
    *out = rb->data[newest];
    return true;
}
