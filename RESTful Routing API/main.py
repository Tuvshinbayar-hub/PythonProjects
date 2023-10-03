from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

API_KEY = 'isSecretKey'


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")
    

# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    all_cafes = Cafe.query.all()
    random_cafe = random.choice(all_cafes)
    print(type(random_cafe))

    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    all_cafes = Cafe.query.all()
    cafes = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafes)


@app.route("/search")
def search():
    location = request.args.get('loc')
    if location is None:
        return 'Sorry None'

    try:
        found_cafes = db.session.execute(db.select(Cafe).where(Cafe.location == location)).scalars().all()
        cafes = [cafe.to_dict() for cafe in found_cafes]
        return jsonify(cafes)
    except Exception as e:
        print(e)
        error = {
            'error': {
                'Not Found': 'Sorry, We do not have a cafe at that location'
            }
        }
        return error


# HTTP POST - Create Record
@app.route("/add", methods=['POST'])
def add_new_cafe():
    api_key = request.args.get('api_key')

    if api_key != API_KEY:
        return jsonify({
            'error': 'please provide valid api_key'
        })

    try:
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=True if request.form.get("sockets").lower() == 'true' else False,
            has_toilet=True if request.form.get("toilet").lower() == 'true' else False,
            has_wifi=True if request.form.get("wifi").lower() == 'true' else False,
            can_take_calls=True if request.form.get("calls").lower() == 'true' else False,
            seats=request.form.get("seats"),
            coffee_price=f'£{request.form.get("coffee_price")}',
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify({
            'success': 'Successfully added the new cafe.'
        })
    except Exception as e:
        print(e)
        return jsonify({
            'failed': 'Sorry failed'
        })


# HTTP PUT/PATCH - Update Record
@app.route('/update-price/<cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    found_cafe = db.get_or_404(Cafe, cafe_id)
    found_cafe.coffee_price = f"£{request.args.get('new_price')}"
    print(found_cafe.coffee_price)
    db.session.commit()

    if found_cafe:
        return f'Succeeded updating coffee price to {found_cafe.coffee_price} of cafe with {cafe_id} id'
    else:
        return 'Failed'


# HTTP DELETE - Delete Record
@app.route('/report-closed/<cafe_id>', methods=['DELETE'])
def report_closed(cafe_id):
    api_key = request.args.get('api_key')

    if api_key != API_KEY:
        return jsonify({
            'error': 'Sorry, that is not allowed. Make sure you have the correct api_key',
        })

    try:
        cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        db.session.delete(cafe)
        db.session.commit()
        return jsonify({
            'success': f'deleted a cafe with {cafe_id} id from the database'
        })
    except Exception as e:
        print(e)
        return jsonify({
            'error': f'Sorry, a cafe with {cafe_id} is not found in our database'
        })

    # Booleans are always true when False is given as parameter
# Finish writing the documentation using POSTMAN


if __name__ == '__main__':
    app.run(debug=True)
