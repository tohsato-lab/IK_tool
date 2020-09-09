from bdmleditor.entrypoint import (
    entry_point,
    arg_check,
)


def main():
    entry_point(arg_check())


if __name__ == '__main__':
    main()
