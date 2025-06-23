from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country = request.form['country']
        city = request.form['city']
        days = int(request.form['days'])
        
        trip_result = trips.insert_one({'country': country, 'city': city, 'days': days})
        trip_id = str(trip_result.inserted_id)

        plan_docs = [
            {'trip_id': trip_id, 'day': day, 'attractions': []}
            for day in range(1, days + 1)
        ]
        plans.insert_many(plan_docs)
        return redirect(url_for('index'))
    all_trips = trips.find()
    return render_template('index.html', trips=all_trips)

@app.post("/trip/<id>/delete/")
def delete(id):
    trips.delete_one({"_id": ObjectId(id)})
    plans.delete_many({"trip_id": id})
    return redirect(url_for('index'))

@app.route("/trip/<id>")
def trip_planner(id):
    trip = trips.find_one({"_id": ObjectId(id)})
    plans_for_trip = list(plans.find({"trip_id": id}))
    return render_template('trip_planner.html', trip=trip, plans=plans_for_trip)

@app.route("/trip/<trip_id>/plan/<plan_id>", methods=['GET', 'POST'])
def add_attractions(trip_id, plan_id):
    if request.method == 'POST':
        attraction = request.form['attraction']
        plan = plans.find_one({'_id': ObjectId(plan_id)})
        if plan and plan.get('trip_id') == trip_id:
            plans.update_one(
                {'_id': ObjectId(plan_id)},
                {'$push': {'attractions': attraction}}
            )
        return redirect(url_for('add_attractions', trip_id=trip_id, plan_id=plan_id))
    trip = trips.find_one({'_id': ObjectId(trip_id)})
    plan = plans.find_one({'_id': ObjectId(plan_id)})
    return render_template('add_attractions.html', trip_id=trip_id, plan_id=plan_id, plan=plan, trip=trip)

@app.route("/trip/<trip_id>/plan/<plan_id>/edit/<int:attr_index>", methods=['POST'])
def edit_attraction(trip_id, plan_id, attr_index):
    new_attraction = request.form['new_attraction']
    plan = plans.find_one({'_id': ObjectId(plan_id)})
    if plan and plan.get('trip_id') == trip_id:
        attractions = plan.get('attractions', [])
        if 0 <= attr_index < len(attractions):
            attractions[attr_index] = new_attraction
            plans.update_one(
                {'_id': ObjectId(plan_id)},
                {'$set': {'attractions': attractions}}
            )
    return redirect(url_for('add_attractions', trip_id=trip_id, plan_id=plan_id))

@app.route("/trip/<trip_id>/plan/<plan_id>/delete/<int:attr_index>", methods=['POST'])
def delete_attraction(trip_id, plan_id, attr_index):
    plan = plans.find_one({'_id': ObjectId(plan_id)})
    if plan and plan.get('trip_id') == trip_id:
        attractions = plan.get('attractions', [])
        if 0 <= attr_index < len(attractions):
            attractions.pop(attr_index)
            plans.update_one(
                {'_id': ObjectId(plan_id)},
                {'$set': {'attractions': attractions}}
            )
    return redirect(url_for('add_attractions', trip_id=trip_id, plan_id=plan_id))

db = client.trip_planner
trips = db.trips
plans = db.plans

if __name__ == "__main__":
    app.run(debug=True)