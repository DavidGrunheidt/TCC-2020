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
# CORES:
# myData = []
# $(".table-condensed").find("tbody").find("tr").each(function() {
#     var colums = $(this).find("td")
#     var date = $(colums[0]).find("span").text()
#     var cores = $(colums[3]).text()
#     myData.push("\""+date+"\" : \""+cores+"\"")
# })
# console.log(myData.reverse().join(",\n"))

top500EfficiencyData = {
	"06/2005" : 0.191,
	"11/2005" : 0.196,
	"11/2007" : 0.205,
	"06/2008" : 0.438,
	"11/2008" : 0.445,
	"11/2009" : 0.253,
	"11/2010" : 0.635,
	"06/2011" : 0.825,
	"11/2011" : 0.830,
	"06/2012" : 2.069,
	"11/2012" : 2.143,
	"06/2013" : 1.902,
	"06/2016" : 6.051,
	"06/2018" : 13.889,
	"11/2018" : 14.668,
	"06/2019" : 14.719,
}

top500CoreData = {
	"06/2005" : "65,536",
	"11/2005" : "131,072",
	"11/2007" : "212,992",
	"06/2008" : "122,400",
	"11/2008" : "129,600",
	"11/2009" : "224,162",
	"11/2010" : "186,368",
	"06/2011" : "548,352",
	"11/2011" : "705,024",
	"06/2012" : "1,572,864",
	"11/2012" : "560,640",
	"06/2013" : "3,120,000",
	"06/2016" : "10,649,600",
	"06/2018" : "2,282,544",
	"11/2018" : "2,397,824",
	"06/2019" : "2,414,592",
}

assert(len(top500EfficiencyData) == len(top500CoreData))
assert(list(top500EfficiencyData.keys()) == list(top500CoreData.keys()))

X = list(top500CoreData.values()) #Cores
Y = list(top500EfficiencyData.values()) #Efficiency
years = list(top500CoreData.keys()) #Years

fig, ax = plt.subplots()

ax.grid(color='grey', linestyle='dotted', zorder=0)
bar_plot = ax.bar(X, Y, align='center', color='grey', zorder=2)

for idx, rect in enumerate(bar_plot):
	height = rect.get_height()
	ax.text(rect.get_x() + rect.get_width()/2., height, years[idx], ha='center', va='bottom', rotation=0, fontsize=13)

ax.set_xlabel('Número de núcelos', fontsize=15)
ax.set_ylabel('Eficiência Energética (GFlops/watts)', fontsize=15)

ax.set_ylim(ymax=16)

plt.xticks(fontsize=15, rotation=25)
plt.yticks(fontsize=15)

for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.5)
    if (axis == "bottom"):
    	ax.spines[axis].set_zorder(3)
    else:
    	ax.spines[axis].set_zorder(0)

fig.set_size_inches(15, 5.2)
fig.tight_layout()
plt.savefig('Figure_Efficiency_X_Cores_Top500.pdf')  