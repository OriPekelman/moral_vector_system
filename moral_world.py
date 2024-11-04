import datetime
import numpy as np

class MoralWorld:
    def __init__(self, world_data):
        self.situations = []

        # Load initial situations and phases
        for situation in world_data["situations"]:
            phases = situation.get("phases", [])
            if phases:
                # Add the phases to the situation as distinct situations over time
                for phase in phases:
                    self.situations.append({
                        "name": phase["name"],
                        "description": phase["description"],
                        "timestamp": datetime.datetime.fromisoformat(phase["timestamp"]),
                        "situation_vector": np.array(phase["situation_vector"])
                    })
            else:
                # Add the original situation
                self.situations.append({
                    "name": situation["name"],
                    "description": situation["description"],
                    "timestamp": datetime.datetime.fromisoformat(situation["timestamp"]),
                    "situation_vector": np.array(situation["situation_vector"])
                })

    def get_situations_over_time(self):
        return sorted(self.situations, key=lambda x: x["timestamp"])