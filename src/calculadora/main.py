def suma(a, b):
    return a + b

def prueba_jinn(a,b):
    return a * b

def modulo_resto(a,b):
    return a % b

if __name__ == "__main__":
    print("Hello, World!")

def numero_mayor(lista):
    if not lista:
        return None 
    return max(lista)

def division(dividendo,divisor):
    if divisor ==0:
        return None
    division=dividendo/divisor
    return division

def resta(a, b):
    return a - b

def potencia(a, b):
    """Devuelve a elevado a la b (soporta enteros y reales)."""
    return a ** b

if __name__ == "__main__":
    print(potencia(2, 3))    # 8
    print(potencia(4, 0.5))  # 2.0 (raíz cuadrada)
    print(potencia(2, -1))   # 0.5


