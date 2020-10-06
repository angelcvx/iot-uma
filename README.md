# Tasks Implementation Selector (TIS) and Optimal Tasks Assigment Framework (OTAF)

Tasks Implementation Selector and Optimal Tasks Assignment Framework. Implementation by UMA.

## Information

The "IoT UMA" directory applies the OTAF to the IoT infrastructure installed at the School of Computer Science Engineering of the Universidad de Málaga. Experiments consider two scenarios. In the first one, the nodes reserve a fixed amount of resources dedicated to computation of offloaded tasks. In the second one (Scenario 2), the nodes do not reserve specific resources for offloaded tasks, so the feasibility of the task offloading process and the reduction in energy consumption will depend on the current nodes workload (randomized in each experiment from 0 to their maximal capabilities). The deployed mobile application is named `La Universidad Aumentada'. This app, developed by the Universidad de Málaga, uses augmented reality to show motivational messages from successful students. These messages are visible by scanning QR (Quick Response) codes spread over the university.

The "Benchmark" directory contains a Benchmark version of the TIS and OTAF, which allows setting the number of devices, tasks and configuration in the case of the TIS and devices and tasks in the case of the OTAF. The characteristics of the devices (CPU, RAM, workload, etc.) and tasks (connections, computational load, hardware and software requirements, time restrictions, etc.) are randomly generated.

## Requirements

- Python (https://www.python.org/). Remember to include python as environment variable. 
- Z3 solver for Python (https://pypi.org/project/z3-solver/).

## Usage

Go to the modules directory and run:  <python .\script_name.py>

## DOI

https://doi.org/10.5281/zenodo.4068123 (v1.0.0)

## License

-GNU GPLv3
