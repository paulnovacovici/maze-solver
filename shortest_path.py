import numpy as np
import cv2

mouseClicks = 0
start = None
end = None

def initImage():
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)   
    imgGS = cv2.imread('zac_maze.png', cv2.IMREAD_GRAYSCALE)
    imgCL = cv2.imread('zac_maze.png', cv2.IMREAD_COLOR)
    imgGS = cv2.resize(imgGS, (960, 540))      
    imgCL = cv2.resize(imgCL, (960, 540))  
    ret, imgGS = cv2.threshold(imgGS, 130, 255, cv2.THRESH_BINARY)
    return imgGS, imgCL


def mouseCallback(event, x, y, flags, param):
    global mouseClicks, start, end
    img = param
    if mouseClicks == 2: 
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        mouseClicks += 1
        if mouseClicks == 1:
            start = y, x
        else:
            end = y, x
            shortestPath = bfs(img, start, end)
            for y,x in shortestPath:
                imgCL[y][x] = [50,205,50]

def backtrace(parents, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parents[path[-1]])
    path.reverse()
    return path


def validMove(img, y, x):
    return img[y][x] != 0


def bfs(img, start, end):
    print("STARTING BFS")
    print(f"START: {start}")
    print(f"END: {end}")
    visited = set()
    parents = {}
    q = [(start, (-1,-1))]

    # Movement only up, left, right, down
    moves = [(1,0), (-1,0), (0, 1), (0, -1), (1,1), (-1,-1), (1,-1), (-1,1)]

    # queue schema: ((y, x), parent)
    while q:
        node, parent = q.pop(0)
        y, x = node
        # Preprocessing
        if y > len(img) or y < 0:
            continue
        if x > len(img[y]) or x < 0:
            continue
        if (y, x) in visited: 
            continue

        # Processing stage
        if (y, x) == end:
            parents[end] = parent
            return backtrace(parents, start, end)
        
        if not validMove(img, y, x):
            continue

        for moveX, moveY in moves:
            q.append(((y + moveY, x + moveX), node))

        parents[node] = parent
        visited.add(node)

    # Couldn't find path
    return []


def driver(img):
    while True:
        cv2.imshow('image', img)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('m'):
            break
        elif k == 27:
            break
    
    cv2.destroyAllWindows()


if __name__ == "__main__":
    imgGL, imgCL = initImage()
    cv2.setMouseCallback('image', mouseCallback, imgGL)
    driver(imgCL)