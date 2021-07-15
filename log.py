import chalk


def print_args(chalk_color, *args):
    print(*[chalk_color(arg) for arg in args])


def print_info(*args):
    print(*args)


def print_error(*args):
    print_args(chalk.red, *args)


def print_success(*args):
    print_args(chalk.green, *args)


def print_header1_info(*args):
    print_args(chalk.yellow, *args)


def print_header2_info(*args):
    print_args(chalk.blue, *args)


def print_sep(n=40):
    print('=' * n)
