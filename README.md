# OBD-II Raspberry Pi Dashboard

A Python application that uses a Raspberry Pi and a Bluetooth OBD-II adapter to retrieve and display real-time vehicle data (Speed, RPM, Engine Load) on a simple graphical interface.

## Prerequisites

### Hardware
*   A Raspberry Pi (tested on Pi 4)
*   A Bluetooth OBD-II Adapter

### Software
*   Python 3
*   Required Python libraries. Install them using pip:
    ```bash
    pip install obd pygame
    ```

## Setup & Installation

1.  **Clone this repository to your Raspberry Pi.**

2.  **Configure the Bluetooth Connection:**
    You must pair the OBD-II adapter with your Raspberry Pi and bind it to a serial port (e.g., `/dev/rfcomm99`). This can be a complex process. This guide is a good reference for the required Linux commands:
    [hackster.io: Raspberry Pi Smart Car](https://www.hackster.io/tinkernut/raspberry-pi-smart-car-8641ca)

## Usage

Once the setup is complete, you can run the application.

*   To run with the default port (`/dev/rfcomm99`):
    ```bash
    python CarInterface.py
    ```

*   If you bound the adapter to a different port, specify it with the `--port` flag:
    ```bash
    python CarInterface.py --port /dev/your_rfcomm_port
    ```

Press the `ESC` key on a connected keyboard to close the application.
