import numpy as np
from moral_abstract import MoralAbstractModel

class MoralVectorSpace:
    def __init__(self, abstract_model):
        self.duties_list = abstract_model.get_all_duties()
        self.num_duties = len(self.duties_list)

    def encode_situation(self, duty_values):
        if len(duty_values) != self.num_duties:
            raise ValueError("Duty values length must match the number of duties.")
        return np.array(duty_values)

    def encode_situation_with_uncertainty(self, duty_values, uncertainties):
        if len(duty_values) != self.num_duties or len(uncertainties) != self.num_duties:
            raise ValueError("Duty values and uncertainties length must match the number of duties.")
        return [(value, uncertainty) for value, uncertainty in zip(duty_values, uncertainties)]
