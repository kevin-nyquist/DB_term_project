import matplotlib.pyplot as plt

def make_pie_plot(data: dict[str, float], title):
    labels = list(data.keys())
    y = list(data.values()) 
    
    plt.pie(y, labels=labels)    
    plt.title(title)
    plt.savefig("idk.png")
