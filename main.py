from canvasapi import Canvas
import json
import datetime
import os
from webbrowser import open as showWeb

def getGrades():
    API_URL = "https://templeu.instructure.com/"

    API_KEY = open('key.txt').read()

    canvas = Canvas(API_URL, API_KEY)

    me = canvas.get_current_user()
    enrollments = list(me.get_enrollments())

    allGrades = {}
    i = 0
    while(i < len(enrollments)):
        score = enrollments[i].grades['current_score']
        grade = enrollments[i].grades['current_grade']
        course = canvas.get_course(enrollments[i].course_id).name
        
        allGrades[course] = score

        i+=1

    today = datetime.date.today()

    final = {
        "grades": allGrades,
        "date": str(today)
    }
    return final

def write(newData):
    data = load()
    data[newData['date']] = newData['grades']
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

def load():
    with open("data.json", "r") as file:
        return json.load(file)
    
def reset():
    with open('data.json', 'w') as file:
        json.dump({}, file, indent=4)

def updateGrades():
    write(getGrades())

def makeStyle():
    style = """
    table{
        border: 1px solid black;
        border-collapse: collapse;
    }

    td{
        border-left: 1px solid black;
        text-align: center;
        padding: 10px;
    }

    """
    return style

def toHTMLTable(grades):
    keys = list(grades.keys())
    vals = list(grades.values())

    keyTR = ""
    valTR = ""

    i = 0
    while(i < len(keys)):
        keyTR += f"<td><p>{keys[i]}</p></td>\n"
        valTR += f"<td><p>{vals[i]}</p></td>\n"
        i+= 1

    table = f"""
    <table>
        <tbody>
            <tr>{keyTR}</tr>
            <tr>{valTR}</tr>
        </tbody>
    </table>
    """
    return table

def makeWebsite():
    recentEntry = load()[list(load())[-1]]

    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <style>
                {makeStyle()}
            </style>
        </head>
        <body>
            <p>
                {toHTMLTable(recentEntry)}
            </p>
        </body>
    </html> 
    """

    with open('grades.html', 'w') as file:
        file.write(html)

def openWebsite(generate=True):
    if generate:
        makeWebsite()

    for file in os.listdir(os.getcwd()):
        if file.split(".")[1] == 'html':
            path = os.path.join(os.getcwd(), file)
            showWeb(path)
            return path