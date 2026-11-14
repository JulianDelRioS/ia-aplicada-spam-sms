# Detección de spam y smishing en SMS

Proyecto capstone, IA Aplicada, Módulo 4. Julian Del Rio

## Problema
Clasificar SMS entrantes como legítimos o spam/smishing para apoyar a un equipo antifraude.
El sistema recomienda **entregar**, **marcar como spam** o **derivar a revisión** (abstención).
No debe usarse como bloqueo automático sin apelación ni en idiomas distintos del inglés sin validación previa.

## Dataset
SMS Spam Collection v.1 (Almeida, Gómez Hidalgo y Yamakami, 2011), UCI Machine Learning Repository (id 228).
Licencia CC BY 4.0. Contiene 5.574 mensajes en inglés (747 spam). El archivo va en `data/raw/SMSSpamCollection`.

## Instalación
```bash
pip install -r requirements.txt
```

## Ejecución
```bash
# Valida el dataset, elimina duplicados y genera el split congelado (semilla 42)
python src/data.py
```

## Resultado principal
_Pendiente (presentación intermedia, 20 nov)._

## Estructura
- `config.yaml`: semillas y parámetros
- `data/raw/`: datos originales (no se modifican)
- `data/splits/`: índices de train / validación / test (test congelado)
- `src/`: carga, validación, partición, baseline y modelos
- `notebooks/`: exploración y experimentos
- `results/`: métricas, tablas y análisis de errores
- `docs/`: propuesta, data card, model/system card, diapositivas
- `BITACORA.md`: evidencias por sesión

## Riesgos, límites y casos de abstención
_Se completará en la model/system card._

## Uso de asistentes de IA
Se usó Claude (asistente de IA) para estructurar el esqueleto de este repositorio.
Las decisiones, la ejecución y la verificación son del autor.
