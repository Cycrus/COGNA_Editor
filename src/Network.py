from src.ParameterHandler import *


class Network:
    def __init__(self):
        self.neurons = []
        self.connections = []

        self.param = ParameterHandler()

        self.param.list["Activation threshold"] = 1.0
        self.param.list["Max activation"] = 50.0
        self.param.list["Min activation"] = 0.0
        self.param.list["Activation Backfall curvature"] = 1.0
        self.param.list["Activation Backfall steepness"] = 0.04
        self.param.list["Transmitter change curvature"] = 1.02
        self.param.list["Influenced transmitter"] = 0
        self.param.list["Influences transmitter"] = 0
        self.param.list["Transmitter influence direction"] = 1
        self.param.list["Random chance"] = 0
        self.param.list["Random activation value"] = 0.0
        self.param.list["Habituation threshold"] = 0.001
        self.param.list["Short habituation curvature"] = 0.65
        self.param.list["Short habituation steepness"] = 0.07
        self.param.list["Short dehabituation curvature"] = 1.0
        self.param.list["Short dehabituation steepness"] = 0.00000005
        self.param.list["Long habituation curvature"] = 0.35
        self.param.list["Long habituation steepness"] = 0.00005
        self.param.list["Long dehabituation curvature"] = 1.0
        self.param.list["Long dehabituation steepness"] = 0.000000000001
        self.param.list["Sensitization threshold"] = 5.0
        self.param.list["Short sensitization curvature"] = 0.65
        self.param.list["Short sensitization steepness"] = 0.07
        self.param.list["Short desensitization curvature"] = 1.0
        self.param.list["Short desensitization steepness"] = 0.00000005
        self.param.list["Long sensitization curvature"] = 1.02
        self.param.list["Long sensitization steepness"] = 0.0001
        self.param.list["Long desensitization curvature"] = 1.0
        self.param.list["Long desensitization steepness"] = 0.000000000001
        self.param.list["Presynaptic potential curvature"] = 0.60
        self.param.list["Presynaptic potential steepness"] = 0.3
        self.param.list["Presynaptic backfall curvature"] = 1.00
        self.param.list["Presynaptic backfall steepness"] = 0.0000002
        self.param.list["Base weight"] = 1.0
        self.param.list["Max weight"] = 5.0
        self.param.list["Min weight"] = 0.0
        self.param.list["Activation type"] = 1
        self.param.list["Activation function"] = 3
        self.param.list["Learning type"] = 1
        self.param.list["Transmitter type"] = 0
        self.param.list["Transmitter Number"] = 1
        self.param.list["Transmitter backfall curvature"] = 1.0
        self.param.list["Transmitter backfall steepness"] = 0.0000001
        self.param.list["Max transmitter weight"] = 5.0
        self.param.list["Min transmitter weight"] = 0.0

        print(self.param.list["Min weight"])