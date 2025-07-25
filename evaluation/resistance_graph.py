
import networkx as nx
import matplotlib.pyplot as plt

class ResistanceGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_step(self, from_node, to_node, resistance=1.0):
        self.graph.add_edge(from_node, to_node, resistance=resistance)

    def visualize(self, title="Inference Resistance Graph"):
        pos = nx.spring_layout(self.graph, seed=42)
        edge_labels = nx.get_edge_attributes(self.graph, 'resistance')
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.title(title)
        plt.show()

    def total_resistance(self, path):
        try:
            return sum(self.graph[u][v]['resistance'] for u, v in zip(path, path[1:]))
        except KeyError:
            return float('inf')  # Infinite resistance if any step is missing

    def find_least_resistant_path(self, start, goal):
        try:
            return nx.dijkstra_path(self.graph, source=start, target=goal, weight='resistance')
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []

# Test run
if __name__ == "__main__":
    rg = ResistanceGraph()
    rg.add_step("P(a)", "Q(a)", resistance=1.0)
    rg.add_step("Q(a)", "R(a)", resistance=0.5)
    rg.add_step("P(a)", "R(a)", resistance=2.0)

    print("Least resistant path from P(a) to R(a):", rg.find_least_resistant_path("P(a)", "R(a)"))
    print("Total resistance:", rg.total_resistance(rg.find_least_resistant_path("P(a)", "R(a)")))

    rg.visualize()
