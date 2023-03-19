import base64

password: str = "Mogus😳"


def main() -> None:
    while True:
        if get_access():
            raw_data = load_data()
            data = decode_data(raw_data)
            print(data)
            break
        else:
            print("Incorrect password, try again")


def get_access() -> bool:
    pwd = input("Please, enter password:")
    return pwd == password


def load_data() -> str:
    with open("data/area_results.dat", "r", encoding="utf-8") as file:
        return file.read()


def decode_data(raw_data: str) -> str:
    return base64.b64decode(raw_data.encode("utf-8")).decode("utf-8")


if __name__ == "__main__":
    main()
