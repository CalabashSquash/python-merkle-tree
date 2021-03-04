import hashlib


class MerkleTreeNode:
    def __init__(self, inp):
        self.data = hashlib.sha256(inp)
        self.l_parent = None
        self.r_parent = None
        self.child = None

    def __str__(self):
        return self.data


class MerkleTree:
    def __init__(self):
        self.leaves = []
        self.root_node = None
        self.nodes = {}
        self.node_count = 0

    def build_tree(self, nodes, is_top_level, current_index):
        if is_top_level:
            if not len(nodes) % 2:
                self.node_count = len(nodes) * 2 - 1
            else:
                self.node_count = len(nodes) * 2

        if len(nodes) <= 0:
            return
        if len(nodes) == 1:
            if is_top_level:
                self.root_node = MerkleTreeNode(nodes[0])
            else:
                self.root_node = nodes[0]
            self.nodes[self.node_count - current_index] = self.root_node
            return
        n = len(nodes)
        hashes = []
        for i in range(0, n, 2):
            if i == n - 1:  # last elem
                if is_top_level:
                    # print(f"Child {nodes[i]} produces ...")
                    left = MerkleTreeNode(nodes[i])
                    self.leaves.append(left)
                    self.nodes[self.node_count - current_index] = left
                    current_index = current_index + 1
                else:
                    # print(f"Child {nodes[i].data.digest()} produces ...")
                    left = nodes[i]
                input_bytes = left.data.digest()

                new_parent = MerkleTreeNode(input_bytes)
                new_parent.l_parent = left
                left.child = new_parent
                hashes.append(new_parent)
                self.nodes[self.node_count - current_index] = new_parent
                current_index = current_index + 1
                # print(f"... parent {new_parent.data.digest()}.")
            else:
                if is_top_level:
                    # print(f"Children {nodes[i]} and {nodes[i + 1]} produce ...")
                    left = MerkleTreeNode(bytes(nodes[i]))
                    right = MerkleTreeNode(bytes(nodes[i + 1]))
                    self.leaves.append(left)
                    self.leaves.append(right)
                    self.nodes[self.node_count - current_index] = left
                    current_index = current_index + 1
                    self.nodes[self.node_count - current_index] = right
                    current_index = current_index + 1
                else:
                    # print(f"Children {nodes[i].data.digest()} and {nodes[i + 1].data.digest()} produce ...")
                    left = nodes[i]
                    right = nodes[i + 1]
                input_bytes = left.data.digest() + right.data.digest()

                new_parent = MerkleTreeNode(input_bytes)

                new_parent.l_child = left
                new_parent.r_child = right
                left.parent = new_parent
                right.parent = new_parent
                print("HI")
                print(left.data.digest())
                print(right.data.digest())
                print(self.node_count - current_index)

                hashes.append(new_parent)
                self.nodes[self.node_count - current_index] = new_parent
                current_index = current_index + 1
                # print(f"... parent {new_parent.data.digest()}.")
        return self.build_tree(hashes, False, current_index)

    def check_equality(self, other_tree):
        return other_tree.root


def check_equality(leaves1, leaves2):
    merk = MerkleTree()
    merk.build_tree(leaves1, True, 1)
    merk2 = MerkleTree()
    merk2.build_tree(leaves2, True, 1)

    return merk.root_node.data.digest() == merk2.root_node.data.digest()


def check_membership_known_index(member, tree, minimum_required_nodes, index):
    """
     Currently only works for checking membership of a leaf node, whose index is known
    """
    member_node = MerkleTreeNode(bytes(member))
    while index > 0:
        if index % 2:  # even. We want the node to the right
            neighbour = minimum_required_nodes[index - 1]
        else:
            neighbour = minimum_required_nodes[index + 1]
        member_node = MerkleTreeNode(member_node.data.digest() + neighbour.data.digest())
        index = index // 2 - 1
    return tree.root_node == member_node


merky = MerkleTree()
print(hashlib.sha256(bytes(1)).digest())
print(hashlib.sha256(bytes(2)).digest())
print((hashlib.sha256(hashlib.sha256(bytes(1)).digest() + hashlib.sha256(bytes(2)).digest())).digest())
# print((hashlib.sha256(hashlib.sha256(bytes(5)).digest() + hashlib.sha256(bytes(6)).digest())).digest())
merky.build_tree([1, 2, 5, 6], True, 1)
print("=======================")
print(merky.nodes[6].data.digest())
print(merky.nodes[5].data.digest())
print(merky.nodes[0].data.digest())
print(merky.nodes[1].data.digest())
print(merky.nodes[2].data.digest())
print(merky.root_node.data.digest())

merky2 = MerkleTree()
merky2.build_tree([1, 2, 5, 7], True, 1)
print("=======================")
print(merky2.root_node.data.digest())
print(merky2.nodes[0].data.digest())

print(check_equality([1, 2, 3, 4], [1, 2, 3, 4]))
print(check_equality([1, 6, 3, 4], [1, 2, 3, 4]))

indices = merky.nodes
print(check_membership_known_index(1, merky, [indices[5], indices[1]], 6))
