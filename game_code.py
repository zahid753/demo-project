from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

# Secret number (1-10)
secret_number = random.randint(1, 10)
attempts = 0

html = """
<h2>🎲 Guess the Number (1 - 10)</h2>
<form method="POST">
    <input type="number" name="guess" placeholder="Enter your guess" required>
    <button type="submit">Guess</button>
</form>
<p>{{ message }}</p>
<p>Attempts: {{ attempts }}</p>
{% if game_over %}
<form method="GET">
    <button type="submit" name="restart" value="1">Restart Game 🔄</button>
</form>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def game():
    global secret_number, attempts
    message = ""
    game_over = False

    # Handle Restart button
    if request.method == "GET" and request.args.get("restart") == "1":
        secret_number = random.randint(1, 10)
        attempts = 0

    if request.method == "POST":
        attempts += 1
        user_guess = int(request.form['guess'])
        if user_guess == secret_number:
            message = f"🎉 Correct! You guessed it in {attempts} attempts!"
            game_over = True
        elif user_guess < secret_number:
            message = "⬆ Too low! Try a bigger number."
        else:
            message = "⬇ Too high! Try a smaller number."

    return render_template_string(html, message=message, attempts=attempts, game_over=game_over)

if __name__ == "__main__":
    app.run(debug=True)