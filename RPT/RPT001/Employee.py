class Employee:
    code = ""
    name = ""
    age = 0
    salary = 0.0

    def __init__(self, code, name, age, salary):
        self.code = code
        self.name = name
        self.age = age
        self.salary = salary

    def income(self):
        return 0.9 * 12 * self.salary

    def increaseSalary(self, amount):
        if amount > 0:
            self.salary += amount
        else:
            print(f"Invalid amount!")
        return self.salary

    def decreaseSalary(self, amount):
        if ((amount > 0) and (amount > 0.2 * self.salary)):
            self.salary -= amount
        else:
            print(f"Invalid amount!")
        return self.salary

    def display(self):
        print(
            f'Code: {self.code}, Name: {self.name}, Age: {self.age}, Salary: {self.salary}, Income: {round(self.income(), 2)}')
