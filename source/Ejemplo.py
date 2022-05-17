def suma(n1, n2):
    return n1 + n2

# podemos declarar una función fuera de clase para ser utilizada para un endpoint
def endPointFuncion():
    return "<p>endpoint funcion</p>"

class Vector:

    # metodo inicializador
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # ejemplo de método de instancia que no hace nada especial
    def sum(self, x, y, z):
        resultado = Vector(self.x + x, self.y + y, self.z + z)
        return resultado

    # método para traducir objeto a string
    def __str__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.z)

    # se puede declarar dentro de una clase
    # podría servir como manera de organizarse pero nada más
    def endPointClase():
        return "<p>endpoint clase</p>"