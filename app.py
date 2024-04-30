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
        return '2Modules are prohibited! <span class="penalty">-10 points penalty<span>'
    elif "open" in code:
        return '2File modification is prohibited! <span class="penalty">-10 points penalty<span>'
    elif "print" in code:
        return "1Use 'return' rather than 'print()'"
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
            return "2Syntax error! <span class='penalty'>-10 points penalty<span>"       #Exception for general errors

        try:
            result = username.usercode()
            

        #Possible errors
        except Exception as error:
            os.remove("SolEld/username.py")
            return f"2{error}! -10 points penalty"
        os.remove("SolEld/username.py")


        return str("0" + str(result))

if __name__ == "__main__":
    app.run(debug=True)