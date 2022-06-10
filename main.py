from flask import Flask, Response, json, request
from db import DB

app = Flask(__name__)
db = DB()


def response(status, body):
    return Response(response=json.dumps(body),
                    status=status,
                    mimetype='application/json')


@app.route('/')
def home():
    return response(200, {"status": "ok"})


# returns a paginated list of vendors
@app.route('/vendors', methods=["GET"])
def get_vendors():
    return db.get_all()


@app.route('/vendor/<vendor_id>', methods=["GET"])
def get_vendor(vendor_id):
    return db.get(vendor_id)


@app.route('/vendor', methods=["POST"])
def create_vendor():
    vendor = request.json
    return db.create(vendor)


@app.route('/vendor/<vendor_id>', methods=["PUT"])
def update_vendor(vendor_id):
    vendor = request.json
    return db.update(vendor_id, vendor)


@app.route('/vendor/<vendor_id>', methods=["DELETE"])
def delete_vendor(vendor_id):
    return db.delete(vendor_id)


if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')
