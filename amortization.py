import inquirer
from datetime import date
from dateutil.relativedelta import relativedelta

def main():
  loanAmount = get_loan_amount()
  interestRate = get_interest_rate()
  termLength = get_term_length()
  termPeriod = get_term_period()
  monthlyPayment = calculate_monthly_payment(loanAmount, termLength, termPeriod, interestRate)
  paymentSchedule = calculate_loan_payments(loanAmount, interestRate, monthlyPayment)

  print(f"loan amount is: ${loanAmount:,.2f} with an interest rate of {interestRate}% for {termLength} {termPeriod}")

  for payment in paymentSchedule:
      print(f"{payment['date']}, {payment['principalPayment']:,.2f}, {payment['interestPayment']:,.2f}, {payment['endingBalance']:,.2f}")

def get_loan_amount():
  while True:
    try:
      loanAmount = float(input("What's the loan amount? "))
    except Exception:
      print("That is not a number")
    else:
      return loanAmount
    
def get_interest_rate():
    while True:
      try:
        interestRate = float(input("What's the interest rate? "))
      except Exception:
        print("That is not a number")
      else:
        return interestRate

def get_term_length():
  while True:
    try:
      termLength = int(input("What's the term length? "))
    except Exception:
      print("That is not a number")
    else:
      return termLength

def get_term_period():
  questions = [
    inquirer.List('period',
      message="What is the term period?",
      choices=['Months', 'Years'],
    ),
  ]
  
  return inquirer.prompt(questions)['period']

def calculate_monthly_payment(loanAmount=0, termLength=0, termPeriod='Months', interestRate=0):
  adjustedTermLength = termLength if termPeriod == 'Months' else termLength*12
  interest = (interestRate/100)/12

  numerator = (interest*(((1+interest)**adjustedTermLength)))
  denominator = (((1+interest)**adjustedTermLength)-1)

  return loanAmount*(numerator/denominator)

def calculate_loan_payments(loanAmount=0, interestRate=0, monthlyPayment=0):
  payments = []
  endingBalance = loanAmount
  interest = (interestRate/100)/12
  paymentDate = date.today()

  while endingBalance > 0:
    interestPayment = endingBalance * interest
    principalPayment = monthlyPayment - interestPayment
    endingBalance = endingBalance - principalPayment
    paymentDate = paymentDate + relativedelta(months=1)

    payments.append(
      {'date': paymentDate.strftime("%m/%d/%Y"), 'principalPayment': principalPayment, 'interestPayment': interestPayment, 'endingBalance': endingBalance}
    )

  return payments

if __name__ == "__main__":
  main()

# Total Payment = Loan Amount×[(i×((1+i)^n))/(((1+i)^n)−1)​]

# where: 
# i=Monthly interest payment
# n=Number of payments​