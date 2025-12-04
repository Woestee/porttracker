from flask import Flask, render_template, request, redirect, url_for, flash

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret"

    # Temporary in-memory "portfolio"
    portfolio = []

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/dashboard")
    def dashboard():
        # Calculate total value (for now treat each share as $10)
        total_value = sum(item["shares"] * item["price"] for item in portfolio)
        return render_template("dashboard.html",
                               portfolio=portfolio,
                               total_value=total_value)

    @app.route("/add-stock", methods=["GET", "POST"])
    def add_stock():
        nonlocal portfolio  # modifies the outer list

        if request.method == "POST":
            ticker = request.form.get("ticker", "").upper().strip()
            shares_raw = request.form.get("shares", "").strip()

            if not ticker or not shares_raw:
                flash("Ticker and Shares are required.")
                return redirect(url_for("add_stock"))

            try:
                shares = int(shares_raw)
                if shares <= 0:
                    raise ValueError
            except ValueError:
                flash("Shares must be a positive integer.")
                return redirect(url_for("add_stock"))

            # Placeholder: each share = $10.00 for now
            price = 10.0
            value = shares * price

            portfolio.append({
                "ticker": ticker,
                "shares": shares,
                "price": price,
                "value": value
            })

            flash(f"Added {shares} shares of {ticker}.")
            return redirect(url_for("dashboard"))

        return render_template("add_stock.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
