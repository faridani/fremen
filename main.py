# main.py
from fremen import Fremen
from fremen.utils import helpful_function

def main():
    fremen = Fremen()
    print(fremen.greet())
    print(helpful_function())

if __name__ == "__main__":
    main()
