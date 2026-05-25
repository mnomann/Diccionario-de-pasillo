# Diccionario-de-pasillo
proyecto semestral asignatura comprension del contexto social

## Integrantes
1. Hector Chavez (Integracion)
2. Gabriel Fierro (Backend)
3. Christian Muñoz (Frontend)

## Traductor de Ironia y Modismos
### Objetivo General
Desarrollar una herramienta de apoyo que facilite la decodificacion de normas sociales
implicitas, ironias y el lenguaje informal chileno, con el proposito de mejorar la interaccion
social, reducir la ansiedad comunicativa y promover la autonomia de personas
neurodivergentes.

### Objetivos Especificos
1. Identificar y catalogar las expresiones informales, modismos (slang chileno) y
situaciones sociales implicitas mas comunes que generan barreras de comprension
en personas con TEA, TDAH u otras neurodivergencias.
2. Disenar una plataforma o recurso accesible que "traduzca" y explique de manera
literal, estructurada y visual los dobles sentidos, las indirectas y el sarcasmo local.
3. Validar la usabilidad y efectividad de la herramienta mediante pruebas directas con
usuarios neurodivergentes, asegurando que se adapte a sus estilos de
procesamiento cognitivo.
4. Fomentar la psicoeducacion en el entorno social general, promoviendo la empatia y
estrategias de comunicacion mas claras y directas para facilitar la inclusion.

## Justificacion
Este proyecto presta su utilidad en la facilidad de comunicacion entre personas con desconocimiento
en la lengua y sus diversificaciones sociales y geograficas ayudando a entender y esclarecer mensajes
dandole forma y formalidad.

## Stack Tecnologico

| Capa                  | Tecnologia                | Version sugerida |
|-----------------------|---------------------------|------------------|
| Frontend              | Vue + React + TypeScript  | Node 18+, npm 9+ |
| Backend               | Python + FastAPI          | Python 3.11+     |
| Base de Datos         | PostgreSQL                | 15+              |
| Control de versiones  | Git + GitHub              | -                |

### Frontend
- **vue**: Empaquetador rapido con HMR (Hot Module Replacement)
- **TypeScript**: Tipado estatico para evitar errores

### Backend
- **Python**: Lenguaje principal del servidor
- **FastAPI**: Framework para crear las APIs REST

### Base de Datos
- **PostgreSQL**: Base de datos relacional

## Instalacion y Uso

### Requisitos
- Node.js 18 o superior
- Python 3.11 o superior
- PostgreSQL 15 o superior
- Git

### Pasos para correr el proyecto

**1. Clonar el repositorio**
```bash
git clone https://github.com/mnomann/Diccionario-de-pasillo
```

**2. Base de datos**
```bash
# Crear la base de datos en PostgreSQL
createdb desenreda

# Ejecutar las migraciones (cuando esten listas)
# psql -U usuario -d diccionario_pasillo -f database/migraciones.sql
```

**3. Backend**
```bash
cd backend
python -m venv venv
```

**4. Frontend**
```bash
cd frontend
npm install
npm run dev
```

### Funcionalidades principales
- **Traductor**: Escribe una frase y recibe la traduccion con explicacion
- **Escenarios**: Explora frases por situacion (entrevista, medico, amigos, etc.)
- **Palabras**: Busca palabras tipicas chilenas con su significado
- **Sugerencias**: Aporta nuevas palabras o frases al diccionario
