from typing import Callable
import math


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y


class Vector:  # stores vector as point and displacement
    def __init__(self, displacement: Point, starting_point: Point = None):
        self.start = Point(0.0, 0.0)
        self.disp = displacement

        if starting_point is not None:
            self.start.x = starting_point.x
            self.start.y = starting_point.y

    def __abs__(self) -> float:
        return math.sqrt(self.disp.x**2+self.disp.y**2)

    def __add__(self, other):
        return Vector(self.disp+other.disp, self.start)

    def __sub__(self, other):
        return Vector(self.disp-other.disp, self.start)

    def __mul__(self, other) -> float:
        """Dot product"""
        return self.disp.x*other.disp.x+self.disp.y*other.disp.y

    def __xor__(self, other) -> float:
        """Cross product"""
        return self.disp.x*other.disp.y-self.disp.y*other.disp.x


class Polygon:
    _complete: bool = False

    def __init__(self, coords: list[Point] = None):
        self.vectors: list[Vector] = []

        if coords is None:
            return

        for displ in coords:
            self.add_side(displ)

        if not self._complete:
            self.autocomplete()

    def is_complete(self) -> bool:
        return self._complete

    def reset(self):
        self.vectors = []
        self._complete = False

    def get_area(self) -> float:
        area: float = 0.0
        for i in range(1, len(self.vectors)):
            vec1: Vector = Vector(self.vectors[i-1].start+self.vectors[i-1].disp)
            vec2: Vector = Vector(self.vectors[i].start+self.vectors[i].disp)
            area += (vec1 ^ vec2)/2

        return abs(area)

    def add_side(self, new_side: Vector):
        if self._complete:
            return

        if self._check_intersections(new_side):
            raise ValueError("new polygon side intersects with existing side")

        self.vectors.append(new_side)

    def autocomplete(self) -> bool:
        if self._complete:
            return True

        last_point: Point = self.vectors[-1].start+self.vectors[-1].disp
        new_vector: Vector = Vector(-last_point, last_point)

        if self._check_intersections(new_vector):
            return False

        self.vectors.append(new_vector)
        self._complete = True
        return True

    def _check_intersections(self, u: Vector) -> bool:
        """Intersections are checked with parametric vector representation
        v:
        x = t*disp.x+start.x
        y = t*disp.y+start.y

        u:
        x = T*disp.x+start.x
        y = T*disp.y+start.y
        """

        for v in self.vectors:
            if u.disp.x*v.disp.y == u.disp.y*v.disp.x:
                if (u.start.x <= v.start.x+v.disp.x <= u.disp.x+u.start.x or u.start.x <= v.start.x <= u.disp.x+u.start.x) \
                        and (u.start.y <= v.start.y+v.disp.y <= u.disp.y+u.start.y or u.start.y <= v.start.y <= u.disp.y+u.start.y):  # конец или начало вектора касаются нового вектора
                    return True
                continue

            t: float = (u.disp.y*(u.start.x-v.start.x)-u.disp.x*(u.start.y-v.start.y))/(u.disp.y*v.disp.x-u.disp.x*v.disp.y)
            T: float = (v.disp.y*(u.start.x-v.start.x)-v.disp.x*(u.start.y-v.start.y))/(u.disp.y*v.disp.x-u.disp.x*v.disp.y)

            if T == 0 and t == 1 and v == self.vectors[-1]:  # new vector is always at the beginning of last added vectors end
                break
            elif T == 1 and t == 0 and v.start.x == 0 and v.start.y == 0:
                self._complete = True
                break
            elif 0 <= T <= 1 and 0 <= t <= 1:
                return True

        return False


class PolygonGenerator:
    def new_polygon(self) -> Polygon:
        print("When polygon will be complete, prompt automatically stops. To automatically complete polygon with existing vectors, leave prompt blank.")
        return self._construct_polygon(input_stream=lambda: input("x y:"), error_handling=lambda: None)

    def new_polygon_file(self, input_file: str):
        with open(input_file, mode="r", encoding="utf-8", buffering=1) as file:
            return self._construct_polygon(input_stream=file.readline, error_handling=interrupt_program)

    def _construct_polygon(self, input_stream: Callable[[], str], error_handling: Callable[[], None]) -> Polygon:
        poly = Polygon()

        old_point: Point = Point(0.0, 0.0)
        new_point: Point = Point(0.0, 0.0)
        while not poly.is_complete():
            old_point = new_point

            try:
                coords_str = input_stream()
                coords_str = coords_str.removesuffix("\n")

                if coords_str == "":
                    if poly.autocomplete():
                        break

                    print("could not autocomplete polygon")
                    error_handling()
                    continue

                x, y = self._parse_coords(coords_str)
                new_point = Point(x, y)

            except ValueError:
                print(f"could not parse coordinates: {coords_str}")
                error_handling()

            try:
                if not new_point == old_point:
                    poly.add_side(Vector(new_point-old_point, old_point))

            except ValueError as e:
                print(f"error when adding new side: {e}")
                error_handling()

        return poly

    def _parse_coords(self, coords_str: str) -> float | float:
        coords = coords_str.split(" ")
        return float(coords[0]), float(coords[1])


def interrupt_program():
    raise RuntimeError("Data passed is of incorrect format. Consult with the documentation about input file format.")
