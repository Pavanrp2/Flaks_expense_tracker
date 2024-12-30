from flask import Flask, Blueprint, request, jsonify
from application.models.database import Expenses
from application import db
from datetime import datetime

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')
#  Adding Expenses
@expenses_bp.route('/add', methods=['POST'])
def addExpenses():
    try:
        data = request.get_json()
        if not data or not data.get('name') or not data.get('amount') or not data.get('category') or not data.get('date'):
            return jsonify({"message" : "Misssing required fields"}), 404
        
        existing = Expenses.query.filter_by(name = data['name']).first()
        if existing:
            return jsonify({"error": f"This {data['name']} Named Expense is Already Exist"})
        
        try:
            expenses_date = datetime.strptime(data['date'], '%d-%m-%Y').date()
        except Exception as e:
            return jsonify({"error":"Invalid date Format. Use DD-MM-YYYY"}), 400
        
        new_expeanses = Expenses(
            name = data['name'],
            amount = float(data['amount']),
            category = data['category'],
            date = expenses_date
        )
        db.session.add(new_expeanses)
        db.session.commit()
        return jsonify({"message":"New Expense added Successfully"}), 200
    except Exception as e:
        return jsonify ({"error": f"An unexpected error occurred: {str(e)}"}), 500
    

# Get all expenses
@expenses_bp.route('/get', methods=['GET'])
def getAllExpenses():
    try:
        data  = Expenses.query.all()
        if not data:
            return jsonify({"message":"Expenses are Empty"}), 404
        expenses_list = []
        for allExpense in data:
            expenses_list.append(allExpense.details())
        return jsonify(expenses_list), 200
    
    except Exception as e:
        return jsonify({"error": f"An Unexpected error occured: {str(e)}"}), 500
    

#  get expense by name    
@expenses_bp.route('/get/<string:expense_name>', methods = ['GET'])
def getExpenses(expense_name):
    try:
        print(expense_name)
        data = Expenses.query.filter_by(name=expense_name).first()
        if not data:
            return jsonify({"message" : "Expense Not Found"}), 404
        return jsonify(data.details()), 200
    
    except Exception as e:
        return jsonify({"error": f"An Unexpected error occured: {str(e)}"})
    
# upadte expenses
@expenses_bp.route('/<string:expense_name>', methods = ['PUT'])
def update(expense_name):
    try:
        expenses = Expenses.query.filter(Expenses.name==expense_name).first()
        if not expenses:
            return jsonify({"message":"Expense Not Found"}), 404
        
        data = request.get_json()
        if 'name' in data:
            expenses.name = data['name']
        if 'amount' in data:
            expenses.ampunt = float(data['amount'])
        if 'category' in data:
            expenses.category = data['category']
        if 'date' in data:
            try:
                expense_time = datetime.strptime(data['date'], '%d-%m-%Y').date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        db.session.commit()
        return jsonify({"message":"Expense updated successfully", "expenses": expenses.details()}), 200
    
    except Exception as e:
        return jsonify({"error":f"{str(e)}"})
    
    # delete expenses
    
@expenses_bp.route('/<string:expense_name>', methods = ['DELETE'])
def delete(expense_name):
    data = Expenses.query.filter(Expenses.name == expense_name).first()
    if not data:
        return jsonify({"message":"Expense Not Found"}), 404
    db.session.delete(data)
    db.session.commit()
    return jsonify({"message":"Expense updated successfully"}), 200
    
    