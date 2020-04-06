import matplotlib.pyplot as plt

# Jquery javascript to get data from top500 site 
#EFFICENCY:
# myData = []
# $(".table-condensed").find("tbody").find("tr").each(function() {
#     var colums = $(this).find("td")
#     var date = $(colums[0]).find("span").text()
#     var efficiency = $(colums[6]).text()
#     myData.push("\""+date+"\" : "+efficiency)
# })
# console.log(myData.reverse().join(",\n"))

top500EfficiencyData = {
	"06/2005" : 0.191,
	"11/2005" : 0.196,
	"06/2006" : 0.196,
	"11/2006" : 0.196,
	"06/2007" : 0.196,
	"11/2007" : 0.205,
	"06/2008" : 0.438,
	"11/2008" : 0.445,
	"06/2009" : 0.445,
	"11/2009" : 0.253,
	"06/2010" : 0.253,
	"11/2010" : 0.635,
	"06/2011" : 0.825,
	"11/2011" : 0.830,
	"06/2012" : 2.069,
	"11/2012" : 2.143,
	"06/2013" : 1.902,
	"11/2013" : 1.902,
	"06/2014" : 1.902,
	"11/2014" : 1.902,
	"06/2015" : 1.902,
	"11/2015" : 1.902,
	"06/2016" : 6.051,
	"11/2016" : 6.051,
	"06/2017" : 6.051,
	"11/2017" : 6.051,
	"06/2018" : 13.889,
	"11/2018" : 14.668,
	"06/2019" : 14.719,
	"11/2019" : 14.719
}

X = list(top500EfficiencyData.keys()) #monthAndYears
Y = list(top500EfficiencyData.values()) #Efficiency

fig, ax = plt.subplots()

ax.plot(X, Y, color='black', marker='s', linewidth=2, markersize=6, clip_on=False)

ax.set_xlabel('Mês e Ano', fontsize=15)
ax.set_ylabel('Eficiência Energética (GFlops/watts)', fontsize=15)

ax.set_ylim(ymin=0, ymax=15)
ax.set_xlim(xmin="06/2005", xmax="11/2019")

ax.grid(color='grey', linestyle='dotted')

plt.xticks(fontsize=15, rotation=45)
plt.yticks(fontsize=15)

for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.5)
    ax.spines[axis].set_zorder(0)

fig.set_size_inches(15, 5)
fig.tight_layout()
plt.savefig('Figure_Efficiency_X_Years_Top500.pdf')  