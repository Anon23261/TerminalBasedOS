import os
import time  # Import time for loading animation
import logging  # Import logging for logging messages
from core.system import register_command, handle_command, load_extensions
from core.commands import register_builtin_commands
from core.platform_utils import (
    load_extensions,
    check_partitions,
    check_linux_kernel,
    build_and_install_linux_kernel,
    install_latest_raspi_firmware,
)

def ghost_boot_screen():
    """Displays the custom Ghost OS boot screen with a loading animation."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "=" * 40)
    print("          GHOST OS BOOTING...".center(40))
    print("      BUILT FOR PYTHON AND GHOSTSEC".center(40))
    print("=" * 40 + "\n")
    print("Initializing system...")
    for i in range(1, 6):
        print(f"Loading... [{i * 20}%]")
        time.sleep(0.5)  # Simulate loading delay
    print("\nSystem initialized successfully!\n")

def main():
    """Main function to start Ghost OS."""
    ghost_boot_screen()
    if not check_linux_kernel():
        print("Linux kernel check failed. Ensure you are running a supported Linux system.")
        return
    build_and_install_linux_kernel()  # Build and install the latest Linux kernel
    if not check_partitions():
        print("Partition check failed. Ensure proper Linux partitions are set up.")
        return
    install_latest_raspi_firmware()  # Install the latest Raspberry Pi firmware
    print("A reboot is recommended to apply kernel and firmware updates.")
    logging.info("System initialization complete. Reboot recommended.")
    load_extensions()
    register_builtin_commands(register_command)
    while True:
        try:
            user_input = input("ghost> ")
            handle_command(user_input)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Ghost OS... Goodbye!")
            logging.info("Exiting Ghost OS.")
            break

if __name__ == "__main__":
    main()
