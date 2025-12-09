from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

# This random number will be the answer (1–10)
secret_number = random.randint(1, 10)

html = """
<h2>Guess the Number (1 - 10)</h2>
<form method="POST">
    <input type="number" name="guess" placeholder="Enter your guess" required>
    <button type="submit">Guess</button>
</form>
<p>{{ message }}</p>
"""

@app.route("/", methods=["GET", "POST"])
def game():
    message = ""
    if request.method == "POST":
        user_guess = int(request.form['guess'])
        if user_guess == secret_number:
            message = "🎉 Correct! You guessed it!"
        elif user_guess < secret_number:
            message = "Too low! Try again."
        else:
            message = "Too high! Try again."
    return render_template_string(html, message=message)

if __name__ == "__main__":
    app.run(debug=True)