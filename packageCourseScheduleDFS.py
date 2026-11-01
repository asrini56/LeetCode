def resolve_install_order(target: str, dependencies: dict) -> list:
    visited_state = {}  # 0: Unvisited, 1: Visiting (Gray/Cycle check), 2: Visited (Black)
    build_order = []

    def dfs(pkg):
        # If package doesn't exist in our map, treat as an external leaf or empty dep
        if pkg not in dependencies:
            return True

        state = visited_state.get(pkg, 0)
        if state == 1:
            # Cycle detected! Currently in recursion stack (Visiting)
            raise ValueError(f"Cyclic dependency detected involving package: '{pkg}'")
        if state == 2:
            # Already processed
            return True

        # Mark as Visiting (Gray)
        visited_state[pkg] = 1

        # Visit all dependencies first (prerequisites)
        for dep in dependencies.get(pkg, []):
            dfs(dep)

        # Mark as Visited (Black) and append to build order
        visited_state[pkg] = 2
        build_order.append(pkg)
        return True

    # Run DFS starting from the target
    dfs(target)
    return build_order

# ==========================================
# Executing Test Cases
# ==========================================
if __name__ == "__main__":
    print("=== Test 1: Valid Target ('app') ===" )
    try:
        order = resolve_install_order("app", dependencies_map)
        print("Successfully resolved install order:", order)
    except ValueError as e:
        print("Error:", e)

    print("\n=== Test 2: Cyclic Target ('bad_pkg') ===")
    try:
        order = resolve_install_order("bad_pkg", dependencies_map)
        print("Successfully resolved install order:", order)
    except ValueError as e:
        print("Caught expected error:", e)
