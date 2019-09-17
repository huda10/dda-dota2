from flask import Flask

app = Flask(__name__)

@app.route("/save", methods = ['GET'])
def save():
    matchid = request.args.get('matchid')
    kills = float(request.args.get('kills'))
    deaths = float(request.args.get('deaths'))
    assists = float(request.args.get('assists'))
    last_hits = float(request.args.get('last_hits'))
    denies = float(request.args.get('denies'))
    gold_per_min = float(request.args.get('gold_per_min'))
    xp_per_min = float(request.args.get('xp_per_min'))
    time = float(request.args.get('time'))
    return "Information is saved successfully."
    
if __name__ == "__main__":
    app.debug = True
    app.run()
