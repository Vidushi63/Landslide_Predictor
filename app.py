
from flask import Flask, render_template, request
import random
app = Flask(__name__)

def calculate_risk(rainfall, slope, soil, vegetation):
    soil_factor=[10,20,30][soil]          # rock,sand,clay
    slope_factor=[5,20,35][slope]         # flat,moderate,steep
    veg_factor=[5,15,25][vegetation]      # dense,medium,low

    score = 0.45*rainfall + slope_factor + soil_factor + veg_factor
    score=min(score,100)

    if score<40:
        return "Low",score
    elif score<70:
        return "Medium",score
    else:
        return "High",score

def get_location_factors(city):
    city=city.lower()

    hilly=["shimla","manali","dehradun","gangtok","darjeeling","nainital"]
    coastal=["mumbai","chennai","kochi","goa"]

    if city in hilly:
        return 2,2,1   # weak soil, steep slope, medium vegetation
    elif city in coastal:
        return 1,0,2
    else:
        return 0,1,0

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():
    city=request.form["city"]
    date=request.form["date"]

    soil,slope,vegetation=get_location_factors(city)
    rainfall=random.randint(0,120)

    risk,score=calculate_risk(rainfall,slope,soil,vegetation)

    trend=[max(0,min(100,int(score+random.randint(-15,15)))) for _ in range(5)]

    return render_template("result.html",
                           city=city,
                           date=date,
                           rainfall=rainfall,
                           risk=risk,
                           score=int(score),
                           trend=trend)

if __name__=="__main__":
    app.run(debug=True)
