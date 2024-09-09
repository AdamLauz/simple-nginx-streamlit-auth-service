from flask import Flask, request, redirect, url_for


app = Flask(__name__)


@app.route("/authentication", methods=["GET"])
def authentication():
    # Redirect to an external URL for authentication, passing the redirect_to_url
    external_auth_url = f"https://external-auth-provider.com/auth?redirect_uri={request.args.get('redirect_to_url')}"
    return redirect(external_auth_url)


# Route to handle login callback with a 'code' parameter
@app.route("/authentication/login", methods=["GET"])
def login():
    # Get the 'code' parameter from the URL
    code = request.args.get("code")

    if not code:
        return "Error: No code provided", 400

    # Exchange the 'code' for a 'token' (mocking the exchange here)
    token = f"token_for_{code}"  # You can replace this with an actual token exchange logic

    # Redirect to a new URL with the 'token' parameter instead of the 'code'
    new_url = url_for('login', token=token, _external=True)
    return redirect(new_url)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
