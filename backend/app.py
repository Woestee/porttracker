from flask import Flask, render_template, request, redirect, url_for, flash
import db
import alpha
from alpha import PriceLookupError


def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret"  # later: pull from env if you want

    # Initialize database
    db.init_db()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/dashboard")
    def dashboard():
        portfolio = db.get_portfolio()
        total_value = sum(item["value"] for item in portfolio)
        return render_template(
            "dashboard.html",
            portfolio=portfolio,
            total_value=total_value
        )

    @app.route("/add-stock", methods=["GET", "POST"])
    def add_stock():
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

            # Use Alpha Vantage for the real price
            try:
                price = alpha.get_latest_price(ticker)
            except PriceLookupError as e:
                flash(f"Could not fetch price for {ticker}: {e}")
                return redirect(url_for("add_stock"))

            db.add_holding(ticker, shares, price)
            flash(f"Added {shares} shares of {ticker} at ${price:.2f}.")
            return redirect(url_for("dashboard"))

        return render_template("add_stock.html")

    @app.route("/delete-stock/<int:holding_id>", methods=["POST"])
    def delete_stock(holding_id):
        db.delete_holding(holding_id)
        flash(f"Removed holding #{holding_id}.")
        return redirect(url_for("dashboard"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
