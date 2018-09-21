from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col
import os
import yaml

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

def read_yaml_config(yaml_file):
    with open(yaml_file,'r') as f:
        config = yaml.safe_load(f)
        return config

try: 
    db_profile = read_yaml_config('.config.yaml')
    db_profile = db_profile['local_db']
except IOError:
    print('No db_profile found')

db_url = (db_profile['protocol'] + "://" + 
          db_profile['username'] + ":" + 
          db_profile['password'] + "@" +
          db_profile['host'] + ":" +
          str(db_profile['port']) + "/" +
          db_profile['db_name'])
app.config['SQLALCHEMY_DATABASE_URI'] = db_url 
db = SQLAlchemy(app)
db.init_app(app)

class results_table(Table):
    saon = Col('saon')
    paon = Col('paon')
    street = Col('street')
    postcode = Col('postcode')
    transfer_date = Col('transfer_date')
    price = Col('price')

def prices_query(postcode='W5 3HR'):
    query_string = """
    WITH cte AS (SELECT saon,paon,max(transfer_date) AS max_transfer_date 
    FROM land_registry_price_paid_uk 
    WHERE postcode = '%s' 
    GROUP by paon,saon) 
    SELECT DISTINCT a.saon,a.paon,a.street,a.postcode,a.transfer_date,a.price 
    FROM land_registry_price_paid_uk a 
    RIGHT OUTER JOIN cte ON cte.paon=a.paon AND cte.max_transfer_date = a.transfer_date 
    WHERE postcode = '%s' ORDER BY paon,saon;""" % (postcode, postcode)
    res = db.session.execute(query_string)
    db.session.commit()
    db.session.close()
    return res

# endpoint to show all houses
@app.route("/", methods = ['GET', 'POST'])
def get_postcode():

    if request.method == 'POST':
        postcode = request.form['postcode']
        res = prices_query(postcode=postcode)
        return render_template("prices.html", table=results_table(items=res), postcode= postcode)

    res = prices_query()
    return render_template("prices.html", table=results_table(items=res), postcode=str('W5 3HR'))

if __name__ == '__main__':
    app.run(debug=True)

