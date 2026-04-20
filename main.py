from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

orders = []
users = []
prices = {
    "20_crowns": 27,
    "50_crowns": 67.5
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
</head>
<body>

<h1>📥 الطلبات</h1>

{% for order in orders %}
<div style="border:1px solid black; padding:10px; margin:10px;">
    <p>👤 {{order.name}}</p>
    <p>📦 {{order.service}}</p>
    <p>📌 {{order.data}}</p>

    <form method="post" action="/done">
        <input type="hidden" name="id" value="{{loop.index0}}">
        <button>✅ تم التنفيذ</button>
    </form>

    <form method="post" action="/reject">
        <input type="hidden" name="id" value="{{loop.index0}}">
        <button>❌ رفض</button>
    </form>

    <form method="post" action="/reply">
        <input type="hidden" name="id" value="{{loop.index0}}">
        <input name="msg" placeholder="رد على العميل">
        <button>💬 إرسال</button>
    </form>
</div>
{% endfor %}

<h2>💰 إدارة الأسعار</h2>
<form method="post" action="/price">
    <input name="item" placeholder="اسم المنتج">
    <input name="value" placeholder="السعر">
    <button>تحديث</button>
</form>

<h2>👤 المستخدمين</h2>
{% for user in users %}
<p>{{user}}</p>
{% endfor %}

<h2>🌍 اللغة</h2>
<form method="post" action="/lang">
    <select name="lang">
        <option value="ar">عربي</option>
        <option value="en">English</option>
    </select>
    <button>تغيير</button>
</form>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, orders=orders, users=users)

@app.route("/done", methods=["POST"])
def done():
    orders.pop(int(request.form["id"]))
    return redirect("/")

@app.route("/reject", methods=["POST"])
def reject():
    orders.pop(int(request.form["id"]))
    return redirect("/")

@app.route("/reply", methods=["POST"])
def reply():
    print("رد:", request.form["msg"])
    return redirect("/")

@app.route("/price", methods=["POST"])
def price():
    prices[request.form["item"]] = request.form["value"]
    return redirect("/")

@app.route("/lang", methods=["POST"])
def lang():
    print("اللغة:", request.form["lang"])
    return redirect("/")

@app.route("/add_test")
def add_test():
    orders.append({
        "name": "Ava",
        "service": "شراء كراونز",
        "data": "ID: 12345"
    })
    return "تم"

app.run(host="0.0.0.0", port=5000)
