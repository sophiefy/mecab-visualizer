import graphviz

from .tagger import MecabTagger
from .utils import draw_graph, draw_graph_nbest


class MecabVisualizer(object):
    def __init__(self) -> None:
        """Initialize.
        """

        self.tagger = MecabTagger()

    def draw_graph(self, text: str, rankdir: str="LR", color: str="black") -> object:
        """Draw graph.

        Args:
            text (str): Input text.
            rankdir (str, optional): Direction. Defaults to "LR".
            color (str, optional): Color. Defaults to "black".

        Returns:
            object:  Digraph object.
        """

        # create graph
        graph = graphviz.Digraph()
        graph.attr(rankdir=rankdir)

        # get features
        features = self.tagger.parse(text)

        # draw graph
        draw_graph(features, graph, color=color)

        return graph
    
    def draw_graph_nbest(self, text: str, num: int=3, rankdir: str="LR", color: str="black") -> object:
        """Draw graph (N best).

        Args:
            text (str): Input text.
            num (int, optional): N. Defaults to 3.
            rankdir (str, optional): Direction. Defaults to "LR".
            color (str, optional): Color. Defaults to "black".

        Returns:
            object: Digraph object.
        """

        # create graph
        graph = graphviz.Digraph()
        graph.attr(rankdir=rankdir)

        # get features
        features_list = self.tagger.parse_nbest(text, num=num)

        # draw graph
        draw_graph_nbest(features_list, graph, color=color)

        return graph
    
    @staticmethod
    def save_graph(graph: object, filename: str, directory: str):
        """Save graph.

        Args:
            graph (object): Digraph object.
            filename (str): File name.
            directory (str): Saving directory.
        """

        # FIXME: other format like "png" will result corrupted characters.
        graph.render(filename=filename, directory=directory, format="svg")
        
        


