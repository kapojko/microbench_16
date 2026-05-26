# Task: `rs_arena_graph_storage`

Repair the arena-backed graph in `src/lib.rs`.

## Requirements

- `insert_child` must return `None` for an invalid parent id.
- Successful `insert_child` calls must wire parent and child consistently.
- `path_to_root(id)` must return ids in **root-to-leaf** order.
- `descendants_bfs(root)` must return descendants in **BFS order**, excluding the root itself.
- `NodeId` values must remain stable after insertion.

## Visible Check

Run:

```bash
cargo test --test visible_smoke
```
