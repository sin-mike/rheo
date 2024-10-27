# REMG Serial Interface Module

## Overview

The `remgSerialInterface` module provides a class to interface with a serial port, read incoming data, and store it in a deque for further processing. This module is designed to work with high baud rates and can handle a large amount of incoming data efficiently.

## Installation

To install the required dependencies, run the following command:

```bash
pip install -e . --no-cache
```


# Usage

## Example

Example usage of the `remgSerialInterface` class:

```python
from REMG import remgSerialInterface

rheo = remgSerialInterface('/dev/cu.usbserial-143101')
rheo.start_reading()

while True:
    if len(rheo.inc_data)>0:
        print(list(rheo.inc_data.popleft()), end='\r')
    time.sleep(0.005)
```

## Example jupyter notebook of streaming to teleplot 

`Examples/remg_streaming.ipynb` — shows how to parse the data and stream to teleplot. 