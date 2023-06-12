from flask import Flask, request, jsonify, render_template
from pony.orm import Database, Required, PrimaryKey, db_session, select
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

db = Database()
db.bind(provider='sqlite', filename='employee_database.sqlite', create_db=True)


class Employee(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    surname = Required(str)
    age = Required(int)
    email = Required(str)
    position = Required(str)
    paycheck = Required(float)


db.generate_mapping(create_tables=True)

@app.route('/employee', methods=['POST'])
@db_session
def add_employee():
    data = request.get_json()
    employee = Employee(
        name=data['name'],
        surname=data['surname'],
        age=data['age'],
        email=data['email'],
        position=data['position'],
        paycheck=data['paycheck']
    )
    return jsonify(employee.to_dict())


@app.route('/employee/<int:emp_id>', methods=['GET'])
@db_session
def get_employee(emp_id):
    employee = Employee.get(id=emp_id)
    if employee is None:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify(employee.to_dict())


@app.route('/employee/<int:emp_id>', methods=['PUT'])
@db_session
def update_employee(emp_id):
    data = request.get_json()
    employee = Employee.get(id=emp_id)
    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    employee.name = data.get('name', employee.name)
    employee.surname = data.get('surname', employee.surname)
    employee.age = data.get('age', employee.age)
    employee.email = data.get('email', employee.email)
    employee.position = data.get('position', employee.position)
    employee.paycheck = data.get('paycheck', employee.paycheck)

    return jsonify(employee.to_dict())


@app.route('/employee/<int:emp_id>', methods=['DELETE'])
@db_session
def delete_employee(emp_id):
    employee = Employee.get(id=emp_id)
    if employee is None:
        return jsonify({"error": "Employee not found"}), 404
    employee.delete()
    return jsonify({"success": f"Employee {emp_id} deleted"})


@app.route('/employees', methods=['GET'])
@db_session
def get_all_employees():
    position = request.args.get('position')
    paycheck = request.args.get('paycheck')
    
    query = select(e for e in Employee)
    
    if position:
        query = query.where(lambda e: e.position == position)
    
    if paycheck:
        try:
            paycheck = float(paycheck)
            query = query.where(lambda e: e.paycheck == paycheck)
        except ValueError:
            return jsonify({"error": "Invalid paycheck value"}), 400

    employees = query[:]
    
    return jsonify([e.to_dict() for e in employees])

@app.route('/paychecks', methods=['GET'])
@db_session
def get_all_paychecks():
    paychecks = select(e.paycheck for e in Employee).distinct()[:]
    return jsonify(list(paychecks))

@app.route('/positions', methods=['GET'])
@db_session
def get_all_positions():
    positions = select(e.position for e in Employee).distinct()[:]
    return jsonify(list(positions))



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 , debug=True)
