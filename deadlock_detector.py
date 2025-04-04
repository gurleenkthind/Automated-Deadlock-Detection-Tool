import networkx as nx

class DeadlockDetector:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_dependency(self, process, resource):
        """Adds a dependency between a process and a resource."""
        self.graph.add_edge(process, resource)

    def release_resource(self, process, resource):
        """Removes a process-resource dependency (resource released)."""
        if self.graph.has_edge(process, resource):
            self.graph.remove_edge(process, resource)

    def detect_deadlock(self):
        """Detects if a deadlock is present in the system."""
        try:
            cycle = nx.find_cycle(self.graph, orientation="original")
            deadlocked_nodes = {node for edge in cycle for node in edge}
            return True, deadlocked_nodes  # Deadlock detected
        except nx.NetworkXNoCycle:
            return False, None  # No deadlock

