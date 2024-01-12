# STIM300 - Serial Communication with GUI

This Python project provides a graphical user interface for serial communication. It includes features for reading and displaying serial data, running test sequences, and more.

## Table of Contents

- [Environment Setup](#environment-setup)
- [Running the Code](#running-the-code)
- [System Overview](#system-overview)
- [Usage Instructions](#usage-instructions)

## Environment Setup

### 1. Install Python and Virtual Environment

```bash
sudo apt update
sudo apt install python3 python3-venv
```

## Running the Code 

#### 1. Clone Repository to your machine

```
git clone https://github.com/angelinath21/STIM300
cd STIM300
```

#### 2. Activate virtual env

```
python3 -m venv venv
source venv/bin/activate
```

#### 4. Setup and launch with launch script

```
chmod +x launch.sh
./launch.sh run
```

## System Overview
##### The Serial Communication GUI consists of a graphical interface for interacting with serial devices. It includes features such as reading and displaying serial data, running test sequences, and more.

## Usage Instructions

#### 1. Sample Frequency:
Enter the desired sample frequency (in Hz) in the provided input field.
Click the "Enter" button to set the sample frequency.

#### 2. Test Buttons:
Click "Test Auto," "Test Normal," or "Test Serial" to add corresponding test sequences to the display.

#### 3. Run Test:
Click the "Run Test" button to start the serial communication based on the defined sample frequency and test sequences.

#### 4. Serial Read Display:
Serial data received will be displayed in the "Serial Read Display" section.

#### 5. Test Sequence:
The test sequence can be entered in the "Test Sequence" section.

#### 6. Clear Test Sequence:
Click "Clear Test Sequence" to clear the test sequence section.

#### 7. Start Serial:
Click "Start Serial" to initiate serial communication.

#### 8. Status Box:
The "Status Box" provides information about the system's current status.

