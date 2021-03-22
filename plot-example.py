#https://community.plotly.com/t/fill-area-under-density-plot/51231

import numpy as np
import plotly.figure_factory as ff

data = np.random.normal(0, 1, 1000)
name = "Example"

fig = ff.create_distplot([data], [name], show_hist=False, show_rug=False)
fig = fig.add_vline(
    x=np.quantile(data, q=0.5),
    line_width=3,
    line_dash="dash",
    line_color="black",
    annotation_text=f"Median: {round(np.quantile(data, q=0.5))}",
    annotation_position="top right",
    annotation_font_size=12,
    annotation_font_color="black",
)
fig = fig.add_vline(
    x=np.quantile(data, q=0.05),
    line_width=3,
    line_dash="dash",
    line_color="red",
    annotation_text=f"5% Quantil: {round(np.quantile(data, q=.05))}",
    annotation_position="bottom right",
    annotation_font_size=12,
    annotation_font_color="red",
)
fig = fig.add_vline(
    x=np.quantile(data, q=0.95),
    line_width=3,
    line_dash="dash",
    line_color="green",
    annotation_text=f"95% Quantil: {round(np.quantile(data, q=.95))}",
    annotation_position="bottom left",
    annotation_font_size=12,
    annotation_font_color="green",
)
fig.update_layout(plot_bgcolor="white")
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
fig.update_layout(showlegend=False)
fig.update_layout(title=name)

xl = np.quantile(data, q=0.05)
xr = np.quantile(data, q=0.95)
x1   = [xc   for xc in fig.data[0].x if xc <xl]
y1   = fig.data[0].y[:len(x1)]

x2   = [xc   for xc in fig.data[0].x if xc > xr]
y2   = fig.data[0].y[-len(x2):]
fig.add_scatter(x=x1, y=y1,fill='tozeroy', mode='none' , fillcolor="red")
fig.add_scatter(x=x2, y=y2,fill='tozeroy', mode='none' , fillcolor='green')

x3 = [xc   for xc in fig.data[0].x if (xc > xl) and (xc < xr)]
y3 = fig.data[0].y[len(x1):-len(x2)]
fig.add_scatter(x=x3, y=y3,fill='tozeroy', mode='none' , fillcolor='lightblue')
fig

