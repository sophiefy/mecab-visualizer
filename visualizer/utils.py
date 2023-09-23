FEATURE_KEYS = ["pos1", "pos2", "pos3", "pos4", "goshu"]

def draw_graph(features: list, graph: object, rank: int=1, color: str="black"):
    """Draw graph according to a list of features.

    Args:
        features (list): List of features.
        graph (object): Digraph object.
        rank (int, optional): Rank of this result.
        color (str, optional): Color. Defaults to "black".
    """

    N = len(features)
    for i in range(N-1):
        feature = features[i]
        node_name, node_cost = add_node(i, feature, graph, rank=rank, color=color)

        # calculate the cost of edge
        node_wcost_next = features[i+1]["word_cost"]
        node_cost_next = features[i+1]["cost"]
        edge_cost = int(node_cost_next) - int(node_cost) - int(node_wcost_next)
        edge_cost = str(edge_cost)

        # add edge to graph
        node_name_next = "node_{}_{}".format(rank, i+1)
        graph.edge(node_name, node_name_next, edge_cost, color=color)

    # handling EOS
    feature = features[N-1]
    add_node(N-1, feature, graph, rank=rank, color=color)

def draw_graph_nbest(features_list: list, graph: object, color: str="black"):
    """Draw graph according to the best N results.

    Args:
        features_list (list): Features list.
        graph (object): Digraph object.
        color (str, optional): Color. Defaults to "black".
    """

    for rank, features in enumerate(features_list):
        draw_graph(features, graph, rank=rank, color=color)

def add_node(index: int, feature: dict, graph: object, rank: int=1, color: str="black") -> tuple:
    """Add a node to graph.

    Args:
        index (int): Index of this node.
        feature (dict): Feature dict.
        graph (object): Digraph object.
        rank (int, optional): Rank of the result this node belong to.
        color (str, optional): Color. Defaults to "black".

    Returns:
        tuple: Name of this node and its cumulative cost.
    """

    # each feature dict reqresents a node
    node_surface = feature["surface"]
    node_wcost = feature["word_cost"]
    node_cost = feature["cost"]
    node_pron = feature["pron"]
    if node_pron == "*":
      node_pron = ""

    node_feature = []
    for key in FEATURE_KEYS:
        feat = feature[key]
        # TODO: maybe not necessary?
        if feat != "*":
            node_feature.append(feat)
    node_feature = ",".join(node_feature)

    # add node to graph
    node_name = "node_{}_{}".format(rank, index)
    node_label = "{}\n{}\n{}\n{}".format(node_surface, node_pron, node_feature, node_wcost)
    graph.node(node_name, node_label, color=color)

    return node_name, node_cost

