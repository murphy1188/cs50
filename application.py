import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    db.execute("DELETE FROM stocks WHERE user_id=:id AND shares = 0", id=session["user_id"])
    user_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    total = user_cash[0]["cash"]
    portfolio = db.execute("SELECT id, symbol, price, shares, curr_price, curr_val FROM stocks JOIN users ON stocks.user_id = id WHERE id = :id", id=session["user_id"])
    for row in portfolio:
        check = lookup(row["symbol"])
        curr_price = check["price"]
        curr_val = curr_price * int(row["shares"])
        total += curr_val
        db.execute("UPDATE stocks SET curr_price=:curr_price, curr_val=:curr_val WHERE symbol=:symbol AND shares=:shares", curr_price=curr_price, curr_val=curr_val, symbol=row["symbol"], shares=row["shares"])
    portfolio = db.execute("SELECT id, symbol, price, shares, curr_val, curr_price, cash FROM stocks JOIN users ON stocks.user_id = id WHERE id = :id AND shares > 0 GROUP BY symbol", id=session["user_id"])
    balance = user_cash[0]["cash"]
    return render_template("index.html", portfolio=portfolio, balance=balance, total=total)

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Account settings"""
    user_id = session["user_id"]
    if request.method == "GET":
        return render_template("settings.html")
    elif request.method == "POST":
        if not request.form.get("curr_pass"):
            flash("Please enter your current password.")
            return render_template("settings.html")
        if not request.form.get("new_pass"):
            flash("Please enter your new password.")
            return render_template("settings.html")
        if not request.form.get("conf_new_pass"):
            flash("Please confirm your new password.")
            return render_template("settings.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id=:id", id=user_id)
        # Ensure current password entered is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("curr_pass")):
            flash("Sorry, the current password you entered is not correct.")
            return render_template("settings.html")
        elif check_password_hash(rows[0]["hash"], request.form.get("curr_pass")):
            hash = generate_password_hash(request.form.get("new_pass"))
            db.execute("UPDATE users SET hash=:hash WHERE id=:id", hash=hash, id=user_id)
            flash("Password successfully changed.")
            return redirect("/")





@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    user = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
    balance = usd(user[0]['cash'])

    if request.method == "POST":
        if request.form.get("symbol") and not request.form.get("shares"):
            quote = lookup(request.form.get("symbol"))
            symbol = request.form.get("symbol")
            if quote == None:
                flash("Sorry, no stock was found for symbol  \"{}\". Try another search.".format(symbol))
                return render_template("buy.html")
            else:
                return render_template("buy2.html", user=user, quote=quote)

        if request.form.get("symbol", "shares"):
            arg_check_shares = request.form.get("shares")
            quote = lookup(request.form.get("symbol"))
            if arg_check_shares.isdigit() == False:
                flash("Must enter positive integer for shares.")
                return render_template("buy2.html", quote=quote)
            if (int(arg_check_shares) < 1):
                flash("Must enter positive integer for shares.")
                return render_template("buy2.html", quote=quote)
            shares = request.form.get("shares")
            symbol = request.form.get("symbol")
            quote = lookup(symbol)
            price = quote['price']
            int_shares = int(shares)
            date_time = datetime.now()
            curr_price = price
            curr_val = int_shares * curr_price
            action = "Purchased"
            trans_amount = curr_price * int(shares)
            if trans_amount > float(user[0]['cash']):
                flash("Not enough cash available!")
                return render_template("buy2.html", quote=quote)
            balance = (user[0]["cash"]) - (price * int(shares))
            port_symbols = db.execute("SELECT * FROM stocks WHERE user_id=:id", id=session["user_id"])
            exist = "false"
            for row in port_symbols:
                if symbol not in row['symbol']:
                    exist = "false"
                    continue
                if symbol in row['symbol']:
                    avg_price = ((curr_price * int_shares) + (row['price'] * row['shares'])) / (int_shares + row['shares'])
                    db.execute("UPDATE stocks SET shares = shares+:shares, price=:price WHERE user_id=:id AND symbol=:symbol", shares=shares, price=avg_price, id=session["user_id"], symbol=symbol)
                    exist = "true"
                    break
            if exist != "true":
                db.execute("INSERT INTO stocks (user_id, symbol, price, shares, curr_price, curr_val, timestamp) VALUES (:user_id, :symbol, :price, :shares, :curr_price, :curr_val, :timestamp)", user_id=user[0]["id"], symbol=symbol, price=price, shares=shares, curr_price=curr_price, curr_val=curr_val, timestamp=date_time)
            db.execute("UPDATE users SET cash=:balance WHERE id=:id", balance=balance, id=session["user_id"])
            db.execute("INSERT INTO history (user_id, action, shares, symbol, price, trans_amount, date_time) VALUES (:user_id, :action, :shares, :symbol, :price, :trans_amount, :date_time)", user_id=session["user_id"], action=action, shares=shares, symbol=symbol, price=curr_price, trans_amount=trans_amount, date_time=date_time)
            if int_shares == 1:
                flash("Congratulations! You successfully purchased {} share of {}.".format(shares, symbol))
            else:
                flash("Congratulations! You successfully purchased {} shares of {}.".format(shares, symbol))
            return redirect("/")

    elif request.method == "GET":
        return render_template("buy.html", user=user, balance=balance)



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        portfolio = db.execute("SELECT * FROM history WHERE user_id=:id", id=session["user_id"])
        return render_template("history.html", portfolio=portfolio)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please enter your username.")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            username = request.form.get("username")
            flash("Please enter your password.")
            return render_template("login.html", username=username)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Sorry, the username and/or password entered are not correct.")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # Ensure stock symbol was submitted, flash error message if not
        if not request.form.get("symbol"):
            flash("Sorry, you must enter a symbol.")
            return render_template("quote.html")
        # Flash error message if input stock symbol does not match any stock
        elif not lookup(request.form.get("symbol")):
            symbol = request.form.get("symbol")
            flash("Sorry, \"{}\" does not match any stocks.".format(symbol))
            return render_template("quote.html")
        # Return quote
        else:
            quote = lookup(request.form.get("symbol"))
            return render_template("quoted.html", quote=quote)
    elif request.method == "GET":
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please enter a username.")
            return render_template("register.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            username= request.form.get("username")
            flash("Please enter a password.")
            return render_template("register.html", username=username)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            username= request.form.get("username")
            flash("Please confirm your password.")
            return render_template("register.html", username=username)

        # Check that password and confirm_password match
        elif request.form.get("password") != request.form.get("confirmation"):
            username= request.form.get("username")
            flash("Sorry, passwords do not match.")
            return render_template("register.html", username=username)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Check that user name has not been taken already
        if len(rows) > 0:
            flash("Sorry, username is already taken.")
            return render_template("register.html")

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username, password=hash)
        flash("Welcome to CS50 Finance!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
    portfolio = db.execute("SELECT * from stocks WHERE user_id=:id AND shares > 0 ORDER BY symbol", id=session["user_id"])
    if request.method == "GET":
        return render_template("sell.html", user=user, portfolio=portfolio)

    if request.method == "POST":

        if request.form.get("symbol", "shares"):
            arg_check_shares = request.form.get("shares")
            select_shares = request.form.get("symbol")
            if select_shares == None:
                flash("Sorry, please select a symbol.")
                return render_template("sell.html", portfolio=portfolio)
            if arg_check_shares.isdigit() == False:
                flash("Must enter positive integer for shares.")
                return render_template("sell.html", portfolio=portfolio)
            if (int(arg_check_shares) < 1 ):
                flash("Must enter positive integer for shares.")
                return render_template("sell.html", portfolio=portfolio)
            shares = db.execute("SELECT shares, timestamp FROM stocks WHERE user_id=:id AND symbol=:symbol AND shares > 0", id=session["user_id"], symbol=request.form.get("symbol"))
            user_id=session["user_id"]
            curr_shares = shares[0]['shares']
            timestamp = shares[0]['timestamp']
            symbol = request.form.get("symbol")
            quote = lookup(symbol)
            curr_price = (quote['price'])
            sell_shares = request.form.get("shares")
            if int(sell_shares) > curr_shares:
                flash("Sorry! You don't have enough shares.")
                return render_template("sell.html", portfolio=portfolio)
            new_shares = curr_shares - int(sell_shares)
            date_time = datetime.now()
            trans_amount = int(sell_shares) * curr_price
            action = "Sold"
            balance = (user[0]["cash"]) + (curr_price * int(sell_shares)) # Multiply current price by shares sold, add to user's current balance
            db.execute("UPDATE stocks SET shares=:shares WHERE user_id=:id AND symbol=:symbol AND timestamp=:timestamp", id=session["user_id"], shares=new_shares, symbol=symbol, timestamp=timestamp)
            db.execute("INSERT INTO history (user_id, action, shares, symbol, price, trans_amount, date_time) VALUES (:user_id, :action, :shares, :symbol, :price, :trans_amount, :date_time)", user_id=session["user_id"], action=action, shares=sell_shares, symbol=symbol, price=curr_price, trans_amount=trans_amount, date_time=date_time)
            db.execute("UPDATE users SET cash=:balance WHERE id=:id", balance=balance, id=session["user_id"])
            if sell_shares == 1:
                flash("Congratulations! You successfully sold {} share of {} for {}.".format(shares, symbol, usd(trans_amount)))
            else:
                flash("Congratulations! You successfully sold {} shares of {} for {}.".format(sell_shares, symbol, usd(trans_amount)))
            return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
