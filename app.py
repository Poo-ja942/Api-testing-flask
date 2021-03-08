from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# __init__ app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# __init__ db
db = SQLAlchemy(app)

# __init__ ma
ma = Marshmallow(app)

# details class/model
class details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    bankname = db.Column(db.String(250))
    totalamount = db.Column(db.Float)
    deposit = db.Column(db.Integer)
    withdraw = db.Column(db.Integer)
    address = db.Column(db.String(300))

    def __init__(self, name, bankname, totalamount,deposit,withdraw, address):
        self.name = name
        self.bankname = bankname
        self.totalamount = totalamount
        self.deposit = deposit
        self.withdraw = withdraw
        self.address = address

# product schema
class detailsSchema(ma.Schema):
    class Meta():
        fields=('id', 'name', 'bankname', 'totalamount','deposit', 'withdraw', 'address')

# __init__ schema
detail_schema = detailsSchema()
details_schema = detailsSchema(many=True)

# create product
@app.route('/detail', methods=['POST'])
def add_details():
    name = request.json['name']
    bankname = request.json['bankname']
    totalamount = request.json['totalamount']
    deposit = request.json['deposit']
    withdraw = request.json['withdraw']
    address = request.json['address']

    result = details(name, bankname, totalamount, deposit, withdraw, address  )

    db.session.add(result)
    db.session.commit()

    return detail_schema.jsonify(result)


# all details of customers
@app.route('/detail', methods=['GET'])
def get_details():
  all_details = details.query.all()
  result = details_schema.dump(all_details)
  return jsonify(result)

@app.route('/detail/<id>', methods=['GET'])
def single_detail(id):
    Detail = details.query.get(id)
    return detail_schema.jsonify(Detail)

@app.route('/detail/<id>', methods=['PUT'])
def update_details(id):
    data = details.query.get(id)

    name = request.json['name']
    bankname = request.json['bankname']
    totalamount = request.json['totalamount']
    deposit = request.json['deposit']
    withdraw = request.json['withdraw']
    address = request.json['address']

    data.name = name
    data.bankname = bankname
    data.totalamount = totalamount
    data.deposit = deposit
    data.withdraw = withdraw
    data.address = address

    db.session.commit()
    return detail_schema.jsonify(data)

@app.route('/detail/<id>', methods=['DELETE'])
def delete_details(id):
    delete_details = details.query.get(id)
    db.session.delete(delete_details)
    db.session.commit()
    return detail_schema.jsonify(delete_details)






if __name__ == '__main__':
    app.run(debug=True)



