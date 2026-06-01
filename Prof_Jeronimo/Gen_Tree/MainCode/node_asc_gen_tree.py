class NodeAscGenTree:
    """
    A class representing a node in an ascending genealogical binary tree.
    
    Attributes:
        _name (str): The name of the person.
        _mother (NodeAscGenTree): Reference to the mother's node.
        _father (NodeAscGenTree): Reference to the father's node.
    """

    def __init__(self, val: str):
        """
        Initializes the node with a person's name.

        Args:
            val (str): The name of the person.
        """
        self._name: str = val
        self._mother = None
        self._father = None

    def get_name(self) -> str:
        """
        Retrieves the name of the person in this node.

        Returns:
            str: The person's name.
        """
        return self._name

    def get_mother(self):
        """
        Retrieves the mother's node.

        Returns:
            NodeAscGenTree: The mother's node, or None if not set.
        """
        return self._mother

    def get_father(self):
        """
        Retrieves the father's node.

        Returns:
            NodeAscGenTree: The father's node, or None if not set.
        """
        return self._father

    def set_mother(self, node):
        """
        Sets the mother's node.

        Args:
            node (NodeAscGenTree): The node representing the mother.
        """
        self._mother = node

    def set_father(self, node):
        """
        Sets the father's node.

        Args:
            node (NodeAscGenTree): The node representing the father.
        """
        self._father = node