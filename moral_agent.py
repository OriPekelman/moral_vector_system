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

        # Emotional state initialization
        self.emotional_state = {
            "stress": 0.5,  # Range from 0 to 1
            "happiness": 0.5,
            "empathy": 0.5
        }

    def judge_situation(self, situation_vector):
        # Decision score influenced by emotions
        emotion_factor = 1 + (self.emotional_state["empathy"] - self.emotional_state["stress"])
        decision_score = np.dot(situation_vector, self.weights) * emotion_factor
        return decision_score

    def resolve_perfect_duty_conflict(self, duties_in_conflict):
        # Prioritize duties with higher weights in case of conflict
        return max(duties_in_conflict, key=lambda duty: self.weights[self.vector_space.duties_list.index(duty)])

    def allocate_resources_to_imperfect_duties(self):
        # Allocate resources proportionally based on inclinations, perceived utility, and available resources
        total_inclination = sum(self.inclinations)
        allocation_summary = ""

        if total_inclination > 0:
            for i, inclination in enumerate(self.inclinations):
                duty_name = self.vector_space.duties_list[len(self.vector_space.duties_list) - len(self.inclinations) + i]
                
                # Utility calculation with diminishing returns
                utility = (inclination / total_inclination) * (1 / (1 + self.time_allocation.get(duty_name, 0) * 0.1))
                time_allocated = utility * self.resources["time"]
                money_allocated = utility * self.resources["money"]

                # Allocation summary update
                if time_allocated <= self.resources["time"] and money_allocated <= self.resources["money"]:
                    allocation_summary += f"- {self.name} allocated {time_allocated:.2f} units of time and {money_allocated:.2f} units of money to {duty_name}.\n"
                    
                    # Update resources
                    self.resources["time"] -= time_allocated
                    self.resources["money"] -= money_allocated

                    # Emotional response to charity duties (increasing empathy)
                    if duty_name in ["charity", "community_support", "help_others"]:
                        self.emotional_state["empathy"] = min(1.0, self.emotional_state["empathy"] + 0.05)

        return allocation_summary

    def update_weights(self, feedback):
        learning_rate = 0.1
        emotional_adjustment = 1 + (self.emotional_state["happiness"] - self.emotional_state["stress"]) * 0.1
        self.weights += learning_rate * feedback * emotional_adjustment
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

    def adjust_emotional_state(self, situation_outcome):
        # Adjust emotional state based on outcome
        if situation_outcome > 0:
            self.emotional_state["happiness"] = min(1.0, self.emotional_state["happiness"] + 0.1)
            self.emotional_state["stress"] = max(0.0, self.emotional_state["stress"] - 0.1)
        else:
            self.emotional_state["stress"] = min(1.0, self.emotional_state["stress"] + 0.1)
            self.emotional_state["happiness"] = max(0.0, self.emotional_state["happiness"] - 0.1)

        # Empathy can increase with positive community-based outcomes
        if situation_outcome > 0.5:
            self.emotional_state["empathy"] = min(1.0, self.emotional_state["empathy"] + 0.05)