from flask import Flask, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# PostgreSQL database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:zahid@localhost/game_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class GameRound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(50), nullable=False)
    max_number = db.Column(db.Integer, nullable=False)
    secret_number = db.Column(db.Integer, nullable=False)
    attempts = db.Column(db.Integer, nullable=False)
    guesses = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def game():
    if "game" not in session:
        session["game"] = {
            "player_name": "",
            "max_number": 10,
            "secret_number": random.randint(1, 10),
            "attempts": 0,
            "guesses": [],
            "game_over": False
        }

    game = session["game"]
    message = ""

    # Restart game
    if request.method == "GET" and request.args.get("restart") == "1":
        game["secret_number"] = random.randint(1, game["max_number"])
        game["attempts"] = 0
        game["guesses"] = []
        game["game_over"] = False
        message = "Game restarted!"

    # Start/reset game
    if request.method == "POST" and "set_game" in request.form:
        game["player_name"] = request.form["player_name"]
        game["max_number"] = int(request.form["max_number"])
        game["secret_number"] = random.randint(1, game["max_number"])
        game["attempts"] = 0
        game["guesses"] = []
        game["game_over"] = False
        message = f"Game started for {game['player_name']}! Guess the number."

    # Handle guess
    elif request.method == "POST" and "guess" in request.form and not game["game_over"]:
        guess = int(request.form["guess"])
        game["attempts"] += 1
        game["guesses"].append(guess)

        if guess == game["secret_number"]:
            message = f"🎉 Correct! {game['player_name']} guessed it in {game['attempts']} attempts!"
            game["game_over"] = True

            guesses_str = ','.join(map(str, game["guesses"]))
            new_game = GameRound(
                player_name=game["player_name"],
                max_number=game["max_number"],
                secret_number=game["secret_number"],
                attempts=game["attempts"],
                guesses=guesses_str
            )
            db.session.add(new_game)
            db.session.commit()

        elif guess < game["secret_number"]:
            message = "⬆ Too low! Try a bigger number."
        else:
            message = "⬇ Too high! Try a smaller number."

    session["game"] = game
    leaderboard = GameRound.query.order_by(GameRound.attempts.asc(), GameRound.timestamp.asc()).limit(10).all()

    return render_template("game.html",
                           message=message,
                           attempts=game["attempts"],
                           guesses=game["guesses"],
                           game_over=game["game_over"],
                           max_number=game["max_number"],
                           player_name=game["player_name"],
                           leaderboard=leaderboard)

if __name__ == "__main__":
    app.run(debug=True)