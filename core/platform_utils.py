import os
import subprocess
import platform
import logging

# Configure logging
logging.basicConfig(filename="ghost_os.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def check_dependencies(dependencies):
    """Checks if required dependencies are installed."""
    missing = []
    for dep in dependencies:
        if subprocess.run(["which", dep], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
            missing.append(dep)
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}. Please install them and try again.")
        logging.error(f"Missing dependencies: {', '.join(missing)}")
        return False
    return True

def check_linux_kernel():
    """Checks if the system is running a Linux kernel and verifies the version."""
    if os.name != "posix":
        print("This feature is only available on Linux.")
        return False
    kernel_name = platform.system()
    if kernel_name != "Linux":
        print(f"Unsupported kernel: {kernel_name}. Only Linux is supported.")
        return False
    kernel_version = platform.release()
    print(f"Linux kernel detected: {kernel_version}")
    return True

def check_partitions():
    """Validates Linux system partitions."""
    print("Checking system partitions...")
    if not check_linux_kernel():
        return False
    try:
        # Use `df` command to check mounted partitions
        result = subprocess.run(["df", "-h"], stdout=subprocess.PIPE, text=True)
        print(result.stdout)
        # Simulate checking for required partitions
        required_partitions = ["/boot", "/root", "/home"]
        for partition in required_partitions:
            if partition not in result.stdout:
                print(f"Missing required partition: {partition}")
                return False
        print("All required partitions are verified.")
        return True
    except Exception as e:
        print(f"Error checking partitions: {e}")
        return False

def update_linux_kernel():
    """Ensures the system is running the newest Linux kernel."""
    if not check_linux_kernel():
        return
    try:
        print("Checking for Linux kernel updates...")
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        # Ensure the Linux kernel package is installed
        subprocess.run(["sudo", "apt-get", "install", "-y", "linux-image-generic"], check=True)
        print("Linux kernel updated successfully. A reboot may be required.")
    except Exception as e:
        print(f"Error updating Linux kernel: {e}")

def load_raspi_firmware():
    """Loads and updates Raspberry Pi firmware if running on a Raspberry Pi."""
    if not check_linux_kernel():
        return
    try:
        # Check if running on Raspberry Pi
        with open("/proc/device-tree/model", "r") as f:
            model = f.read().strip()
        if "Raspberry Pi" not in model:
            print("This system is not a Raspberry Pi. Skipping firmware loading.")
            return
        print("Checking for Raspberry Pi firmware...")
        firmware_path = "/boot/firmware"
        if not os.path.exists(firmware_path):
            print(f"Firmware path not found: {firmware_path}. Installing firmware...")
            subprocess.run(["sudo", "apt-get", "install", "-y", "raspberrypi-bootloader", "raspberrypi-kernel"], check=True)
        else:
            print(f"Firmware path exists: {firmware_path}. Updating firmware...")
            subprocess.run(["sudo", "apt-get", "install", "--only-upgrade", "raspberrypi-bootloader", "raspberrypi-kernel"], check=True)
        print("Raspberry Pi firmware updated successfully. A reboot may be required.")
    except FileNotFoundError:
        print("Device model information not found. Ensure this is a Raspberry Pi.")
    except Exception as e:
        print(f"Error updating Raspberry Pi firmware: {e}")

def build_and_install_linux_kernel():
    """Builds and installs the latest Linux kernel from source."""
    if not check_linux_kernel():
        return
    if not check_dependencies(["wget", "make", "gcc"]):
        return
    try:
        print("Downloading the latest Linux kernel source...")
        logging.info("Downloading the latest Linux kernel source...")
        subprocess.run(["wget", "-O", "linux.tar.xz", "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.5.tar.xz"], check=True)
        print("Extracting the Linux kernel source...")
        subprocess.run(["tar", "-xf", "linux.tar.xz"], check=True)
        os.chdir("linux-6.5")
        print("Building the Linux kernel (this may take some time)...")
        subprocess.run(["make", "defconfig"], check=True)
        subprocess.run(["make", "-j$(nproc)"], check=True)
        print("Installing the Linux kernel...")
        subprocess.run(["sudo", "make", "modules_install"], check=True)
        subprocess.run(["sudo", "make", "install"], check=True)
        print("Linux kernel built and installed successfully. A reboot is required.")
        logging.info("Linux kernel built and installed successfully.")
    except Exception as e:
        print(f"Error building and installing Linux kernel: {e}")
        logging.error(f"Error building and installing Linux kernel: {e}")
    finally:
        os.chdir("..")  # Return to the original directory

def install_latest_raspi_firmware():
    """Downloads and installs the latest Raspberry Pi firmware."""
    if not check_linux_kernel():
        return
    if not check_dependencies(["rpi-update"]):
        return
    try:
        # Check if running on Raspberry Pi
        with open("/proc/device-tree/model", "r") as f:
            model = f.read().strip()
        if "Raspberry Pi" not in model:
            print("This system is not a Raspberry Pi. Skipping firmware installation.")
            logging.info("System is not a Raspberry Pi. Skipping firmware installation.")
            return
        print("Downloading and installing the latest Raspberry Pi firmware...")
        subprocess.run(["sudo", "rpi-update"], check=True)
        print("Raspberry Pi firmware installed successfully. A reboot is required.")
        logging.info("Raspberry Pi firmware installed successfully.")
    except FileNotFoundError:
        print("Device model information not found. Ensure this is a Raspberry Pi.")
        logging.error("Device model information not found. Ensure this is a Raspberry Pi.")
    except Exception as e:
        print(f"Error installing Raspberry Pi firmware: {e}")
        logging.error(f"Error installing Raspberry Pi firmware: {e}")
