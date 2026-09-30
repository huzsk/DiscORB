<div align="center">
<img src="https://huzske.com/discorb.png" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.7+-3572A5?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20Only-555555?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/huzsk/DiscORB)
[![License](https://img.shields.io/badge/License-GPL%20v3-c0392b?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](./LICENSE)

<br/>

*Small tool. Big download energy.*

<br/>

[Get Started](#installation) &nbsp;·&nbsp; [How it works](#how-it-works) &nbsp;·&nbsp; [Steam Mode](#steam-quest-mode) &nbsp;·&nbsp; [Usage](#usage) &nbsp;·&nbsp; [Structure](#project-structure) &nbsp;·&nbsp; [Legal](#legal-notice)

</div>

<br/>

<div align="center">
<img width="340" alt="image" src="https://huzske.com/pyorb.png" style="border-radius: 16px"/>
</div>

## What is this

DiscORB is a lightweight Python tool that simulates Discord detectable game processes for Orb quests without requiring the actual games to be installed.
No client changes. No injected code. No unusual network activity. Just a process name appearing in your task list — the only thing Discord looks for.

> **Educational purposes only.** This tool is intended for educational and research purposes to better understand Discord’s game detection behavior and process-level experimentation. Use it responsibly and ensure your use complies with Discord’s terms of service and any applicable rules or policies.

<br/>

## 🚨 Steam Quest Mode

Some games use a more advanced detection system. Instead of relying only on the process name, Discord may also check whether Steam recognizes the game as actively downloading. Because of that extra verification, standard spoofing methods may not work. Steam Quest Mode is designed to account for that additional check.

### How it works

Search for the game directly in the tool and it pulls the required Steam metadata automatically, including install paths, depot info, and your Steam ID. It then creates a temporary app manifest and executable in the expected Steam folders so Discord can detect the game as active. When you're finished, the generated files are removed automatically.

**Supported:**
`Any game requiring a Steam manifest` &nbsp; `Fully automatic, no manual AppID lookup` &nbsp; `Uses your real Steam ID` &nbsp; `Searches demos and full games separately` &nbsp; `Auto-cleanup on exit`

> **Tip:** If a quest targets a demo, search for `"Toxic Commando Demo"` instead of `"Toxic Commando"`. They have different AppIDs and the wrong one won't trigger the quest.

<br/>

## Features

**Automatic Game Detection** pulls Discord’s latest detectable game list and includes smart search for names and abbreviations like PUBG, LoL, and CSGO. Launching is handled automatically in the background.

**Self-Executing Timer & Embedded Config** creates renamed game executables that run their own countdown timer when opened, with the selected duration and cleanup settings built in. No extra console window is shown.

**Automatic Cleanup (`AUTO_DELETE`)** removes generated executables, folders, and temporary Steam manifest files once the timer finishes.

**Multi-Game Support** allows multiple simulated game processes to run at the same time. Each runs independently so several quests can be handled in one session.

**Backup Database** uses a GitHub-hosted fallback if Discord’s API is unavailable, keeping game detection available when the primary source goes down.

**Custom Game** uses a GitHub-hosted fallback if Discord’s API is unavailable, keeping game detection available when the primary source goes down.

**Polished Interface** uses a colored terminal layout with loading animations and cleaner navigation for a more refined experience.

<br/>

## Why this method works

Discord's game detection reads your Windows process list. It sees `TslGame.exe` and assumes you're playing PUBG. There is no technical mechanism in place to verify whether that process is the actual game or a renamed executable. The name is all it checks.

To detect this method, Discord would need kernel-level anti-cheat software comparable to Valorant's Vanguard deep system access, raised privacy concerns, a broken promise of being a lightweight chat app. That is not happening for cosmetic orb quests.

**What this is not:** This tool does not inject code into Discord's console, modify client files, or send fake API requests. Those methods leave traces. Discord can detect when their JavaScript has been tampered with. Our approach leaves Discord's client completely untouched. The tool uses Discord's own public API to fetch the game list. No client modification. No integrity violations.

<br/>

## Requirements

Python 3.7 or higher, Windows only. Internet connection for database fetching. Discord must be running the spoofer only works when Discord is active and scanning processes.

<br/>

## Installation

```bash
git clone https://github.com/huzsk/DiscORB.git
cd DiscORB
pip install -r requirements.txt
```

<br/>

## Usage

```bash
python discorb.py
```

Or via the package entry point:

```bash
python -m discorb
```

### Menu options

`1` Search game database by name or abbreviation

`2` Custom game, enter a custom executable name

`3` Steam special quest mode

`4` Credits and project info

`5` Exit

### Completing all quests in 15 minutes

Launch the tool and select your first game. Once it starts, press Enter to return to the main menu and choose another. Repeat as needed without opening additional windows. Each process runs independently in parallel, allowing Discord to detect them at the same time. Let the timer finish, then close the tool when you're done.

<br/>

## How it works

The tool pulls Discord’s live detectable-game list from its official API and identifies the exact executable name associated with each title. It then creates a renamed copy of the spoofer executable in the configured location and embeds the selected settings directly into it.

Each generated executable runs as a standalone countdown timer. When the timer ends, it can automatically remove the generated files and any empty folders if AUTO_DELETE is enabled.

Steam Quest Mode adds Steam-specific metadata by creating a temporary `appmanifest_<appid>.acf` file in `steamapps/` and places the executable in `steamapps/common/<game>/`, satisfying Discord's additional manifest check for games like Marathon or Toxic Commando.

<br/>

## Project Structure

```
DiscORB/
├── discorb.py          Main entry point
├── DiscORB/
│   ├── __init__.py        Version and author metadata
│   ├── __main__.py        Package entry point, --timer-mode support
│   ├── config.py          Centralized configuration with settings.py overrides
│   ├── faker.py           Fake executable creation and launch logic
│   ├── discord_db.py      Game database loading, search, and selection
│   ├── steam.py           Steam registry helpers and manifest generation
│   ├── updater.py         Auto-update from GitHub releases
│   ├── net.py             HTTP helpers
│   ├── ui.py              Terminal colors, animations, prompts
│   └── errors.py          Custom exception hierarchy
├── settings.py            User-editable configuration
├── requirements.txt
```

<br/>

## Configuration

User-configurable options are stored in `settings.py` at the project root. These values are loaded at startup and override the defaults in `DiscORB/config.py`. including runtime preferences and API timeout settings. The application version is assigned from the Git tag used during the build process and should not be edited manually, as doing so can interfere with update detection.

<br/>

## Auto-updater

When a new version tag is pushed, GitHub Actions builds a standalone Windows executable using PyInstaller and publishes it as a GitHub Release. The tool checks for updates on launch, downloads the new binary, swaps it in place, and restarts automatically. No Python installation needed to run the distributed executable.

<br/>

## Legal Notice

**Educational purposes only. No commercial use.**

This tool is provided strictly for educational and research purposes to study how Discord's game detection system works and to explore process manipulation techniques. Commercial use, distribution, or sale is strictly prohibited.

Users are solely responsible for compliance with all applicable laws, Discord's Terms of Service, and any other relevant agreements. The developers do not condone misuse and are not responsible for any consequences resulting from use of this software. No warranties or guarantees are provided. Use at your own risk.

Misuse of this tool may violate Discord's Terms of Service.

<br/>

## License

GPL v3. Attribution required. Modified versions must also be GPL v3. Source code must be provided with any distribution. Commercial use is strictly prohibited. See [LICENSE](./LICENSE) for full terms.

<br/>

<div align="center">

made and designed by **Huzske | Tombstoned**

</div>
