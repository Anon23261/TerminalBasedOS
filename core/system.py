import os
import importlib

commands = {}  # Stores command names and their corresponding handler functions

def register_command(name: str, handler: callable):
    """Registers a new command with its handler function."""
    commands[name] = handler

def handle_command(command: str):
    """Handles a user-entered command."""
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
