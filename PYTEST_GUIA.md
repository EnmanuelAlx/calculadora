# Pytest - Guía Rápida

Pytest es el framework de testing más popular para Python. Es simple, potente y requiere poco código boilerplate.

---

## Instalación

```bash
pip install pytest

# O con uv
uv add --dev pytest
```

---

## Tu primer test

```python
# test_ejemplo.py
def test_suma():
    assert 2 + 2 == 4

# Ejecutar: pytest test_ejemplo.py
```

**Regla de oro:** Las funciones de test deben empezar con `test_`.

---

## Asserts en pytest

Pytest tiene asserts inteligentes que muestran qué salió mal:

```python
def test_asserts_basicos():
    assert 5 > 3           # True
    assert "hola" in "hola mundo"
    assert [1, 2, 3] == [1, 2, 3]

def test_assert_con_mensaje():
    resultado = 5
    esperado = 10
    assert resultado == esperado, f"Esperaba {esperado}, obtuve {resultado}"

def test_excepciones():
    with pytest.raises(ZeroDivisionError):
        1 / 0
    
    with pytest.raises(ValueError, match="invalid"):
        int("no es un numero")
```

---

## Organización de tests

### Estructura recomendada

```
mi_proyecto/
├── src/
│   └── mi_modulo.py
└── tests/
    ├── __init__.py
    ├── test_modulo.py          # Tests de un módulo
    └── test_integration.py     # Tests de integración
```

### Clases para agrupar tests

```python
class TestCalculadora:
    """Grupo de tests relacionados"""
    
    def test_suma_positivos(self):
        assert suma(2, 3) == 5
    
    def test_suma_negativos(self):
        assert suma(-2, -3) == -5
    
    def test_suma_cero(self):
        assert suma(5, 0) == 5
```

**Ventaja:** Los tests se organizan por funcionalidad en el reporte.

---

## Fixtures (datos de prueba)

Las fixtures preparan datos/recursoss para tus tests:

```python
import pytest

@pytest.fixture
def usuario_ejemplo():
    """Crea un usuario de prueba"""
    return {"nombre": "Juan", "edad": 30}

def test_usuario_nombre(usuario_ejemplo):
    assert usuario_ejemplo["nombre"] == "Juan"

def test_usuario_edad(usuario_ejemplo):
    assert usuario_ejemplo["edad"] == 30
```

### Fixture con setup/teardown

```python
@pytest.fixture
def archivo_temp():
    # Setup: crear archivo
    archivo = open("/tmp/test.txt", "w")
    archivo.write("contenido")
    archivo.close()
    
    yield archivo  # Lo que retorna al test
    
    # Teardown: limpiar después
    import os
    os.remove("/tmp/test.txt")

def test_leer_archivo(archivo_temp):
    with open("/tmp/test.txt", "r") as f:
        assert f.read() == "contenido"
```

### Scope de fixtures

```python
@pytest.fixture(scope="function")   # Nueva por cada test (default)
@pytest.fixture(scope="class")      # Una por clase de tests
@pytest.fixture(scope="module")     # Una por archivo de test
@pytest.fixture(scope="session")  # Una por toda la ejecución
```

---

## Parametrización (múltiples casos)

Ejecuta el mismo test con diferentes datos:

```python
import pytest

@pytest.mark.parametrize("a, b, resultado", [
    (2, 3, 5),      # caso 1
    (-1, 1, 0),     # caso 2
    (0, 0, 0),      # caso 3
    (10, -5, 5),    # caso 4
])
def test_suma_parametrizada(a, b, resultado):
    assert suma(a, b) == resultado
```

Salida:
```
test_suma_parametrizada[2-3-5]    PASSED
test_suma_parametrizada[-1-1-0]   PASSED
test_suma_parametrizada[0-0-0]    PASSED
test_suma_parametrizada[10--5-5] PASSED
```

---

## Marcadores (markers)

### Saltar tests

```python
@pytest.mark.skip(reason="No implementado aún")
def test_feature_nueva():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="No funciona en Windows")
def test_unix_only():
    pass
```

### Tests que esperan fallar

```python
@pytest.mark.xfail(reason="Bug conocido #123")
def test_con_bug():
    assert funcion_rota() == resultado_esperado
```

### Tests lentos

```python
@pytest.mark.slow
def test_integracion_completa():
    # Toma mucho tiempo
    pass

# Ejecutar solo tests lentos: pytest -m slow
# Excluir tests lentos: pytest -m "not slow"
```

---

## Comandos útiles

```bash
# Ejecutar todos los tests
pytest

# Ejecutar archivo específico
pytest tests/test_calculadora.py

# Ejecutar función específica
pytest tests/test_calculadora.py::test_suma

# Ejecutar clase de tests
pytest tests/test_calculadora.py::TestCalculadora

# Verbose (más detalle)
pytest -v

# Parar en el primer fallo
pytest -x

# Mostrar prints y outputs
pytest -s

# Medir cobertura (necesitas pytest-cov)
pytest --cov=src --cov-report=html

# Solo tests fallidos del anterior run
pytest --lf

# N tests en paralelo (necesitas pytest-xdist)
pytest -n auto
```

---

## Aproximaciones (para floats)

```python
import pytest

def test_calculo_decimal():
    resultado = 0.1 + 0.2
    # ❌ assert resultado == 0.3  # Falla por precisión
    
    # ✅ Usa aprox
    assert resultado == pytest.approx(0.3)
    
    # Con tolerancia personalizada
    assert 3.14159 == pytest.approx(3.14, rel=1e-2)  # 1% de tolerancia
```

---

## Conftest.py (fixtures globales)

Crea un archivo `conftest.py` en tu carpeta `tests/` para compartir fixtures entre archivos:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def cliente_api():
    from mi_app import crear_cliente
    return crear_cliente()

@pytest.fixture
def datos_csv():
    return "nombre,edad\nJuan,30\nMaria,25"
```

Ahora cualquier test en `tests/` puede usar `cliente_api` y `datos_csv`.

---

## Plugins útiles

| Plugin | Comando instalar | Uso |
|--------|-----------------|-----|
| pytest-cov | `pip install pytest-cov` | Medir cobertura de código |
| pytest-xdist | `pip install pytest-xdist` | Tests en paralelo (`-n auto`) |
| pytest-django | `pip install pytest-django` | Testing con Django |
| pytest-asyncio | `pip install pytest-asyncio` | Tests async/await |

---

## Ejemplo completo

```python
# tests/test_calculadora.py
import pytest
from calculadora import suma, division


class TestSuma:
    """Tests para la función suma."""

    @pytest.mark.parametrize("a, b, esperado", [
        (2, 3, 5),
        (-1, -1, -2),
        (0, 5, 5),
    ])
    def test_suma(self, a, b, esperado):
        assert suma(a, b) == esperado


class TestDivision:
    """Tests para la función división."""

    def test_division_normal(self):
        assert division(10, 2) == 5

    def test_division_por_cero(self):
        assert division(10, 0) is None

    @pytest.mark.slow
    def test_division_masiva(self):
        # Test que toma tiempo
        for i in range(1000000):
            assert division(i, 1) == i
```

Ejecutar:
```bash
pytest tests/test_calculadora.py -v
```

---

## Recursos

- [Documentación oficial](https://docs.pytest.org/)
- [Lista de plugins](https://docs.pytest.org/en/latest/reference/plugin_list.html)
