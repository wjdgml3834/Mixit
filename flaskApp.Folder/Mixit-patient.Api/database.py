from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session
import os, json

#functie voor de connectie van de database.
def session(username: str, password: str, database: str):
        
    url_object = URL.create(
        "mysql",
        username= username,
        password= password, 
        host="oege.ie.hva.nl",
        database= database,
        port=3306,
    )

    engine  = create_engine(url_object, connect_args={'ssl': {'ssl-mode': 'preferred'}})
    session = Session(engine)

    return session


#functie om de credentials op te halen van de databases
def get_creds(files):
    
    cwd         = os.path.dirname(os.path.realpath(__file__))
    filepath    = os.path.join(cwd, files)
    
    with open(filepath, "r") as f:
        return json.load(f)