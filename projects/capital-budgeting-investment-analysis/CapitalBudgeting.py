# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 12:12:04 2019

Author: Andrew Jaroncyk
Title: Capital Budgeting with Python
Purpose: Evaluates capital budgeting projects by calculating Net Present Value 
(NPV), Internal	Rate of	Return (IRR), and Return on	Investment (ROI) using user-
defined functions. The program initiates by asking the user to select and input
appropriate project parameters:
    
1.	Required Rate of Return
2.	Lifetime of	project (years)
3.	Initial	investment
4.	Annual cash	inflow assumed to be constant each year 
5.	Annul cash outflow	associated with	the	project (functions	default to 0)

Once the parameters	are entered, the user is presented a menu, where an option 
must be selected:

 D - Input Data
 N - Net Present Value Calculation
 I - Internal Rate of Return
 R – Return on Investment
 T – Project Report
 Q - Quit
 
The option that is selected is presented with the appropriate result. Once 
completed, the program automatically reloads the Main Menu after each selection.

The program	continues until the user selects "Quit" (Q).
"""

def get_data():
    """Collects project values"""
    cashflow = []
    initial_investment = float(input("Enter initial investment: ")) * -1
    cashflow.append(initial_investment)
    annual_cash_inflow = float(input("Enter the cashflow per year: "))
    annual_cash_outflow = float(input("Enter projected continuing outflow: "))
    if annual_cash_outflow == "":
        annual_cash_outflow = 0
    total_cash_flow = annual_cash_inflow - annual_cash_outflow
    cashflow.append(total_cash_flow)
    project_lifetime = int(input("Enter the term (in years): "))
    for i in range(project_lifetime - 1):
        cashflow.append(total_cash_flow)  
    required_rate_of_return = float(input("Enter the required rate of return: "))
    irr_rate = required_rate_of_return
    data_dictionary = {"Initial Investment": initial_investment, "Annual Cash Inflow": annual_cash_inflow, "Annual Cash Outflow": annual_cash_outflow, "Project Lifetime": project_lifetime, "Required Rate of Return": required_rate_of_return, "Total Cashflow": cashflow, "IRR Rate": irr_rate}
    return data_dictionary


def NPV(data_dictionary):
    """Sum of the present value of projected net cash flows minus the initial investment"""
    npv = 0
    discount_rate = 1 + data_dictionary["Required Rate of Return"] 
    for i in range(data_dictionary["Project Lifetime"] + 1):
        npv += data_dictionary["Total Cashflow"][i] / ((discount_rate) ** i)
        npv = round(npv)
    return npv
    

def IRR(data_dictionary):
    """Required Rate of Return that has NPV = 0"""
    irr = data_dictionary["Required Rate of Return"]
    PV = 1
    while PV > 0: 
        PV = NPV(data_dictionary)
        data_dictionary["Required Rate of Return"] += 0.001
    var = data_dictionary["Required Rate of Return"]
    var = round(var * 100, 2)
    data_dictionary["Required Rate of Return"] = irr
    return var
        


def ROI(data_dictionary):
    """NPV/sum of Present Value of all cash outflows"""
    discounted_cash_outflows = (data_dictionary["Annual Cash Outflow"]) * ((1-(1+data_dictionary["Required Rate of Return"])**(-data_dictionary["Project Lifetime"]))/(data_dictionary["Required Rate of Return"]))
    roi = (NPV(data_dictionary)/(discounted_cash_outflows - data_dictionary["Initial Investment"]))
    roi = round(roi * 100,2)
    return roi

def proj_report(data_dictionary):
    """Prints Investment Analysis of project given parameters inputted by user"""
    print("Investment Analysis")
    print("-" * 50)
    n = data_dictionary["Project Lifetime"]
    Years = ["Year: "]
    for i in range(n + 1):
        Years.append(str(i))
    for i in range(len(Years)):
        print("{:20s}".format(Years[i]), end = " ")
    print("\n")

    cf = data_dictionary["Total Cashflow"]  
    CF = ["Net Cashflow: "]
    for i in range(len(cf)):
        CF.append(str("${:,.2f}".format(cf[i])))
    for i in range(len(CF)):
        print("{:19s}".format(CF[i]), end = " ")
    print("\n")
    print("IRR: {:.2f}%".format(IRR(data_dictionary)))
    print("ROI: {:.2f}%".format(ROI(data_dictionary)))
    print("NPV: ${:,.2f}".format(NPV(data_dictionary)))
    print("\n")
    if NPV(data_dictionary) > 0:
        print("Project is worth consideration")
    else:
        print("Project is not worth consideration")
    

def main():
    run_program = True
    counter = 0
    while run_program:
        if counter == 0:
            data_dictionary = get_data()
            print("Investment Calculator")
            print("Pick a Menu Option to Choose: ")
            print("-" * 30)
            
            options = "Input Data, Net Present Value Calculation, Internal Rate of Return, Return on Investment, Project Report, Quit".split(", ")
            options_letters = "D, N, I, R, T, Q".split(", ")
            for item in range(0, len(options)):
                print("{} - {}".format(options_letters[item], options[item]))
                    
            choice = input("Selection: ").upper()
                
            if choice == "D":
                get_data()
                print("\n")
            elif choice == "N":
                print(NPV(data_dictionary))
                print("\n")
            elif choice == "I":
                print(IRR(data_dictionary))
                print("\n")
            elif choice == "R":
                print(ROI(data_dictionary))
                print("\n")
            elif choice == "T":
                proj_report(data_dictionary)
                print("\n")
            elif choice == "Q":
                run_program = False 
            counter += 1
            
        else:
            options = "Input Data, Net Present Value Calculation, Internal Rate of Return, Return on Investment, Project Report, Quit".split(", ")
            options_letters = "D, N, I, R, T, Q".split(", ")
            for item in range(0, len(options)):
                print("{} - {}".format(options_letters[item], options[item]))
                    
            choice = input("Selection: ").upper()
                
            if choice == "D":
                get_data()
                print("\n")
            elif choice == "N":
                print(NPV(data_dictionary))
                print("\n")
            elif choice == "I":
                print(IRR(data_dictionary))
                print("\n")
            elif choice == "R":
                print(ROI(data_dictionary))
                print("\n")
            elif choice == "T":
                proj_report(data_dictionary)
                print("\n")
            elif choice == "Q":
                run_program = False 
    
if __name__ == "__main__":
    main()
