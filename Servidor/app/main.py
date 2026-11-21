from flask import Flask, request, make_response, redirect

app = Flask(__name__)

FORM = """
<h1>Login</h1>
<form method="POST" action="/login">
  <input name="usuario" placeholder="usuario">
  <input name="senha" type="password" placeholder="senha">
  <button>Entrar</button>
</form>
"""

@app.get("/")
def index():
    return FORM

@app.post("/login")
def login():
    if request.form["usuario"] == "user" and request.form["senha"] == "123456":
        resp = make_response(redirect("/admin"))
        resp.set_cookie("sessao", "abc123")
        return resp
    return "Credenciais invalidas", 401

@app.get("/admin")
def admin():
    if request.cookies.get("sessao") == "abc123":
        return "<h1>Area protegida</h1>"
    return "Nao autorizado", 403

app.run(host="0.0.0.0", port=5000)