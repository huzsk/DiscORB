"""
ui.py: Terminal UI helpers: colors, banners, animations, menus, credits.
"""

import builtins
import re
import unicodedata
import shutil
import sys
import time

from . import config


class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

    # DiscORB theme roles use standard terminal colors.
    PRIMARY = MAGENTA
    ACCENT = CYAN
    TEXT = WHITE
    MUTED = BLUE
    PROMPT = CYAN


_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


PANEL_WIDTH = 76


def _cell_width(char: str) -> int:
    if unicodedata.combining(char):
        return 0
    return 2 if unicodedata.east_asian_width(char) in ("W", "F") else 1


def _visible_width(text: str) -> int:
    """Measure terminal cells without counting ANSI color sequences."""
    return sum(_cell_width(char) for char in _ANSI_ESCAPE.sub("", text))


def _layout(width: int = PANEL_WIDTH) -> tuple[int, str]:
    columns = max(2, shutil.get_terminal_size(fallback=(80, 24)).columns)
    width = min(width, columns - 1)
    return width, " " * max(0, (columns - width) // 2)


def _wrap_colored(line: str, width: int) -> list[str]:
    """Wrap long output without changing text or splitting color codes."""
    rows, row, cells = [], "", 0
    for token in re.findall(r"\x1b\[[0-9;]*m|[^\x1b]", line.expandtabs(4)):
        size = 0 if _ANSI_ESCAPE.fullmatch(token) else _cell_width(token)
        if cells + size > width and cells:
            rows.append(row)
            row, cells = "", 0
        row += token
        cells += size
    rows.append(row)
    return rows


def _format_panel(text: str, width: int = PANEL_WIDTH) -> str:
    width, padding = _layout(width)
    rows = []
    for line in text.split("\n"):
        for row in _wrap_colored(line, width):
            rows.append(padding + row if _ANSI_ESCAPE.sub("", row).strip() else row)
    return "\n".join(rows)


def panel_print(*values, sep=" ", end="\n", file=None, flush=False) -> None:
    """Print within a centered column, keeping list indentation intact."""
    stream = sys.stdout if file is None else file
    text = sep.join(str(value) for value in values)
    builtins.print(_format_panel(text), end=end, file=stream, flush=flush)


def panel_input(prompt: str = "") -> str:
    """Position a prompt and the input cursor inside the same column."""
    formatted = _format_panel(prompt)
    if not prompt or prompt.endswith("\n"):
        formatted += _layout()[1]
    return builtins.input(formatted)


def _print_centered_block(text: str, width: int = 0) -> None:
    """Center artwork or a title as one block, ignoring color codes."""
    lines = text.split("\n")
    block_width = max([width] + [_visible_width(line) for line in lines])
    builtins.print(_format_panel(text, max(1, block_width)))


def print_color(text: str, color: str = Colors.TEXT, bold: bool = False) -> None:
    """Print colored text."""
    style = Colors.BOLD if bold else ''
    panel_print(f"{style}{color}{text}{Colors.RESET}")


def print_boxed_title(title: str, width: int = 50,
                      color: str = Colors.PRIMARY, centered: bool = True) -> None:
    """Print a boxed title, optionally centered in the terminal."""
    width = min(max(width, _visible_width(title) + 4), _layout()[0])
    border = f"{Colors.BOLD}{color}{'+' + '=' * (width - 2) + '+'}{Colors.RESET}"
    title_padding = (width - _visible_width(title) - 2) // 2
    extra_space = (width - _visible_width(title) - 2) % 2
    title_line = (
        f"{Colors.BOLD}{color}|{' ' * title_padding}{title}"
        f"{' ' * (title_padding + extra_space)}|{Colors.RESET}"
    )
    block = f"\n{border}\n{title_line}\n{border}\n"
    if centered:
        _print_centered_block(block, width)
    else:
        print(block)


def print_banner() -> None:
    """Display ASCII banner."""
    banner = f"""
{Colors.PRIMARY}{Colors.BOLD}


    ██████╗░██╗░██████╗░█████╗░░█████╗░██████╗░██████╗░
    ██╔══██╗██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗
    ██║░░██║██║╚█████╗░██║░░╚═╝██║░░██║██████╔╝██████╦╝
    ██║░░██║██║░╚═══██╗██║░░██╗██║░░██║██╔══██╗██╔══██╗
    ██████╔╝██║██████╔╝╚█████╔╝╚█████╔╝██║░░██║██████╦╝
    ╚═════╝░╚═╝╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░

{Colors.RESET}
    {Colors.MUTED}Developer: {Colors.ACCENT}{config.DEVELOPER}{Colors.RESET}
    {Colors.MUTED}Version: {Colors.TEXT}{config.VERSION}{Colors.RESET}
    {Colors.MUTED}Database: {Colors.ACCENT}Discord Official API + GitHub Archive{Colors.RESET}
"""
    _print_centered_block("\n".join(line.strip() for line in banner.split("\n")))


def loading_animation(text: str, duration: float = 1.5) -> None:
    """Display loading animation."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    ascii_frames = ["|", "/", ".", "\\"]
    text = _ANSI_ESCAPE.sub("", text)
    text = _wrap_colored(text, max(1, _layout()[0] - 2))[0]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        try:
            sys.stdout.write(
                f"\r{_layout()[1]}{Colors.PRIMARY}{frames[i % len(frames)]}{Colors.RESET} {Colors.TEXT}{text}{Colors.RESET}")
            sys.stdout.flush()
        except UnicodeEncodeError:
            try:
                sys.stdout.write(
                    f"\r{_layout()[1]}{Colors.PRIMARY}{ascii_frames[i % len(ascii_frames)]}{Colors.RESET} {Colors.TEXT}{text}{Colors.RESET}")
                sys.stdout.flush()
            except Exception:
                pass
        except Exception:
            pass
        time.sleep(0.1)
        i += 1
    try:
        sys.stdout.write("\r\033[2K")
        sys.stdout.flush()
    except Exception:
        pass


def ask_confirm(prompt: str = "Create and launch?") -> bool:
    """Ask a Y/n confirmation question. Returns True if user confirms."""
    answer = panel_input(
        f"\n{Colors.BOLD}{Colors.PROMPT}{prompt}{Colors.RESET} {Colors.ACCENT}[Y/n]: {Colors.RESET}").strip().lower()
    return answer in ('', 'y', 'yes')


def print_menu() -> None:
    """Center the menu beneath the banner with aligned option labels."""
    width = PANEL_WIDTH
    print_boxed_title("MAIN MENU", width=width, color=Colors.PRIMARY, centered=True)
    options = [
        f"  {Colors.BOLD}{Colors.ACCENT}1.{Colors.RESET} {Colors.TEXT}Search Game Database (Discord API){Colors.RESET}",
        f"  {Colors.BOLD}{Colors.ACCENT}2.{Colors.RESET} {Colors.TEXT}Custom Game (Not Listed){Colors.RESET}",
        f"  {Colors.BOLD}{Colors.ACCENT}3.{Colors.RESET} {Colors.TEXT}Steam Quest Mode {Colors.PRIMARY}[Steam integration]{Colors.RESET}",
        f"  {Colors.BOLD}{Colors.ACCENT}4.{Colors.RESET} {Colors.TEXT}Credits & Info{Colors.RESET}",
        f"  {Colors.BOLD}{Colors.MAGENTA}5.{Colors.RESET} {Colors.TEXT}Exit{Colors.RESET}",
    ]
    _print_centered_block("\n".join(options) + "\n", width)


def show_credits() -> None:
    """Display project information and credits."""
    print_boxed_title("ABOUT DiscORB", width=65, color=Colors.PRIMARY)
    credits_text = f"""
    {Colors.BOLD}{Colors.ACCENT}Developer:{Colors.RESET} {Colors.TEXT}{config.DEVELOPER}{Colors.RESET}
    {Colors.BOLD}{Colors.ACCENT}Version:{Colors.RESET}   {Colors.TEXT}{config.VERSION}{Colors.RESET}

    {Colors.BOLD}{Colors.PRIMARY}Overview{Colors.RESET}
    {Colors.TEXT}DiscORB is a Python toolkit for simulating game processes
    recognized by Discord. It combines game database lookup,
    configurable process selection and Steam integration in a
    streamlined terminal interface.{Colors.RESET}

    {Colors.BOLD}{Colors.PRIMARY}Process Simulation{Colors.RESET}
    {Colors.TEXT}The application retrieves game metadata, identifies associated
    executable names and launches simulated processes using those
    names. Discord must remain open to detect active processes.
    Detection depends on the game and its specific requirements.{Colors.RESET}

    {Colors.BOLD}{Colors.PRIMARY}Steam Integration{Colors.RESET}
    {Colors.TEXT}Steam Quest Mode retrieves application metadata and prepares
    simulated executable files and Steam manifest information
    for supported workflows. Compatibility may vary by title.{Colors.RESET}

    {Colors.BOLD}{Colors.PRIMARY}Database Sources{Colors.RESET}
    {Colors.ACCENT}Primary:{Colors.RESET} {Colors.TEXT}Discord Official API{Colors.RESET}
    {Colors.ACCENT}Backup:{Colors.RESET}  {Colors.TEXT}GitHub Archive by Cynosphere{Colors.RESET}

    {Colors.BOLD}{Colors.PRIMARY}Project Credits{Colors.RESET}
    {Colors.TEXT}DiscORB is based on OrbsHacker. Credit for the original
    implementation belongs to its authors and contributors.{Colors.RESET}

    {Colors.BOLD}{Colors.PRIMARY}Usage Notes{Colors.RESET}
    {Colors.TEXT}1. Keep Discord open while using process simulation.
    2. Keep the selected process running while detection is needed.
    3. Review each quest's requirements before choosing a mode.
    Quest progress and reward completion are not guaranteed.{Colors.RESET}

    {Colors.BOLD}{Colors.YELLOW}Responsible Use{Colors.RESET}
    {Colors.TEXT}Users are responsible for following Discord's terms and any
    applicable agreements. DiscORB is an independent project and
    is not affiliated with or endorsed by Discord or Valve.{Colors.RESET}

    {Colors.BOLD}{Colors.PROMPT}Press Enter to return to the menu.{Colors.RESET}

"""
    panel_print(credits_text)
    panel_input()