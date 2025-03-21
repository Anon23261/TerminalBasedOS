import os
import platform
import subprocess
import socket
from cryptography.fernet import Fernet  # Requires `cryptography` library

def register_builtin_commands(register_command):
    """Registers all built-in commands."""
    register_command("help", builtin_help)
    register_command("clear", builtin_clear)
    register_command("sysinfo", builtin_sysinfo)
    register_command("ping", builtin_ping)
    register_command("portscan", builtin_portscan)
    register_command("encrypt", builtin_encrypt)

def builtin_help(args):
    """Displays available commands."""
    print("Available commands:")
    for cmd in commands:
        print(f"  {cmd}")

def builtin_clear(args):
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def builtin_sysinfo(args):
    """Displays system information."""
    print("System Information:")
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Version: {platform.version()}")
    print(f"  Python: {platform.python_version()}")

def builtin_ping(args):
    """Performs a basic ping to a specified host."""
    if not args:
        print("Usage: ping <hostname>")
        return
    hostname = args[0]
    try:
        response = subprocess.run(
            ["ping", "-c", "4", hostname] if os.name != "nt" else ["ping", hostname],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(response.stdout)
    except Exception as e:
        print(f"Error executing ping: {e}")

def builtin_portscan(args):
    """Performs a basic port scan on a specified host."""
    if not args:
        print("Usage: portscan <hostname>")
        return
    hostname = args[0]
    print(f"Scanning ports on {hostname}...")
    try:
        for port in range(1, 1025):  # Scan ports 1-1024
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((hostname, port)) == 0:
                    print(f"Port {port}: OPEN")
    except Exception as e:
        print(f"Error during port scan: {e}")

def builtin_encrypt(args):
    """Encrypts a file using a generated key."""
    if len(args) < 1:
        print("Usage: encrypt <file_path>")
        return
    file_path = args[0]
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    try:
        key = Fernet.generate_key()
        cipher = Fernet(key)
        with open(file_path, "rb") as f:
            data = f.read()
        encrypted_data = cipher.encrypt(data)
        with open(file_path + ".enc", "wb") as f:
            f.write(encrypted_data)
        print(f"File encrypted successfully. Key: {key.decode()}")
    except Exception as e:
        print(f"Error encrypting file: {e}")
