def print_color(text, color):
    # 定义 ANSI 转义码
    class TerminalColors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'

    # 根据传入的颜色选择相应的 ANSI 转义码
    if color == 'header':
        color_code = TerminalColors.HEADER
    elif color == 'blue':
        color_code = TerminalColors.OKBLUE
    elif color == 'green':
        color_code = TerminalColors.OKGREEN
    elif color == 'warning':
        color_code = TerminalColors.WARNING
    elif color == 'fail':
        color_code = TerminalColors.FAIL
    else:
        raise ValueError("Unsupported color.")

    # 打印带有颜色的文本
    print(f"{color_code}{text}{TerminalColors.ENDC}")

