"""
Management command to seed Module 2: "Fundamentos del Mercado de Valores"
6 full lessons with rich content and 3 quizzes each (18 quizzes total).
"""

from django.core.management.base import BaseCommand

from apps.lessons.models import Lesson, Module, Quiz, QuizOption

MODULE_DATA = {
    "title": "Fundamentos del Mercado de Valores",
    "description": (
        "Comprende cómo funciona el mercado de valores, desde los índices bursátiles "
        "hasta la mecánica del trading. Conocimiento esencial para cualquier inversor."
    ),
    "icon": "📊",
    "color": "#10b981",
    "difficulty": "beginner",
    "order": 1,
    "xp_reward": 600,
}

# ---------------------------------------------------------------------------
LESSON_1 = {
    "title": "Cómo Funcionan los Mercados",
    "description": "Entiende la estructura básica de los mercados financieros y el papel de la oferta y la demanda.",
    "estimated_time": 6,
    "content": """# Cómo Funcionan los Mercados

Un mercado financiero es, en esencia, un lugar donde compradores y vendedores se encuentran para intercambiar activos. Aunque hoy casi todo es electrónico, los principios son los mismos que en un mercado callejero.

## La Bolsa de Valores

La bolsa de valores es un mercado organizado donde se compran y venden acciones de empresas que cotizan públicamente. Las bolsas más importantes del mundo son:

- **NYSE** (New York Stock Exchange): La más grande por capitalización.
- **NASDAQ**: Enfocada en empresas tecnológicas (Apple, Google, Amazon).
- **Bolsa de Madrid**: Principal mercado de valores de España.
- **London Stock Exchange**, **Tokyo Stock Exchange**, **Shanghai Stock Exchange**...

Cuando una empresa quiere que sus acciones se negocien en bolsa, realiza una **OPV (Oferta Pública de Venta)** o **IPO** en inglés. A partir de ese momento, cualquier persona puede comprar y vender sus acciones.

## Oferta y Demanda

El precio de una acción lo determina la **oferta y la demanda**:

- Si muchos inversores quieren comprar una acción (alta demanda) y pocos quieren vender (baja oferta), el precio sube.
- Si muchos quieren vender (alta oferta) y pocos quieren comprar (baja demanda), el precio baja.

> El precio de una acción en cada momento refleja lo que los compradores están dispuestos a pagar y los vendedores a aceptar.

## Participantes del Mercado

- **Inversores minoristas**: Personas individuales como tú que invierten su propio dinero.
- **Inversores institucionales**: Fondos de pensiones, fondos de inversión, bancos y aseguradoras. Mueven grandes volúmenes.
- **Market makers**: Intermediarios que garantizan que siempre haya liquidez (alguien dispuesto a comprar o vender).
- **Reguladores**: Organismos como la CNMV (España) o la SEC (EE.UU.) que supervisan el mercado para proteger a los inversores.

## Mercado Primario vs. Secundario

- **Mercado primario**: Donde las empresas emiten acciones o bonos por primera vez (IPO). El dinero va directamente a la empresa.
- **Mercado secundario**: Donde los inversores compran y venden entre sí acciones ya emitidas. Es lo que la mayoría llama "la bolsa".
""",
    "quizzes": [
        {
            "question": "¿Qué determina el precio de una acción en la bolsa?",
            "explanation": "El precio de una acción se establece por la interacción entre oferta (vendedores) y demanda (compradores). Cuando más gente quiere comprar que vender, el precio sube, y viceversa.",
            "options": [
                ("Lo decide el gobierno cada semana", False),
                ("La oferta y la demanda entre compradores y vendedores", True),
                ("El director de la empresa fija el precio cada día", False),
                ("Es siempre el mismo que en la IPO", False),
            ],
        },
        {
            "question": "¿Cuál es la diferencia entre mercado primario y secundario?",
            "explanation": "En el mercado primario la empresa emite nuevas acciones (IPO) y recibe el dinero. En el secundario, los inversores negocian entre sí acciones ya existentes.",
            "options": [
                ("No hay ninguna diferencia", False),
                ("El primario es para bonos y el secundario para acciones", False),
                (
                    "En el primario se emiten nuevas acciones; en el secundario se negocian entre inversores",
                    True,
                ),
                ("El primario es más arriesgado porque no está regulado", False),
            ],
        },
        {
            "question": "¿Qué es una OPV (IPO)?",
            "explanation": "Una OPV (Oferta Pública de Venta) o IPO (Initial Public Offering) es el proceso por el cual una empresa pone sus acciones a disposición del público por primera vez, comenzando a cotizar en bolsa.",
            "options": [
                ("Una penalización por vender acciones demasiado rápido", False),
                ("Un tipo de bono del gobierno", False),
                ("Un fondo de inversión especial", False),
                (
                    "El proceso por el cual una empresa sale a cotizar en bolsa por primera vez",
                    True,
                ),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
LESSON_2 = {
    "title": "Leyendo Cotizaciones",
    "description": "Aprende a interpretar la información de cotización de una acción: precio, volumen, variación y más.",
    "estimated_time": 6,
    "content": """# Leyendo Cotizaciones de Acciones

Cuando abres cualquier plataforma financiera, verás una tabla llena de números y abreviaturas. Puede parecer abrumador al principio, pero en realidad la información es bastante sencilla. Vamos a desglosarla.

## Datos Básicos de una Cotización

### Símbolo (Ticker)
Cada empresa cotizada tiene un código único:
- **AAPL** = Apple
- **MSFT** = Microsoft
- **SAN** = Banco Santander

### Precio Actual
El último precio al que se ha negociado la acción. Cambia constantemente durante el horario de mercado.

### Variación Diaria
Cuánto ha cambiado el precio respecto al cierre del día anterior, expresado en valor absoluto y en porcentaje:
- **+2,35 (+1,50%)** → La acción ha subido 2,35 € (un 1,50%) hoy.
- **-1,20 (-0,80%)** → Ha bajado 1,20 € (un 0,80%) hoy.

### Volumen
El número de acciones negociadas durante el día. Un volumen alto indica mucho interés en esa acción.

## Datos Avanzados

- **Apertura**: El precio al que comenzó a cotizar hoy.
- **Máximo / Mínimo del día**: El precio más alto y más bajo alcanzado hoy.
- **Máximo / Mínimo de 52 semanas**: El rango de precios del último año. Útil para ver si la acción está cerca de sus máximos o mínimos históricos recientes.
- **Capitalización bursátil (Market Cap)**: Precio de la acción × número total de acciones. Indica el tamaño de la empresa en bolsa.

> Una empresa con una capitalización de 2.000 millones de euros se considera de mediana capitalización. Por encima de 10.000 millones es gran capitalización (large-cap).

## P/E Ratio (PER)

El **Price-to-Earnings Ratio** o PER es uno de los indicadores más utilizados:

**PER = Precio de la acción ÷ Beneficio por acción**

- Un PER de 15 significa que estás pagando 15 € por cada 1 € de beneficio que genera la empresa.
- Un PER alto puede indicar que el mercado espera un gran crecimiento futuro.
- Un PER bajo puede indicar que la acción está infravalorada... o que la empresa tiene problemas.

## Dividend Yield

Si la empresa paga dividendos, el **dividend yield** indica qué porcentaje del precio de la acción se reparte en dividendos anuales:

**Dividend Yield = (Dividendo anual por acción ÷ Precio de la acción) × 100**

Un yield del 4% significa que por cada 100 € invertidos recibes 4 € anuales en dividendos.
""",
    "quizzes": [
        {
            "question": "Si una acción muestra '-3,50 (-2,10%)', ¿qué significa?",
            "explanation": "La variación muestra el cambio respecto al cierre del día anterior. En este caso, la acción ha bajado 3,50 € en valor absoluto, lo que representa un descenso del 2,10%.",
            "options": [
                ("La acción ha subido un 2,10% hoy", False),
                (
                    "La acción ha bajado 3,50 € respecto al cierre de ayer (un 2,10%)",
                    True,
                ),
                ("La empresa ha perdido el 2,10% de sus empleados", False),
                ("Se han vendido 3,50 millones de acciones", False),
            ],
        },
        {
            "question": "¿Qué indica un PER (P/E Ratio) de 20?",
            "explanation": "Un PER de 20 significa que el precio de la acción es 20 veces el beneficio por acción. En otras palabras, estás pagando 20 € por cada 1 € de beneficio anual que genera la empresa.",
            "options": [
                ("La empresa tiene 20 empleados", False),
                ("La acción ha subido un 20% este año", False),
                ("La acción lleva 20 años cotizando en bolsa", False),
                ("El precio es 20 veces el beneficio por acción", True),
            ],
        },
        {
            "question": "¿Qué es la capitalización bursátil de una empresa?",
            "explanation": "La capitalización bursátil se calcula multiplicando el precio actual de la acción por el número total de acciones en circulación. Indica el valor total de la empresa en el mercado.",
            "options": [
                (
                    "El precio de la acción × el número total de acciones en circulación",
                    True,
                ),
                ("El beneficio total de la empresa en el último año", False),
                ("El número de inversores que tienen acciones de la empresa", False),
                ("El dinero que la empresa tiene en el banco", False),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
LESSON_3 = {
    "title": "Órdenes de Mercado vs. Límite",
    "description": "Aprende los diferentes tipos de órdenes que puedes usar para comprar y vender acciones.",
    "estimated_time": 5,
    "content": """# Órdenes de Mercado vs. Límite

Cuando decides comprar o vender una acción, no basta con decir "quiero comprar Apple". Necesitas especificar **cómo** quieres ejecutar la operación. Para eso existen diferentes tipos de órdenes.

## Orden de Mercado (Market Order)

Es la más sencilla: compras o vendes **inmediatamente al mejor precio disponible**.

- **Ventaja**: Ejecución garantizada e instantánea.
- **Desventaja**: No controlas el precio exacto. En acciones poco líquidas, el precio podría ser peor de lo esperado.

Ideal para: acciones muy líquidas (alto volumen) donde la diferencia entre el precio que ves y el que obtienes es mínima.

## Orden Límite (Limit Order)

Especificas el **precio máximo** que estás dispuesto a pagar (compra) o el **precio mínimo** que aceptas (venta).

- **Orden límite de compra**: "Quiero comprar Apple, pero solo si baja a 170 € o menos."
- **Orden límite de venta**: "Quiero vender mis acciones de Tesla, pero solo si suben a 300 € o más."

- **Ventaja**: Controlas el precio.
- **Desventaja**: La orden podría no ejecutarse nunca si el precio no alcanza tu límite.

## Stop Loss

Una orden de **stop loss** se activa automáticamente si el precio baja hasta un nivel que tú determinas. Sirve para **limitar pérdidas**.

Ejemplo: Compraste una acción a 100 € y pones un stop loss a 90 €. Si el precio baja a 90 €, se vende automáticamente, limitando tu pérdida al 10%.

> El stop loss es una herramienta esencial de gestión del riesgo. Muchos inversores profesionales los usan en todas sus posiciones.

## Take Profit

Es lo contrario del stop loss: una orden que se activa cuando el precio **sube** hasta un nivel objetivo, asegurando tus ganancias.

Ejemplo: Compraste a 100 € y pones un take profit a 120 €. Si llega a 120 €, se vende automáticamente con un 20% de ganancia.

## ¿Cuál Usar?

- **Principiantes**: Órdenes de mercado para empezar; son simples y directas.
- **Inversores activos**: Órdenes límite para controlar mejor el precio de entrada y salida.
- **Siempre recomendable**: Usar stop loss para proteger tu capital de caídas inesperadas.
""",
    "quizzes": [
        {
            "question": "¿Qué tipo de orden garantiza la ejecución inmediata al mejor precio disponible?",
            "explanation": "La orden de mercado (market order) se ejecuta inmediatamente al mejor precio disponible. Es la más simple, pero no te permite elegir el precio exacto.",
            "options": [
                ("Orden límite", False),
                ("Stop loss", False),
                ("Orden de mercado", True),
                ("Take profit", False),
            ],
        },
        {
            "question": "Compraste una acción a 50 € y pones un stop loss a 45 €. ¿Qué ocurre si el precio baja a 44 €?",
            "explanation": "El stop loss se activa cuando el precio alcanza los 45 €, vendiendo automáticamente la acción para limitar tu pérdida al 10%. La venta se ejecuta en torno a 45 €, antes de que llegue a 44 €.",
            "options": [
                ("No pasa nada, el stop loss solo funciona si subes el precio", False),
                (
                    "La acción se vende automáticamente en torno a 45 € para limitar la pérdida",
                    True,
                ),
                ("Se compran más acciones automáticamente", False),
                ("La bolsa cierra y no puedes vender", False),
            ],
        },
        {
            "question": "Quieres comprar acciones de Microsoft, pero solo si bajan a 350 €. ¿Qué orden usarías?",
            "explanation": "Una orden límite de compra te permite especificar el precio máximo que estás dispuesto a pagar. La orden solo se ejecutará si el precio de Microsoft baja a 350 € o menos.",
            "options": [
                ("Orden de mercado", False),
                ("Stop loss a 350 €", False),
                ("Take profit a 350 €", False),
                ("Orden límite de compra a 350 €", True),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
LESSON_4 = {
    "title": "Entendiendo los Índices",
    "description": "Descubre qué son los índices bursátiles (S&P 500, IBEX 35...) y por qué son tan importantes.",
    "estimated_time": 5,
    "content": """# Entendiendo los Índices Bursátiles

Cuando escuchas en las noticias "el IBEX 35 ha subido un 1,2% hoy", ¿sabes realmente qué significa? Los índices bursátiles son una de las herramientas más importantes para entender la salud del mercado.

## ¿Qué es un Índice?

Un índice bursátil es una **cesta de acciones** seleccionadas que representan un mercado o un sector. Su valor refleja el comportamiento conjunto de todas las acciones que lo componen.

Piensa en él como un termómetro: no mide cada acción individual, pero te da una lectura general de cómo va el mercado.

## Los Índices más Importantes

### S&P 500 (Estados Unidos)
- **500 empresas** más grandes de EE.UU.
- Considerado el mejor indicador de la salud de la economía estadounidense.
- Incluye Apple, Microsoft, Amazon, Google, etc.

### IBEX 35 (España)
- **35 empresas** más líquidas de la Bolsa de Madrid.
- Incluye Santander, Inditex, Iberdrola, Telefónica, etc.

### Otros índices clave
- **Dow Jones Industrial Average**: 30 grandes empresas de EE.UU. Uno de los más antiguos.
- **NASDAQ Composite**: Enfocado en tecnología.
- **EURO STOXX 50**: 50 grandes empresas de la eurozona.
- **MSCI World**: Más de 1.500 empresas de 23 países desarrollados. Muy usado en ETFs globales.

## ¿Cómo se Calcula un Índice?

Hay dos métodos principales:

- **Ponderado por capitalización**: Las empresas más grandes tienen más peso. Si Apple representa el 7% del S&P 500, un movimiento de Apple afecta más al índice que un movimiento de una empresa pequeña. Este es el método más común.
- **Ponderado por precio**: Las empresas con acciones más caras tienen más peso, independientemente del tamaño de la empresa. Así funciona el Dow Jones.

## ¿Por Qué son Importantes?

- **Referencia de rendimiento (benchmark)**: Si tu cartera subió un 8% pero el S&P 500 subió un 12%, lo hiciste peor que el mercado.
- **Invertir en el índice**: Los ETFs indexados replican un índice. Comprar un ETF del S&P 500 es como comprar una pequeña parte de las 500 empresas de una vez.
- **Indicador económico**: Los índices reflejan las expectativas de los inversores sobre la economía.
""",
    "quizzes": [
        {
            "question": "¿Cuántas empresas componen el S&P 500?",
            "explanation": "El S&P 500 incluye las 500 empresas más grandes de Estados Unidos por capitalización bursátil. Es el índice de referencia más seguido del mundo.",
            "options": [
                ("50 empresas", False),
                ("500 empresas", True),
                ("35 empresas", False),
                ("100 empresas", False),
            ],
        },
        {
            "question": "En un índice ponderado por capitalización, ¿qué empresas tienen más influencia?",
            "explanation": "En un índice ponderado por capitalización, las empresas con mayor capitalización bursátil (precio × acciones) tienen más peso. Por eso un movimiento de Apple afecta más al S&P 500 que una empresa pequeña.",
            "options": [
                ("Las que tienen las acciones más baratas", False),
                ("Todas las empresas tienen el mismo peso", False),
                ("Las que reparten más dividendos", False),
                ("Las de mayor capitalización bursátil (las más grandes)", True),
            ],
        },
        {
            "question": "Si tu cartera subió un 5% y el IBEX 35 subió un 8%, ¿cómo interpretarías tu rendimiento?",
            "explanation": "Los índices sirven como benchmark (referencia). Si tu cartera subió menos que el índice de referencia, tu rendimiento fue inferior al del mercado general, aunque seguiste ganando dinero.",
            "options": [
                ("Excelente, porque ganaste dinero", False),
                (
                    "Tu rendimiento fue inferior al del mercado (no batiste al índice)",
                    True,
                ),
                (
                    "No tiene relación, los índices no se pueden comparar con carteras personales",
                    False,
                ),
                ("Deberías vender todo inmediatamente", False),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
LESSON_5 = {
    "title": "Mercados Alcistas y Bajistas",
    "description": "Aprende a identificar las fases del mercado y cómo actuar en cada una.",
    "estimated_time": 6,
    "content": """# Mercados Alcistas y Bajistas

Los mercados financieros se mueven en ciclos. Hay períodos de subidas prolongadas y períodos de bajadas. Entender estas fases te ayuda a mantener la calma y tomar mejores decisiones.

## Mercado Alcista (Bull Market)

Un **mercado alcista** se define técnicamente como una subida del 20% o más desde un mínimo reciente, sostenida en el tiempo. Se caracteriza por:

- Optimismo generalizado entre los inversores.
- Crecimiento económico y buenos resultados empresariales.
- Alta participación de inversores minoristas (la gente "quiere entrar").
- Los precios suben de forma sostenida durante meses o años.

El mercado alcista más largo de la historia (en EE.UU.) duró desde marzo de 2009 hasta febrero de 2020 — casi 11 años.

## Mercado Bajista (Bear Market)

Un **mercado bajista** se define como una caída del 20% o más desde un máximo reciente. Se caracteriza por:

- Pesimismo y miedo entre los inversores.
- Ralentización económica o recesión.
- Los inversores venden en pánico, lo que empuja los precios aún más abajo.
- Puede durar meses o incluso años, aunque históricamente son más cortos que los alcistas.

## Correcciones

Una **corrección** es una caída de entre el 10% y el 20%. Son más frecuentes que los mercados bajistas y se consideran parte normal del funcionamiento del mercado.

> Dato: El S&P 500 ha tenido una corrección del 10% o más, en promedio, una vez al año. Son completamente normales.

## ¿Cómo Actuar en Cada Fase?

### En mercado alcista
- No te dejes llevar por la euforia. No inviertas más de lo que puedes permitirte.
- Mantén tu estrategia. No cambies tu asignación de activos solo porque todo sube.
- Es buen momento para revisar tu portafolio y rebalancear si algún activo ha crecido mucho.

### En mercado bajista
- **No vendas en pánico**. Históricamente, los mercados siempre se han recuperado.
- Si tienes un horizonte largo, las bajadas son oportunidades de compra (todo está "en rebajas").
- Revisa tu fondo de emergencia para asegurarte de que no necesitarás el dinero invertido.

### La lección más importante

**El tiempo en el mercado supera al timing del mercado.** Intentar entrar y salir en el momento perfecto es casi imposible. Los mejores días de bolsa suelen ocurrir justo después de los peores, y perderte esos días reduce drásticamente tus rendimientos a largo plazo.
""",
    "quizzes": [
        {
            "question": "¿Qué porcentaje de caída define técnicamente un mercado bajista (bear market)?",
            "explanation": "Un mercado bajista se define como una caída del 20% o más desde el máximo reciente. Una caída entre el 10% y el 20% se considera una corrección.",
            "options": [
                ("5% o más", False),
                ("10% o más", False),
                ("20% o más", True),
                ("50% o más", False),
            ],
        },
        {
            "question": "¿Cuál es la mejor estrategia cuando el mercado baja un 30% y tienes un horizonte de inversión de 20 años?",
            "explanation": "Con un horizonte de 20 años, históricamente los mercados siempre se han recuperado de las caídas. Vender en pánico cristaliza las pérdidas. Mantener la inversión (o incluso comprar más) ha sido la estrategia más rentable a largo plazo.",
            "options": [
                ("Vender todo inmediatamente para evitar más pérdidas", False),
                ("Invertir todo en oro", False),
                (
                    "Mantener la calma y no vender — con 20 años el mercado se recuperará",
                    True,
                ),
                ("Dejar de invertir para siempre", False),
            ],
        },
        {
            "question": "¿Qué significa la frase 'el tiempo en el mercado supera al timing del mercado'?",
            "explanation": "Estudios demuestran que estar invertido de forma constante genera mejores rendimientos que intentar predecir las subidas y bajadas. Los mejores días de bolsa suelen ocurrir justo después de los peores.",
            "options": [
                ("Que solo debes invertir unos minutos al día", False),
                ("Que debes comprar y vender cada hora", False),
                ("Que cuanto más rápido operes, más ganarás", False),
                (
                    "Que estar invertido de forma constante es mejor que intentar entrar y salir en el momento perfecto",
                    True,
                ),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
LESSON_6 = {
    "title": "Horarios de Trading",
    "description": "Conoce los horarios de los principales mercados y cómo afectan a la operativa.",
    "estimated_time": 5,
    "content": """# Horarios de Trading

A diferencia de una tienda online, los mercados de valores no están abiertos las 24 horas. Cada bolsa tiene sus propios horarios, y es importante conocerlos para operar correctamente.

## Horarios de las Principales Bolsas

### Bolsa de Madrid (BME)
- **Apertura**: 9:00 (hora española)
- **Cierre**: 17:30
- **Subasta de apertura**: 8:30 - 9:00 (se calculan los precios de apertura)
- **Subasta de cierre**: 17:30 - 17:35

### Wall Street (NYSE / NASDAQ)
- **Apertura**: 15:30 (hora española) / 9:30 (hora de Nueva York)
- **Cierre**: 22:00 (hora española) / 16:00 (hora de Nueva York)
- **Pre-market**: 10:00 - 15:30 (hora española)
- **After-hours**: 22:00 - 2:00 (hora española)

### Bolsa de Tokio
- **Apertura**: 1:00 (hora española)
- **Cierre**: 7:00 (hora española)

## Pre-Market y After-Hours

Fuera del horario regular, algunos brokers permiten operar en sesiones extendidas:

- **Pre-market**: Antes de la apertura oficial. Menos volumen, más volatilidad.
- **After-hours**: Después del cierre. Se negocian acciones basándose en noticias publicadas tras el cierre.

> Las operaciones fuera de horario suelen tener menos liquidez y spreads más amplios. Se recomienda precaución para principiantes.

## ¿Qué es el Spread?

El **spread** es la diferencia entre el precio de compra (ask) y el de venta (bid):

- **Bid**: El precio más alto que un comprador está dispuesto a pagar.
- **Ask**: El precio más bajo que un vendedor está dispuesto a aceptar.
- **Spread = Ask - Bid**

Un spread estrecho (ej: 0,01 €) indica alta liquidez. Un spread amplio (ej: 0,50 €) indica poca liquidez.

## Días de Cierre

Las bolsas cierran en:
- **Fines de semana**: Sábado y domingo.
- **Festivos**: Cada país tiene sus propios festivos bursátiles (Navidad, Año Nuevo, festivos nacionales...).

## Solapamiento de Mercados

Cuando dos grandes mercados están abiertos al mismo tiempo, hay más volumen y liquidez. El solapamiento más importante es entre Europa y EE.UU. (de 15:30 a 17:30 hora española), que suele ser el período más activo del día.

## Consejo para Principiantes

- Opera durante el **horario regular** del mercado, cuando hay más liquidez.
- Evita las operaciones en los primeros 15-30 minutos tras la apertura, ya que la volatilidad suele ser alta.
- Si inviertes a largo plazo con aportaciones mensuales, el horario exacto importa muy poco.
""",
    "quizzes": [
        {
            "question": "¿A qué hora (española) abre la Bolsa de Nueva York (Wall Street)?",
            "explanation": "Wall Street abre a las 9:30 hora de Nueva York, que corresponden a las 15:30 hora española (peninsular). Es uno de los datos que todo inversor debe conocer.",
            "options": [
                ("9:00 hora española", False),
                ("15:30 hora española", True),
                ("12:00 hora española", False),
                ("22:00 hora española", False),
            ],
        },
        {
            "question": "¿Qué indica un spread amplio en una acción?",
            "explanation": "El spread es la diferencia entre precio de compra y de venta. Un spread amplio indica poca liquidez: hay pocos compradores y vendedores, lo que puede hacer que pagues más o recibas menos.",
            "options": [
                ("Que la acción es muy popular y líquida", False),
                ("Que la empresa tiene muchos beneficios", False),
                ("Que hay poca liquidez y operar puede ser más costoso", True),
                ("Que la bolsa va a cerrar pronto", False),
            ],
        },
        {
            "question": "¿Cuál es el período más activo del día en los mercados europeos?",
            "explanation": "El solapamiento entre la bolsa europea y Wall Street (de 15:30 a 17:30 hora española) concentra el mayor volumen de operaciones del día, ya que ambos grandes mercados están abiertos simultáneamente.",
            "options": [
                ("A primera hora de la mañana (9:00-10:00)", False),
                ("A medianoche", False),
                ("Los fines de semana", False),
                ("El solapamiento con Wall Street (15:30 - 17:30 hora española)", True),
            ],
        },
    ],
}


ALL_LESSONS = [LESSON_1, LESSON_2, LESSON_3, LESSON_4, LESSON_5, LESSON_6]


class Command(BaseCommand):
    help = "Seed Module 2 'Fundamentos del Mercado de Valores' — 6 full lessons with 18 quizzes."

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
