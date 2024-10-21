import pygame
from maze import SearchSpace, Node
from const import*
from pygame.locals import*
import heapq

 # Ở đây chúng ta dùng CTDL <set> triển khai dựa trên bảng băm cho closed_set
 # Mỗi phần tử được ánh xạ tới một giá trị duy nhất, giúp việc truy cập, tìm kiếm, thêm, xóa nhanh hơn



# Hàm đánh dấu ô hiện tại trên maze
def mark_current_node(node: Node, sc:pygame.Surface):
    image_path = 'dino.png'
    dino_image = pygame.image.load(image_path)
    dino_image = pygame.transform.scale(dino_image, (A, A))
    dino_rect = pygame.Rect(node.rect.x, node.rect.y, A, A)
    
    sc.blit (dino_image, dino_rect)

# Hàm vẽ đường đi ngược (reconstructor path)
def draw_path(g: SearchSpace, father: list, sc: pygame.Surface):
    current_id = g.goal.id

    length = 1
    # Draw the path
    while father[current_id] != -1:
        current_node = g.grid_cells[current_id]

        next_node = g.grid_cells[father[current_id]]
        pygame.draw.line(sc, WHITE, current_node.rect.center, next_node.rect.center, 1)
        pygame.time.delay(30)
        pygame.display.update()
        length += 1
        current_id = father[current_id]

    print(f"- length[path] = { length }")
# DFS algorithm
# ----------------------------------------------------
def DFS(g: SearchSpace, sc: pygame.Surface):
    print('Implement DFS algorithm')
       
    # Tập hợp thứ tự (id) các nút có thể phát hiện
    open_set = [g.start.id]                                     # <list>: mô tả stack

    # Tập hợp lưu trữ (id) các nút đã được phát hiện: BLUE COLOR
    closed_set = set()                                          # <set>: mô tả hashmap
    
    # Tập hợp lưu trữ "node cha" của mỗi nút (được phát hiện)
    father = { node.id: -1 for node in g.grid_cells }

    # Duyệt tới khi không phát hiện được nút nào khác hoặc tới đích
    while open_set:

        # Lấy và xóa (stack.pop) phần tử cuối của [open_set]: tính chất DFS
        current_id = open_set.pop()

        # Nếu node hiện tại đã phát hiện thì bỏ qua
        if current_id in closed_set: continue
        
        # Thêm "nút vừa được phát hiện" vào [closed_set]
        closed_set.add(current_id)

        # Lấy "nút hiện tại" dựa vào [id]
        current_node = g.grid_cells[current_id]

        # Kiểm tra nếu đã tới đích:
        if g.is_goal(current_node):
            print("DFS complete")
            print(f"- cost[search] = {len(closed_set)} ")

            # Draw result path
            draw_path(g, father, sc)
            return
        
        # Đánh dấu nút hiện tại trên [maze]
        if current_node not in [g.start, g.goal]:
            mark_current_node(current_node, sc)

        # Duyệt lần lượt các phần tử của "danh sách kề" hiện tại
        for neighbor_node in g.get_neighbors(current_node):

            # Bỏ qua nếu "nút kề" đã nằm trong [closed_set]
            if neighbor_node.id in closed_set: continue     

            # Thêm "nút kề" vào [open_set], thêm mặc dù có thể đã được phát hiện trước đó: đảm bảo tính chất DFS
            # Không thực hiện xóa node: Đánh đổi chi phí không gian lấy chi phí thời gian
            open_set.append(neighbor_node.id)

            # Cập nhật "nút cha" cho các "nút kề"
            father[neighbor_node.id] = current_id

            # Đánh dấu cho các "nút kề"
            if neighbor_node not in [g.start, g.goal]:
                neighbor_node.set_color(RED, sc)

        # Kết thúc vòng lặp, lúc này, các [ô] kề mới trong "danh sách có thể phát hiện" được bốc ra theo độ ưu tiên: sau > trước
        # Mặc dù không đúng thứ tự thăm như cách triển khai của đệ quy, nhưng vẫn thể hiện được duyệt theo chiều sâu

        # Tạo độ trễ: Hình dung kết quả và cách thức tìm kiếm
        pygame.time.delay(50)
        pygame.display.update()

        # Đánh dấu node hiện tại đã đi qua
        if current_node not in [g.start, g.goal]:
            current_node.set_color(BLUE, sc)

    # Exception:
    raise NotImplementedError('not implemented')
# ----------------------------------------------------

# BFS algorithm
# ----------------------------------------------------
def BFS(g: SearchSpace, sc: pygame.Surface):
    print('Implement BFS algorithm')

    # Tập hợp thứ tự (id) các nút có thể phát hiện
    open_set = [g.start.id]                                     # <list>: mô tả stack                                    
    
    # Tập hợp lưu trữ (id) các nút đã được phát hiện: BLUE & RED (tối ưu thứ tự BFS)
    closed_set = set()                                          # <set>: mô tả <hashmap>
    
    # Tập hợp lưu trữ nút cha của mỗi nút (được phát hiện)
    father = { node.id: -1 for node in g.grid_cells }
    
    # Duyệt tới khi không phát hiện được nút nào khác hoặc tới đích
    while open_set:
        # Lấy và xóa (queue.dequeue) phần tử cuối của [open_set]: tính chất BFS
        current_id = open_set.pop(0)

        # Thêm "nút vừa được phát hiện" vào [closed_set]
        closed_set.add(current_id)
        
        # Lấy nút hiện tại dựa vào [id]
        current_node = g.grid_cells[current_id]

        # Kiểm tra nếu đã tới đích:
        if g.is_goal(current_node):
            print("BFS complete")
            print(f"- cost[search] = {len(closed_set)} ")

            # Draw result path
            draw_path(g, father, sc)
            return

        # Đánh dấu nút hiện tại trên [maze]
        if current_node not in [g.start, g.goal]:
            mark_current_node(current_node, sc)

        # Duyệt lần lượt các phần tử của "danh sách kề" hiện tại
        for neighbor_node in g.get_neighbors(current_node):
            
            # Bỏ qua nếu "nút kề" đã nằm trong [closed_set]
            if neighbor_node.id in closed_set: continue
            
            # Thêm "nút kề" vào [open_set]
            open_set.append(neighbor_node.id)
            
            # Thêm "nút kề" vào [closed_set]: Để tránh trường hợp các nút có chung nút kề
            closed_set.add(neighbor_node.id)

            # Cập nhật "nút cha" cho các "nút kề"
            father[neighbor_node.id] = current_id

            # Đánh dấu các "nút kề"
            if neighbor_node not in [g.start, g.goal]:
                neighbor_node.set_color(RED, sc)

        # Tạo độ trễ: Hình dung kết quả và cách thức tìm kiếm
        pygame.time.delay(20)
        pygame.display.update()
        
        # Đánh dấu nút hiện tại đã đi qua
        if current_node not in [g.start, g.goal]:
            current_node.set_color(BLUE, sc)

    raise NotImplementedError('not implemented')
# ----------------------------------------------------

# class: Định nghĩa lại các phương thức của cho <heapq>
# ----------------------------------------------------
class PrioQueue:
    def __init__(self, prio_val = None, node_id = None):
        self.elements = [(prio_val, node_id)]

    def is_empty(self):
        return len(self.elements) == 0

    def push(self, prio_value, node_id):
        # Đánh giá độ ưu tiên dựa trên giá trị ưu tiên trước (có thể là khoảng cách), rồi tới id của node
        heapq.heappush(self.elements, (prio_value, node_id))

    def pop(self):
        return heapq.heappop(self.elements)[1]
# Sử dụng hàng đợi ưu tiên cho AStar & Dijkstra: Đảm bảo chi phí thêm, tìm kiếm, xóa, ... là O(log(n))

# Hàm tính khoảng cách Euclidean của 2 node
def Euclidean_distance(node_1: Node, node_2: Node) -> float:
    # Tính vị trí 
    x1, y1 = node_1.id%COLS, node_1.id//COLS
    x2, y2 = node_2.id%COLS, node_2.id//COLS
    dx = x1 - x2
    dy = y1 - y2
    return (dx**2 + dy**2)**0.5
# ----------------------------------------------------

# AStar algorithm
# ----------------------------------------------------
def AStar(g: SearchSpace, sc: pygame.Surface):
    print('Implement AStar algorithm')

    # Tập hợp chứa các nút có thể phát hiện: Sử dụng hàng đợi ưu tiên đảm bảo chi phí
    open_set = PrioQueue(0, g.start.id)

    # Tập hợp chứa các nút được phát hiện
    closed_set = set()

    # Node cha của mỗi nút trong đường đi
    father = {node.id: -1 for node in g.grid_cells}

    # Chi phí để đến từ start đến mỗi nút
    cost = {node.id: float('inf') for node in g.grid_cells}
    cost[g.start.id] = 0

    # Duyệt tới khi không phát hiện được nút nào khác hoặc tới đích
    while not open_set.is_empty():
        # Lấy và xóa id node hiện tại từ hàng đợi ưu tiên (đánh giá dựa trên khoảng cách tới đích)
        current_id = open_set.pop()

        # Nếu node đã nằm trong danh sách được phát hiện thì bỏ qua
        if current_id in closed_set: continue

        # Thêm "nút vừa được phát hiện" vào [closed_set]
        closed_set.add(current_id)
        
        # Lấy node hiện tại dựa vào id
        current_node = g.grid_cells[current_id]

        # Kiểm tra nếu đã tới đích:
        if g.is_goal(current_node):
            print("AStar complete")
            print(f"- cost[search] = {len(closed_set)} ")
            # Draw result path
            draw_path(g, father, sc)
            return

        # Đánh dấu nút hiện tại trên [maze]
        if current_node not in [g.start, g.goal]:
            mark_current_node(current_node, sc)

        # Duyệt lần lượt các phần tử của "danh sách kề" hiện tại
        for neighbor_node in g.get_neighbors(current_node):

            # Bỏ qua nếu "nút kề" đã nằm trong [closed_set]
            if neighbor_node.id in closed_set: continue

            # Chi phí cho nút kề
            neighbor_cost = Euclidean_distance(current_node, neighbor_node) + cost[current_id]

            # Bỏ qua nếu "nút kề" có chi phí khác nhỏ hơn, hoặc đã có cách cho tương tự: Giảm chi phí
            if neighbor_cost >= cost[neighbor_node.id]: continue

            # Giá trị đánh giá dựa trên tổng chi phí: "start to neighbor" + "neighbor to goal"
            heuristic = Euclidean_distance(neighbor_node, g.goal) + neighbor_cost

            # Thêm "nút kề" vào [open_set], với giá trị đánh giá
            open_set.push(heuristic, neighbor_node.id)
            
            # Cập nhật "nút cha" cho các "nút kề"
            father[neighbor_node.id] = current_id
            
            # Cập nhật chi phí cho các "nút kề"
            cost[neighbor_node.id] = neighbor_cost
            
            # Đánh dấu cho các "nút kề"
            if neighbor_node not in [g.start, g.goal]:
                neighbor_node.set_color(RED, sc)

        # Tạo độ trễ: Hình dung kết quả và cách thức tìm kiếm
        pygame.time.delay(50)
        pygame.display.update()

        # Đánh dấu node đã nằm trong danh sách được phát hiện
        if current_node not in [g.start, g.goal]:
            current_node.set_color(BLUE, sc) 

    raise NotImplementedError('not implemented')
# ----------------------------------------------------

# Dijkstra algorithm
# ----------------------------------------------------
def Dijkstra(g: SearchSpace, sc: pygame.Surface):
    print('Implement Dijkstra algorithm')
    
    # Tập hợp chứa các nút có thể phát hiện: Sử dụng hàng đợi ưu tiên
    open_set = PrioQueue(0, g.start.id)

    # Tập hợp chứa các nút được phát hiện
    closed_set = set()

    # Node cha của mỗi nút trong đường đi
    father = {node.id: -1 for node in g.grid_cells}

    # Chi phí để đến từ start đến mỗi nút
    cost = {node.id: float('inf') for node in g.grid_cells}
    cost[g.start.id] = 0

    # Duyệt tới khi không phát hiện được nút nào khác hoặc tới đích
    while not open_set.is_empty():

        # Lấy và xóa id node hiện tại từ hàng đợi ưu tiên (đánh giá dựa trên khoảng cách tới đích)
        current_id = open_set.pop()

        # Nếu node đã nằm trong danh sách được phát hiện thì bỏ qua
        if current_id in closed_set: continue

        # Thêm "nút vừa được phát hiện" vào [closed_set]
        closed_set.add(current_id)
        
        # Lấy node hiện tại dựa vào id
        current_node = g.grid_cells[current_id]

        # Kiểm tra nếu đã tới đích:
        if g.is_goal(current_node):
            print("Dijkstra complete")
            print(f"- cost[search] = {len(closed_set)} ")
            # Draw result path
            draw_path(g, father, sc)
            return

        # Đánh dấu nút hiện tại trên [maze]
        if current_node not in [g.start, g.goal]:
            mark_current_node(current_node, sc)
        
        # Duyệt lần lượt các phần tử của "danh sách kề" hiện tại
        for neighbor_node in g.get_neighbors(current_node):
              
            # Chi phí tới nút kề:
            neighbor_cost = cost[current_id] + Euclidean_distance(current_node, neighbor_node)

            # Bỏ qua nếu "nút kề" đã nằm trong [closed_set], hoặc có cách khác không nhiều chi phí hơn:
            if neighbor_node.id in closed_set or neighbor_cost >= cost[neighbor_node.id]: continue

            # Thêm "nút kề" vào [open_set], với đánh giá dựa trên chi phí
            open_set.push(neighbor_cost, neighbor_node.id)

            # Cập nhật "nút cha" cho các "nút kề"
            father[neighbor_node.id] = current_id

            # Cập nhật chi phí cho các "nút kề"
            cost[neighbor_node.id] = neighbor_cost
            
            # Đánh dấu cho các "nút kề"
            if neighbor_node not in [g.start, g.goal]:
                neighbor_node.set_color(RED, sc)

        # Tạo độ trễ: Hình dung kết quả và cách thức tìm kiếm
        pygame.time.delay(20)
        pygame.display.update()

        # Đánh dấu node đã nằm trong danh sách được phát hiện
        if current_node not in [g.start, g.goal]:
            current_node.set_color(BLUE, sc)

    raise NotImplementedError('not implemented')
# ----------------------------------------------------