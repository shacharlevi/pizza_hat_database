import atexit
import sys


from persistence import repo, Repository


def main():
    repo.create_tables()

    config = sys.argv[1]
    orders = sys.argv[2]
    output = sys.argv[3]

    repo.read_config(config)
    repo.read_orders(orders)
    repo.write_output(output)


if __name__ == '__main__':
    main()
