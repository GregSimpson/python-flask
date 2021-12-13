from flask import Flask, jsonify, request

from cashman.model.expense import Expense, ExpenseSchema
from cashman.model.income import Income, IncomeSchema
from cashman.model.transaction_type import TransactionType

app = Flask(__name__)


transactions = [
  Income('Salary', 5000),
  Income('Dividends', 200),
  Expense('pizza', 50),
  Expense('GJS Rock Concert', 100)
]



# earlier example

incomes = [
  { 'description': 'salary', 'amount': 5000 }
]


# curl http://localhost:5000/incomes | jq '.'
## curl http://localhost:5000/incomes | json_pp -json_opt pretty,canonical
@app.route('/incomes')
def get_incomes():
  schema = IncomeSchema(many=True)
  incomes = schema.dump(
    filter(lambda t: t.type == TransactionType.INCOME, transactions)
  )
  return jsonify(incomes.data)


#   newer example
@app.route('/incomes', methods=['POST'])
def add_income():
  income = IncomeSchema().load(request.get_json())
  transactions.append(income.data)
  return "", 204


@app.route('/expenses')
def get_expenses():
  schema = ExpenseSchema(many=True)
  expenses = schema.dump(
      filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
  )
  return jsonify(expenses.data)


@app.route('/expenses', methods=['POST'])
def add_expense():
  expense = ExpenseSchema().load(request.get_json())
  transactions.append(expense.data)
  return "", 204



#  run this with:
# # start the application
# ./bootstrap.sh &
#
# # get expenses
# curl http://localhost:5000/expenses | jp '.'
#
# # add a new expense
# curl -X POST -H "Content-Type: application/json" -d '{
#     "amount": 20,
#     "description": "lottery ticket"
# }' http://localhost:5000/expenses
#
# # get incomes
# curl http://localhost:5000/incomes  | jp '.'
#
# # add a new income
# curl -X POST -H "Content-Type: application/json" -d '{
#     "amount": 300.0,
#     "description": "loan payment"
# }' http://localhost:5000/incomes

if __name__ == "__main__":
    app.run()
