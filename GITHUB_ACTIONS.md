# GitHub Actions - Guía Completa

## ¿Qué es GitHub Actions?

GitHub Actions es una **plataforma de CI/CD (Integración Continua / Despliegue Continuo)** integrada en GitHub. Te permite automatizar tareas cada vez que ocurre algo en tu repositorio.

### Conceptos clave

| Concepto | Explicación |
|----------|-------------|
| **Workflow** | Un archivo YAML que define una o más tareas automatizadas |
| **Event (Trigger)** | Lo que "dispara" el workflow (push, pull_request, etc.) |
| **Job** | Un conjunto de pasos que se ejecutan en el mismo runner |
| **Step** | Una tarea individual dentro de un job |
| **Runner** | La máquina (servidor) que ejecuta tus jobs |
| **Action** | Tareas pre-construidas que puedes reutilizar del marketplace |

---

## Estructura básica de un workflow

```yaml
# .github/workflows/mi-workflow.yml
name: Nombre del Workflow    # Opcional, aparece en la UI de GitHub

on:                          # Cuándo se ejecuta
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:                        # Qué tareas ejecutar
  build:                     # Nombre del job
    runs-on: ubuntu-latest   # En qué sistema operativo
    steps:
      - name: Checkout       # Nombre del paso
        uses: actions/checkout@v4   # Usar una action pre-construida

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Run tests
        run: pytest          # Comando a ejecutar
```

---

## Triggers (Eventos) más comunes

```yaml
on:
  # Cada push a cualquier rama
  push:

  # Solo push a ramas específicas
  push:
    branches:
      - main
      - develop

  # Cada pull request hacia main
  pull_request:
    branches: [main]

  # Excluir ciertas ramas
  push:
    branches-ignore:
      - 'docs/**'

  # En cada pull request (sin importar rama destino)
  pull_request:
    types: [opened, synchronize, reopened]

  # Programado (cron)
  schedule:
    - cron: '0 0 * * *'  # Todos los días a medianoche

  # Manual (botón en GitHub)
  workflow_dispatch:
```

### Ejemplo: Ejecutar solo en PRs a master

```yaml
on:
  pull_request:
    branches:
      - master
    types: [opened, synchronize, reopened]
```

Esto ejecutará el workflow cuando:
- Se abra un PR hacia master
- Se hagan cambios en un PR existente hacia master (synchronize)
- Se reabra un PR hacia master

---

## Casos de uso comunes

### 1. Ejecutar tests automáticamente

```yaml
name: Tests

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install pytest
          pip install -e .

      - name: Run tests
        run: pytest
```

### 2. Lint y formato de código

```yaml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install ruff
        run: pip install ruff

      - name: Check formatting
        run: ruff check .

      - name: Check style
        run: ruff format --check .
```

### 3. Despliegue a producción

```yaml
name: Deploy

on:
  push:
    tags:
      - 'v*'    # Solo cuando se crean tags como v1.0.0

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install build twine

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
        run: twine upload dist/*
```

### 4. Matrix de pruebas (múltiples versiones)

```yaml
name: Test Matrix

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Run tests
        run: |
          pip install pytest
          pytest
```

---

## Variables y secretos

### Variables de entorno

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: postgres://localhost/test
      API_KEY: test-key
    steps:
      - run: echo $DATABASE_URL
```

### Secretos de GitHub

Los secretos se configuran en **Settings > Secrets and variables > Actions**:

```yaml
jobs:
  deploy:
    steps:
      - name: Deploy
        env:
          API_TOKEN: ${{ secrets.API_TOKEN }}
          DATABASE_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: |
          echo "Desplegando con token $API_TOKEN"
```

### Variables del contexto

```yaml
jobs:
  build:
    steps:
      - name: Mostrar info
        run: |
          echo "Branch: ${{ github.ref }}"
          echo "Commit: ${{ github.sha }}"
          echo "Autor: ${{ github.actor }}"
          echo "Repo: ${{ github.repository }}"
          echo "Evento: ${{ github.event_name }}"
```

---

## GitHub Actions Marketplace

El marketplace tiene miles de actions pre-construidas:

**Populares para Python:**
- `actions/setup-python@v5` - Instala Python
- `actions/checkout@v4` - Hace checkout del código
- `codecov/codecov-action@v3` - Reporta cobertura
- `snok/install-poetry@v1` - Instala Poetry
- `astral-sh/setup-uv@v3` - Instala uv

**Ejemplo de uso:**

```yaml
steps:
  # Action oficial de GitHub
  - uses: actions/checkout@v4

  # Action de terceros para uv
  - uses: astral-sh/setup-uv@v3
    with:
      version: "0.6.0"

  # Action para reportar cobertura
  - uses: codecov/codecov-action@v3
    with:
      files: ./coverage.xml
```

---

## Ejemplo completo: CI/CD para Python con uv

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup uv
        uses: astral-sh/setup-uv@v3
        with:
          version: "0.6.0"
          enable-cache: true

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: uv sync --all-extras --dev

      - name: Run tests
        run: uv run pytest tests/

      - name: Run type checking
        run: uv run mypy src/

      - name: Run linter
        run: uv run ruff check .
```

---

## Tips y buenas prácticas

1. **Usa versiones específicas** de las actions (`@v4` en vez de `@main`)
2. **Cachea dependencias** para que los workflows sean más rápidos
3. **Usa matrices** para probar en múltiples versiones de Python
4. **No commitees secretos**, usa `secrets.*` siempre
5. **Haz los workflows específicos**, ejecuta solo cuando sea necesario
6. **Añade badges** al README para ver el estado de los workflows


---

## Ejecución en paralelo y asíncrona

GitHub Actions permite ejecutar múltiples jobs en paralelo y dentro de un mismo job, ejecutar pasos de forma asíncrona.

### Jobs en paralelo

Por defecto, los jobs se ejecutan en paralelo. No necesitas configuración especial:

```yaml
name: Jobs Paralelos

on: [push]

jobs:
  test-unitarios:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Run unit tests
        run: pytest tests/unit/

  test-integracion:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Run integration tests
        run: pytest tests/integration/

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run linter
        run: ruff check .
```

En este ejemplo, `test-unitarios`, `test-integracion` y `lint` corren al mismo tiempo en diferentes runners.

### Dependencias entre jobs (needs)

Si necesitas que un job espere a otro, usa `needs`:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Ejecutando tests"

  lint:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Ejecutando linter"

  deploy:
    needs: [test, lint]  # Espera que test y lint terminen
    runs-on: ubuntu-latest
    steps:
      - run: echo "Desplegando..."
```

Aquí `deploy` espera que **ambos** `test` y `lint` terminen exitosamente.

### Matrix strategy (paralelismo masivo)

La estrategia matrix crea múltiples jobs en paralelo con diferentes configuraciones:

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false  # Si uno falla, los demás siguen corriendo
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.9', '3.10', '3.11', '3.12']
        
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Run tests
        run: pytest
```

Esto crea **12 jobs en paralelo** (3 OS × 4 versiones de Python).

### Pasos asíncronos dentro de un job (background)

Para ejecutar procesos en segundo plano dentro de un job:

```yaml
jobs:
  test-con-servicios:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Iniciar servicio en background
      - name: Start database
        run: |
          docker run -d --name postgres -p 5432:5432 postgres:15
          sleep 10  # Esperar a que inicie
      
      # Mientras el database corre, ejecutar tests
      - name: Run tests
        run: pytest tests/integration/
        env:
          DATABASE_URL: postgres://localhost:5432/test
      
      # Limpiar el servicio
      - name: Cleanup
        if: always()
        run: docker stop postgres
```

### Services (contenedores auxiliares)

Para servicios que deben iniciar antes de los pasos:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Run tests
        run: pytest tests/
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
          REDIS_URL: redis://localhost:6379
```

Los servicios (`postgres`, `redis`) inician en paralelo **antes** de que comiencen los steps.

### Ejemplo completo: CI con paralelismo

```yaml
name: CI Paralelo

on: [push, pull_request]

jobs:
  # Job 1: Tests unitarios (rápidos)
  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: pip install pytest
      - run: pytest tests/unit/ -v

  # Job 2: Linter (independiente)
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff
      - run: ruff check .

  # Job 3: Type checking (independiente)
  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install mypy
      - run: mypy src/

  # Job 4: Tests de integración (lentos, con servicios)
  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests  # Espera tests unitarios
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install pytest psycopg2
      - run: pytest tests/integration/ -v

  # Job 5: Build (solo si todo lo demás pasa)
  build:
    needs: [unit-tests, lint, typecheck]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m build
```

En este workflow:
- `unit-tests`, `lint`, `typecheck` corren en paralelo inmediatamente
- `integration-tests` espera que `unit-tests` termine
- `build` espera que unit-tests, lint y typecheck terminen

---

## Enlaces útiles

- [Documentación oficial](https://docs.github.com/es/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Workflow syntax](https://docs.github.com/es/actions/using-workflows/workflow-syntax-for-github-actions)
- [Eventos que disparan workflows](https://docs.github.com/es/actions/using-workflows/events-that-trigger-workflows)
