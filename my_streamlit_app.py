import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Challenge Voitures!')

st.write("Dataset des voitures")

link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df = pd.read_csv(link)

# Here we use "magic commands":
df

st.write("Heatmap")
viz_heatmap = sns.heatmap(df.corr(), 
								center=0,
								cmap = sns.color_palette("vlag", as_cmap=True),
                                annot=True
								)

st.pyplot(viz_heatmap.figure)

st.write("Pairplot")
viz_pairplot = sns.pairplot(df)

st.pyplot(viz_pairplot.figure)



st.write("""Le Heatmap et le pairplot ci_dessus nous indique de fortes correlations positives entre « cylinders », « cubicinches », « hp » et « weightlbs » avec des coefficients allant de 0.85 à 0.95
Nous pouvons aussi constaté de fortes correlations négatives entre « mpp » et ces 4 derniers « cylinders »,  « cubicinches », « hp » et « weightlbs » avec des coefficients allant de -0.78 à -0.82
En revanche il est clair qu’il y a une corrélation faible voire nulle entre « years » et toutes les autres variables\n
\n\nCi-dessous 4 graphiques reprennants les fortes correlatons par régions""")



all_symbols = df.continent.unique()
options = st.multiselect("Choose stocks to visualize", all_symbols, all_symbols[:3])

st.write('You selected:', options)

df_choice = df[df.continent.isin(options)]




fig, ax= plt.subplots(figsize = (60,50))

plt.suptitle('Correlation par région', size = 50)

ax1 = fig.add_subplot(221)
ax1 = sns.barplot(x="cylinders", y="cubicinches", hue="continent", data=df_choice)
ax1.set_xlabel("cylinders",fontsize=40)
ax1.set_ylabel("cubicinches",fontsize=40)

ax2 = fig.add_subplot(222)
ax2 = sns.barplot(x="cylinders", y="weightlbs", hue="continent", data=df_choice)
ax2.set_xlabel("cylinders",fontsize=40)
ax2.set_ylabel("weightlbs",fontsize=40)

ax3 = fig.add_subplot(223)
ax3 = sns.barplot(x="cylinders", y="mpg", hue="continent", data=df_choice)
ax3.set_xlabel("cylinders",fontsize=40)
ax3.set_ylabel("mpg",fontsize=40)

ax4 = fig.add_subplot(224)
ax4 = sns.barplot(x="cylinders", y="hp", hue="continent", data=df_choice)
ax4.set_xlabel("cylinders",fontsize=40)
ax4.set_ylabel("hp",fontsize=40)



st.pyplot(ax.figure)
