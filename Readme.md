# COGNA Graphical Editor

## Requirements and Startup
You need at least Python 3.6 and the packages defined in the Requirements.txt file.
Start the editor by launching either "Run COGNA Editor.bat" or "Run COGNA Editor.sh" or by simply launching COGNA_Editor_entry.py with Python.

On a Linux based system you must install tkinter and pillow with the following lines:
- sudo apt install python3-tk
- sudo apt install python3-pil python3-pil.imagetk

## Description
This editor is supposed to allow an easier way of building and editing COGNA networks and architectures than scripting. The main advantage is a better overview due to the visualization of neural pathways while editing.

## General Usage
Change the content of the file "COGNA_PATH.config" to the path where you want your COGNA network files to be stored in. If the path does not exist, the editor will use a "Projects" folder in its root folder.

Start up the editor as described above. There you can edit one or multiple networks (shown in a tab bar at the top of the screen). The large area shows the topology of the network. You can navigate in there by holding the center mouse button for moving, scrolling the wheel for zooming, and pressing space to return to the default position. The blue cross marks the 0,0 coordinate. By pressing "g" you can toggle a grid layout. If it is active, a grid snap is active too.

The left side shows at the top the different tools you can use:
- S: The select tool. You can select all neurons, synapses and nodes with it to move them around, delete them with "del" and edit their parameters in the area below. If nothing is selected, you can edit the parameters of the network in general.
- N: The neuron tool. With left click you can place new neurons, with right click, you can remove them.
- C: The connection tool. With left click on a neuron you can start a new connection. Then click on a neuron, an output node or on another connection to connect it with this entity.
- I: The incode tool. With this you can include all other networks in the network folder of your current project. Only possible if another network exists, which enables a drop down list on the left side. You can connect the included network with your outer network if you defined input/output nodes in the inner network.
- E: The exchange tool. With this you can place nodes. Subnet input/output are used with an ID. Interface input/output are UDP networking nodes which can be given an ip address to send to or receive from, a port, and a channel, which defines the position of a message coming in on the same port. Subnet nodes can only be given an ID and therefore be activated, if the parameters input_nodes/output_nodes in the network parameters are larger than 0.

The top menu offers options to load/save a project/network and to import a network into another project. You can also in the Configuration tab edit multiple crucial parameters for the network, such as neuron types acting as templates for neurons, and neurotransmitters.

## File Format
The main file format is Json.

## Screenshot of Editor
![Example Screenshot Dark Mode](https://github.com/Cycrus/COGNA_Editor/blob/main/planning/editor_example_image.PNG)
