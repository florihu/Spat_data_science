



class Animals():

    number_animals = 0
    def __int__(self, name, age, id):
        self.name = name
        self.age = age
        self.id = id


class Herbivors(Animals):

    def __init__(self, name, age, id):
        self.name = name
        self.age = age
        self.id = id


class Turtle(Herbivors):
    def __init__(self, name, age, id, caloric_demand):
        self.name = name
        self.age = age
        self.id = id
        self.caloric_demand = caloric_demand

    def food_data(self, food_name, type_food, caloric_value):
        self.food = Food(food_name, type_food, caloric_value)


    def saturation(self, servings):
        if (self.caloric_value * servings / self.caloric_demand) < 1:
            print('I need more food')
        else:
            print('Now i will reproduce')


class Food:
    def __init__(self, name, type, caloric_value):
        self.name = name
        self.type = type
        self.caloric_value = caloric_value





turtle1 = Turtle('peter', 120, 123, 'algae', 'cucumber', 100)



turtle1.saturation(10)


