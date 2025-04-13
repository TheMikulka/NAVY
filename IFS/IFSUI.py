import plotly.graph_objects as go

class IFSUI:
    @staticmethod
    def plot_3d(points, title):
        fig = go.Figure(data=[go.Scatter3d(
            x=points[:,0], y=points[:,1], z=points[:,2],
            mode='markers',
            marker=dict(size=5,color=points[:,2],colorscale='Inferno', opacity=0.7)
        )])

        fig.update_layout(title=title, scene=dict(
            xaxis_title='X', yaxis_title='Y', zaxis_title='Z'
        ))
        fig.show()
