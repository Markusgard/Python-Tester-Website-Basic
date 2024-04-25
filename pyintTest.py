from flask import Flask, redirect, render_template, request
from importlib import reload

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def game():
    return render_template("gamepage.html")

### !!! BAD IDEA TO USE ROUTE FOR THE INTERPRETER, TRY AJAX ###
###
### - code attempts is remembered by the browser. (RESOLVED)
### - code attempt is stuck on first attempt.
###
### > first attempt directs user to "/run" route, stays there (RESOLVED)
### > "/run" responds with old user code
### <> "/run" process in a separate python file did not work

@app.route("/run", methods=["POST"])
def run():
    import os

    code = request.form.get("py")

    if "import" in code:
        return "Prohibited"
    else: 

        codeind = code.replace("\n", "\n    ")      #Adds indentation

        with open("username.py", "x") as codefile:
            codefile.write("import math\n")
            codefile.write("def usercode():\n")
            codefile.write(f"    {codeind}\n")        #Added indentation for the function to work

        try:
            import username
            reload(username)
        except:
            os.remove("username.py")
            return "Syntax error"       #Exception for general errors

        try:
            result = username.usercode()    ### !!! ERROR: Result never updates
        except:
            os.remove("username.py")
            return "General error"
        os.remove("username.py")
        print(result)
        return str(result)      #String for now

if __name__ == "__main__":
    app.run(debug=True)