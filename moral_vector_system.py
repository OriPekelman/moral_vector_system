import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.stats import norm
import datetime
import random
import json

# Abstract Model of Moral Duties
class MoralAbstractModel:
    def __init__(self):
        self.duties = {
            "perfect": [
                "honesty", "non_harm", "keep_promises", "respect_rights",
                "justice", "non_stealing", "truthfulness", "avoid_exploitation",
                "non_manipulation", "no_false_testimony"
            ],
            "imperfect": [
                "self_improvement", "help_others", "charity", "develop_talents",
                "promote_welfare", "environmental_care", "fairness", "education",
                "community_support", "personal_growth"
            ]
        }

    def get_all_duties(self):
        return self.duties["perfect"] + self.duties["imperfect"]

# Vector Representation and Operations
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

# Individual Moral Agent
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

# Environment Representation (Situations and Temporal Tracking)
class MoralWorld:
    def __init__(self, world_data):
        self.situations = [
            {"name": situation["name"], "description": situation["description"], "timestamp": datetime.datetime.fromisoformat(situation["timestamp"]), "situation_vector": np.array(situation["situation_vector"])}
            for situation in world_data["situations"]
        ]

    def get_situations_over_time(self):
        return self.situations

# Visualizer for Moral Judgments and Vector Evolution
class Visualizer:
    def visualize_vectors(self, agents, situations):
        pca = PCA(n_components=2)
        data = []
        labels = []
        colors = []

        for agent in agents:
            data.append(agent.weights)
            labels.append(f'{agent.name} Weights')
            colors.append('r')

        for situation in situations:
            data.append(situation["situation_vector"])
            labels.append(f'Situation: {situation["name"]}')
            colors.append('b')

        data = np.vstack(data)
        reduced_data = pca.fit_transform(data)

        plt.figure(figsize=(10, 8))
        for i, point in enumerate(reduced_data):
            plt.scatter(point[0], point[1], color=colors[i], label=labels[i] if i < len(agents) or i == len(agents) else "")
        
        plt.title('Moral Vectors in Reduced Space')
        plt.xlabel('Moral Prioritization Spectrum')
        plt.ylabel('Conflict Sensitivity Dimension')
        plt.legend()
        plt.show()

    def visualize_weight_changes_over_time(self, agents):
        plt.figure(figsize=(12, 8))
        for agent in agents:
            if len(agent.weight_history) > 0:
                timestamps, weights = zip(*agent.weight_history)
                weights = np.array(weights)
                for i in range(weights.shape[1]):
                    plt.plot(timestamps, weights[:, i], label=f'{agent.name} - Duty {i+1}')
        
        plt.title('Weight Changes Over Time')
        plt.xlabel('Time')
        plt.ylabel('Weight Value')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Learning Module for Adaptive Weights
class LearningModule:
    def __init__(self, agent):
        self.agent = agent

    def provide_feedback(self, situation, outcome):
        # Simple feedback mechanism (for demonstration purposes)
        ideal_outcome = random.uniform(0, 1)  # Assume an arbitrary ideal outcome
        feedback = ideal_outcome - outcome
        return feedback

    def adjust_weights(self, situation_vector, outcome):
        feedback = self.provide_feedback(situation_vector, outcome)
        self.agent.update_weights(feedback)

# Storytelling Functionality
class StoryGenerator:
    def __init__(self, agents, world):
        self.agents = agents
        self.world = world

    def generate_story(self):
        story = """# Moral Scenario Story

The world is filled with individuals who have different perspectives and duties they value. Let's meet our agents and understand the choices they make in different situations.\n"""
        for agent in self.agents:
            story += f"\n## Agent: {agent.name} ({agent.social_class})\n"
            story += f"**Description**: {agent.description}\n"
            story += f"**Initial Weights**: {agent.weights.tolist()}\n"
            story += f"**Initial Inclinations**: {agent.inclinations.tolist()}\n"
            story += f"**Resources**: Time - {agent.resources['time']}, Money - {agent.resources['money']}\n"

        for situation in self.world.get_situations_over_time():
            story += f"\n### Situation: {situation['name']}\n"
            story += f"**Description**: {situation['description']}\n"
            for agent in self.agents:
                outcome = agent.judge_situation(situation["situation_vector"])
                story += f"\n#### {agent.name}'s Decision Score: {outcome:.2f}\n"
                decision = 'support' if outcome > 0 else 'oppose'
                story += f"**Decision**: {agent.name} decides to {decision} the situation.\n"
                perfect_duties, imperfect_duties = agent.map_situation_to_duties(situation["situation_vector"])
                story += f"**Perfect Duties Considered**: {perfect_duties}\n"
                story += f"**Imperfect Duties Considered**: {imperfect_duties}\n"
                story += f"**Effects of Judgments**: {agent.name} considers the impact of the situation as follows:\n"
                for duty, value in perfect_duties.items():
                    story += f"- Perfect Duty ({duty}): Impact Value = {value:.2f}\n"
                for duty, value in imperfect_duties.items():
                    story += f"- Imperfect Duty ({duty}): Impact Value = {value:.2f}\n"
                story += f"**Choices and Resource Allocation**:\n"
                agent.allocate_resources_to_imperfect_duties()
                story += "\n"
                resource_allocation = agent.allocate_resources_to_imperfect_duties()
                if resource_allocation:
                    story += resource_allocation
                else:
                    story += "No resources were allocated.\n"
                story += "\n"
        return story

# Main Logic for Testing the System
if __name__ == "__main__":
    # Load data from JSON file
    with open("moral_scenario.json", "r") as infile:
        data = json.load(infile)

    # Initialize agents and world from the JSON data
    agents = [MoralAgent(agent_data) for agent_data in data["agents"]]
    world = MoralWorld(data["world"])
    visualizer = Visualizer()
    story_generator = StoryGenerator(agents, world)

    # Generate and print the story
    story = story_generator.generate_story()
    print(story)

    # Process each agent for each situation
    learning_module = LearningModule(agents[0])
    for situation in world.get_situations_over_time():
        for agent in agents:
            outcome = agent.judge_situation(situation["situation_vector"])
            print(f"Agent {agent.name} Decision Score at {situation['timestamp']}: {outcome}")
            learning_module.agent = agent
            learning_module.adjust_weights(situation["situation_vector"], outcome)
            agent.allocate_resources_to_imperfect_duties()

    # Visualizing moral vectors and weight changes over time for all agents in a single plot
    visualizer.visualize_vectors(agents, world.get_situations_over_time())
    visualizer.visualize_weight_changes_over_time(agents)

    # Save the story to a JSON file
    with open("moral_story_output.json", "w") as outfile:
        json.dump({"story": story}, outfile, indent=4)

    # Save the story to a Markdown file
    with open("moral_story_output.md", "w") as mdfile:
        mdfile.write(story)
