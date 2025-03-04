# Prompt Rose

<img src="icon.png" alt="Prompt Rose Logo" width="128" height="128">

## 🌹 What is Prompt Rose?

"Prompt Rose" is a sleek productivity tool that, with just a press and hold of the Alt key (customizable), brings up a radial menu similar to those found in the Battlefield game series. Instead of game commands, this menu is filled with quick prompt instructions designed for Large Language Models (LLMs). This eliminates the need for users to search through their notebooks for prompts.

Designed for Windows platforms, "Prompt Rose" also allows for prompt management directly from the right-click system tray.

## ✨ Features

- **Intuitive Radial Menu**: Press and hold your hotkey to bring up a wheel of prompts
- **Quick Selection**: Simply move your mouse in the direction of the desired prompt and release
- **Customizable Prompts**: Add, edit, or remove prompts through an easy-to-use interface
- **Customizable Hotkey**: Choose your preferred activation key combination
- **Direct Pasting**: Automatically pastes your selected prompt into the active application
- **System Tray Integration**: Minimal footprint with easy access to all functions
- **Persistent Settings**: Your configurations are saved and loaded between sessions

## 🚀 Quick Start

1. Execute `start.bat` to launch Prompt Rose
2. Press and hold the Alt key (default) to display the prompt wheel
3. Move your mouse to select a prompt
4. Release the key to paste the selected prompt into your current application
5. Right-click the system tray icon for additional options

## 🛠️ Requirements

- Windows 10 or higher
- Python with PyQt6, keyboard, and pyperclip packages
- Conda environment named "promptrose" (used by start.bat)

## 💻 Files

- `prompt_wheel.py` - Main application
- `icon.png` / `icon.ico` - Application icons
- `create_icon.py` - Script used to generate the icon
- `start.bat` - Launcher script that activates conda environment
- `.gitignore` - Git ignore file

## 🔧 Usage

### System Tray Options

- **Show Wheel**: Manually display the prompt wheel
- **Manage Prompts**: Add, edit, or delete prompts
- **Settings**: Configure hotkeys and paste behavior
- **Exit**: Close the application

## 📝 License

This project is licensed under the MIT License.

---

*Made with ❤️ by a passionate developer*
