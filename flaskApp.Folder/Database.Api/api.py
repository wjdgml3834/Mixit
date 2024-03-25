from sqlalchemy import URL, create_engine, text
from flask import Flask, jsonify
import json, os

app = Flask(__name__)


#functie voor de connectie van de database.
def connection(username:str, password:str, database:str):
        
    url_object = URL.create(
        "mysql",
        username= username,
        password= password, 
        host="oege.ie.hva.nl",
        database= database,
        port=3306,
    )

    engine  = create_engine(url_object, connect_args={'ssl': {'ssl-mode': 'preferred'}})
    conn    = engine.connect()

    return conn


#functie om de credentials op te halen van de databases
def get_creds(files):

    cwd         = os.path.dirname(os.path.realpath(__file__))
    filepath    = os.path.join(cwd, files)
    
    with open(filepath, "r") as f:
        return json.load(f)


#Geeft data terug van een patient op basis van de hash van een bsn-nummer
@app.route("/patient/<hashedbsn>")
def patient(hashedbsn):

    creds   = get_creds("cred.json")
    conn    = connection(creds['mixit-patient']['username'], creds['mixit-patient']['password'], creds['mixit-patient']['database_name'])

    try:
        keypairDict = {
            "hbsn": text(hashedbsn)
        }

        query   = text("select * from patient where hashedbsn = :hbsn;")
        result  = conn.execute(query, keypairDict)

        for row in result:
            respond = jsonify({'id': row.id, 'firstname': row.firstname, 'lastname': row.lastname, 'birthdate': row.birthdate, 'comment': row.comment, 'hashedbsn': row.hashedbsn, 'address_id': row.address_id})
        conn.close()
        return respond
    except:
        respond = jsonify({'message': 'patient not found'}), 404
        conn.close()
        return respond
    

#Geeft data terug van het adres op basis van de hash van een bsn-nummer
@app.route("/address/<hashedbsn>")
def address(hashedbsn):

    creds   = get_creds("cred.json")
    conn    = connection(creds['mixit-patient']['username'], creds['mixit-patient']['password'], creds['mixit-patient']['database_name'])

    try:
        keypairDict = {
            "hbsn": text(hashedbsn)
        }

        query   = text(f"select id from patient where hashedbsn = :hbsn;")
        result  = conn.execute(query, keypairDict)

        for row in result:
            respond1 = row.id

        keypairDict = {
            "respond1": text(str(respond1))
        }

        query   = text("select address.id, address.province, address.city, address.country, address.postcode, address.housenumber, address.streetname from address inner join patient on address.id = patient.id where patient.id = :respond1;")
        result  = conn.execute(query, keypairDict)

        for row in result:
            respond2 = jsonify({'id': row.id, 'province': row.province, 'city': row.city, 'country': row.country, 'postcode': row.postcode, 'housenumber': row.housenumber, 'streetname': row.streetname})
        
        conn.close()
        return respond2
    except:
        respond = jsonify({'message': 'patient not found'}), 404
        conn.close()
        return respond


# Geef patient policy op basis van HashedBSN
@app.route("/mixitpatient/policy/<hashedbsn>")
def policy(hashedbsn):
    try:
        creds   = get_creds("cred.json")
        dbContext    = connection(creds['mixit-patient']['username'], creds['mixit-patient']['password'], creds['mixit-patient']['database_name'])

        query = text("select id from patient where hashedbsn = :hbsn")
    
        keypairDict = {
            "hbsn": text(hashedbsn)
        }
        
        queryResult = dbContext.execute(query, keypairDict)
        for row in queryResult:
            queryResultId = row.id
            
        query = text("SELECT policy.id AS policyid, policy_has_policy_option.policy_id, policy_has_policy_option.policy_option_id, policy_option.name, policy.patient_id AS patient_id from policy INNER JOIN policy_has_policy_option ON policy.id = policy_has_policy_option.policy_id INNER JOIN policy_option ON policy_option.id = policy_has_policy_option.policy_option_id INNER JOIN patient ON policy.patient_id = patient.id WHERE patient.id = :patientId")
        
        keypairDict = {
            "patientId": queryResultId
        }
        
        queryResult = dbContext.execute(query, keypairDict)
        
        toReturn = [{'patient_id':row.patient_id,'policy.id':row.policyid,'policy_has_policy_option.policy_option_id':row.policy_option_id,'policyname':row.name} for row in queryResult]
        
        if (toReturn.__len__() == 0) :
            return jsonify({'message': 'No policies found for patient'}), 404
        
        dbContext.close()    
        return jsonify(toReturn)
    except:
        dbContext.close()
        return jsonify({'message': 'Error getting the policies'}), 500


if __name__ == "__main__":
    app.run(debug=True)