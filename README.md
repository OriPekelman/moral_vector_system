# Moral Vector System

## Overview
The **Moral Vector System** is a Python-based implementation that models moral decision-making for agents in various societal scenarios. Each agent is represented with a unique moral vector space that includes weights for different duties and inclinations. This system is inspired by Kantian ethics, with duties categorized as perfect or imperfect.

The project includes:
- **Moral Agents**: Represented as agents with distinct social classes, weights, inclinations, resources, and time allocations.
- **Moral World**: Represents different scenarios that agents must judge.
- **Story Generation**: Generates a Markdown file describing the scenarios, agents' decisions, and the effects of their judgments.
- **Visualization**: PCA-based visualization of agent weights and their changes over time.

## Features
- **Agent Representation**: Each agent has:
  - A set of **weights** reflecting their moral priorities for perfect duties.
  - **Inclinations** that influence their approach to imperfect duties.
  - **Resources** (time and money) and **time allocation** for various activities.
  - A **description** that summarizes the agent's character traits.

- **Scenario Judgments**: Agents judge scenarios by calculating decision scores based on their weights and inclinations.
  - **Perfect Duties**: Strict duties that agents try to fulfill.
  - **Imperfect Duties**: Flexible duties that agents weigh based on inclinations.

- **Story Generation**: Produces a detailed story that includes agents, their decisions, and resource allocations for each scenario. The output is available in both JSON and Markdown formats.

- **Visualization**:
  - **Moral Vectors in Reduced Space**: Displays agent weights and scenario vectors in a PCA-reduced 2D space.
  - **Weight Changes Over Time**: Shows how each agent's moral weights evolve.

## Installation
### Prerequisites
- Python 3.8 or higher
- `matplotlib`
- `scikit-learn`
- `scipy`

### Installation Steps
1. Clone this repository:
   ```sh
   git clone <repository-url>
   ```

2. Install the required Python packages using `pip`:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. Ensure the data file (`moral_scenario.json`) is present in the project directory. This file contains agent and scenario data.
2. Run the Python script:
   ```sh
   python moral_vector_system.py
   ```
3. The script will:
   - Generate and display the moral story (`moral_story_output.md` and `moral_story_output.json`).
   - Show visualizations of agent decisions and weight changes.

## File Structure
- **moral_vector_system.py**: Main Python script containing all classes and logic for the moral vector system.
- **moral_scenario.json**: Data file with details on agents and world situations.
- **moral_story_output.md**: Markdown output of the generated story.
- **moral_story_output.json**: JSON output of the generated story.
- **requirements.txt**: List of Python dependencies.

## JSON File Structure
The JSON file (`moral_scenario.json`) consists of two main parts:
1. **Agents**: Defines each agent's properties, including name, social class, weights, inclinations, resources, and time allocation.
2. **World Situations**: Defines various scenarios that agents must judge.

Example agent:
```json
{
  "name": "Alice Johnson",
  "social_class": "upper",
  "description": "A wealthy individual who is family-oriented and community-focused.",
  "weights": [0.3, 0.5, 0.2, 0.1, 0.4, ...],
  "inclinations": [0.8, 0.4, 0.9, 0.6, 0.7, ...],
  "resources": {
    "time": 120,
    "money": 1000
  },
  "time_allocation": {
    "sleep": 56,
    "recreation": 28,
    "learning": 10,
    "subsistence_work": 14,
    "community_service": 14,
    "family_care": 28
  }
}
```

## Visualizations
- **Moral Vectors in Reduced Space**: A 2D PCA representation of moral priorities for all agents and scenarios.
- **Weight Changes Over Time**: A line plot showing the evolution of agent weights.

## Story Generation
The story generation component outputs detailed Markdown describing each agent's decision in each scenario. It includes:
- **Agent Descriptions**: Their character traits, inclinations, and resources.
- **Scenario Analysis**: Decision scores, chosen actions, and the effects of judgments for each situation.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## License
This project is licensed under the MIT License.


