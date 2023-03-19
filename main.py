import os
import argparse
import geometry.polygon as geom
import base64


def main() -> None:  # No DB connection because the program would not work on other PCs (and also it's completely meaningless)
    manual, input_file = parse_flags()

    gen: geom.PolygonGenerator = geom.PolygonGenerator()
    poly: geom.Polygon = None

    if manual:
        poly = gen.new_polygon()
    elif input_file == "":
        raise FileNotFoundError("Input file location not provided, cannot proceed.")
    else:
        poly = gen.new_polygon_file(input_file)

    save_results_file(poly)


def parse_flags() -> bool | str:
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--manual", default=False, action="store_true",
                        help="If provided, user would have to input points manually. By default, it is false and location of input file must be specified.")

    parser.add_argument("-i", "--inputfile", type=str, default="", help="Relative location of the input file.")

    args = parser.parse_args()
    return args.manual, args.inputfile


def save_results_file(poly: geom.Polygon) -> None:
    if not os.path.isdir("data"):
        os.mkdir("data")

    buffer: str = ""
    buffer += f"Polygon with {len(poly.vectors)} angles has area {poly.get_area()}\n"
    buffer += "List of points in order:\n"
    for vector in poly.vectors:
        buffer += f"({vector.start.x};{vector.start.y})\n"
    buffer += "\n\n"

    if os.path.isfile("data/area_results.dat"):
        with open("data/area_results.dat", "r", encoding="utf-8") as file:
            raw_data = file.read()
            data_decoded = base64.b64decode(raw_data)
            data = data_decoded.decode('utf-8')
            buffer += str(data)

    encoded: bytes = base64.b64encode(buffer.encode("utf-8"))

    with open("data/area_results.dat", "w", encoding="utf-8") as file:
        file.write(encoded.decode())


if __name__ == "__main__":
    main()
