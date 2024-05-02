from flask import Flask, redirect, render_template, request
from importlib import reload
import json

app = Flask(__name__)

@app.route("/")
def index():
    data=open("cases.json", "r")
    pdata = json.load(data)
    desc1 = pdata["1"]["description"]
    ldata=open("leaderboard.json", "r")
    ldata = json.load(ldata)
        
    return render_template("index.html", caseDesc1=desc1, leaderboard=ldata)

@app.route("/leaderboard")
def leaderboard():
    with open("leaderboard.json", "r") as data:
        pdata = json.load(data)
    return render_template("leaderboard.html", leaderboard=pdata)

@app.route("/game")
def game():
    with open("cases.json", "r") as data:
        pdata = json.load(data)
        dtil = pdata["1"]["title"]
        desc = pdata["1"]["description"]
        dset = pdata["1"]["dataset"]
        dres = pdata["1"]["result"]
    return render_template("gamepage.html", caseDesc=desc, caseDset=dset, caseDres=dres, caseTitle=dtil)



@app.route("/run/<usrRes>", methods=["POST"])
def run():
    import os

    code = request.form.get("py")
    answer = ""

    lineCount = 0
    for letter in code:
        if letter == "\n":
            lineCount += 1

    # Code inspection before running

    if "import" in code:
        return '2> Modules are prohibited! -10 points penalty'
    elif "open" in code:
        return '2> File modification is prohibited! <span class="penalty">-10 points penalty<span>'
    elif "print" in code:
        return "1> Use 'return' rather than 'print()'"
    elif lineCount < 1:
        return "1> Solving by hand is cheating!"
    else: 

        codeind = code.replace("\n", "\n    ")      #Adds indentation

        with open("username.py", "x") as codefile:
            codefile.write("import math\n")
            codefile.write("def usercode():\n")
            codefile.write(f"    {codeind}\n")

        try:
            import username
            reload(username)
        except:
            os.remove("username.py")
            return "2> Invalid syntax!-10 points penalty"       #Exception for syntax error

        try:
            result = username.usercode()



        #Possible errors

        except Exception as error:
            os.remove("username.py")
            return f"2> {error}! -10 points penalty"
        os.remove("username.py")


        #Check result. 

        correct = 0
        if result == answer:
            correct = 1


        return str("0" + correct + "> " + str(result))

if __name__ == "__main__":
    app.run(debug=True)