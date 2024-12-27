""" Application entry point """
from src import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5001', debug=True) # DEV
    # app.run(host='0.0.0.0', debug=False) # PROD

    
