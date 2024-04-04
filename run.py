from flaskr import create_app

if __name__ == "__main__":
    # Create the app
    app = create_app()
    app.logger.info("Starting app")
    # Run the app
    app.run()
