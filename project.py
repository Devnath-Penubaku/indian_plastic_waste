import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio

df = pd.read_csv("plastic_waste_india.csv")
df.head()

df = df.rename(columns={
    "State/UT-wise": "State"
})


df = df.drop(columns=["Sl. No."])


df = df.fillna(0)


years = [
    "2016-17",
    "2017-18",
    "2018-19",
    "2019-20",
    "2020-21"
]


df["Plastic_Waste"] = df[years].sum(axis=1)


print(df.head())


india = gpd.read_file(
    "india_states.geojson"
)
# india.explore() 
india = india.explode(index_parts=False)
india.plot(edgecolor="black", facecolor="lightgrey")
plt.show()





india = india.rename(columns={"NAME_1": "State"})
india = india.loc[:, ~india.columns.duplicated()]
df = df.loc[:, ~df.columns.duplicated()]


india["State"] = india["State"].replace({

    "Andaman and Nicobar": "Andaman and Nicobar Islands",
    "Dadra and Nagar Haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "Daman and Diu": "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi": "NCT of Delhi",
    "Orissa": "Odisha",
    "Uttaranchal": "Uttarakhand",
    "Andaman & Nicobar Island": "Andaman and Nicobar Islands",
    "Arunanchal Pradesh": "Arunachal Pradesh"
})

india.loc[:, "State"] = india["State"].astype(str)
df.loc[:, "State"] = df["State"].astype(str)
map_data = india.merge(df, on="State", how="left")



top = df.sort_values(
    "Plastic_Waste",
    ascending=False
).head(15)


fig = px.bar(
    top,
    x="State",
    y="Plastic_Waste",

    title="Top Indian States Plastic Waste Generation",

    labels={
        "Total_Plastic":
        "Plastic Waste (Tonnes)"
    }
)


fig.update_layout(
    xaxis_tickangle=-45
)

fig.show()


fig, ax = plt.subplots(figsize=(10, 12))

map_data.plot(
    column="Plastic_Waste",
    cmap="Reds",
    legend=True,
    edgecolor="black",
    linewidth=0.5,
    ax=ax,
    missing_kwds={'color': 'lightgrey'}
)

ax.set_title("India State-wise Plastic Waste Generation", fontsize=15, pad=20)
ax.axis("off")
plt.show()



map_data = map_data.to_crs(epsg=4326)
fig = px.choropleth(
    map_data,
    geojson=map_data.geometry,
    locations=map_data.index,
    color="Plastic_Waste",
    color_continuous_scale="Reds",
    hover_name="State",
    hover_data={
    "2016-17": ":,.0f",
    "2017-18": ":,.0f",
    "2018-19": ":,.0f",
    "2019-20": ":,.0f",
    "2020-21": ":,.0f",
    "Plastic_Waste": ":,.0f"
},
    title="India State-wise Plastic Waste Generation"
)


fig.update_geos(
    scope="asia",
    fitbounds="locations",      
    visible=False,              
    showcoastlines=False,       
    showland=False,             
    showocean=False,            
    showlakes=False             
)


fig.update_layout(
    title_x=0.5,               
    margin={"r":0,"t":50,"l":0,"b":0}
)

fig.show()



fig = px.choropleth(
    map_data,

    geojson=map_data.__geo_interface__,

    locations="ID_1",

    color="Plastic_Waste",

    color_continuous_scale="Reds",

    hover_name="State",

    hover_data={
        "2016-17": ":,.0f",
        "2017-18": ":,.0f",
        "2018-19": ":,.0f",
        "2019-20": ":,.0f",
        "2020-21": ":,.0f",
        "Plastic_Waste": ":,.0f"
    },

    title="India State-wise Plastic Waste Generation"
)


fig.update_geos(
    fitbounds="locations",
    visible=False
)


fig.write_html(
    "india_plastic_waste_map.html"
)

print("HTML exported successfully")
