"""
Management command to seed Module 4: "Análisis Técnico"
4 full lessons with rich content and 3 quizzes each (12 quizzes total).
Correct-answer positions are distributed across A/B/C/D.
"""

from django.core.management.base import BaseCommand

from apps.lessons.models import Lesson, Module, Quiz, QuizOption

MODULE_DATA = {
    "title": "Análisis Técnico",
    "description": (
        "Aprende a leer gráficos, identificar patrones y usar indicadores técnicos "
        "para tomar decisiones de trading informadas."
    ),
    "icon": "📉",
    "color": "#8b5cf6",
    "difficulty": "intermediate",
    "order": 3,
    "xp_reward": 800,
}

# ---------------------------------------------------------------------------
# LESSON 1
# ---------------------------------------------------------------------------
LESSON_1 = {
    "title": "Introducción a los Gráficos",
    "description": "Conoce los principales tipos de gráficos financieros y aprende a leer la información que contienen.",
    "estimated_time": 7,
    "content": """# Introducción a los Gráficos Financieros

Los gráficos son la herramienta principal del análisis técnico. Representan visualmente la evolución del precio de un activo a lo largo del tiempo y permiten identificar **tendencias, patrones y señales** que ayudan a tomar decisiones de inversión.

## ¿Qué es el análisis técnico?

El análisis técnico estudia los movimientos de precio y volumen **pasados** para intentar predecir movimientos **futuros**. Se basa en tres premisas:

1. **El precio lo descuenta todo**: Toda la información disponible ya está reflejada en el precio.
2. **Los precios se mueven en tendencias**: Una vez establecida, una tendencia tiende a continuar.
3. **La historia se repite**: Los patrones de precio tienden a repetirse porque la psicología humana no cambia.

> El análisis técnico no predice el futuro con certeza — identifica probabilidades y gestiona el riesgo.

## Tipos de gráficos

### Gráfico de líneas
- El más simple: une los precios de cierre con una línea continua.
- Ventaja: Limpio y fácil de leer.
- Desventaja: No muestra la variación intradía (máximo, mínimo, apertura).

### Gráfico de barras (OHLC)
Cada barra muestra cuatro datos:
- **O** (Open): Precio de apertura
- **H** (High): Precio máximo del periodo
- **L** (Low): Precio mínimo del periodo
- **C** (Close): Precio de cierre

### Gráfico de velas japonesas (Candlestick)
Es el más popular entre los traders. Cada vela muestra los mismos datos OHLC que las barras, pero de forma más visual:
- **Cuerpo verde/blanco**: El precio subió (cierre > apertura).
- **Cuerpo rojo/negro**: El precio bajó (cierre < apertura).
- **Mechas/sombras**: Líneas finas que muestran el máximo y mínimo del periodo.

## Temporalidades (Timeframes)

El mismo activo se ve diferente según la escala temporal:
- **1 minuto, 5 minutos, 15 minutos**: Para day trading.
- **1 hora, 4 horas**: Para swing trading a corto plazo.
- **Diario**: El más usado para análisis general.
- **Semanal, mensual**: Para inversiones a largo plazo.

### Consejo importante
Siempre analiza **al menos dos temporalidades**: una mayor para ver la tendencia general y una menor para afinar tu punto de entrada.

## El volumen

El volumen indica **cuántas acciones o contratos se han negociado** en un periodo. Es crucial porque confirma o invalida los movimientos de precio:

- **Precio sube con volumen alto**: La subida tiene fuerza, probablemente continuará.
- **Precio sube con volumen bajo**: La subida es débil, podría revertirse.
- **Precio baja con volumen alto**: La bajada tiene convicción, cuidado.

> El precio te dice QUÉ está pasando. El volumen te dice si es REAL.
""",
    "quizzes": [
        {
            "question": "¿Qué tipo de gráfico es el más popular entre los traders?",
            "explanation": "Las velas japonesas (candlestick) son el tipo de gráfico más usado por los traders porque muestran de forma muy visual los cuatro datos clave (apertura, cierre, máximo, mínimo) y permiten identificar patrones rápidamente.",
            "options": [
                ("Gráfico de líneas", False),
                ("Gráfico de sectores (circular)", False),
                ("Gráfico de velas japonesas (candlestick)", True),
                ("Gráfico de barras horizontales", False),
            ],
        },
        {
            "question": "Si una vela japonesa tiene cuerpo verde/blanco, ¿qué significa?",
            "explanation": "Un cuerpo verde o blanco indica que el precio de cierre fue mayor que el precio de apertura, es decir, el precio subió durante ese periodo.",
            "options": [
                ("Que el precio bajó durante ese periodo", False),
                ("Que el volumen fue muy alto", False),
                ("Que no hubo cambios en el precio", False),
                ("Que el precio subió (cierre mayor que apertura)", True),
            ],
        },
        {
            "question": "¿Qué indica un precio que sube pero con volumen bajo?",
            "explanation": "Cuando el precio sube pero el volumen es bajo, la subida carece de fuerza y convicción. Pocos participantes están comprando, lo que sugiere que el movimiento podría revertirse fácilmente.",
            "options": [
                ("Que la subida es débil y podría revertirse", True),
                ("Que la subida es muy fuerte y va a continuar", False),
                ("Que es buen momento para comprar", False),
                ("Que el mercado está cerrado", False),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# LESSON 2
# ---------------------------------------------------------------------------
LESSON_2 = {
    "title": "Soporte y Resistencia",
    "description": "Aprende a identificar los niveles de soporte y resistencia, las zonas clave donde el precio tiende a reaccionar.",
    "estimated_time": 7,
    "content": """# Soporte y Resistencia

Los niveles de soporte y resistencia son, posiblemente, los conceptos más importantes del análisis técnico. Son las **zonas de precio donde la oferta y la demanda se encuentran** y provocan reacciones en el precio.

## ¿Qué es un soporte?

Un soporte es un nivel de precio donde la **demanda (compradores) es suficientemente fuerte** para detener la caída del precio. Es como un "suelo" que impide que el precio baje más.

### ¿Por qué funciona?
- Los compradores recuerdan que a ese precio fue una buena compra anteriormente.
- Los vendedores en corto toman beneficios a ese nivel.
- Se acumulan órdenes de compra pendientes en esa zona.

## ¿Qué es una resistencia?

Una resistencia es un nivel de precio donde la **oferta (vendedores) es suficientemente fuerte** para detener la subida. Es como un "techo" que impide que el precio suba más.

### ¿Por qué funciona?
- Los compradores que estaban "atrapados" en pérdidas venden para recuperar su dinero cuando el precio vuelve a ese nivel.
- Los traders toman beneficios al llegar a ese precio.
- Se acumulan órdenes de venta pendientes.

## La regla de la inversión de roles

Uno de los principios más poderosos del análisis técnico:

> Cuando un soporte se rompe, se convierte en resistencia. Cuando una resistencia se rompe, se convierte en soporte.

Esto ocurre por la psicología del mercado:
- Si el precio rompe un soporte hacia abajo, los que compraron en ese nivel ahora están en pérdidas. Cuando el precio vuelva a subir a ese nivel, venderán para "salir sin pérdidas", creando resistencia.
- Lo contrario ocurre cuando una resistencia se rompe al alza.

## Cómo identificar soportes y resistencias

### 1. Máximos y mínimos anteriores
Busca niveles donde el precio rebotó varias veces. Cuantas más veces haya rebotado en un nivel, más fuerte es.

### 2. Números redondos
Los precios psicológicos (10 €, 50 €, 100 €, 1.000 €) suelen actuar como soporte o resistencia porque muchos traders colocan órdenes en cifras redondas.

### 3. Zonas, no líneas exactas
Los soportes y resistencias no son precios exactos, sino **zonas**. Un soporte en 45 € realmente podría actuar entre 44,50 € y 45,50 €.

## ¿Qué pasa cuando se rompen?

Una **ruptura (breakout)** ocurre cuando el precio atraviesa un soporte o resistencia con fuerza. Para confirmar que es una ruptura real:

- **Volumen**: Debe aumentar significativamente en la ruptura.
- **Cierre**: El precio debe cerrar por encima/debajo del nivel, no solo tocarlo intradía.
- **Retesteo**: A menudo el precio vuelve a probar el nivel roto antes de continuar la dirección.

### Rupturas falsas (fakeouts)
A veces el precio rompe un nivel pero vuelve rápidamente. Es una trampa. Por eso es importante esperar confirmación (volumen + cierre) antes de actuar.
""",
    "quizzes": [
        {
            "question": "¿Qué ocurre cuando un nivel de soporte se rompe?",
            "explanation": "La regla de inversión de roles dice que cuando un soporte se rompe, se convierte en resistencia. Los compradores que perdieron dinero en ese nivel venderán cuando el precio vuelva allí, creando presión vendedora.",
            "options": [
                ("Desaparece y ya no tiene relevancia", False),
                ("Se convierte en un nivel de resistencia", True),
                ("Se vuelve un soporte aún más fuerte", False),
                ("El mercado cierra automáticamente", False),
            ],
        },
        {
            "question": "¿Cuál de estos factores ayuda a confirmar que una ruptura de resistencia es real?",
            "explanation": "Un aumento significativo del volumen durante la ruptura confirma que hay convicción detrás del movimiento. Sin volumen, la ruptura puede ser falsa (fakeout).",
            "options": [
                ("Que el precio toque el nivel una sola vez", False),
                ("Que sea lunes por la mañana", False),
                ("Un aumento significativo del volumen en la ruptura", True),
                ("Que el precio baje inmediatamente después", False),
            ],
        },
        {
            "question": "¿Por qué los números redondos (como 100 € o 1.000 €) actúan a menudo como soporte o resistencia?",
            "explanation": "Los números redondos son niveles psicológicos donde muchos traders colocan sus órdenes de compra o venta. Esta concentración de órdenes crea zonas de soporte o resistencia naturales.",
            "options": [
                ("Porque los brokers los eligen como límites de precio", False),
                (
                    "Porque muchos traders colocan órdenes en cifras redondas por psicología",
                    True,
                ),
                ("Porque son los precios oficiales de la bolsa", False),
                ("No actúan como soporte ni resistencia, es un mito", False),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# LESSON 3
# ---------------------------------------------------------------------------
LESSON_3 = {
    "title": "Medias Móviles",
    "description": "Entiende qué son las medias móviles, cómo se calculan y cómo usarlas para identificar tendencias y señales de compra/venta.",
    "estimated_time": 8,
    "content": """# Medias Móviles

Las medias móviles son uno de los indicadores técnicos más utilizados. Suavizan el ruido del precio para revelar la **tendencia subyacente** de un activo.

## ¿Qué es una media móvil?

Una media móvil calcula el **precio promedio** de un activo durante un número determinado de periodos. A medida que avanza el tiempo, los datos más antiguos se descartan y se incluyen los nuevos — por eso se llama "móvil".

## Tipos principales

### Media Móvil Simple (SMA)
Calcula la media aritmética de los últimos N precios de cierre.

**Ejemplo**: SMA de 10 días = suma de los últimos 10 cierres ÷ 10.

- Ventaja: Fácil de calcular y entender.
- Desventaja: Da el mismo peso a todos los precios, los datos antiguos influyen igual que los recientes.

### Media Móvil Exponencial (EMA)
Da **más peso a los precios recientes**, por lo que reacciona más rápido a los cambios de precio.

- Ventaja: Más sensible a movimientos recientes.
- Desventaja: Puede generar más señales falsas por ser más reactiva.

## Periodos más usados

- **EMA 9 / SMA 10**: Muy corto plazo, para day trading.
- **SMA 20 / EMA 21**: Corto plazo, tendencia de las últimas 4 semanas.
- **SMA 50**: Medio plazo, referencia habitual para swing trading.
- **SMA 200**: Largo plazo, la más importante. Separa mercados alcistas de bajistas.

> Si el precio está por encima de la SMA 200 → tendencia alcista. Por debajo → tendencia bajista. Así de simple (y así de poderoso).

## Señales de las medias móviles

### El precio cruza la media
- **Precio cruza al alza la media**: Señal alcista (posible compra).
- **Precio cruza a la baja la media**: Señal bajista (posible venta).

### Cruce de medias (Golden Cross / Death Cross)
Cuando usas dos medias de diferente periodo:

- **Golden Cross** (Cruce Dorado): La media corta (ej. SMA 50) cruza al alza la media larga (ej. SMA 200). Es una señal alcista de largo plazo muy seguida por los inversores.
- **Death Cross** (Cruce de la Muerte): La media corta cruza a la baja la media larga. Señal bajista de largo plazo.

### Ejemplo histórico
En marzo de 2020, tras el crash por COVID, las principales bolsas formaron un Golden Cross en mayo-junio de 2020, anticipando uno de los rallies más fuertes de la historia.

## Medias móviles como soporte/resistencia dinámicos

Las medias móviles actúan como **soportes y resistencias que se mueven con el precio**:
- En tendencia alcista, el precio suele rebotar en la media móvil (actúa como soporte).
- En tendencia bajista, el precio suele encontrar resistencia en la media móvil.

## Limitaciones

- **Indicador retrasado**: Las medias móviles se basan en datos pasados, así que siempre van detrás del precio actual.
- **Mercados laterales**: En rangos sin tendencia clara, las medias generan muchas señales falsas.
- **No usar solas**: Siempre combina las medias móviles con otros indicadores y análisis del contexto general.
""",
    "quizzes": [
        {
            "question": "¿Qué diferencia principal tiene la EMA respecto a la SMA?",
            "explanation": "La Media Móvil Exponencial (EMA) da más peso a los precios más recientes, lo que la hace más sensible y reactiva a los cambios de precio. La SMA trata todos los precios por igual.",
            "options": [
                (
                    "La EMA solo usa precios de apertura, la SMA usa precios de cierre",
                    False,
                ),
                (
                    "La EMA da más peso a los precios recientes, reaccionando más rápido",
                    True,
                ),
                ("La EMA es más lenta que la SMA", False),
                ("No hay ninguna diferencia, son lo mismo", False),
            ],
        },
        {
            "question": "¿Qué es un 'Golden Cross' (Cruce Dorado)?",
            "explanation": "El Golden Cross ocurre cuando una media móvil de corto plazo (ej. SMA 50) cruza al alza una media de largo plazo (ej. SMA 200). Es una señal alcista muy seguida por inversores institucionales.",
            "options": [
                ("Cuando el precio alcanza su máximo histórico", False),
                ("Cuando la SMA 50 cruza a la baja la SMA 200", False),
                ("Cuando dos acciones diferentes tienen el mismo precio", False),
                (
                    "Cuando la media corta (ej. SMA 50) cruza al alza la media larga (ej. SMA 200)",
                    True,
                ),
            ],
        },
        {
            "question": "Si el precio de una acción está por encima de la SMA 200, ¿qué indica generalmente?",
            "explanation": "La SMA 200 es la referencia más importante para determinar la tendencia de largo plazo. Un precio por encima de la SMA 200 indica que la tendencia general es alcista.",
            "options": [
                ("Que la acción es cara y hay que vender", False),
                ("Que la tendencia de largo plazo es alcista", True),
                ("Que la acción va a bajar pronto", False),
                ("Que el volumen es alto", False),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# LESSON 4
# ---------------------------------------------------------------------------
LESSON_4 = {
    "title": "Patrones de Velas Japonesas",
    "description": "Aprende a reconocer los patrones de velas japonesas más comunes y su significado para anticipar movimientos del precio.",
    "estimated_time": 8,
    "content": """# Patrones de Velas Japonesas

Los patrones de velas japonesas fueron desarrollados en Japón en el siglo XVIII para el comercio de arroz. Hoy son una de las herramientas más poderosas del análisis técnico moderno. Cada vela cuenta una historia sobre la **batalla entre compradores y vendedores**.

## Patrones de una sola vela

### Doji
- El precio de apertura y cierre son prácticamente iguales.
- Indica **indecisión** en el mercado.
- Tras una tendencia prolongada, puede señalar un posible cambio de dirección.

### Martillo (Hammer)
- Cuerpo pequeño en la parte superior, mecha inferior larga (al menos 2x el cuerpo).
- Aparece en **tendencias bajistas**.
- Indica que los compradores rechazaron los precios bajos → posible **reversal alcista**.

### Estrella Fugaz (Shooting Star)
- Cuerpo pequeño en la parte inferior, mecha superior larga.
- Aparece en **tendencias alcistas**.
- Indica que los vendedores rechazaron los precios altos → posible **reversal bajista**.

### Marubozu
- Vela con cuerpo largo y sin mechas (o muy pequeñas).
- **Marubozu alcista** (verde): Gran fuerza compradora.
- **Marubozu bajista** (rojo): Gran fuerza vendedora.

## Patrones de dos velas

### Envolvente Alcista (Bullish Engulfing)
- Una vela roja pequeña seguida de una vela verde grande que "envuelve" completamente a la anterior.
- Señal de **reversal alcista** — los compradores han tomado el control.

### Envolvente Bajista (Bearish Engulfing)
- Una vela verde pequeña seguida de una vela roja grande que envuelve a la anterior.
- Señal de **reversal bajista** — los vendedores han tomado el control.

## Patrones de tres velas

### Estrella de la Mañana (Morning Star)
1. Vela roja grande (tendencia bajista).
2. Vela pequeña (doji o cuerpo diminuto) — indecisión.
3. Vela verde grande que cierra por encima del punto medio de la primera vela.

Es una de las señales alcistas más fiables.

### Estrella de la Tarde (Evening Star)
El patrón inverso:
1. Vela verde grande.
2. Vela pequeña — indecisión.
3. Vela roja grande.

Señal bajista muy fiable.

### Tres Soldados Blancos / Tres Cuervos Negros
- **Tres Soldados Blancos**: Tres velas verdes consecutivas, cada una cerrando más arriba. Fuerte señal alcista.
- **Tres Cuervos Negros**: Tres velas rojas consecutivas, cada una cerrando más abajo. Fuerte señal bajista.

## Reglas para usar patrones de velas

1. **El contexto importa**: Un martillo solo es relevante tras una tendencia bajista. En medio de un rango lateral, pierde valor.
2. **Busca confirmación**: No actúes solo por un patrón. Espera a que la siguiente vela confirme la señal.
3. **Combina con otros indicadores**: Los patrones son más fiables cuando coinciden con niveles de soporte/resistencia, medias móviles o divergencias de volumen.
4. **La temporalidad importa**: Un patrón en gráfico diario o semanal es mucho más fiable que en un gráfico de 5 minutos.

> Los patrones de velas no son predicciones — son pistas sobre la psicología del mercado que aumentan las probabilidades a tu favor.
""",
    "quizzes": [
        {
            "question": "¿Qué indica un patrón de vela 'Martillo' (Hammer) cuando aparece tras una tendencia bajista?",
            "explanation": "El Martillo muestra que durante el periodo los vendedores llevaron el precio muy abajo (mecha larga inferior), pero los compradores reaccionaron con fuerza y cerraron cerca del máximo. Tras una tendencia bajista, sugiere un posible cambio a tendencia alcista.",
            "options": [
                ("Que la tendencia bajista va a acelerarse", False),
                ("Que el mercado está cerrado", False),
                ("Un posible cambio a tendencia alcista (reversal alcista)", True),
                ("Que hay que vender inmediatamente", False),
            ],
        },
        {
            "question": "¿Qué es un patrón 'Envolvente Alcista' (Bullish Engulfing)?",
            "explanation": "El patrón Envolvente Alcista consiste en una vela roja pequeña seguida de una vela verde grande cuyo cuerpo envuelve completamente al de la vela anterior. Indica que los compradores han tomado el control con fuerza.",
            "options": [
                ("Tres velas verdes consecutivas", False),
                ("Una vela verde pequeña seguida de una roja grande", False),
                (
                    "Una vela roja pequeña seguida de una vela verde grande que la envuelve completamente",
                    True,
                ),
                ("Una vela sin cuerpo ni mechas", False),
            ],
        },
        {
            "question": "¿Cuál de estas reglas es correcta al usar patrones de velas?",
            "explanation": "Los patrones de velas son más fiables cuando coinciden con otros indicadores (soporte/resistencia, medias móviles, volumen). Un patrón aislado puede ser engañoso; la confluencia de señales aumenta la probabilidad de acierto.",
            "options": [
                ("Siempre comprar inmediatamente al ver un martillo", False),
                ("Los patrones en gráfico de 1 minuto son los más fiables", False),
                ("El contexto no importa, solo el patrón", False),
                (
                    "Combinar los patrones con otros indicadores como soporte/resistencia y volumen",
                    True,
                ),
            ],
        },
    ],
}

ALL_LESSONS = [LESSON_1, LESSON_2, LESSON_3, LESSON_4]


class Command(BaseCommand):
    help = "Seed Module 4 'Análisis Técnico' — 4 full lessons with 12 quizzes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing module before seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted = Module.objects.filter(title=MODULE_DATA["title"]).delete()
            if deleted[0]:
                self.stdout.write(
                    self.style.WARNING(
                        f"Deleted existing module ({deleted[0]} objects)."
                    )
                )

        if Module.objects.filter(title=MODULE_DATA["title"]).exists():
            self.stdout.write(
                self.style.WARNING("Module already exists. Use --clear to replace it.")
            )
            return

        module = Module.objects.create(**MODULE_DATA)
        self.stdout.write(self.style.SUCCESS(f"Created module: {module.title}"))

        total_quizzes = 0
        for order, lesson_data in enumerate(ALL_LESSONS):
            lesson = Lesson.objects.create(
                module=module,
                title=lesson_data["title"],
                description=lesson_data["description"],
                content=lesson_data["content"].strip(),
                order=order,
                xp_reward=50,
                estimated_time=lesson_data["estimated_time"],
            )
            self.stdout.write(f"  Lesson {order + 1}: {lesson.title}")

            for q_order, q_data in enumerate(lesson_data["quizzes"]):
                quiz = Quiz.objects.create(
                    lesson=lesson,
                    question=q_data["question"],
                    explanation=q_data["explanation"],
                    order=q_order,
                    xp_reward=10,
                )
                for opt_order, (text, is_correct) in enumerate(q_data["options"]):
                    QuizOption.objects.create(
                        quiz=quiz, text=text, is_correct=is_correct, order=opt_order
                    )
                total_quizzes += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone: {len(ALL_LESSONS)} lessons, {total_quizzes} quizzes."
            )
        )
