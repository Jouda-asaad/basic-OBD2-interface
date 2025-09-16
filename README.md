# OBD-II Raspberry Pi Dashboard

A Python application that uses a Raspberry Pi and an OBD-II adapter (Bluetooth or USB) to retrieve and display real-time vehicle data (Speed, RPM, Engine Load) on a simple graphical interface.

## Prerequisites

### Hardware
*   A Raspberry Pi (tested on Pi 4)
*   An OBD-II Adapter (USB or Bluetooth). Note: The setup for Bluetooth adapters requires manual configuration (see below).

### Software
*   Python 3
*   Required Python libraries. Install them using pip:
    ```bash
    pip install obd pygame
    ```

## Setup & Installation

1.  **Clone this repository to your Raspberry Pi.**

2.  **Configure the Bluetooth Connection (Bluetooth adapters only):**

    a. **Scan for and pair the adapter**
    Use the `bluetoothctl` command to find your device's MAC address and pair with it.
    ```bash
    bluetoothctl
    scan on
    # Wait for your device to appear, then copy the MAC address
    pair <your_mac_address>
    # Enter the PIN, usually 1234 or 0000
    trust <your_mac_address>
    exit
    ```
    b. **Bind the device to a serial port**
    Use the `rfcomm` command to bind the MAC address to a port.
    ```bash
    sudo rfcomm bind 99 <your_mac_address> 1
    ```
    This will create a `/dev/rfcomm99` device that the application can use.

## Usage

Once the setup is complete, you can run the application.

*   **For USB Adapters:**
    The script can auto-detect the serial port for most USB ELM327 adapters. Simply run:
    ```bash
    python CarInterface.py
    ```

*   **For Bluetooth Adapters:**
    If you have configured a Bluetooth adapter using `rfcomm` (as described in the setup), you must specify the port:
    ```bash
    python CarInterface.py --port /dev/rfcomm99
    ```
    Replace `/dev/rfcomm99` with the port you created.

Press the `ESC` key on a connected keyboard to close the application.
