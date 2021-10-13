#!/usr/bin/env python3

from containerdshim import containerdshim;

def main():
    containerdshim.list_images()


if __name__ == '__main__':
    main()