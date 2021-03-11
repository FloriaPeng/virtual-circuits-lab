from collections import namedtuple

class Circuit_element():

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.circuit_components = []

    
    # Returns a new tuple subclass named typename. The new subclass is used to create tuple-like objects that have fields accessible by attribute 
    # lookup as well as being indexable and iterable. 

    # Method creates tuple subclasses of type line or part, depending on partType, and then stores them in a list of circuit components
    def extract_parts(self):
        for key, value in self.raw_data.items():
            if value["partType"] == "line":
                line_object = namedtuple("Line", value.keys())(*value.values())
                self.circuit_components.append(line_object)
            else:
                part_object = namedtuple("Part", value.keys())(*value.values())
                self.circuit_components.append(part_object)

    def get_circuit_components(self):
        return self.circuit_components

    def print_circuit_components(self):
        for x in self.circuit_components:
            print(x)
