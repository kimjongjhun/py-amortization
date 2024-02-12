import inquirer
from datetime import date
from dateutil.relativedelta import relativedelta

def main():
  loan_amount = get_loan_amount()
  interest_rate = get_interest_rate()
  term_length = get_term_length()
  term_period = get_term_period()
  monthly_payment = calculate_monthly_payment(loan_amount, term_length, term_period, interest_rate)
  payment_schedule = calculate_loan_payments(loan_amount, interest_rate, monthly_payment)
  additional_principal_schedule = calculate_additional_principle()

def get_loan_amount():
  while True:
    try:
      loan_amount = float(input("What's the loan amount? "))
    except Exception:
      print("That is not a number")
    else:
      return loan_amount
    
def get_interest_rate():
    while True:
      try:
        interest_rate = float(input("What's the interest rate? "))
      except Exception:
        print("That is not a number")
      else:
        return interest_rate

def get_term_length():
  while True:
    try:
      term_length = int(input("What's the term length? "))
    except Exception:
      print("That is not a number")
    else:
      return term_length

def get_term_period():
  questions = [
    inquirer.List('period',
      message="What is the term period?",
      choices=['Months', 'Years'],
    ),
  ]
  
  return inquirer.prompt(questions)['period']

def calculate_monthly_payment(loan_amount=0, term_length=0, term_period='Months', interest_rate=0):
  adjusted_term_length = term_length if term_period == 'Months' else term_length*12
  interest = (interest_rate/100)/12

  numerator = (interest*(((1+interest)**adjusted_term_length)))
  denominator = (((1+interest)**adjusted_term_length)-1)

  return loan_amount*(numerator/denominator)

def calculate_loan_payments(loan_amount=0, interest_rate=0, monthly_payment=0):
  payments = []
  ending_balance = loan_amount
  interest = (interest_rate/100)/12
  payment_date = date.today()

  while ending_balance > 0:
    interest_payment = ending_balance * interest
    principal_payment = monthly_payment - interest_payment
    ending_balance = ending_balance - principal_payment
    payment_date = payment_date + relativedelta(months=1)

    payments.append(
      {'date': payment_date.strftime("%m/%d/%Y"), 'principal_payment': principal_payment, 'interest_payment': interest_payment, 'ending_balance': ending_balance}
    )

  return payments

def calculate_additional_principle():
    while True:
      try:
        additional_principle_amount = float(input("Would you like to make an additional payment towards the principle? "))
      except Exception:
        print("That is not a number")
      else:
        return additional_principle_amount


if __name__ == "__main__":
  main()

# Total Payment = Loan Amount×[(i×((1+i)^n))/(((1+i)^n)−1)​]

# where: 
# i=Monthly interest payment
# n=Number of payments​