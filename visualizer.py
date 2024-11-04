import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

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
