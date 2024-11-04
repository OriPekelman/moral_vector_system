import json
from moral_agent import MoralAgent
from moral_world import MoralWorld
from learning_module import LearningModule
from visualizer import Visualizer
from story_generator import StoryGenerator

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
    decisions_per_situation = {}  # Track decisions for majority voting

    for situation in world.get_situations_over_time():
        decisions_per_situation[situation["name"]] = []
        for agent in agents:
            outcome = agent.judge_situation(situation["situation_vector"])
            decision = 'support' if outcome > 0 else 'oppose'
            decisions_per_situation[situation["name"]].append(decision)
            print(f"Agent {agent.name} Decision Score at {situation['timestamp']}: {outcome}")
            learning_module.agent = agent
            learning_module.adjust_weights(situation["situation_vector"], outcome)
            agent.allocate_resources_to_imperfect_duties()

    # Determine election outcomes based on majority vote
    election_outcomes = {}
    for situation_name, decisions in decisions_per_situation.items():
        support_count = decisions.count('support')
        oppose_count = decisions.count('oppose')
        if support_count > oppose_count:
            election_outcomes[situation_name] = 'Majority supports'
        else:
            election_outcomes[situation_name] = 'Majority opposes'

    # Print election outcomes
    for situation_name, outcome in election_outcomes.items():
        print(f"Election Outcome for {situation_name}: {outcome}")

    # Visualizing moral vectors and weight changes over time for all agents in a single plot
    visualizer.visualize_vectors(agents, world.get_situations_over_time())
    visualizer.visualize_weight_changes_over_time(agents)

    # Save the story to a JSON file
    with open("moral_story_output.json", "w") as outfile:
        json.dump({"story": story, "election_outcomes": election_outcomes}, outfile, indent=4)

    # Save the story to a Markdown file
    with open("moral_story_output.md", "w") as mdfile:
        mdfile.write(story)
        mdfile.write("\n\n# Election Outcomes\n")
        for situation_name, outcome in election_outcomes.items():
            mdfile.write(f"- **{situation_name}**: {outcome}\n")
