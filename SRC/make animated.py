import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import networkx as nx
import numpy as np
import os

# Demonstration animation based on the mining-fleet graph from the conversation.
# Routes below are illustrative examples, not solver output.
nodes = {
    "S1": (0, 0, "junction"),
    "S2": (0, 4, "junction"),
    "L1": (2, 1, "load"),
    "L2": (2, 3, "load"),
    "L3": (4, 2, "load"),
    "D1": (7, 1, "dump"),
    "D2": (7, 4, "dump"),
    "A": (1, 1, "junction"),
    "B": (3, 1, "junction"),
    "C": (3, 3, "junction"),
    "E": (5, 3, "junction"),
    "F": (6, 2, "junction"),
}
edges = [
    ("S1","A"), ("A","S1"), ("S2","C"), ("C","S2"),
    ("A","B"), ("B","A"), ("A","C"), ("C","A"),
    ("B","C"), ("C","B"), ("B","F"), ("F","B"),
    ("C","E"), ("E","C"), ("E","F"), ("F","E"),
    ("A","L1"), ("L1","A"), ("C","L2"), ("L2","C"),
    ("B","L3"), ("L3","B"), ("F","D1"), ("D1","F"),
    ("E","D2"), ("D2","E"), ("L1","B"), ("B","L1"),
    ("L2","E"), ("E","L2"), ("L3","F"), ("F","L3"),
    ("B","D1"), ("D1","B"), ("C","D2"), ("D2","C")
]
G = nx.DiGraph()
for n, (x, y, kind) in nodes.items():
    G.add_node(n, pos=(x, y), kind=kind)
G.add_edges_from(edges)
pos = {n: (x, y) for n, (x, y, kind) in nodes.items()}

routes= paths
# Convert routes to polylines and sample them uniformly by edge length.
route_points = {}
for truck, route in routes.items():
    pts = []
    for u, v in zip(route[:-1], route[1:]):
        p1 = np.array(pos[u], dtype=float)
        p2 = np.array(pos[v], dtype=float)
        n_samples = max(2, int(np.linalg.norm(p2-p1) * 12))
        segment = [p1 + (p2-p1)*t for t in np.linspace(0, 1, n_samples, endpoint=False)]
        pts.extend(segment)
    pts.append(np.array(pos[route[-1]], dtype=float))
    route_points[truck] = np.array(pts)

# Use different phase offsets to make motion visible and stagger trucks.
colors = {"Truck_1": "tab:blue", "Truck_2": "tab:orange", "Truck_3": "tab:green"}
fig, ax = plt.subplots(figsize=(11, 6.5))
ax.set_title("Mining fleet movement — illustrative animation (not solver output)", fontsize=13)
ax.set_xlabel("X, m (schematic)")
ax.set_ylabel("Y, m (schematic)")
ax.set_xlim(-0.7, 7.7)
ax.set_ylim(-0.7, 4.7)
ax.set_aspect("equal", adjustable="box")
ax.grid(True, alpha=0.25)

# Draw roads once.
nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray", arrows=True,
                       arrowsize=10, width=1.3, connectionstyle="arc3,rad=0.03")
node_colors = []
for n in G.nodes:
    kind = G.nodes[n]["kind"]
    node_colors.append({"junction": "lightgray", "load": "gold", "dump": "tomato"}[kind])
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=620,
                       edgecolors="black", linewidths=0.8)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=9)

# Legend for node types.
from matplotlib.lines import Line2D
legend_items = [
    Line2D([0], [0], marker='o', color='w', label='Junction', markerfacecolor='lightgray', markeredgecolor='black', markersize=9),
    Line2D([0], [0], marker='o', color='w', label='Loading', markerfacecolor='gold', markeredgecolor='black', markersize=9),
    Line2D([0], [0], marker='o', color='w', label='Dump', markerfacecolor='tomato', markeredgecolor='black', markersize=9),
]
for truck, color in colors.items():
    legend_items.append(Line2D([0], [0], marker='o', color=color, label=truck, markersize=8, linewidth=2))
ax.legend(handles=legend_items, loc="upper left", bbox_to_anchor=(1.01, 1), frameon=True)
plt.tight_layout()

truck_markers = {}
truck_labels = {}
for truck, color in colors.items():
    marker, = ax.plot([], [], marker='o', markersize=12, color=color,
                      markeredgecolor='black', zorder=10)
    label = ax.text(0, 0, "", fontsize=8, weight="bold", color=color,
                    ha="left", va="bottom", zorder=11)
    truck_markers[truck] = marker
    truck_labels[truck] = label

max_frames = 180
def update(frame):
    for idx, truck in enumerate(routes):
        pts = route_points[truck]
        # Stagger starts by 20 frames to make individual movement easier to see.
        local = frame - idx * 20
        if local < 0:
            marker_pos = np.array(pos[routes[truck][0]], dtype=float)
            status = "ожидает старта"
        else:
            progress = min(local / 120, 1.0)
            point_idx = int(progress * (len(pts)-1))
            marker_pos = pts[point_idx]
            if progress >= 1:
                status = "маршрут завершён"
            else:
                status = f"движение {int(progress*100)}%"
        truck_markers[truck].set_data([marker_pos[0]], [marker_pos[1]])
        truck_labels[truck].set_position((marker_pos[0] + 0.12, marker_pos[1] + 0.12))
        truck_labels[truck].set_text(truck)
    ax.set_title(f"Движение машин по графу — демонстрация | кадр {frame+1}/{max_frames}")
    return list(truck_markers.values()) + list(truck_labels.values())

anim = FuncAnimation(fig, update, frames=max_frames, interval=80, blit=False)
out_path = "mining_fleet_movement_demo.gif"
anim.save(out_path, writer=PillowWriter(fps=12))
plt.close(fig)

print(f"Готово: {out_path}")
print("Важно: показаны демонстрационные маршруты; это не результат запуска CP-SAT.")
