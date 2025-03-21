# Ghost OS

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Raspberry%20Pi-orange)

Ghost OS is a terminal-based operating system built with Python. It supports custom commands, extensions, and platform-specific features, making it ideal for Python developers and cybersecurity enthusiasts.

---

## ⚠️ Warning

Ghost OS is a tool designed for **ethical use only**. Misuse of this software for malicious purposes is strictly prohibited and may violate laws in your jurisdiction. Always ensure you have proper authorization before using any cybersecurity tools.

---

## Features

- **Dynamic Boot Sequence**: Includes a loading screen and partition checks.
- **Modular Architecture**: Core system, commands, and platform-specific tasks are modularized.
- **Cross-Platform Compatibility**: Works on Linux systems and supports Raspberry Pi firmware.
- **Cybersecurity Tools**: Includes port scanning and file encryption.

---

## Built-in Commands

- `help`: Displays available commands.
- `clear`: Clears the terminal screen.
- `sysinfo`: Displays system information.
- `ping`: Performs a basic ping to a specified host.
- `portscan`: Scans ports on a specified host.
- `encrypt`: Encrypts a file using a generated key.

---

## Platform-Specific Features

- Linux kernel compatibility.
- Partition check for Linux systems.
- Raspberry Pi firmware loading.

---

## Extensions

You can add custom commands by placing Python files in the `extensions` folder. Each file should define a `register` function to register commands.

---

## Ethical Use

Ghost OS is intended for **educational purposes** and **ethical cybersecurity practices**. By using this software, you agree to:

1. Use it only in environments where you have explicit permission.
2. Avoid using it for malicious or illegal activities.
3. Respect the privacy and security of others.

---

## License

This project is licensed under the [MIT License](./LICENSE).

