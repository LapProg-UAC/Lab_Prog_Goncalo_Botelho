from node_asc_gen_tree import NodeAscGenTree

class AscGenTree:
    """
    A class representing an ascending genealogical (binary) tree.
    
    Attributes:
        _root (NodeAscGenTree): The root node of the tree.
    """

    def __init__(self, node: NodeAscGenTree = None):
        """
        Initializes the tree with an optional root node.

        Args:
            node (NodeAscGenTree, optional): The root node. Defaults to None.
        """
        self._root = node

    def get_root(self) -> NodeAscGenTree:
        """
        Retrieves the root node of the tree.

        Returns:
            NodeAscGenTree: The root node.
        """
        return self._root

    def set_root(self, node: NodeAscGenTree):
        """
        Sets the root node of the tree.

        Args:
            node (NodeAscGenTree): The new root node.
        """
        self._root = node

    def find_person(self, current_node: NodeAscGenTree, target_name: str):
        """
        Recursively searches for a person in the tree by their name.

        Args:
            current_node (NodeAscGenTree): The starting node for the search.
            target_name (str): The name of the person to find.

        Returns:
            NodeAscGenTree: The node containing the person, or None if not found.
        """
        if current_node is None:
            return None
        if current_node.get_name() == target_name:
            return current_node
        
        found_mother = self.find_person(current_node.get_mother(), target_name)
        if found_mother:
            return found_mother
            
        return self.find_person(current_node.get_father(), target_name)

    def add_parents(self, child_name: str, mother_name: str, father_name: str) -> bool:
        """
        Adds both mother and father to an existing person in the tree.
        Ensures no nodes of degree 1 are created.

        Args:
            child_name (str): The name of the child already in the tree.
            mother_name (str): The name of the mother to add.
            father_name (str): The name of the father to add.

        Returns:
            bool: True if parents were successfully added, False otherwise.
        """
        child_node = self.find_person(self._root, child_name)
        if child_node:
            if child_node.get_mother() is None and child_node.get_father() is None:
                child_node.set_mother(NodeAscGenTree(mother_name))
                child_node.set_father(NodeAscGenTree(father_name))
                return True
        return False

    def load_from_file(self, file_path: str):
        """
        Builds the tree by reading data from a text file.
        Each line should follow the format: Person, Mother, Father.

        Args:
            file_path (str): The path to the text file.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            data = line.strip().split(',')
            if len(data) == 3:
                person, mother, father = data[0].strip(), data[1].strip(), data[2].strip()
                
                if self._root is None:
                    self._root = NodeAscGenTree(person)
                
                self.add_parents(person, mother, father)

    def get_parents(self, person_name: str) -> tuple:
        """
        Retrieves the names of a person's parents.

        Args:
            person_name (str): The name of the person whose parents are being searched.

        Returns:
            tuple: A tuple containing (Mother's Name, Father's Name), or None if not found.
        """
        node = self.find_person(self._root, person_name)
        if node and node.get_mother() and node.get_father():
            return (node.get_mother().get_name(), node.get_father().get_name())
        return None

    def get_ancestors(self, person_name: str, degree: int, side: str) -> list:
        """
        Retrieves a list of ancestors for a given degree and family side.

        Args:
            person_name (str): The name of the starting person.
            degree (int): The degree of ancestry (e.g., 1 for parents, 2 for grandparents).
            side (str): The family side to search ('maternal' or 'paternal').

        Returns:
            list: A list of ancestor names matching the criteria.
        """
        node = self.find_person(self._root, person_name)
        if not node or degree < 1 or degree > 4:
            return []

        if side.lower() == 'maternal':
            return self._collect_degree_recursive(node.get_mother(), degree - 1)
        elif side.lower() == 'paternal':
            return self._collect_degree_recursive(node.get_father(), degree - 1)
        return []

    def _collect_degree_recursive(self, node: NodeAscGenTree, remaining_degree: int) -> list:
        """
        Helper method to recursively collect ancestors at a specific depth.

        Args:
            node (NodeAscGenTree): The current node in the traversal.
            remaining_degree (int): The remaining depth to traverse.

        Returns:
            list: A list of ancestor names found at the target depth.
        """
        if node is None:
            return []
        
        if remaining_degree == 0:
            return [node.get_name()]
            
        ancestors = []
        ancestors.extend(self._collect_degree_recursive(node.get_mother(), remaining_degree - 1))
        ancestors.extend(self._collect_degree_recursive(node.get_father(), remaining_degree - 1))
        return ancestors