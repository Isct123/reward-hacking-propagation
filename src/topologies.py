"""Frozen six-agent topology and visibility implementation."""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

MESH_EDGE_PROB = 0.45
HIERARCHY_BRANCHING = 2


def stable_seed(*parts: object) -> int:
    payload = "||".join(str(part) for part in parts).encode("utf-8")
    return int.from_bytes(hashlib.blake2b(payload, digest_size=8).digest(), "big")


@dataclass
class Network:
    topology: str
    n_agents: int
    edges: Set[Tuple[int, int]]
    parent: Dict[int, Optional[int]] = field(default_factory=dict)

    def neighbours(self, agent_id: int) -> List[int]:
        return sorted({hi if lo == agent_id else lo for lo, hi in self.edges if agent_id in (lo, hi)})


def _connected(edges: Set[Tuple[int, int]], n_agents: int) -> bool:
    seen, frontier = {0}, [0]
    while frontier:
        node = frontier.pop()
        for edge in edges:
            if node not in edge:
                continue
            other = edge[1] if edge[0] == node else edge[0]
            if other not in seen:
                seen.add(other)
                frontier.append(other)
    return len(seen) == n_agents


def build_network(topology: str, n_agents: int, rng: random.Random) -> Network:
    parent: Dict[int, Optional[int]] = {}
    if topology == "mesh_full":
        edges = {(i, j) for i in range(n_agents) for j in range(i + 1, n_agents)}
    elif topology == "mesh_random":
        edges: Set[Tuple[int, int]] = set()
        for _ in range(200):
            candidate = {(i, j) for i in range(n_agents) for j in range(i + 1, n_agents) if rng.random() < MESH_EDGE_PROB}
            if _connected(candidate, n_agents):
                edges = candidate
                break
        if not edges:
            order = list(range(n_agents)); rng.shuffle(order)
            edges = {(min(order[i - 1], order[i]), max(order[i - 1], order[i])) for i in range(1, n_agents)}
    elif topology in ("static_hierarchy_root", "static_hierarchy_leaf"):
        order = list(range(n_agents))
        if topology == "static_hierarchy_leaf":
            order = order[1:] + [0]
        edges = set()
        for index in range(1, n_agents):
            child, boss = order[index], order[(index - 1) // HIERARCHY_BRANCHING]
            edges.add((min(child, boss), max(child, boss)))
            parent[child] = boss
        parent[order[0]] = None
    elif topology == "dynamic_authority":
        edges = set()
    else:
        raise ValueError(topology)
    return Network(topology, n_agents, edges, parent)


def visible_agent_ids(network: Network, agent_id: int, leader_id: Optional[int]) -> Set[int]:
    if network.topology == "dynamic_authority":
        if leader_id is None:
            return set()
        return set(range(network.n_agents)) - {agent_id} if agent_id == leader_id else {leader_id}
    if network.topology.startswith("static_hierarchy_"):
        seen: Set[int] = set()
        node = network.parent.get(agent_id)
        while node is not None:
            seen.add(node); node = network.parent.get(node)
        seen.update(child for child, boss in network.parent.items() if boss == agent_id)
        return seen
    return set(network.neighbours(agent_id))


def dynamic_leader(pass_history: Dict[int, List[bool]], leader_rank: Dict[int, int]) -> int:
    scores = {i: sum(history[-2:]) + 0.01 * len(history) for i, history in pass_history.items()}
    best = max(scores.values())
    return min((i for i, score in scores.items() if score == best), key=lambda i: leader_rank[i])
