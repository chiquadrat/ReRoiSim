import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
from scipy.stats import iqr


def figure_ein_aus_gabeparameter(
    ergebnis, eingabeparameter, name, zeichen, x, runden, area, kaufpreis
):
    if name == "Minimaler Cashflow":
        eingabeparameter = np.array(ergebnis[eingabeparameter])
        eingabeparameter = eingabeparameter[~np.isnan(eingabeparameter)]
        upper_bound = np.quantile(eingabeparameter, q=0.75) + 4.5 * iqr(
            eingabeparameter
        )
        lower_bound = np.quantile(eingabeparameter, q=0.75) - 4.5 * iqr(
            eingabeparameter
        )
        eingabeparameter = eingabeparameter[
            (eingabeparameter > lower_bound) & (eingabeparameter < upper_bound)
        ]
    else:
        eingabeparameter = np.array(ergebnis[eingabeparameter])
        eingabeparameter = eingabeparameter[~np.isnan(eingabeparameter)]

    if np.all(eingabeparameter == eingabeparameter[0]) == True:
        fig = go.Figure(data=[go.Table()])
    else:
        fig = ff.create_distplot(
            [eingabeparameter], [name], show_hist=False, show_rug=False
        )

        if (name == "Verkaufspreis") and (eingabeparameter.min() < kaufpreis):
            # print(len(eingabeparameter[eingabeparameter<kaufpreis])/len(eingabeparameter))
            fig = fig.add_vline(
                x=kaufpreis,
                line_width=3,
                line_dash="dash",
                line_color="black",
                annotation_text=f"{round(len(eingabeparameter[eingabeparameter<kaufpreis])/len(eingabeparameter)*100,2)} % Quantil",
                annotation_position="bottom right",
                annotation_font_size=12,
                annotation_font_color="black",
                annotation_bgcolor="white",
            )
        elif (name == "Gewinn") and (eingabeparameter.min() < 0):
            # print(len(eingabeparameter[eingabeparameter<kaufpreis])/len(eingabeparameter))
            fig = fig.add_vline(
                x=0,
                line_width=3,
                line_dash="dash",
                line_color="black",
                annotation_text=f"{round(len(eingabeparameter[eingabeparameter<0])/len(eingabeparameter)*100,2)} % Quantil",
                annotation_position="bottom right",
                annotation_font_size=12,
                annotation_font_color="black",
                annotation_bgcolor="white",
            )
        elif (name == "Objektrendite" or name == "Eigenkapitalrendite") and (
            eingabeparameter.min() < 0
        ):
            fig = fig.add_vline(
                x=0,
                line_width=3,
                line_dash="dash",
                line_color="black",
                annotation_text=f"{round(len(eingabeparameter[eingabeparameter<0])/len(eingabeparameter)*100,2)} % Quantil",
                annotation_position="bottom right",
                annotation_font_size=12,
                annotation_font_color="black",
                annotation_bgcolor="white",
            )
        else:
            if runden == 0:
                annotation_tmp = f"5% Quantil: {int(np.quantile(eingabeparameter, q=.05)*x)} {zeichen}"
            else:
                annotation_tmp = f"5% Quantil: {round(np.quantile(eingabeparameter, q=.05)*x,runden)} {zeichen}"
            fig = fig.add_vline(
                x=np.quantile(eingabeparameter, q=0.05),
                line_width=3,
                line_dash="dash",
                line_color="black",
                annotation_text=annotation_tmp,
                annotation_position="bottom right",
                annotation_font_size=12,
                annotation_font_color="black",
                annotation_bgcolor="white",
            )
        if runden == 0:
            annotation_tmp = (
                f"95% Quantil: {int(np.quantile(eingabeparameter, q=.95)*x)} {zeichen}"
            )
        else:
            annotation_tmp = f"95% Quantil: {round(np.quantile(eingabeparameter, q=.95)*x,runden)} {zeichen}"
        fig = fig.add_vline(
            x=np.quantile(eingabeparameter, q=0.95),
            line_width=3,
            line_dash="dash",
            line_color="black",
            annotation_text=annotation_tmp,
            annotation_position="bottom right",
            annotation_font_size=12,
            annotation_font_color="black",
            annotation_bgcolor="white",
        )

        if runden == 0:
            annotation_tmp = (
                f"Median: {int(np.quantile(eingabeparameter, q=0.5)*x)} {zeichen}"
            )
        else:
            annotation_tmp = f"Median: {round(np.quantile(eingabeparameter, q=0.5)*x,runden)} {zeichen}"
        fig = fig.add_vline(
            x=np.quantile(eingabeparameter, q=0.5),
            line_width=3,
            line_dash="dash",
            line_color="black",
            annotation_text=annotation_tmp,
            annotation_position="top right",
            annotation_font_size=12,
            annotation_font_color="black",
            annotation_bgcolor="white",
        )

        # fig = fig.add_vline(
        #         x=eingabeparameter.mean(),
        #         line_width=3,
        #         line_dash="dash",
        #         line_color="red",
        #         annotation_text="",
        #         annotation_position="top right",
        #         annotation_font_size=12,
        #         annotation_font_color="black",
        #     )

        fig.update_yaxes(rangemode="tozero")
        fig.update_layout(plot_bgcolor="white")
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="lightgrey")
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgrey")
        fig.update_layout(showlegend=False)
        fig.update_layout(title=name)

        if area == "middle":
            xl = np.quantile(eingabeparameter, q=0.05)
            xr = np.quantile(eingabeparameter, q=0.95)
            x1 = [xc for xc in fig.data[0].x if xc < xl]
            y1 = fig.data[0].y[: len(x1)]

            x2 = [xc for xc in fig.data[0].x if xc > xr]
            y2 = fig.data[0].y[-len(x2) :]

            x3 = [xc for xc in fig.data[0].x if (xc > xl) and (xc < xr)]
            y3 = fig.data[0].y[len(x1) : -len(x2)]

            fig.add_scatter(
                x=x3,
                y=y3,
                fill="tozeroy",
                mode="none",
                fillcolor="lightblue",
                name=name,
            )

            # fig.add_scatter(x=x1, y=y1,fill='tozeroy', mode='none' , fillcolor="red")
            # fig.add_scatter(x=x2, y=y2,fill='tozeroy', mode='none' , fillcolor='green')
        if name == "Verkaufspreis":
            x1 = [xc for xc in fig.data[0].x if xc < kaufpreis]
            y1 = fig.data[0].y[: len(x1)]
            fig.add_scatter(
                x=x1, y=y1, fill="tozeroy", mode="none", fillcolor="red", name=name
            )

        if (
            (name == "Objektrendite")
            or (name == "Eigenkapitalrendite")
            or (name == "Gewinn")
        ):
            x1 = [xc for xc in fig.data[0].x if xc < 0]
            y1 = fig.data[0].y[: len(x1)]
            fig.add_scatter(
                x=x1, y=y1, fill="tozeroy", mode="none", fillcolor="red", name=name
            )

        if name == "Minimaler Cashflow":
            xl = np.quantile(eingabeparameter, q=0.05)
            x1 = [xc for xc in fig.data[0].x if xc < xl]
            y1 = fig.data[0].y[: len(x1)]
            fig.add_scatter(
                x=x1, y=y1, fill="tozeroy", mode="none", fillcolor="red", name=name
            )

    return fig


def figure_etf_vergleich(
    ergebnis,
    eingabeparameter1,
    eingabeparameter2,
    name1,
    name2,
    zeichen,
    x,
    runden,
    ueberschrift,
):

    eingabeparameter1 = np.array(ergebnis[eingabeparameter1])
    eingabeparameter1 = eingabeparameter1[~np.isnan(eingabeparameter1)]

    eingabeparameter2 = np.array(ergebnis[eingabeparameter2])
    eingabeparameter2 = eingabeparameter2[~np.isnan(eingabeparameter2)]

    fig = ff.create_distplot(
        [eingabeparameter1, eingabeparameter2],
        [name1, name2],
        show_hist=False,
        show_rug=False,
    )

    if runden == 0:
        annotation_tmp = (
            f"Median: {int(np.quantile(eingabeparameter1, q=0.5)*x)} {zeichen}"
        )
    else:
        annotation_tmp = (
            f"Median: {round(np.quantile(eingabeparameter1, q=0.5)*x,runden)} {zeichen}"
        )
    fig = fig.add_vline(
        x=np.quantile(eingabeparameter1, q=0.5),
        line_width=3,
        line_dash="dash",
        line_color="cornflowerblue",
        annotation_text=annotation_tmp,
        annotation_position="top left",
        annotation_font_size=12,
        annotation_font_color="black",
        annotation_bgcolor="white",
    )

    if runden == 0:
        annotation_tmp = (
            f"Median: {int(np.quantile(eingabeparameter2, q=0.5)*x)} {zeichen}"
        )
    else:
        annotation_tmp = (
            f"Median: {round(np.quantile(eingabeparameter2, q=0.5)*x,runden)} {zeichen}"
        )
    fig = fig.add_vline(
        x=np.quantile(eingabeparameter2, q=0.5),
        line_width=3,
        line_dash="dash",
        line_color="orange",
        annotation_text=annotation_tmp,
        annotation_position="bottom right",
        annotation_font_size=12,
        annotation_font_color="black",
        annotation_bgcolor="white",
    )

    fig.update_yaxes(rangemode="tozero")
    fig.update_layout(plot_bgcolor="white")
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="lightgrey")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgrey")
    fig.update_layout(title=ueberschrift)

    return fig


def figure_vermoegensentwicklung(
    ergebnisse_investiert,
    ergebnisse_nicht_investiert,
    grafik_selector_investiert,
    grafik_selector_nicht_investiert,
):

    farben = [
        "#636EFA",
        "#EF553B",
        "#00CC96",
        "#AB63FA",
        "#FFA15A",
        "#19D3F3",
        "#FF6692",
        "#B6E880",
        "#FF97FF",
        "#FECB52",
    ]

    farben_rgb = [
        "rgba(99, 110, 250, 0.3)",
        "rgba(239, 85, 59, 0.3)",
        "rgba(0, 204, 150, 0.3)",
        "rgba(171, 99, 250, 0.3)",
        "rgba(255, 161, 90, 0.3)",
        "rgba(25, 211, 243, 0.3)",
        "rgba(255, 102, 146, 0.3)",
        "rgba(182, 232, 128, 0.3)",
        "rgba(255, 151, 255, 0.3)",
        "rgba(254, 203, 82, 0.3)",
    ]

    fig_vermoegen_investiert = go.Figure()
    for i, wahl in enumerate(grafik_selector_investiert):
        fig_vermoegen_investiert.add_trace(
            go.Scatter(
                x=ergebnisse_investiert["jahr_pj"],
                y=ergebnisse_investiert[wahl],
                mode="lines+markers",
                line_color=farben[i],
                name=wahl,
            )
        )

        fig_vermoegen_investiert.add_scatter(
            name="Upper Bound",
            x=ergebnisse_investiert["jahr_pj"],
            y=np.array(ergebnisse_investiert[wahl + " + lower bound"]),
            mode="lines",
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False,
        ),
        fig_vermoegen_investiert.add_scatter(
            name="Lower Bound",
            x=ergebnisse_investiert["jahr_pj"],
            y=np.array(ergebnisse_investiert[wahl + " + upper bound"]),
            marker=dict(color="#444"),
            line=dict(width=0),
            mode="lines",
            fillcolor=farben_rgb[i],
            fill="tonexty",
            opacity=0.5,
            showlegend=False,
        )

    fig_vermoegen_investiert.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01,)
    )
    fig_vermoegen_investiert.update_layout(plot_bgcolor="white")
    fig_vermoegen_investiert.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor="lightgrey"
    )
    fig_vermoegen_investiert.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor="lightgrey"
    )

    fig_vermoegen_nicht_investiert = go.Figure()
    for i, wahl in enumerate(grafik_selector_nicht_investiert):
        # print(ergebnisse_nicht_investiert["jahr_pj"])
        # print(ergebnisse_nicht_investiert[wahl2])
        fig_vermoegen_nicht_investiert.add_trace(
            go.Scatter(
                x=ergebnisse_nicht_investiert["jahr_pj"],
                y=ergebnisse_nicht_investiert[wahl],
                mode="lines+markers",
                line_color=farben[i],
                name=wahl,
            )
        )

        fig_vermoegen_nicht_investiert.add_scatter(
            name="Upper Bound",
            x=ergebnisse_nicht_investiert["jahr_pj"],
            y=np.array(ergebnisse_nicht_investiert[wahl + " + lower bound"]),
            mode="lines",
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False,
        ),
        fig_vermoegen_nicht_investiert.add_scatter(
            name="Lower Bound",
            x=ergebnisse_nicht_investiert["jahr_pj"],
            y=np.array(ergebnisse_nicht_investiert[wahl + " + upper bound"]),
            marker=dict(color="#444"),
            line=dict(width=0),
            mode="lines",
            fillcolor=farben_rgb[i],
            fill="tonexty",
            opacity=0.5,
            showlegend=False,
        )

    fig_vermoegen_nicht_investiert.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    fig_vermoegen_nicht_investiert.update_layout(plot_bgcolor="white")
    fig_vermoegen_nicht_investiert.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor="lightgrey"
    )
    fig_vermoegen_nicht_investiert.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor="lightgrey"
    )

    return fig_vermoegen_investiert, fig_vermoegen_nicht_investiert
