from routes import app

app.config["VERSION"] = "0.2.0"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
