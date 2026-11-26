import streamlit as st
import matplotlib.pyplot as plt
import heapq

st.set_page_config(page_title="AERO EAGLE", page_icon="🦅", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #08111f;
    color: white;
}
h1, h2, h3 {
    color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)

st.title("🦅 AERO EAGLE")
st.subheader("Smart Campus Drone Route Planner")
st.caption("Emergency First-Aid Delivery • Route Planning Simulation")

st.markdown("---")

ROWS, COLS = 12, 12

buildings = {
    (2,2), (2,3), (3,2), (3,3),
    (2,7), (2,8), (3,7), (3,8),
    (6,3), (6,4), (7,3), (7,4),
    (8,8), (8,9), (9,8), (9,9),
    (5,6), (5,7)
}

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def find_path(start, goal):
    queue = [(0, start)]
    came_from = {}
    cost = {start: 0}

    while queue:
        _, current = heapq.heappop(queue)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            neighbor = (current[0]+dr, current[1]+dc)

            if not (0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS):
                continue

            if neighbor in buildings:
                continue

            new_cost = cost[current] + 1

            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                came_from[neighbor] = current
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(queue, (priority, neighbor))

    return None

available = [
    (r, c)
    for r in range(ROWS)
    for c in range(COLS)
    if (r, c) not in buildings
]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📍 Starting Point")
    start = st.selectbox(
        "Choose drone starting location",
        available,
        index=0,
        format_func=lambda p: f"Grid {p[0]+1}, {p[1]+1}"
    )

with col2:
    st.markdown("### 🏥 Destination")
    goal = st.selectbox(
        "Choose first-aid delivery location",
        available,
        index=len(available)-1,
        format_func=lambda p: f"Grid {p[0]+1}, {p[1]+1}"
    )

st.markdown("---")

if start == goal:
    st.warning("Please choose different start and destination locations.")
    path = None
else:
    path = find_path(start, goal)

if path:
    st.success("✅ Safe route successfully calculated!")

    distance = len(path) - 1

    m1, m2, m3 = st.columns(3)
    m1.metric("Route Length", f"{distance} grid units")
    m2.metric("Path Points", len(path))
    m3.metric("Status", "Route Found")

    st.markdown("### 🗺️ Campus Route Map")

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor("#08111f")
    ax.set_facecolor("#101e30")

    # Buildings
    for r, c in buildings:
        ax.add_patch(plt.Rectangle(
            (c, ROWS-1-r), 1, 1,
            color="#64748b"
        ))

    # Route
    xs = [c + 0.5 for r, c in path]
    ys = [ROWS-1-r + 0.5 for r, c in path]

    ax.plot(xs, ys, color="#38bdf8", linewidth=3, marker="o")

    # Start
    ax.scatter(
        start[1]+0.5, ROWS-1-start[0]+0.5,
        color="#22c55e", s=180, label="Start"
    )

    # Destination
    ax.scatter(
        goal[1]+0.5, ROWS-1-goal[0]+0.5,
        color="#f59e0b", s=180, label="Destination"
    )

    ax.set_xlim(0, COLS)
    ax.set_ylim(0, ROWS)
    ax.set_xticks(range(COLS))
    ax.set_yticks(range(ROWS))
    ax.grid(color="#334155", linewidth=0.5)
    ax.tick_params(colors="white")
    ax.set_aspect("equal")
    ax.legend(facecolor="#101e30", labelcolor="white")

    st.pyplot(fig)

    st.markdown("### 🚁 Flight Simulation")

    if st.button("▶️ Simulate Delivery"):
        st.info("Simulation complete! The virtual drone followed the calculated route.")
        st.progress(100)
        st.success("🧰 First-aid kit delivered successfully (simulation).")

    with st.expander("View route coordinates"):
        st.write(path)

else:
    st.error("No route found. Try another location.")

st.markdown("---")

st.markdown("""
### ℹ️ About AERO EAGLE
AERO EAGLE is a student project demonstrating intelligent pathfinding
for emergency first-aid delivery across a simulated campus.

**Algorithm:** A* Pathfinding  
**Purpose:** Educational route-planning simulation  
**Note:** This app is a simulation and does not control a real drone.
""")

st.caption("AERO EAGLE | Student Innovation Project 🦅")
