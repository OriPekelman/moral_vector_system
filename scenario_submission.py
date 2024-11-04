# scenario_submission.py

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/submit_scenario', methods=['POST'])
def submit_scenario():
    try:
        # Load the current scenarios
        with open("moral_scenario.json", "r") as infile:
            data = json.load(infile)

        # Get the new scenario data from the request
        new_scenario = request.json

        # Validate required fields
        required_fields = ["name", "description", "timestamp", "situation_vector"]
        for field in required_fields:
            if field not in new_scenario:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Add the new scenario to the world data
        data["world"]["situations"].append(new_scenario)

        # Save updated scenarios back to JSON file
        with open("moral_scenario.json", "w") as outfile:
            json.dump(data, outfile, indent=4)

        return jsonify({"message": "Scenario added successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)