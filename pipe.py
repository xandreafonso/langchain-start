class Run1:
    def __init__(self, text) -> None:
        self.text = text

    def __ror__(self, other):
        print("Run1 recebe: ", other)
        self.text = other.text + ", " + self.text
        return self
    
class Run2:
    def __init__(self, text) -> None:
        self.text = text

    def __ror__(self, other):
        print("Run2 recebe: ", other)
        self.text = other.text + ", " + self.text
        return self

class Run3:
    def __init__(self, text) -> None:
        self.text = text

    def __ror__(self, other):
        print("Run3 recebe: ", other)
        self.text = other.text + ", " + self.text
        return self
    
final = Run1("Passou pelo run 1") | Run2("Passou pelo run 2") | Run3("Passou pelo run 3")

print("Resultado final: ", final.text)
