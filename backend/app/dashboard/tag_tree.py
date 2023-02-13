class TagTreeNode:
    def __init__(self, slug=None, group='root', children=None):
        self.slug = slug
        self.name = slug
        self.group = group
        if not children:
            children = []
        self.children = children

    def add_child(self, child):
        self.child = child


class TagTree:
    def __init__(self):
        self.root = TagTreeNode()

    @classmethod
    def from_yaml_repr(cls, yaml_repr):
        tree = cls()
        for tag_data in yaml_repr:
            _tree_from_yaml_rec(tree.root, tag_data)

        return tree

    def __eq__(self, other):
        return _nodes_equal_rec(self.root, other.root)

    def get_tags(self):
        return list(_get_tags_rec(self.root))

    def get_nodes(self):
        return _get_node_list_rec(self.root)


def _tree_from_yaml_rec(root, tag_data, group=''):
    if isinstance(tag_data, dict):
        for slug, children in tag_data.items():
            new_group = f'{group}/{slug}' if group else slug
            node = TagTreeNode(slug, new_group)
            root.children.append(node)
            for child in children:
                _tree_from_yaml_rec(node, child, new_group)
    else:
        new_group = f'{group}/{tag_data}' if group else tag_data
        root.children.append(TagTreeNode(tag_data, new_group))


def _nodes_equal_rec(root1, root2):
    if (
        root1.slug != root2.slug
        or root1.group != root2.group
        or len(root1.children) != len(root2.children)
    ):
        return False

    # The order matters for a tag tree
    for child1, child2 in zip(root1.children, root2.children):
        if not _nodes_equal_rec(child1, child2):
            return False

    return True


def _get_tags_rec(root):
    tags = set()
    if root.slug:
        tags.add(root.slug)

    for child in root.children:
        tags |= _get_tags_rec(child)

    return tags


def _get_node_list_rec(root):
    nodes = []
    if root.slug:
        nodes.append(root)

    for child in root.children:
        nodes += _get_node_list_rec(child)

    return nodes
