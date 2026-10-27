
import random

NUM_TRUCKS =20

random.seed(42)


# ============================================================
# 2. ТИПЫ ДОРОГ
# ============================================================

ROAD_TYPES = {
    "paved": {
        "factor": 1.0,
        "capacity": 10,
    },
    "gravel": {
        "factor": 0.75,
        "capacity": 4,
    },
    "dirt": {
        "factor": 0.50,
        "capacity": 2,
    },
}


# ============================================================
# 3. ДАННЫЕ ГРАФА
# ============================================================

DATA = {
    "NODES": [
        # Стартовые вершины
        {
            "node_id": "S1",
            "kind": "junction",
            "x_m": 0,
            "y_m": 0,
            "z_m": 100,
        },
        {
            "node_id": "S2",
            "kind": "junction",
            "x_m": 0,
            "y_m": 400,
            "z_m": 120,
        },

        # Пункты загрузки
        {
            "node_id": "L1",
            "kind": "load",
            "x_m": 200,
            "y_m": 100,
            "z_m": 108,
        },
        {
            "node_id": "L2",
            "kind": "load",
            "x_m": 200,
            "y_m": 300,
            "z_m": 115,
        },
        {
            "node_id": "L3",
            "kind": "load",
            "x_m": 400,
            "y_m": 200,
            "z_m": 110,
        },

        # Пункты разгрузки
        {
            "node_id": "D1",
            "kind": "dump",
            "x_m": 700,
            "y_m": 100,
            "z_m": 90,
        },
        {
            "node_id": "D2",
            "kind": "dump",
            "x_m": 700,
            "y_m": 400,
            "z_m": 85,
        },

        # Промежуточные вершины
        {
            "node_id": "A",
            "kind": "junction",
            "x_m": 100,
            "y_m": 100,
            "z_m": 105,
        },
        {
            "node_id": "B",
            "kind": "junction",
            "x_m": 300,
            "y_m": 100,
            "z_m": 112,
        },
        {
            "node_id": "C",
            "kind": "junction",
            "x_m": 300,
            "y_m": 300,
            "z_m": 118,
        },
        {
            "node_id": "E",
            "kind": "junction",
            "x_m": 500,
            "y_m": 300,
            "z_m": 100,
        },
        {
            "node_id": "F",
            "kind": "junction",
            "x_m": 600,
            "y_m": 200,
            "z_m": 95,
        },
    ],

    "EDGES": [
        ("S1", "A", 100, "paved"),
        ("A", "S1", 100, "paved"),

        ("S2", "C", 150, "gravel"),
        ("C", "S2", 150, "gravel"),

        ("A", "B", 200, "paved"),
        ("B", "A", 200, "paved"),

        ("A", "C", 250, "gravel"),
        ("C", "A", 250, "gravel"),

        ("B", "C", 200, "paved"),
        ("C", "B", 200, "paved"),

        ("B", "F", 300, "gravel"),
        ("F", "B", 300, "gravel"),

        ("C", "E", 250, "paved"),
        ("E", "C", 250, "paved"),

        ("E", "F", 150, "paved"),
        ("F", "E", 150, "paved"),

        ("A", "L1", 150, "gravel"),
        ("L1", "A", 150, "gravel"),

        ("C", "L2", 100, "paved"),
        ("L2", "C", 100, "paved"),

        ("B", "L3", 150, "dirt"),
        ("L3", "B", 150, "dirt"),

        ("F", "D1", 180, "paved"),
        ("D1", "F", 180, "paved"),

        ("E", "D2", 250, "gravel"),
        ("D2", "E", 250, "gravel"),

        ("L1", "B", 180, "paved"),
        ("B", "L1", 180, "paved"),

        ("L2", "E", 220, "gravel"),
        ("E", "L2", 220, "gravel"),

        ("L3", "F", 200, "dirt"),
        ("F", "L3", 200, "dirt"),

        ("B", "D1", 450, "gravel"),
        ("D1", "B", 450, "gravel"),

        ("C", "D2", 500, "dirt"),
        ("D2", "C", 500, "dirt"),
    ],

    "VEHICLES": [
        {
            "vehicle_id": f"Truck_{i + 1}",
            "model": (
                "CAT_777"
                if i % 3 == 0
                else "BelAZ_7513"
                if i % 3 == 1
                else "BelAZ_7547"
            ),
            "capacity_t": random.choice([45, 60, 90]),
        }
        for i in range(NUM_TRUCKS)
    ],
}
