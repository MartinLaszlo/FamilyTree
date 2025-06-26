from datetime import datetime, date

# Base Class: Person (Class 1)
class Person:
    def __init__(self, name, gender, birth_date, death_date):
        self.name = name  # Name of the individual
        self.gender = gender  # Gender of the individual
        self.birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()  # Parse birth_date to datetime.date
        self.death_date = datetime.strptime(death_date, "%Y-%m-%d").date() if death_date else None  # Parse death_date if provided
        self.children = []  # List of children for this person
        self.parents = []  # List of parents for this person
        self.siblings = []  # List of siblings
        self.spouses = []  # List of spouses

    def add_parent(self, parent):
        if parent not in self.parents:
            self.parents.append(parent)
            parent.add_child(self)  # Add child to parent's list

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            child.add_parent(self)  # Add parent to child's list

    def add_sibling(self, sibling):
        if sibling not in self.siblings:
            self.siblings.append(sibling)
            sibling.add_sibling(self)  # Add sibling to the other person

    def add_spouse(self, spouse):
        if spouse not in self.spouses:
            self.spouses.append(spouse)
            spouse.add_spouse(self)  # Add spouse to the other person

    def calculate_number_of_children(self):
        return len(self.children)

    def __repr__(self):
        return self.name

# Utility Class: ImmediateFamily (Class 2)
class ImmediateFamily:
    def get_immediate_family(person):
        parent_names = [parent.name for parent in person.parents]
        child_names = [child.name for child in person.children]
        sibling_names = [sibling.name for sibling in person.siblings]
        spouse_names = [spouse.name for spouse in person.spouses]
        return {
            'Name': person.name,
            'Parents': parent_names,
            'Children': child_names,
            'Siblings': sibling_names,
            'Spouse(s)': spouse_names
        }

    def get_family_birthdays(person):
        family_members = person.parents + person.children + person.siblings + person.spouses
        birthdays = [(member.name, member.birth_date.strftime("%B %d")) for member in family_members]
        sorted_birthdays = sorted(birthdays, key=lambda x: datetime.strptime(x[1], "%B %d"))
        birthday_list = "\n".join([f"{name}: {birthday}" for name, birthday in sorted_birthdays])
        return f"Family Birthdays for {person.name} in order:\n{birthday_list}" if sorted_birthdays else f"No family birthdays found for {person.name}."


# Utility Class: ExtendedFamily (Class 3)
class ExtendedFamily:
    def get_extended_family(person):
        aunts_uncles = []
        cousins = []
        for parent in person.parents:
            for sibling in parent.siblings:
                aunts_uncles.append(sibling.name)
                cousins.extend([child.name for child in sibling.children])
        return {
            'Name': person.name,
            'Aunts/Uncles': aunts_uncles,
            'Cousins': cousins
        }

    def get_cousins(person):
        cousins = []
        for parent in person.parents:
            for sibling in parent.siblings:
                cousins.extend([child.name for child in sibling.children])
        return {
            'Name': person.name,
            'Cousins': cousins
        }


# Utility Class: FamilyStatistics (Class 4)
class FamilyStatistics:
    def calculate_age(person):
        today = date.today()
        end_date = person.death_date if person.death_date else today
        age = end_date.year - person.birth_date.year - (
            (end_date.month, end_date.day) < (person.birth_date.month, person.birth_date.day)
        )
        return age

    def calculate_average_age(person):
        family_members = person.parents + person.children + person.siblings + person.spouses
        if not family_members:
            return f"No family members found for {person.name} to calculate average age."
        ages = [FamilyStatistics.calculate_age(member) for member in family_members] # (POLYMORPHISM)
        average_age = sum(ages) / len(ages)
        return f"Average age of {person.name}'s immediate family is {average_age:.2f} years."

    def calculate_average_number_of_children(person):
        family_members = [person] + person.parents + person.siblings + person.spouses
        if not family_members:
            return f"No family members found for {person.name} to calculate average number of children."
        children_counts = [member.calculate_number_of_children() for member in family_members] #member can be any instance of person, method is defined in Person class (POLYMORPHISM)
        average_children = sum(children_counts) / len(family_members)
        return f"Average number of children for {person.name}'s immediate family is {average_children:.2f}."


# Example Usage
john = Person("John", "Male", "1950-01-01", "2000-01-01")
jane = Person("Jane", "Female", "1970-01-01", "2020-01-01")
alice = Person("Alice", "Female", "1990-01-01", None)
bob = Person("Bob", "Male", "1992-02-15", None)
kate = Person("Kate", "Female", "1975-03-20", None)
mike = Person("Mike", "Male", "1977-04-18", None)
susan = Person("Susan", "Female", "2000-05-25", None)

john.add_parent(jane)
alice.add_parent(john)
bob.add_parent(john)
john.add_sibling(kate)
mike.add_sibling(jane)
kate.add_child(susan)

# Testing
print("Average age of family:")
print(FamilyStatistics.calculate_average_age(john))  # Average age of Alice's family
print("########################################################")
print("Extended family details:")
print(ExtendedFamily.get_extended_family(john))  # Extended family details of Kate
print("########################################################")
print("Average number of children for person's family:")
print(FamilyStatistics.calculate_average_number_of_children(john))  # Average number of children for John's family
print("########################################################")
print("Immediate family details of person:")
print(ImmediateFamily.get_immediate_family(alice))  # Immediate family details of Jane
print("########################################################")
print("Cousins of person:")
print(ExtendedFamily.get_cousins(alice))

#ALL METHODS IN UTILITY CLASSES (ImmediateFamily, ExtendedFamily and FamilyStatistics) RELY ON THE Person CLASS
#THEREFORE, ALL METHODS, FUNCTIONS ETC. OUTSIDE OF THE Person CLASS USE (POLYMORPHISM)