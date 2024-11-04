import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import plotly.graph_objects as go
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend

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

        # Save the plot as an image file
        plt.savefig('static/moral_vectors.png')
        plt.close()

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

        # Save the plot as an image file
        plt.savefig('static/weight_changes.png')
        plt.close()

    def visualize_decision_timeline(self, agents, situations):
        fig = go.Figure()

        for agent in agents:
            timestamps = []
            decision_scores = []
            for situation in situations:
                outcome = agent.judge_situation(situation["situation_vector"])
                timestamps.append(situation["timestamp"])
                decision_scores.append(outcome)

            fig.add_trace(go.Scatter(x=timestamps, y=decision_scores,
                                     mode='lines+markers',
                                     name=f'{agent.name} Decision Score'))

        fig.update_layout(title='Decision Scores Over Time',
                          xaxis_title='Time',
                          yaxis_title='Decision Score',
                          template='plotly_dark')
        # Save the Plotly figure as an HTML file
        fig.write_html("static/decision_timeline.html")