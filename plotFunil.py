import plotly.express as px
data = dict(
    number=[460866, 264861, 25193 , 24457, 1059],
    Etapas=["PRs", "Issues", "Issues com tag 'Bug'", "PRs com 'test'", "PRs com alterações em asserts"])
fig = px.funnel(data, x='number', y='Etapas', font_size=20)
fig.show()