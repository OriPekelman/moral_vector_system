import numpy as np
import datetime
from moral_abstract import MoralAbstractModel
from moral_vector_space import MoralVectorSpace

class MoralAgent:
    def __init__(self, agent_data):
        self.name = agent_data["name"]
        self.social_class = agent_data["social_class"]
        self.description = agent_data["description"]
        self.weights = np.array(agent_data["weights"])
        self.inclinations = np.array(agent_data["inclinations"])
        self.resources = agent_data["resources"]
        self.time_allocation = agent_data["time_allocation"]
        self.vector_space = MoralVectorSpace(MoralAbstractModel())
        self.weight_history = []

    def judge_situation(self, situation_vector):
        decision_score = np.dot(situation_vector, self.weights)
        return decision_score

    def resolve_perfect_duty_conflict(self, duties_in_conflict):
        # Strict enforcement of perfect duties
        return min(duties_in_conflict, key=lambda duty: self.weights[self.vector_space.duties_list.index(duty)])

    def allocate_resources_to_imperfect_duties(self):
        # Allocate resources proportionally based on inclinations and available resources
        total_inclination = sum(self.inclinations)
        allocation_summary = ""
        if total_inclination > 0:
            for i, inclination in enumerate(self.inclinations):
                duty_name = self.vector_space.duties_list[len(self.vector_space.duties_list) - len(self.inclinations) + i]
                allocation = (inclination / total_inclination)
                time_allocated = allocation * self.resources["time"]
                money_allocated = allocation * self.resources["money"]
                if time_allocated <= self.resources["time"] and money_allocated <= self.resources["money"]:
                    allocation_summary += f"- {self.name} allocated {time_allocated:.2f} units of time and {money_allocated:.2f} units of money to {duty_name}.\n"
        return allocation_summary

    def update_weights(self, feedback):
        learning_rate = 0.1
        self.weights += learning_rate * feedback
        self.weight_history.append((datetime.datetime.now(), self.weights.copy()))

    def map_situation_to_duties(self, situation_vector):
        perfect_duties = {}
        imperfect_duties = {}
        
        for i, value in enumerate(situation_vector):
            duty_name = self.vector_space.duties_list[i]
            if duty_name in self.vector_space.duties_list[:len(MoralAbstractModel().duties["perfect"])]:
                perfect_duties[duty_name] = value * self.weights[i]
            else:
                imperfect_duties[duty_name] = value * self.inclinations[i - len(MoralAbstractModel().duties["perfect"])]
        
        return perfect_duties, imperfect_duties
