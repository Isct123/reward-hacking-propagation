import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from topologies import build_network, stable_seed, visible_agent_ids


class TopologyTests(unittest.TestCase):
    def test_seed_is_process_stable(self):
        self.assertEqual(stable_seed(20260804, "lcbhard_0", 1, "queue"), stable_seed(20260804, "lcbhard_0", 1, "queue"))

    def test_full_mesh_visibility(self):
        net = build_network("mesh_full", 6, random.Random(1))
        self.assertEqual(visible_agent_ids(net, 0, None), {1, 2, 3, 4, 5})

    def test_leaf_seed_has_parent(self):
        net = build_network("static_hierarchy_leaf", 6, random.Random(1))
        self.assertIsNotNone(net.parent[0])
        self.assertIn(net.parent[0], visible_agent_ids(net, 0, None))

    def test_random_mesh_connected(self):
        net = build_network("mesh_random", 6, random.Random(7))
        seen, frontier = {0}, [0]
        while frontier:
            node = frontier.pop()
            for other in net.neighbours(node):
                if other not in seen:
                    seen.add(other); frontier.append(other)
        self.assertEqual(len(seen), 6)


if __name__ == "__main__":
    unittest.main()
