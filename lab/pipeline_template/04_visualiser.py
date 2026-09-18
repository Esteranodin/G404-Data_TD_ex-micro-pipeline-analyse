"""Étape 04 : rendre les distributions visibles et comparables."""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from chemins_projet import (
    CSV_NETTOYE,
    HTML_BOITE,
    HTML_DISTRIBUTIONS,
    creer_dossiers_sortie,
)


def calculer_kde(valeurs, grille):
    valeurs = np.asarray(valeurs, dtype=float)
    nombre_valeurs = len(valeurs)

    ecart_type = valeurs.std(ddof=1)
    largeur = 1.06 * ecart_type * nombre_valeurs ** (-1 / 5)

    differences = (
        grille[:, None] - valeurs[None, :]
    ) / largeur

    densite = (
        np.exp(-0.5 * differences ** 2).sum(axis=1)
        / (nombre_valeurs * largeur * np.sqrt(2 * np.pi))
    )

    return densite


def ecrire_graphiques(tickets_nettoyes):
    """Écrire deux graphiques HTML utilisables hors connexion.

    À FAIRE :

    - ajouter un trait par observation sous chaque histogramme (rug) ;


    Facultatif après les histogrammes : une vue séparée avec densité estimée (KDE).
    Utiliser histnorm="probability density" pour comparer histogramme et KDE.
    ff.create_distplot, utilisé au cours précédent, ne fonctionne plus en 7.
    """
    canaux = tickets_nettoyes["channel"].unique()

    couleurs_canaux = {
    "email": "#008C95",
    "phone": "#F06B52",
    "chat": "#5B6CFF",
    }
    
    histogramme = make_subplots(
        rows=len(canaux),
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=[f"{canal}" for canal in canaux],
        specs=[[{"secondary_y": True}] for _ in canaux],
    )

    for numero_ligne, canal in enumerate(canaux, start=1):
        durees = tickets_nettoyes.loc[
            tickets_nettoyes["channel"] == canal,
            "resolution_minutes",
        ].to_numpy()

        grille_x = np.linspace(0, 430, 500)
        densite = calculer_kde(durees, grille_x)

        histogramme.add_trace(
            go.Histogram(
                x=durees,
                histnorm=None,
                xbins=dict(
                    start=5,
                    end=425,
                    size=10,
                ),
                marker_color=couleurs_canaux[canal],
                marker_line_color="white",
                marker_line_width=1,
                opacity=0.75,
                name="Nombre de tickets",
                showlegend=False,
            ),
            row=numero_ligne,
            col=1,
            secondary_y=False,
        )

        histogramme.add_trace(
        go.Scatter(
            x=grille_x,
            y=densite,
            mode="lines",
            line=dict(
                color="black",
                width=2,
            ),
            opacity=0.55,
            name="KDE",
            showlegend=numero_ligne == 1,
        ),
        row=numero_ligne,
        col=1,
        secondary_y=True,
        )

        histogramme.add_trace(
            go.Scatter(
                x=durees,
                y=np.zeros(len(durees)),
                mode="markers",
                marker=dict(
                    symbol="line-ns",
                    size=8,
                    color="black",
                ),
                name="Observations",
                showlegend=False,
            ),
            row=numero_ligne,
            col=1,
            secondary_y=False,
        )

    histogramme.update_layout(
        height=1100,
        template="plotly_white",
        title="Distributions des durées de résolution par canal",
        margin=dict(t=100, b=80, l=80, r=40),
    )

    histogramme.update_xaxes(
        title_text="Durée de résolution (minutes)",
        range=[0, 430],
    )

    for numero_ligne in range(1, len(canaux) + 1):
        histogramme.update_yaxes(
            title_text="Nombre de tickets",
            secondary_y=False,
            row=numero_ligne,
            col=1,
        )

        histogramme.update_yaxes(
            title_text="Densité KDE",
            secondary_y=True,
            row=numero_ligne,
            col=1,
            showgrid=False,
        )

    histogramme.write_html(
        HTML_DISTRIBUTIONS,
        include_plotlyjs=True,
    )

# *****************************************************************************************
# ------------- Boîte à moustaches -------------
# *****************************************************************************************
    boite = px.box(
        tickets_nettoyes,
        x="channel",
        y="resolution_minutes",
        color="channel",
        color_discrete_sequence=["#008C95", "#F06B52", "#5B6CFF"],
        points="all",
        template="plotly_white",
        title="Centre et dispersion des durées de résolution",
        labels={
            "channel": "Canal",
            "resolution_minutes": "Durée de résolution (minutes)",
        },
    )

    boite.update_layout(
        height=500,
        font_size=14,
        showlegend=False,
    )

    boite.write_html(
        HTML_BOITE,
        include_plotlyjs=True,
    )


def main():
    """Créer les graphiques des distributions de durées.

    Lit les tickets nettoyés, génère les graphiques des distributions
    et de la dispersion des durées par canal, puis les enregistre dans
    des fichiers HTML autonomes.
    """

    tickets_nettoyes = pd.read_csv(CSV_NETTOYE)
    creer_dossiers_sortie()
    ecrire_graphiques(tickets_nettoyes)

    print(f"Vue des formes : {HTML_DISTRIBUTIONS}")
    print(f"Vue centre/dispersion : {HTML_BOITE}")
    print("Contrôle : ouvrir les deux fichiers et expliquer chaque graphique.")


if __name__ == "__main__":
    main()
