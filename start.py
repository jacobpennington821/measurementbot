from routes import app

if __name__ == "__main__":
    app.config["VERSION"] = "0.1"
    app.run(host="0.0.0.0")
