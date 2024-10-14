from flask import Flask, redirect, render_template, request, flash, session, jsonify
from importlib import reload
import json
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
import random
import importlib
from datetime import date
from multiprocessing import Process

app = Flask(__name__)
app.secret_key = 'some_secret'
app.debug = True

### OTHER FUNCTIONS ###

def sok_etter_user_id(username):
    with open("leaderboard.json", "r") as file:
                pdata = json.load(file)
    for bruker in pdata:
            if pdata[bruker]["username"] == username:
                user_id = bruker
                break
            else:
                 user_id=False
    return user_id
    
### ERROR HANDLERS ###

@app.errorhandler(HTTPException)
def exception_handler(e):
    
    if isinstance(e,str):
        name=e
        code="unexpected error"

        return render_template("error_handler.html", code=code, name=name)
    elif e.code == 404:
        err_name = "This page was either deleted, or doesn't exist."
    else:
        err_name = e.name
    
    return render_template("error_handler.html", code=e.code, name=err_name)

### ROUTES ###

@app.route("/")
def index():
    
    data=open("cases.json", "r")
    pdata = json.load(data)
    desc1 = [pdata["1"]["tiny_desc"], pdata["1"]["title"]]
    desc2 = [pdata["2"]["tiny_desc"], pdata["2"]["title"]]
    desc3 = [pdata["3"]["tiny_desc"], pdata["3"]["title"]]

    ldata=open("leaderboard.json", "r")
    ldata = json.load(ldata)
    username=session.get("username")
    if username == None:
        placement = "Not Found, 404"
    else:
        user_id=sok_etter_user_id(username)
        with open("leaderboard.json", "r") as file:
                pdata = json.load(file)
                placement=pdata[user_id]["placement"]
                    
        
    return render_template("index.html", caseDesc1=desc1,caseDesc2=desc2,caseDesc3=desc3, leaderboard=ldata, username=session.get("username"),placement=placement,role=session.get("role"))

@app.route("/check_username", methods=["GET"])
def check_username():
    username = request.args.get("user")
    print(username)
    with open("leaderboard.json", "r") as file:
        pdata = json.load(file)
        for bruker in pdata:
            if pdata[bruker]["username"] == username:
                return "1"
        return "0"

@app.route("/leaderboard")
def leaderboard():
    with open("leaderboard.json", "r") as file:
        pdata = json.load(file)
        username=session.get("username")
        for bruker in pdata:
            if pdata[bruker]["username"] == username:
                user_id=bruker
                break
        placement=pdata[bruker]["placement"]
        Admin=session.get("role")
        return render_template("leaderboard.html", Admin=Admin, username=session.get("username"),placement=placement)

@app.route("/getleaderboard/<sortm>")
def board(sortm):
    with open("leaderboard.json", "r") as data:
        pdata = json.load(data)

    #Sort & search method

    match sortm:
        case "place":
            sdata = sorted(pdata.values(), key=lambda x: x["placement"])
            return sdata
        case "name":
            sdata = sorted(pdata.values(), key=lambda x: x["username"])
            return sdata
        case _:
            sdata = {}
            for i, user in enumerate(pdata.values()):
                if sortm in user["username"].lower():
                    sdata[i] = user
            return sdata


@app.route("/profile")
def profile():
    return render_template("profile.html",username=session.get("username"))




@app.route("/game/<gameId>")
def game(gameId):
    user = session.get("username")
    placement = ""
    with open("cases.json", "r") as data:
        pdata = json.load(data)
        dtil = pdata[gameId]["title"]
        desc = pdata[gameId]["description"]
        dset = pdata[gameId]["dataset"]
        with open("leaderboard.json", "r") as data:
            pdata = json.load(data)
            user_id=sok_etter_user_id(session.get("username"))
            placement=pdata[user_id]["placement"]
    return render_template("gamepage.html", caseDesc=desc, caseDset=dset, caseTitle=dtil, caseId=gameId, username=session.get("username"),placement = placement)


# run() will return a string of format "XX> Message", where 'X' are numbers.
# The page will only display the '>' sign and the message, the numbers only determines color and result respectively.


@app.route("/run/<gameId>", methods=["POST"])
def run(gameId):
    import os

    user = session.get("username")

    with open("cases.json", "r") as data:
        pdata = json.load(data)
        answer = pdata[gameId]["result"]
        gameDset = pdata[gameId]["dataset"]

    code = request.form.get("py")
    print(code)

    # Code inspection before running

    if "import" in code:
        return '20> Modules are prohibited! -1 points penalty'
    elif "open" in code:
        return '20> File modification is prohibited! -1 points penalty'
    elif "print(" in code:
        return "10> Use 'return' rather than 'print()'"
    else: 

        codeind = code.replace("\n", "\n    ")      #Adds indentation

        with open(f"{user}.py", "x") as codefile:
            codefile.write("import math\n")
            codefile.write("def usercode():\n")
            codefile.write(f"    data = '{gameDset}'\n")
            codefile.write(f"    {codeind}\n")

        try:
            userFunction = __import__(user)
            userFunction
            reload(userFunction)                # Prepares for next run
        except Exception as error:
            # os.remove(f"{user}.py")
            return f"20>Invalid syntax!-1 points penalty"       # Exception if app.py fails to run the user's code
        

        try:
            process = Process(target=userFunction.usercode)     # Tests if the code times out
            process.start()
            process.join(5)
            if process.is_alive():
                process.terminate()
                os.remove(f"{user}.py")
                return "20>Your code is taking too long! -1 points penalty"
            result = userFunction.usercode()            # Runs the user's code again if it didn't time out


        #Possible errors

        except Exception as error:
            os.remove(f"{user}.py")
            return f"20> {error}! -1 points penalty"
        os.remove(f"{user}.py")


        #Check the user's result.
        #2 = wrong answer. 1 = correct answer. 0 = ignored.

        compared = "1"
        if str(result) == answer:
            compared = "2"
            


        return str("0" + compared + "> " + str(result))

def valid_login(username,password):
        with open("leaderboard.json", "r") as file:
            pdata = json.load(file)
            user_id=sok_etter_user_id(username)
            if user_id:
                if pdata[user_id]["username"] == username:
                    print(pdata[user_id]["password"])
                    print("HER E PASSORDET")
                    print(password)
                    hash=check_password_hash(pdata[user_id]["password"], password)
                    print(hash)
                    if hash:
                        return True
                    else:
                        
                        return False
            else:
                 return False
            
            


@app.route("/create_account", methods=["POST"])
def create_account():
    # Get username and password from the request form data
    username = request.form.get("username")
    password = request.form.get("password")
    password = generate_password_hash(password)
    if len(password) < 8:
        flash("Password has to be atleast 8 characters")
        return render_template("create_account.html")
    if username =="" or password == "":
        flash("Missing either password or username")
        return render_template("create_account.html")
    with open("leaderboard.json", "r") as file:
        pdata = json.load(file)
        for bruker in pdata:
            if pdata[bruker]["username"] == username:
                flash('a person with that username allready exsist')
                return render_template("create_account.html")
                break
            
        id = random.randint(1, 999)
        while id in pdata:
            id = random.randint(1, 999)
            # Add the new user to the data
        placement_list=[]
        for brukere in pdata:
            placement_list.append(int(pdata[bruker]["points"]))
        placement=len(placement_list)+1


        pdata[id] = {"username": username, "password": password,"points":0,"placement":placement, "date":"", "role":"None"}
            
        with open("leaderboard.json", "w") as file:
            json.dump(pdata, file,indent=4)

            session["username"] = username
            return redirect("/")
        


@app.route("/delete_user/<user>", methods=["GET","POST"])
def delete_user(user):
    with open("leaderboard.json", "r") as file:
            pdata = json.load(file)
            username = user
            if not session.get("username"):
                return exception_handler("User not logged in 401")
            if session.get("role") != "Admin":
                return exception_handler("Only admins can delete users.")
            user_id = sok_etter_user_id(username)
            if user_id:
                keys_to_delete = []
                keys_to_delete.append(user_id)
                for bruker in pdata:
                            if pdata[bruker]["placement"] >= pdata[user_id]["placement"]:
                                pdata[bruker]["placement"]=pdata[bruker]["placement"]-1
                                #RETTER PÅ LEADERBOARD
                for key in keys_to_delete:
                    pdata.pop(key)
                with open("leaderboard.json", "w") as file:
                    json.dump(pdata, file,indent=4)
                if username != session.get("username"):
                    return redirect("/leaderboard")
                else:
                    return redirect("/logout")
                
@app.route("/delete_profile", methods=["GET","POST"])
def delete_profile():

        with open("leaderboard.json", "r") as file:
            pdata = json.load(file)
        username = request.args.get("username") or request.form.get("username")    
        if username == None:
            username = session.get("username")
            if not session.get("username"):
                return exception_handler("User not logged in 401")
        
        
        user_id = sok_etter_user_id(username)
        if user_id:
            keys_to_delete = []
            keys_to_delete.append(user_id)
            for bruker in pdata:
                        if pdata[bruker]["placement"] >= pdata[user_id]["placement"]:
                            pdata[bruker]["placement"]=pdata[bruker]["placement"]-1
                            #RETTER PÅ LEADERBOARD
            for key in keys_to_delete:
                pdata.pop(key)

            with open("leaderboard.json", "w") as file:
                json.dump(pdata, file,indent=4)

            if request.form.get("username") and username != session.get("username"):
                return redirect("/leaderboard")
            elif username == session.get("username"):
                return redirect("/logout")
            else:
                return redirect("/logout")
        
            
    
  


@app.route("/login", methods=["GET", "POST"])
def login():
    with open("leaderboard.json", "r") as file:
                pdata = json.load(file)
                username = request.form.get("username")
                password = request.form.get("password")
                if valid_login(username,password):
                    session["username"] = username
                    user_id=sok_etter_user_id(username)
                    session["role"] = pdata[user_id]["role"]
                    return redirect("/")
                else:
                    flash("Invalid username or password!")
                    return redirect("/")
    
        

    



@app.route("/logout")
def logout():
 session.clear()
 return redirect("/")

@app.route("/route_to_create_account")
def routeCA():
    return render_template("create_account.html")
    

@app.route("/placement", methods=["GET", "POST"])
def placement():
    
        with open("leaderboard.json", "r") as file:
            pdata = json.load(file)
        if request.args.get("points") is not None:
            points = int(request.args.get("points"))
            username = session.get("username")
            user_id=sok_etter_user_id(username)
            pdata[user_id]["points"] += points
            pdata[user_id]["date"] = str(date.today())
            
            if not username:
                exception_handler("User not logged in 401")
                

        elif request.form.get("points") is not None:
            points = int(request.form.get("points"))
            username = request.form.get("username")
            user_id=sok_etter_user_id(username)
            pdata[user_id]["points"] = points

        else:
            return exception_handler("Points parameter is missing 400")
                
            

    
        sorted_users = sorted(pdata.items(), key=lambda item: item[1]["points"], reverse=True)
        for index, (bruker, user_data) in enumerate(sorted_users):
            user_data["placement"] = index + 1
        try:
            with open("leaderboard.json", "w") as file:
                json.dump(pdata, file, indent=4)
        except Exception as e:
            exception_handler(e)

        return redirect("/leaderboard")

if __name__ == "__main__":
    app.run(debug=True)









