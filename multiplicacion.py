def multiplicacion():
    """Función para multiplicar dos números ingresados por el usuario"""
    try:
        a = float(input("Ingresa el primer número (a): "))
        b = float(input("Ingresa el segundo número (b): "))
        resultado = a * b
        print(f"\n{a} × {b} = {resultado}")
        return resultado
    except ValueError:
        print("Error: Debes ingresar números válidos")
        return None


if __name__ == "__main__":
    multiplicacion()

