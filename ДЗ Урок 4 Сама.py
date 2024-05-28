class Car:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

    def __repr__(self):
        return f"Car(brand='{self.brand}', year={self.year}')"
    
    def __str__(self):
        return f"{self.brand}, {self.year}"
    
class ElectricCar(Car):
    def __init__(self, brand, year, battery_capacity):
        super().__init__(brand, year)
        self.battery_capacity = battery_capacity
        
  
