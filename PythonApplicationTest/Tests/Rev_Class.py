#Classes

class Dog:
    species = "Canis familiaris"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name} is {self.age} years old"

    def speak(self, sound):
        return f"{self.name} barks {sound}"


class JackRussellTerrier(Dog):
    def speak(self, sound="Arf"):
        return super().speak(sound)
    pass
    

class Dachshund(Dog):
    def speak(self, sound="Woof"):
        return f"{self.name} says {sound}"

class GoldenRetriever(Dog):
    def speak(self, sound="Bark"):
        return super().speak(sound)

class Bulldog(Dog):
    pass


dogInst = Dog("MyDog", 6)
miles = JackRussellTerrier("Miles", 4)
buddy = Dachshund("Buddy", 9)
jack = Bulldog("Jack", 3)
jim = Bulldog("Jim", 5)
gr = GoldenRetriever("gr", 5)

print(isinstance(miles, Dog))
print(isinstance(miles, Bulldog))

print(miles.speak())
print(jack.speak("BarkBark!"))
print(miles.speak("ArfModified"))
print(dogInst.speak("DogSound"))
print(gr.speak())
