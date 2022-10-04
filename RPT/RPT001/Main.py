from encodings import utf_8
import matplotlib.pyplot as plt
import numpy as np
import Employee as emp

menu_options = {
    1: 'Load data from file',
    2: 'Add new employee',
    3: 'Display list of employee',
    4: 'Show employee details',
    5: 'Update employee information',
    6: 'Delete employee',
    7: 'Increase salary of employee',
    8: 'Decrease salary of employee',
    9: 'Show total employee a month',
    10: 'Show total salary a month',
    11: 'Show average of salary a month',
    12: 'Show average of age',
    13: 'Show maximum age',
    14: 'Sort list of employee according to salary by ascending',
    15: 'Draw salary according to age',
    16: 'Draw average of salary chart by age group',
    17: 'Draw percentage of salary by age group',
    18: 'Draw percentage of total employee by age group',
    19: 'Store data to file',
    'Others': 'Exit program'
}


def print_menu():
    print("\n")
    for index, value in menu_options.items():
        print(f"{index}: {value}")


employees = []
filePath = "RPT001/In_Employee_DB.db"

while (True):
    print_menu()
    userChoice = ''
    try:
        userChoice = int(input('INPUT CHOOSE: '))
    except:
        print('Invalid input, try again!')
        continue

    # Option 1
    if userChoice == 1:
        readStream = open(filePath, mode='r', encoding='utf-8')
        for line in readStream:
            employee = line.strip('\n').split(',')
            code = employee[0]
            name = employee[1]
            age = int(employee[2])
            salary = float(employee[3])
            employees.append(emp.Employee(code, name, age, salary))
        readStream.close()

    # Option 2
    elif userChoice == 2:
        code = input("Input code: ")
        name = input("Input name: ")
        age = int(input("Input age: "))
        salary = float(input("Input salary: "))
        employees.append(emp.Employee(code, name, age, salary))

    # Option 3
    elif userChoice == 3:
        for employee in employees:
            employee.display()

    # Option 4
    elif userChoice == 4:
        code = input("Input code: ")
        for employee in employees:
            if (code == employee.code):
                employee.display()
                break
        else:
            print("Nothing Here!")

    # Option 5:
    elif userChoice == 5:
        code = input("Input code: ")
        for employee in employees:
            if (code == employee.code):
                employee.name = input("Input name: ")
                employee.age = int(input("Input age: "))
                employee.salary = float(input("Input salary: "))
                break
        else:
            print("Nothing Here!")

    # Option 6:
    elif userChoice == 6:
        code = input("Input code: ")
        for employee in employees:
            if (code == employee.code):
                employees.remove(employee)
                break
        else:
            print("Nothing Here!")

    # Option 7:
    elif userChoice == 7:
        code = input("Input code: ")
        for employee in employees:
            if (code == employee.code):
                amount = float(input("Input amount: "))
                employee.salary = employee.increaseSalary(amount)
                break
        else:
            print("Nothing Here!")

    # Option 8:
    elif userChoice == 8:
        code = input("Input code: ")
        for employee in employees:
            if (code == employee.code):
                amount = float(input("Input amount: "))
                employee.salary = employee.decreaseSalary(amount)
                break
        else:
            print("Nothing Here!")

    # Option 9:
    elif userChoice == 9:
        employeeNumber = len(employees)
        print(f"Number of employee: {employeeNumber}")

    # Option 10:
    elif userChoice == 10:
        totalSalary = 0.0
        for employee in employees:
            totalSalary += employee.salary
        print(f'Total salary: {totalSalary}')

    # Option 11:
    elif userChoice == 11:
        employeeNumber = len(employees)
        totalSalary = 0.0
        for employee in employees:
            totalSalary += employee.salary
        avgSalary = round(totalSalary / employeeNumber, 2)
        print(f'AVG salary: {avgSalary}')

    # Option 12:
    elif userChoice == 12:
        employeeNumber = len(employees)
        totalAge = 0
        for employee in employees:
            totalAge += employee.age
        avgAge = round(totalAge / employeeNumber, 2)
        print(f'AVG Age: {avgAge}')

    # Option 13:
    elif userChoice == 13:
        maxAge = 0
        for employee in employees:
            if employee.age > maxAge:
                maxAge = employee.age
        print(f"Max age: {maxAge}")

        for employee in employees:
            if employee.age == maxAge:
                employee.display()

    # Option 14:
    elif userChoice == 14:
        employees.sort(key=(lambda emp: emp.age))

    # Option 15:
    elif userChoice == 15:
        ages = []
        salaries = []
        for employee in employees:
            ages.append(employee.age)
            salaries.append(employee.salary)

        plt.title("Age and salary chart")
        plt.xlabel("Age")
        plt.ylabel("Salary")
        plt.plot(ages, salaries, "go")
        plt.show()

    # Option 16:
    elif userChoice == 16:
        salariesLessThan35 = []
        salariesLessThan50 = []
        salariesMoreThan50 = []

        for employee in employees:
            if (employee.age < 35):
                salariesLessThan35.append(employee.salary)
            elif (employee.age < 50):
                salariesLessThan50.append(employee.salary)
            else:
                salariesMoreThan50.append(employee.salary)

        avgSalariesLessThan35 = np.average(salariesLessThan35)
        avgSalariesLessThan50 = np.average(salariesLessThan50)
        avgSalariesMoreThan50 = np.average(salariesMoreThan50)
        avgSalariesSalaryTitle = np.array(
            ["Less Than 35", "35 to 50", "More Than 50"])
        avgSalary = np.array(
            [avgSalariesLessThan35, avgSalariesLessThan50, avgSalariesMoreThan50])
        plt.title("AVG Salary group by age")
        plt.xlabel("Age")
        plt.ylabel("AVG Salary")
        plt.bar(avgSalariesSalaryTitle, avgSalary)
        plt.show()

    # Option 17:
    elif userChoice == 17:
        totalSalariesLessThan35 = 0
        totalSalariesLessThan50 = 0
        totalSalariesMoreThan50 = 0

        for employee in employees:
            if (employee.age < 35):
                totalSalariesLessThan35 += employee.salary
            elif (employee.age < 50):
                totalSalariesLessThan50 += employee.salary
            else:
                totalSalariesMoreThan50 += employee.salary

        totalSalaries = totalSalariesLessThan35 + \
            totalSalariesLessThan50 + totalSalariesMoreThan50
        salariesLessThan35Per = round(
            totalSalariesLessThan35 / totalSalaries, 2) * 100
        salariesLessThan50Per = round(
            totalSalariesLessThan50 / totalSalaries, 2) * 100
        salariesMoreThan50Per = 100 - salariesLessThan35Per - salariesLessThan50Per

        perSalaryTitle = np.array(["Less Than 35", "35 to 50", "More Than 50"])
        perSalary = np.array(
            [salariesLessThan35Per, salariesLessThan50Per, salariesMoreThan50Per])
        print(perSalary)
        perExplore = np.array([0, 0.1, 0])

        plt.title("Percentage of salary by age group")
        plt.pie(perSalary, labels=perSalaryTitle, explode=perExplore)
        plt.legend()
        plt.show()

    # Option 18:
    elif userChoice == 18:
        employeesLessThan35 = 0
        employeesLessThan50 = 0
        employeesMoreThan50 = 0

        for employee in employees:
            if (employee.age < 35):
                employeesLessThan35 += 1
            elif (employee.age < 50):
                employeesLessThan50 += 1
            else:
                employeesMoreThan50 += 1

        totalAgeTitle = np.array(["Less Than 35", "35 to 50", "More Than 50"])
        totalAge = np.array(
            [employeesLessThan35, employeesLessThan50, employeesMoreThan50])
        ageExplore = np.array([0, 0.1, 0])

        plt.title("Percentage of total employee by age group")
        plt.pie(totalAge, labels=totalAgeTitle, explode=ageExplore)
        plt.legend()
        plt.show()

    # Option 19:
    elif userChoice == 19:
        outputFilePath = "RPT001/OUT_Employee_DB.db"
        writeStream = open(outputFilePath, mode='w', encoding='utf_8')
        for employee in employees:
            writeStream.write(
                f"{employee.code}-{employee.name}-{employee.age}-{employee.salary}\n")
        print("Write File Success!")
        writeStream.close()
    else:
        print('Quit! Goodbye!')
        break
