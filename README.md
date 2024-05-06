# ttm4115_project
Project for NTNU subject TTM4115 - Design of Communicating Systems, spring 2024

The main executabes are found in the root directory, and in the *web_display* directory. To execute the locations software, run:
```bash
python3 location.py
```
on the Raspberry Pi with the sense hat installed. This requires the python3 packages `stmypy`, `sense_hat` and `paho-mqtt` to be installed. To execute the server software, run:
```bash
python3 server.py
```
on the other Raspberry Pi. This requires the python3 packages `stmypy`, and `paho-mqtt` to be installed. Finally, to run the user interface, run:
```bash
python3 web_display/Skeleton_WebServer.py
```
on a personal machine and enter the link [http://localhost:12000/web_display/index.html](http://localhost:12000/web_display/index.html) in a web browser. All of these require an internet connection in some way for MQTT to work.

The *shared/* directory contains libraries which were originally planned to be shared and used from multiple different executables. Only *shared/mqtt_opts.py* ended up being so. *shared/availability_data.py* was originally planned to be used for communication between server and user interface, but was dropped in favour of JSON. *shared/charger_data.py* contains most of the implementation for the locations simulation.
