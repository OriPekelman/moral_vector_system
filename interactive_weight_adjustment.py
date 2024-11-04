import json

def adjust_agent_weights(agent_data):
    print(f"Adjusting weights for agent: {agent_data['name']} ({agent_data['social_class']})")
    print(f"Current weights: {agent_data['weights']}")
    
    # Loop through each weight and allow the user to adjust
    for i, weight in enumerate(agent_data["weights"]):
        new_weight = input(f"Enter new weight for duty {i + 1} (current: {weight}): ")
        if new_weight.strip():
            try:
                new_weight = float(new_weight)
                agent_data["weights"][i] = new_weight
            except ValueError:
                print("Invalid input, keeping original weight.")
    
    print(f"Updated weights: {agent_data['weights']}")

if __name__ == "__main__":
    # Load data from JSON file
    with open("moral_scenario.json", "r") as infile:
        data = json.load(infile)

    # Adjust agent weights interactively
    for agent_data in data["agents"]:
        adjust_agent_weights(agent_data)

    # Save updated data back to JSON file
    with open("moral_scenario.json", "w") as outfile:
        json.dump(data, outfile, indent=4)

    print("Agent weights have been updated.")