from lib.client import Client
from lib.utils import generate_keys


def main():
    KEY = generate_keys()

    client = Client(KEY)

    api_key = client.return_api_key()

    print(api_key)


if __name__ == '__main__':
    main()