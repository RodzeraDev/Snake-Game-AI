import heapq
from collections import deque

class SnakeBot:
    def __init__(self):
        pass

    def next_move(self, state):
        DIRS = {
            "UP": (0, -1), "DOWN": (0, 1),
            "LEFT": (-1, 0), "RIGHT": (1, 0)
        }

        board_w = state["board_width"]
        board_h = state["board_height"]
        snake = list(state["snake"])
        head = snake[0]
        tail = snake[-1]
        food = state["food"]

        def neighbors(pos, body_set):
            for dx, dy in DIRS.values():
                nx, ny = pos[0] + dx, pos[1] + dy
                if (0 <= nx < board_w and 0 <= ny < board_h and (nx, ny) not in body_set):
                    yield (nx, ny)

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def astar(start, goal, body):
            frontier = [(heuristic(start, goal), 0, start, [])]
            visited = set()
            while frontier:
                _, cost, current, path = heapq.heappop(frontier)
                if current in visited:
                    continue
                visited.add(current)
                if current == goal:
                    return path
                for neighbor in neighbors(current, set(body)):
                    new_path = path + [neighbor]
                    heapq.heappush(frontier, (
                        cost + 1 + heuristic(neighbor, goal),
                        cost + 1,
                        neighbor,
                        new_path
                    ))
            return None

        def bfs(start, goal, body):
            queue = deque([start])
            visited = set()
            body_set = set(body[:-1])
            while queue:
                current = queue.popleft()
                if current == goal:
                    return True
                for nx, ny in neighbors(current, body_set):
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
            return False

        def simulate_path(path):
            sim_snake = list(snake)
            for pos in path:
                sim_snake.insert(0, pos)
                if pos != food:
                    sim_snake.pop()
            return sim_snake

        path_to_food = astar(head, food, snake)
        if path_to_food:
            sim_snake = simulate_path(path_to_food)
            if bfs(sim_snake[0], sim_snake[-1], sim_snake):
                next_pos = path_to_food[0]
                dx = next_pos[0] - head[0]
                dy = next_pos[1] - head[1]
                for dir_name, (vx, vy) in DIRS.items():
                    if (dx, dy) == (vx, vy):
                        return dir_name

        # fallback: follow tail
        path_to_tail = astar(head, tail, snake)
        if path_to_tail:
            next_pos = path_to_tail[0]
            dx = next_pos[0] - head[0]
            dy = next_pos[1] - head[1]
            for dir_name, (vx, vy) in DIRS.items():
                if (dx, dy) == (vx, vy):
                    return dir_name

        # fallback: safe move
        for dir_name, (dx, dy) in DIRS.items():
            nx, ny = head[0] + dx, head[1] + dy
            if 0 <= nx < board_w and 0 <= ny < board_h and (nx, ny) not in snake:
                return dir_name

        return state["direction"]

if __name__ == "__main__":
    try:
        from snake_game import run_episode
    except ImportError:
        print("❌ Could not import snake_game. Make sure snake_game.py is in the same folder.")
        exit(1)

    bot = SnakeBot()
    run_episode(bot, render=True)
