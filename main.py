import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# This dataframe has 244 lines, but 4 distinct values for `day`
df = px.data.tips()
data = pd.read_csv("E:/COUR/Master2BI/These/donnee Alsocovid/wp2/resultats.csv")
valeurs = [
    ('intervalAge','age'),
    ('donneesWP2/donnee_socio/religion','confession religieuse'),
    ('donneesWP2/historique/consomme_stupefiant/chicha',"consommer chicha"),
    ('donneesWP2/historique/consomme_stupefiant/tabac',"consommer tabac"),
    ('donneesWP2/donnee_socio/groupe_socio_culturel','groupe socio_culturel'),
    ('donneesWP2/donnee_Geo/moyen_deplacement/0/moyen_depl','moyen de deplacement'),
    ('donneesWP2/donnee_socio/niveau_etude',"niveau d'etude"),
    ('donneesWP2/donnee_socio/profession','profession'),
    ('donneesWP2/donnee_socio/revenu_mensuel','revenu mensuel'),
    ('donneesWP2/donnee_socio/secteur_activite',"secteur d'activité"),
    ('donneesWP2/donnee_socio/sexe', 'sexe'),
    ('donneesWP2/historique/statut_covid',"statut covid-19"),
    ('donneesWP2/donnee_socio/statut_matrimonial','statut matrimoniale'),
    ('donneesWP2/pratique/information_masque/type_de_masque',"type de masque")
]

data['intervalAge']=data['donneesWP2/donnee_socio/age'].apply(lambda x: "[00 - 14]" if (x>=00 and x<=14) else ("[15 - 20]" if (x>=15 and x<=20) else ("[21 - 25]" if (x>=21 and x<=25) else ("[26 - 40]" if (x>=26 and x<=40) else "[51 - 100]" ))))
#data["_7_Quel_est_votre_pl_haut_niveau_d_tude_"]=data["_7_Quel_est_votre_pl_haut_niveau_d_tude_"].apply(lambda x: "Non scolarisé " if x == 0 else("Primaire" if x ==1 else("Secondaire 1er cycle (6ème à 3ème) " if x ==2 else ("Secondaire second cycle (Seconde à Terminale) " if x ==3 else 'Universitaire' ) )) )


app = dash.Dash(__name__)
app.layout = html.Div([
    html.P("Names:"),
    dcc.Dropdown(
        id='names', 
        value='intervalAge',
        options=[{'value': x, 'label': y}
                 for (x,y) in valeurs],
        clearable=False
    ),
    dcc.Graph(id="pie-chart"),
    dcc.Graph(id="bar-chart")
])

@app.callback(
    Output("pie-chart", "figure"),
    Output("bar-chart", "figure"),
    [Input("names", "value")])
def generate_chart(names):
    fig = px.pie(data, names=names)
    newData = data.groupby([names]).count()
    mydata = get_axis(newData)
    fig2 = px.bar(mydata, x='nom', y='valeur')
    return fig,fig2

def get_axis(mesDonnee):
    newdata = pd.DataFrame(columns=['nom','valeur'])
    for i in range(len(mesDonnee)):
        newdata.loc[i]= [str(mesDonnee.iloc[i,].name),mesDonnee.iloc[i,0]]
    return newdata

app.run_server(debug=True)