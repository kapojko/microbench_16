use arena_graph::ArenaGraph;

#[test]
fn visible_smoke() {
    let mut graph = ArenaGraph::new();
    let root = graph.insert_root("root");
    let child = graph.insert_child(root, "child").expect("child");
    assert_eq!(graph.parent(child), Some(root));
    assert_eq!(graph.path_to_root(child), Some(vec![root, child]));
}
