from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder="templates")

database_products = {

}

@app.route("/products")
def users():
	return render_template(
		"products.html", products=database_products,
	)

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		product: str = request.form.get("product")
		try:
			price: int = int(request.form.get("price"))
			discount :int = int(request.form.get("discount"))
			if price < 0 or discount < 0:
				return
		except :
			return render_template("error.html")
		database_products[product] = (price,discount)
		return redirect('/login')
	return render_template("login.html")

@app.route("/")
def main():
	return render_template("main.html")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=9000, debug=True)