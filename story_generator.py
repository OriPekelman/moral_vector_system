class StoryGenerator:
    def __init__(self, agents, world):
        self.agents = agents
        self.world = world

    def generate_story(self):
        story = """# Moral Scenario Story

The world is filled with individuals who have different perspectives and duties they value. Let's meet our agents and understand the choices they make in different situations.
"""
        for agent in self.agents:
            story += f"\n## Agent: {agent.name} ({agent.social_class})\n"
            story += f"**Description**: {agent.description}\n"
            story += f"**Initial Weights**: {agent.weights.tolist()}\n"
            story += f"**Initial Inclinations**: {agent.inclinations.tolist()}\n"
            story += f"**Resources**: Time - {agent.resources['time']}, Money - {agent.resources['money']}\n"

        for situation in self.world.get_situations_over_time():
            story += f"\n### Situation: {situation['name']}\n"
            story += f"**Description**: {situation['description']}\n---\n"
            for agent in self.agents:
                outcome = agent.judge_situation(situation["situation_vector"])
                story += f"\n#### {agent.name}'s Decision Score: {outcome:.2f}\n"
                decision = 'support' if outcome > 0 else 'oppose'
                story += f"* **Decision**: {agent.name} decides to {decision} the situation.\n"
                perfect_duties, imperfect_duties = agent.map_situation_to_duties(situation["situation_vector"])
                story += f"* **Perfect Duties Considered**: {perfect_duties}\n"
                story += f"* **Imperfect Duties Considered**: {imperfect_duties}\n"
                story += f"* **Effects of Judgments**: {agent.name} considers the impact of the situation as follows:\n"
                for duty, value in perfect_duties.items():
                    story += f"- Perfect Duty ({duty}): Impact Value = {value:.2f}\n"
                for duty, value in imperfect_duties.items():
                    story += f"- Imperfect Duty ({duty}): Impact Value = {value:.2f}\n"
                story += f"\n\n**Choices and Resource Allocation**:\n"
                allocation_summary = agent.allocate_resources_to_imperfect_duties()
                if allocation_summary:
                    story += f"\n* {allocation_summary}"
                else:
                    story += "No resources were allocated.\n"
                story += "\n"
        return story
