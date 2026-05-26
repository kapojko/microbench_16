#[derive(Copy, Clone, Debug, Eq, PartialEq, Hash)]
pub struct NodeId(pub usize);

#[derive(Debug)]
struct Node<T> {
    value: T,
    parent: Option<NodeId>,
    children: Vec<NodeId>,
}

#[derive(Debug, Default)]
pub struct ArenaGraph<T> {
    nodes: Vec<Node<T>>,
}

impl<T> ArenaGraph<T> {
    pub fn new() -> Self {
        Self { nodes: Vec::new() }
    }

    pub fn insert_root(&mut self, value: T) -> NodeId {
        let id = NodeId(self.nodes.len());
        self.nodes.push(Node {
            value,
            parent: None,
            children: Vec::new(),
        });
        id
    }

    pub fn insert_child(&mut self, parent: NodeId, value: T) -> Option<NodeId> {
        if self.nodes.get(parent.0).is_none() {
            return None;
        }
        let child_id = NodeId(self.nodes.len());
        self.nodes.push(Node {
            value,
            parent: Some(parent),
            children: Vec::new(),
        });
        // BUG: parent.children is never updated.
        Some(child_id)
    }

    pub fn value(&self, id: NodeId) -> Option<&T> {
        self.nodes.get(id.0).map(|node| &node.value)
    }

    pub fn parent(&self, id: NodeId) -> Option<NodeId> {
        self.nodes.get(id.0).and_then(|node| node.parent)
    }

    pub fn path_to_root(&self, id: NodeId) -> Option<Vec<NodeId>> {
        let mut current = Some(id);
        let mut path = Vec::new();
        while let Some(node_id) = current {
            let node = self.nodes.get(node_id.0)?;
            path.push(node_id);
            current = node.parent;
        }
        // BUG: path is leaf-to-root, but the contract wants root-to-leaf.
        Some(path)
    }

    pub fn descendants_bfs(&self, root: NodeId) -> Option<Vec<NodeId>> {
        if self.nodes.get(root.0).is_none() {
            return None;
        }
        let mut out = Vec::new();
        let mut stack = self.nodes[root.0].children.clone();
        // BUG: this is depth-first because it pops from the end.
        while let Some(node_id) = stack.pop() {
            out.push(node_id);
            if let Some(node) = self.nodes.get(node_id.0) {
                for child in &node.children {
                    stack.push(*child);
                }
            }
        }
        Some(out)
    }
}
