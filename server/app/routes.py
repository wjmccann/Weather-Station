from app import app
from flask import render_template, redirect, url_for
from flask import request
from app import db
from app.models import Day, Temperature, Rain
from sqlalchemy import func

currentData = {
        'date': '',
        'temp': 0.0,
        'windspeed': 0.0,
        'winddir': '',
        'humidity': '',
        'rain': 0.0
        }

temprange = {
        'maxtemp': 0.0,
        'maxtime': '',
        'mintemp': 0.0,
        'mintime': '',
        'avetemp': 0.0
        }

temps = []
temptime = []
rain = []
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        year = request.form['date'][:4]
        month = request.form['date'][5:7]
        day = request.form['date'][8:10]
        return redirect(url_for('day_page', y=year, m=month, dy=day))
        print(request.form['date'])
    return render_template('index.html', myData=currentData, range=temprange)

def parse_data(data):
    latestDate = str(data['time'])
    if latestDate[:10] != currentData['date'][:10]:
        d = Day(year=currentData['date'][:4], month=currentData['date'][5:7], day=currentData['date'][8:10], maxtemp=temprange['maxtemp'], mintemp=temprange['mintemp'], avetemp=temprange['avetemp'], rain=currentData['rain'])
        db.session.add(d)
        db.session.commit()
        del temps[:]
        del temptime[:]
        del rain[:]
        print("New Day!")
    currentData['date'] = str(data['time'])
    try:
        try:
            checkDate = Temperature.query.all()
            if checkDate[0].date[:10] != latestDate[:10]:
                Temperature.query.delete()
                Rain.query.delete()
                db.session.commit()
        except Exception:
            pass

        currentData['temp'] = round((float(data['temperature_F'])-32)*(0.55), 2)
        t = Temperature(date = currentData['date'], temp = currentData['temp'])
        db.session.add(t)
        db.session.commit()

        myTemps = Temperature.query.all()
        for x in myTemps:
            temps.append(x.temp)
            temptime.append(x.date)

        temprange['maxtemp'] = max(temps)
        temprange['maxtime'] = temptime[temps.index(max(temps))]
        temprange['mintemp'] = min(temps)
        temprange['mintime'] = temptime[temps.index(min(temps))]
        temprange['avetemp'] = round(sum(temps) / float(len(temps)), 2)
        
        del temps[:]
        del temptime[:]
        
        
    except Exception:
        pass
    try:
        currentData['windspeed'] = round(float(data['wind_speed_mph'])*1.60934, 2)
        #print(currentWindSpeed)
    except Exception:
        pass
    try:
        currentData['winddir'] = str(data['wind_dir'])
        #print(currentWindDir)
    except Exception:
        pass
    try:
        currentData['humidity'] = str(data['humidity'])
        #print(currentHumidity)
    except Exception:
        pass
    try:
        r = Rain(rain=float(data['raincounter_raw']))
        db.session.add(r)
        db.session.commit()
        myRain = Rain.query.all()
        for x in myRain:
            rain.append(x.rain)
        currentData['rain'] = (max(rain) - min(rain)) * 0.25
        del rain[:]

        #print(currentRain)
    except Exception:
        pass




@app.route('/data', methods=['GET', 'POST'])
def parseData():

    if request.is_json:
        data = request.get_json()
        parse_data(data)
    return render_template('index.html', myData=currentData)

@app.route('/<y>/<m>/<dy>')
def day_page(y, m, dy):
    myDay = ''
    days = Day.query.all()
    for d in days:
        if str(d.year)==str(y):
            if str(d.month)==str(m):
                if str(d.day)==str(dy):
                    print("Got the Right Day!")
                    myDay = d
    
    return render_template('day.html', data=myDay)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    myDays = []
    if request.method == 'POST':
        y = request.form['date'][:4]
        m = request.form['date'][5:7]
        days = Day.query.all()
        for d in days:
            if str(d.year)==str(y):
                if(d.month)==str(m):
                    myDays.append(d)
        
        for d in myDays:
            print(d)

        if request.form['options']=='max':
            myTitle = "Maximum Temperatures for " + str(request.form['date'][5:7]) + "/" + str(request.form['date'][:4])
            return render_template('maxtemp.html', title=myTitle, data=myDays)
        if request.form['options']=='min':
            myTitle = "Minimum Temperatures for " + str(request.form['date'][5:7]) + "/" + str(request.form['date'][:4])
            return render_template('mintemp.html', title=myTitle, data=myDays)
        if request.form['options']=='ave':
            myTitle = "Average Temperatures for " + str(request.form['date'][5:7]) + "/" + str(request.form['date'][:4])
            return render_template('avetemp.html', title=myTitle, data=myDays)
        if request.form['options']=='rain':
            myTitle = "Rainfall for " + str(request.form['date'][5:7]) + "/" + str(request.form['date'][:4])
            return render_template('rainfall.html', title=myTitle, data=myDays)
    return render_template('graph.html')
@app.route('/daily')
def daily():
    myDays = []
    newDay = {
            'year': '',
            'month': '',
            'day': '',
            'hour': '',
            'minute': '',
            'temp': ''
            }

    myTemps = Temperature.query.all()
    for x in myTemps:
        temps.append(x.temp)
        temptime.append(x.date)

    index =0
    for t in temptime:
        newDay['year'] = str(t[:4])
        newDay['month'] = str(t[5:7])
        newDay['day'] = str(t[8:10])
        newDay['hour'] = str(t[11:13])
        newDay['minute'] = str(t[14:16])
        newDay['temp'] = temps[index]
        index += 1
        myDays.append(newDay)
        newDay = {
                'year': '',
                'month': '',
                'day': '',
                'hour': '',
                'minute': '',
                'temp': ''
                }

    title = "Temperatures for " + str(temptime[0][8:10]) + "/" + str(temptime[0][5:7]) + "/" + str(temptime[0][:4])
    return render_template('daily.html', title=title, data=myDays)
