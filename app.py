from flask import Flask, redirect, render_template, request
from importlib import reload

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def game():
    return render_template("gamepage.html")



@app.route("/run", methods=["POST"])
def run():
    import os

    code = request.form.get("py")

    if "import" in code:
        return "Prohibited"
    elif "print" in code:
        return "Please use 'return' instead of 'print()'"
    else: 

        codeind = code.replace("\n", "\n    ")      #Adds indentation

        with open("SolEld/username.py", "x") as codefile:
            codefile.write("import math\n")
            codefile.write("def usercode():\n")
            codefile.write(f"    {codeind}\n")

        try:
            import username
            reload(username)
        except:
            os.remove("SolEld/username.py")
            return [True, "Syntax error"]       #Exception for general errors

        try:
            result = username.usercode()    ### !!! ERROR: Result never updates
        except:
            os.remove("SolEld/username.py")
            return "General error"
        os.remove("SolEld/username.py")
        return str(result)      #String for now

if __name__ == "__main__":
    app.run(debug=True)