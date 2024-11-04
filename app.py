from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import json
import markdown
from moral_agent import MoralAgent
from moral_world import MoralWorld
from visualizer import Visualizer
from story_generator import StoryGenerator

app = Flask(__name__)
duties = [
"Honesty", "Non-harm", "Keep Promises", "Respect Rights",
"Justice", "Non-stealing", "Truthfulness", "Avoid Exploitation",
"Non-manipulation", "No False Testimony", "Self-improvement", "Help Others",
"Charity", "Develop Talents", "Promote Welfare", "Environmental Care",
"Fairness", "Education", "Community Support", "Personal Growth"
]


# Load initial data
with open("moral_scenario.json", "r") as infile:
    data = json.load(infile)
agents = [MoralAgent(agent_data) for agent_data in data["agents"]]
world = MoralWorld(data["world"])
visualizer = Visualizer()
story_generator = StoryGenerator(agents, world)

@app.route('/')
def index():
    return render_template('index.html', agents=agents)

@app.route('/adjust_weights', methods=['GET', 'POST'])
def adjust_weights():
    if request.method == 'POST':
        agent_name = request.form['agent']
        new_weights = request.form.getlist('weights')
        for agent in agents:
            if agent.name == agent_name:
                agent.weights = [float(w) for w in new_weights]
        return redirect(url_for('index'))
    return render_template('adjust_weights.html', agents=agents)

@app.route('/submit_scenario', methods=['POST'])
def submit_scenario():
    new_scenario = request.json
    # Validate and add the new scenario
    required_fields = ["name", "description", "timestamp", "situation_vector"]
    for field in required_fields:
        if field not in new_scenario:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    world.situations.append({
        "name": new_scenario["name"],
        "description": new_scenario["description"],
        "timestamp": new_scenario["timestamp"],
        "situation_vector": new_scenario["situation_vector"]
    })
    return jsonify({"message": "Scenario added successfully."}), 200

@app.route('/visualize')
def visualize():
    try:
        # Call visualizer to generate plots and save them in static/
        visualizer.visualize_vectors(agents, world.get_situations_over_time())
        visualizer.visualize_weight_changes_over_time(agents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return redirect(url_for('view_visualizations'))

@app.route('/visualize_decision_timeline')
def visualize_decision_timeline():
    try:
        visualizer.visualize_decision_timeline(agents, world.get_situations_over_time())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return redirect(url_for('view_visualizations'))

@app.route('/view_visualizations')
def view_visualizations():
    return render_template('visualizations.html')

@app.route('/view_image/<image_name>')
def view_image(image_name):
    return send_file(f'static/{image_name}')

@app.route('/story')
def story():
    story_output =markdown.markdown(story_generator.generate_story())
    return render_template('story.html', story=story_output)

@app.route('/api/duties', methods=['GET'])
def get_duties():
    return jsonify({"duties": duties})


if __name__ == '__main__':
    app.run(debug=True, port=5050, host='127.0.0.1')
