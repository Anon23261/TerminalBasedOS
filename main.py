import os
import importlib
from core.system_utils import register_system_commands

# Dictionary to store commands and their handlers
commands = {}  # Stores command names and their corresponding handler functions

def register_command(name: str, handler: callable):
    """Registers a new command with its handler function.
    
    Args:
        name (str): The name of the command to register.
        handler (callable): The function that handles the command.
    """
    commands[name] = handler

def handle_command(command: str):
    """Handles a user-entered command.
    
    Args:
        command (str): The full command entered by the user.
    """
    if not command:
        return

    args = command.split()
    cmd = args[0]
    if cmd in commands:
        try:
            commands[cmd](args[1:])  # Pass arguments to the handler
        except Exception as e:
            print(f"Error executing command '{cmd}': {e}")
    else:
        print(f"Command not found: {cmd}. Type 'help' for a list of commands.")

# Register built-in commands
def builtin_help(args):
    """Displays available commands."""
    print("Available commands:")
    for cmd in commands:
        print(f"  {cmd}")

def builtin_clear(args):
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def ghost_boot_screen():
    """Displays the custom Ghost OS boot screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "=" * 40)
    print("          ghost os loading...".center(40))
    print("      built for python and ghostsec".center(40))
    print("=" * 40 + "\n")

register_command("help", builtin_help)
register_command("clear", builtin_clear)

# Dynamically load extensions
def load_extensions():
    """Loads commands from the extensions folder."""
    extensions_dir = "extensions"
    if not os.path.exists(extensions_dir):
        os.makedirs(extensions_dir)

    for filename in os.listdir(extensions_dir):
        if filename.endswith(".py") and not filename.startswith("_"):
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f"extensions.{module_name}")
                if hasattr(module, "register"):
                    module.register(register_command)
            except Exception as e:
                print(f"Failed to load extension {module_name}: {e}")

# Boot sequence and startup
def main():
    """Main function to start Ghost OS."""
    ghost_boot_screen()
    load_extensions()
    register_system_commands(register_command)
    while True:
        try:
            user_input = input("ghost> ")
            handle_command(user_input)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting ghost os... Goodbye!")
            break

if __name__ == "__main__":
    main()
