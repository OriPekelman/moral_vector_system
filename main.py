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