def waste_far_from_accessioning(layout, min_dist=20):
    g1 = layout["Waste"][3]
    g2 = layout["Accessioning"][3]
    return g1.centroid.distance(g2.centroid) >= min_dist


def courier_near_accessioning(layout, max_dist=8):
    g2 = layout["Accessioning"][3]
    dock = layout.get("Courier Dock")
    if not dock:
        return True
    return dock[3].centroid.distance(g2.centroid) <= max_dist


def micro_path_not_adjacent_to_chem(layout, min_dist=8):
    chem = layout["Chemistry"][3]

    for k in ["Microbiology", "Pathology"]:
        if chem.centroid.distance(layout[k][3].centroid) < min_dist:
            return False
    return True


def total_flow_distance(layout):
    pairs = [
        ("Accessioning", "Chemistry"),
        ("Accessioning", "Microbiology"),
        ("Accessioning", "Pathology"),
        ("Chemistry", "Cold Storage"),
    ]

    d = 0
    for a, b in pairs:
        d += layout[a][3].centroid.distance(layout[b][3].centroid)
    return d
