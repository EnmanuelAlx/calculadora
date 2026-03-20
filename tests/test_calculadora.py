"""Tests para la calculadora."""
import pytest
from calculadora import (
    suma,
    resta,
    multiplicacion,
    division,
    potencia,
    promedio,
    numero_mayor,
    modulo_resto,
    prueba_jinn,
)


class TestSuma:
    """Tests para la función suma."""

    def test_suma_positivos(self):
        assert suma(2, 3) == 5
        assert suma(10, 20) == 30

    def test_suma_negativos(self):
        assert suma(-2, -3) == -5
        assert suma(-10, -20) == -30

    def test_suma_mixta(self):
        assert suma(-5, 10) == 5
        assert suma(10, -5) == 5

    def test_suma_ceros(self):
        assert suma(0, 0) == 0
        assert suma(5, 0) == 5
        assert suma(0, 5) == 5

    def test_suma_decimales(self):
        assert suma(2.5, 3.5) == 6.0
        assert suma(1.1, 2.2) == pytest.approx(3.3)


class TestResta:
    """Tests para la función resta."""

    def test_resta_positivos(self):
        assert resta(5, 3) == 2
        assert resta(10, 7) == 3

    def test_resta_negativos(self):
        assert resta(-5, -3) == -2
        assert resta(-3, -5) == 2

    def test_resta_resultado_negativo(self):
        assert resta(3, 5) == -2

    def test_resta_cero(self):
        assert resta(5, 0) == 5
        assert resta(0, 5) == -5


class TestMultiplicacion:
    """Tests para la función multiplicacion."""

    def test_multiplicacion_positivos(self):
        assert multiplicacion(3, 4) == 12
        assert multiplicacion(5, 6) == 30

    def test_multiplicacion_negativos(self):
        assert multiplicacion(-3, -4) == 12
        assert multiplicacion(-2, -5) == 10

    def test_multiplicacion_mixta(self):
        assert multiplicacion(-3, 4) == -12
        assert multiplicacion(3, -4) == -12

    def test_multiplicacion_cero(self):
        assert multiplicacion(5, 0) == 0
        assert multiplicacion(0, 100) == 0

    def test_multiplicacion_decimales(self):
        assert multiplicacion(2.5, 4) == 10.0
        assert multiplicacion(0.5, 0.5) == 0.25


class TestDivision:
    """Tests para la función division."""

    def test_division_exacta(self):
        assert division(10, 2) == 5
        assert division(20, 4) == 5.0

    def test_division_con_decimales(self):
        assert division(10, 4) == 2.5
        assert division(7, 2) == 3.5

    def test_division_por_cero(self):
        assert division(10, 0) is None
        assert division(0, 0) is None

    def test_division_negativos(self):
        assert division(-10, 2) == -5
        assert division(10, -2) == -5
        assert division(-10, -2) == 5

    def test_division_cero_numerador(self):
        assert division(0, 5) == 0


class TestPotencia:
    """Tests para la función potencia."""

    def test_potencia_enteros(self):
        assert potencia(2, 3) == 8
        assert potencia(5, 2) == 25

    def test_potencia_exponente_cero(self):
        assert potencia(5, 0) == 1
        assert potencia(100, 0) == 1

    def test_potencia_exponente_negativo(self):
        assert potencia(2, -1) == 0.5
        assert potencia(4, -2) == 0.0625

    def test_potencia_raiz_cuadrada(self):
        assert potencia(4, 0.5) == 2.0
        assert potencia(9, 0.5) == 3.0

    def test_potencia_base_cero(self):
        assert potencia(0, 5) == 0
        assert potencia(0, 100) == 0


class TestPromedio:
    """Tests para la función promedio."""

    def test_promedio_enteros(self):
        assert promedio([1, 2, 3, 4, 5]) == 3.0
        assert promedio([10, 20, 30]) == 20.0

    def test_promedio_decimales(self):
        assert promedio([1.5, 2.5, 3.0]) == pytest.approx(2.333, rel=1e-3)

    def test_promedio_lista_vacia(self):
        assert promedio([]) is None

    def test_promedio_un_elemento(self):
        assert promedio([42]) == 42.0


class TestNumeroMayor:
    """Tests para la función numero_mayor."""

    def test_numero_mayor_lista(self):
        assert numero_mayor([1, 5, 3, 9, 2]) == 9
        assert numero_mayor([100, 50, 75]) == 100

    def test_numero_mayor_negativos(self):
        assert numero_mayor([-1, -5, -3]) == -1

    def test_numero_mayor_mixto(self):
        assert numero_mayor([-10, 0, 5, -3]) == 5

    def test_numero_mayor_lista_vacia(self):
        assert numero_mayor([]) is None

    def test_numero_mayor_un_elemento(self):
        assert numero_mayor([42]) == 42


class TestModuloResto:
    """Tests para la función modulo_resto."""

    def test_modulo_basico(self):
        assert modulo_resto(10, 3) == 1
        assert modulo_resto(17, 5) == 2

    def test_modulo_divisible(self):
        assert modulo_resto(10, 5) == 0
        assert modulo_resto(100, 10) == 0

    def test_modulo_negativos(self):
        assert modulo_resto(-10, 3) == 2
        assert modulo_resto(10, -3) == -2


class TestPruebaJinn:
    """Tests para la función prueba_jinn (multiplicación alternativa)."""

    def test_multiplicacion_basica(self):
        assert prueba_jinn(3, 4) == 12

    def test_multiplicacion_cero(self):
        assert prueba_jinn(5, 0) == 0

    def test_multiplicacion_negativos(self):
        assert prueba_jinn(-2, 5) == -10
