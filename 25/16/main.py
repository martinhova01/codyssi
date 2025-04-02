import time
import numpy as np
import re
import math


def rotate_point_x(point: tuple[float, float, float], positive_dir: bool) -> tuple[float, float, float]:
    """Rotate a point along the x-axis.

    Args:
        point tuple[float, float, float]: the original point
        positive_dir (bool): True if rotation is along positive direction

    Returns:
        tuple[float, float, float]: the rotated point
    """
    if positive_dir:
        return (point[0], -point[2], point[1])
    else:
        return (point[0], point[2], -point[1])

def rotate_point_y(point: tuple[float, float, float], positive_dir: bool) -> tuple[float, float, float]:
    """Rotate a point along the y-axis.

    Args:
        point tuple[float, float, float]: the original point
        positive_dir (bool): True if rotation is along positive direction

    Returns:
        tuple[float, float, float]: the rotated point
    """
    if positive_dir:
        return (point[2], point[1], -point[0])
    else:
        return (-point[2], point[1], point[0])


def biggest_row_col(grid: np.ndarray):
    largest = 0
    for _ in range(2):
        for row in grid:
            largest = max(largest, sum(row))
        grid = np.transpose(grid)
    return int(largest)
        

class Cube():
    """ The center of the cube has coordinated (0, 0, 0).
    Front/current face has z = 40.
    Back face has z = -40.
    Left face has x = -40.
    Right face has x = 40.
    Up face has y = -40.
    Down face has y = 40.
    """
    
    def __init__(self, N):
        self.N = N
        self.faces: dict[tuple[int, int, int], int] = self.init_faces()
        self.points: dict[tuple[float, float, float], int] = self.init_points()
        
    def dominant_sum_front_face(self):
        face = []
        for y in range(-self.N // 2, self.N // 2):
            row = []
            for x in range(-self.N // 2, self.N // 2):
                point = (x + 0.5, y + 0.5, self.N / 2)
                row.append(self.points[point])
            face.append(row)
        return biggest_row_col(np.array(face))
        
    def get_dominant_sums(self):
        _sums = []
        _sums.append(self.dominant_sum_front_face())
        self.rotate_x(True)
        _sums.append(self.dominant_sum_front_face())
        self.rotate_x(True)
        _sums.append(self.dominant_sum_front_face())
        self.rotate_x(True)
        _sums.append(self.dominant_sum_front_face())
        self.rotate_x(True)
        
        self.rotate_y(True)
        _sums.append(self.dominant_sum_front_face())
        self.rotate_y(True)
        self.rotate_y(True)
        _sums.append(self.dominant_sum_front_face())
        
        #make sure the rotation is the same as before method is called
        self.rotate_y(True)
        
        return math.prod(_sums)
        
    
    def init_faces(self):
        faces = {}
        for face in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            faces[face] = 0
        return faces
    
    def get_current_face(self):
        return (0, 0, 1)

    def absorb(self, instruction: str):
        if instruction.startswith("FACE"):
            value = int(re.findall(r"-?\d+", instruction)[0])
            self.faces[self.get_current_face()] += value * self.N**2
        
        elif instruction.startswith("ROW") or instruction.startswith("COL"):
            _, value = map(int, re.findall(r"-?\d+", instruction))
            self.faces[self.get_current_face()] += value * self.N
    
    def update_points(self, points: set[tuple[float, float, float]], value: int):
        for point in points:
            self.points[point] += value
            if self.points[point] > 100:
                self.points[point] %= 100
    
    def perform_instruction(self, instruction: str, part3=False):
        value = None
        points_to_update = set()
        if instruction.startswith("FACE"):
            value = int(re.findall(r"-?\d+", instruction)[0])
            for point in self.points:
                if point[2] == self.N / 2:
                    points_to_update.add(point)
        
        elif instruction.startswith("ROW"):
            row, value = map(int, re.findall(r"-?\d+", instruction))
            for point in self.points:
                if point[1] == row - (self.N / 2 + 0.5) and (point[2] == self.N / 2 or part3):
                    points_to_update.add(point)
        
        else:
            col, value = map(int, re.findall(r"-?\d+", instruction))
            for point in self.points:
                if point[0] == col - (self.N / 2 + 0.5) and (point[2] == self.N / 2 or part3):
                    points_to_update.add(point)
        
        self.update_points(points_to_update, value)
        
    def rotate_x(self, positive_dir: bool):
        new_points = {}
        for point, val in self.points.items():
            new_points[rotate_point_x(point, positive_dir)] = val
        self.points = new_points
        
        new_faces = {}
        for face, value in self.faces.items():
            new_faces[rotate_point_x(face, positive_dir)] = value
        self.faces = new_faces
            
    def rotate_y(self, positive_dir: bool):
        new_points = {}
        for point, val in self.points.items():
            new_points[rotate_point_y(point, positive_dir)] = val
        self.points = new_points
        
        new_faces = {}
        for face, value in self.faces.items():
            new_faces[rotate_point_y(face, positive_dir)] = value
        self.faces = new_faces
        
    def init_points(self):
        points = {}
        for x in range(-self.N // 2, self.N // 2):
            for y in range(-self.N // 2, self.N // 2):
                front_point = (x + 0.5, y + 0.5, self.N / 2)
                points[front_point] = 1
                points[rotate_point_x(front_point, True)] = 1
                points[rotate_point_x(front_point, False)] = 1
                points[rotate_point_y(front_point, True)] = 1
                points[rotate_point_y(front_point, False)] = 1
                points[rotate_point_x(rotate_point_x(front_point, True), True)] = 1
        return points

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(self.filename).read().rstrip()
        instructions, self.twists = self.data.split("\n\n")
        self.instructions = instructions.split("\n")
    
    def run(self, part: int):
        self.cube = Cube(80)
        for i in range(len(self.instructions)):
            instruction = self.instructions[i]
            if part == 1: 
                self.cube.absorb(instruction)
            elif part == 2:
                self.cube.perform_instruction(instruction)
            else:
                self.cube.perform_instruction(instruction, part3=True)
            
            if i == len(self.twists):
                break
            twist = self.twists[i]
            if twist == "L":
                self.cube.rotate_y(True)
            elif twist == "R":
                self.cube.rotate_y(False)
            elif twist == "D":
                self.cube.rotate_x(True)
            else:
                self.cube.rotate_x(False)
        
    def part1(self):
        self.run(1)
        return math.prod(sorted(self.cube.faces.values(), reverse=True)[:2])
    
    def part2(self):
        self.run(2)
        return self.cube.get_dominant_sums()
    
    def part3(self):
        self.run(3)   
        return self.cube.get_dominant_sums()
    
def main():
    start = time.perf_counter()
    
    s = Solution(test=True)
    print("---TEST---")
    print(f"part 1: {s.part1()}")
    print(f"part 2: {s.part2()}")
    print(f"part 3: {s.part3()}\n")
    
    s = Solution()
    print("---MAIN---")
    part1 = s.part1()
    assert part1 == 207644207974400
    print(f"part 1: {part1}")
    part2 = s.part2()
    assert part2 == 62512563005136804672000
    print(f"part 2: {part2}")
    part3 = s.part3()
    assert part3 == 12132795764574629153856
    print(f"part 3: {part3}")
    
    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")
    
main()