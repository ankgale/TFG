"""
Management command to seed Module 1: "Introducción a la Inversión"
5 full lessons with rich content and 3 quizzes each (15 quizzes total).
Correct-answer positions are distributed across A/B/C/D.
"""

from django.core.management.base import BaseCommand

from apps.lessons.models import Lesson, Module, Quiz, QuizOption

MODULE_DATA = {
    "title": "Introducción a la Inversión",
    "description": (
        "Aprende los fundamentos de la inversión, incluyendo acciones, bonos y fondos mutuos. "
        "Perfecto para principiantes que comienzan su camino financiero."
    ),
    "icon": "📈",
    "color": "#6366f1",
    "difficulty": "beginner",
    "order": 0,
    "xp_reward": 500,
}

# ---------------------------------------------------------------------------
# LESSON 1
# ---------------------------------------------------------------------------
LESSON_1 = {
    "title": "¿Qué es Invertir?",
    "description": "Aprende los conceptos fundamentales de la inversión y por qué es importante para tu futuro financiero.",
    "estimated_time": 6,
    "content": """# ¿Qué es Invertir?

Invertir es el acto de asignar dinero o recursos con la expectativa de generar ingresos o ganancias a lo largo del tiempo. A diferencia del ahorro, donde simplemente guardas dinero en una cuenta bancaria, invertir pone tu dinero a trabajar en activos que pueden crecer de valor.

## ¿Por qué Invertir?

1. **Superar la Inflación**: Cada año, la inflación reduce el poder adquisitivo de tu dinero. Si dejas 10.000 € en una cuenta que no genera intereses, en 10 años valdrá significativamente menos en términos reales. Invertir te ayuda a proteger y hacer crecer tu patrimonio.

2. **El Poder del Interés Compuesto**: Albert Einstein supuestamente llamó al interés compuesto "la octava maravilla del mundo". Cuando reinviertes tus ganancias, estas generan más ganancias. Una inversión de 5.000 € con un rendimiento del 8% anual se convierte en más de 23.000 € en 20 años — sin añadir un solo euro más.

3. **Alcanzar Metas Financieras**: Ya sea la jubilación, comprar una vivienda, financiar la educación de tus hijos o simplemente tener libertad financiera, invertir es el vehículo más eficaz para alcanzar objetivos a medio y largo plazo.

## Ahorro vs. Inversión

Es importante entender la diferencia:

- **Ahorrar** significa apartar dinero en un lugar seguro (cuenta de ahorro, depósito). El riesgo es muy bajo, pero la rentabilidad también es mínima.
- **Invertir** significa comprar activos (acciones, bonos, fondos) que pueden crecer de valor. Existe riesgo de pérdida, pero el potencial de ganancia es mucho mayor.

> Regla práctica: primero construye un fondo de emergencia (3-6 meses de gastos) en ahorro, y después comienza a invertir el excedente.

## Conceptos Clave

### Riesgo y Rentabilidad
Generalmente, mayores rendimientos potenciales vienen acompañados de mayor riesgo. Un depósito bancario es seguro pero rinde poco; las acciones pueden subir mucho pero también bajar. Entender tu tolerancia al riesgo es el primer paso.

### Diversificación
No pongas todos los huevos en la misma cesta. Distribuir las inversiones entre diferentes tipos de activos, sectores y regiones geográficas reduce el impacto de que una sola inversión vaya mal.

### Horizonte Temporal
Cuanto más tiempo puedas dejar tu dinero invertido, más tiempo tendrá para crecer y recuperarse de las fluctuaciones del mercado. Un joven de 25 años puede asumir más riesgo que alguien que se jubila en 5 años.
""",
    "quizzes": [
        {
            "question": "¿Cuál es la principal diferencia entre ahorrar e invertir?",
            "explanation": "Ahorrar significa guardar dinero en cuentas seguras con baja rentabilidad. Invertir implica comprar activos que pueden crecer de valor, asumiendo cierto riesgo a cambio de mayor potencial de ganancia.",
            "options": [
                (
                    "Invertir pone tu dinero a trabajar en activos que pueden crecer, mientras que ahorrar solo lo guarda",
                    True,
                ),
                ("Ahorrar genera más dinero que invertir a largo plazo", False),
                ("No existe ninguna diferencia real entre ambos conceptos", False),
                ("Ahorrar es más arriesgado que invertir en acciones", False),
            ],
        },
        {
            "question": "Si inviertes 5.000 € al 8% anual durante 20 años sin añadir más dinero, ¿aproximadamente cuánto tendrás?",
            "explanation": "Gracias al interés compuesto, 5.000 € al 8% anual se convierten en más de 23.000 € en 20 años. Las ganancias generan más ganancias cada año.",
            "options": [
                ("Exactamente 13.000 € (5.000 + 8.000 de intereses)", False),
                ("Unos 8.000 €", False),
                ("Más de 23.000 €", True),
                ("5.000 € — el dinero no crece si no añades más", False),
            ],
        },
        {
            "question": "¿Qué deberías hacer ANTES de empezar a invertir?",
            "explanation": "Los expertos recomiendan tener un fondo de emergencia de 3-6 meses de gastos antes de invertir, para no tener que vender inversiones en un mal momento por una necesidad urgente.",
            "options": [
                ("Pedir un préstamo para invertir más", False),
                ("Invertir todo tu sueldo inmediatamente", False),
                ("Esperar a tener 100.000 € ahorrados", False),
                ("Construir un fondo de emergencia de 3-6 meses de gastos", True),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# LESSON 2
# ---------------------------------------------------------------------------
LESSON_2 = {
    "title": "Tipos de Inversiones",
    "description": "Conoce los principales tipos de activos: acciones, bonos, fondos de inversión, ETFs y bienes raíces.",
    "estimated_time": 7,
    "content": """# Tipos de Inversiones

Existen muchas formas de invertir tu dinero. Cada tipo de activo tiene características diferentes en cuanto a riesgo, rentabilidad y liquidez. Vamos a explorar los más importantes.

## Acciones (Renta Variable)

Cuando compras una acción, adquieres una pequeña parte de una empresa. Si la empresa crece y tiene beneficios, el valor de tu acción sube y puedes ganar dinero de dos formas:

- **Plusvalía**: Vendes la acción a un precio mayor del que la compraste.
- **Dividendos**: Algunas empresas reparten parte de sus beneficios a los accionistas periódicamente.

Las acciones son uno de los activos con mayor potencial de rentabilidad a largo plazo, pero también con mayor volatilidad a corto plazo.

## Bonos (Renta Fija)

Un bono es esencialmente un préstamo que le haces a un gobierno o empresa. A cambio, te pagan intereses periódicos (llamados **cupón**) y te devuelven el capital al vencimiento.

- **Bonos del Estado**: Emitidos por gobiernos. Generalmente más seguros.
- **Bonos corporativos**: Emitidos por empresas. Mayor riesgo, pero mayor rentabilidad.

> Los bonos suelen ser más estables que las acciones, pero ofrecen menor rentabilidad a largo plazo.

## Fondos de Inversión

Un fondo de inversión reúne el dinero de muchos inversores y lo invierte en una cartera diversificada de activos. Un gestor profesional se encarga de tomar las decisiones de inversión.

- **Ventaja principal**: Diversificación automática, incluso con poco dinero.
- **Desventaja**: Comisiones de gestión que reducen la rentabilidad.

## ETFs (Fondos Cotizados)

Los ETFs funcionan como fondos de inversión, pero se compran y venden en bolsa como si fueran acciones. La mayoría son de **gestión pasiva**: simplemente replican un índice (como el IBEX 35 o el S&P 500).

- **Comisiones muy bajas** comparadas con fondos de gestión activa.
- **Transparencia**: Sabes exactamente en qué estás invertido.
- **Liquidez**: Puedes comprar y vender en cualquier momento del día.

## Bienes Raíces

Invertir en inmuebles (pisos, locales, terrenos) puede generar ingresos por alquiler y plusvalías por revalorización. Sin embargo, requiere una inversión inicial elevada y tiene poca liquidez.

- **Alternativa accesible**: Los **REITs** (Sociedades de Inversión Inmobiliaria) te permiten invertir en inmuebles a través de la bolsa, sin tener que comprar un piso.

## ¿Cuál es mejor?

No existe un "mejor" tipo de inversión. La clave está en **combinar varios tipos** según tu perfil de riesgo, horizonte temporal y objetivos. Esto es la base de la diversificación.
""",
    "quizzes": [
        {
            "question": "¿Cuáles son las dos formas principales de ganar dinero con acciones?",
            "explanation": "Las acciones generan rentabilidad mediante plusvalías (vender a un precio mayor) y dividendos (reparto de beneficios de la empresa a los accionistas).",
            "options": [
                ("Cupones e intereses fijos", False),
                (
                    "Plusvalías (vender más caro) y dividendos (reparto de beneficios)",
                    True,
                ),
                ("Comisiones y gastos de gestión", False),
                ("Solo se gana dinero cuando la empresa quiebra", False),
            ],
        },
        {
            "question": "¿Qué diferencia principal tienen los ETFs frente a los fondos de inversión tradicionales?",
            "explanation": "Los ETFs se compran y venden en bolsa en tiempo real como acciones, y la mayoría son de gestión pasiva con comisiones muy bajas, a diferencia de muchos fondos tradicionales de gestión activa.",
            "options": [
                ("Los ETFs no permiten diversificación", False),
                ("Los fondos tradicionales siempre son más baratos", False),
                ("Los ETFs solo invierten en bonos del Estado", False),
                (
                    "Los ETFs cotizan en bolsa, tienen comisiones más bajas y la mayoría replican un índice",
                    True,
                ),
            ],
        },
        {
            "question": "¿Qué es un bono?",
            "explanation": "Un bono es un instrumento de deuda: el inversor presta dinero al emisor (gobierno o empresa), quien se compromete a devolver el capital más intereses periódicos.",
            "options": [
                ("Una participación en la propiedad de una empresa", False),
                (
                    "Un préstamo que haces a un gobierno o empresa a cambio de intereses",
                    True,
                ),
                ("Un tipo de cuenta de ahorro sin intereses", False),
                ("Una acción que nunca pierde valor", False),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# LESSON 3
# ---------------------------------------------------------------------------
LESSON_3 = {
    "title": "Riesgo y Rentabilidad",
    "description": "Entiende la relación entre riesgo y rendimiento, la volatilidad y cómo identificar tu perfil de inversor.",
    "estimated_time": 7,
    "content": """# Riesgo y Rentabilidad

Una de las reglas fundamentales de la inversión es que **riesgo y rentabilidad van de la mano**. No existe una inversión de alta rentabilidad sin riesgo, ni una inversión sin riesgo con alta rentabilidad. Entender esta relación es esencial para tomar buenas decisiones.

## ¿Qué es el Riesgo?

En inversión, el riesgo es la posibilidad de que el resultado sea diferente al esperado. Esto incluye:

- **Riesgo de mercado**: El valor de tu inversión baja por condiciones generales del mercado.
- **Riesgo de crédito**: El emisor de un bono no puede pagar lo que debe.
- **Riesgo de liquidez**: No puedes vender tu inversión cuando quieres sin perder valor.
- **Riesgo de inflación**: Tu inversión no supera la inflación y pierdes poder adquisitivo.

## La Volatilidad

La volatilidad mide cuánto fluctúa el precio de un activo. Un activo muy volátil sube y baja mucho en poco tiempo. Las acciones de empresas pequeñas, por ejemplo, suelen ser más volátiles que las de grandes empresas consolidadas.

> Importante: la volatilidad no es lo mismo que pérdida. Un activo volátil puede dar excelentes rendimientos a largo plazo, pero hay que soportar las bajadas intermedias.

## La Frontera Eficiente

Los economistas Harry Markowitz y William Sharpe demostraron que existe una combinación óptima de activos que maximiza la rentabilidad para cada nivel de riesgo. Este concepto se llama **frontera eficiente**:

- No tiene sentido asumir más riesgo si puedes obtener la misma rentabilidad con menos.
- La diversificación te acerca a esta frontera porque combina activos que no se mueven igual.

## Perfil de Inversor

Tu perfil de inversor depende de tres factores:

1. **Tolerancia al riesgo**: ¿Cuánta volatilidad puedes soportar emocionalmente sin vender en pánico?
2. **Capacidad financiera**: ¿Puedes permitirte perder parte del capital invertido sin que afecte tu vida?
3. **Horizonte temporal**: ¿Cuánto tiempo puedes dejar el dinero invertido?

Los perfiles típicos son:

- **Conservador**: Prioriza la seguridad. Mayoritariamente bonos y depósitos.
- **Moderado**: Equilibrio entre acciones y bonos. Acepta volatilidad moderada.
- **Agresivo**: Mayoría en acciones y activos de alto riesgo. Busca máxima rentabilidad a largo plazo.

## Rendimiento Histórico Promedio

Para tener una referencia realista:

- **Depósitos bancarios**: 0-2% anual
- **Bonos del Estado**: 2-4% anual
- **Acciones (S&P 500 histórico)**: ~10% anual (antes de inflación)
- **Inmobiliario**: 4-8% anual (varía mucho por ubicación)

Recuerda: **rendimientos pasados no garantizan rendimientos futuros**.
""",
    "quizzes": [
        {
            "question": "¿Qué significa que un activo es 'volátil'?",
            "explanation": "La volatilidad mide cuánto fluctúa el precio de un activo en un período de tiempo. Alta volatilidad significa grandes subidas y bajadas, pero no necesariamente pérdida permanente.",
            "options": [
                ("Que siempre pierde dinero", False),
                ("Que su precio fluctúa mucho en poco tiempo", True),
                ("Que no se puede vender nunca", False),
                ("Que es una inversión ilegal", False),
            ],
        },
        {
            "question": "Un inversor de perfil 'conservador' debería tener una cartera mayoritariamente compuesta por:",
            "explanation": "Los inversores conservadores priorizan la seguridad del capital sobre la rentabilidad, por lo que su cartera se compone principalmente de bonos y depósitos, con poca exposición a acciones.",
            "options": [
                ("100% acciones de empresas tecnológicas", False),
                ("Solo criptomonedas", False),
                ("Bonos y depósitos bancarios, con poca exposición a acciones", True),
                ("Solo bienes raíces", False),
            ],
        },
        {
            "question": "¿Cuál ha sido el rendimiento histórico anual promedio del S&P 500 (antes de inflación)?",
            "explanation": "El índice S&P 500, que agrupa las 500 mayores empresas de EE.UU., ha tenido un rendimiento histórico promedio de aproximadamente un 10% anual antes de descontar la inflación.",
            "options": [
                ("Aproximadamente 2% anual", False),
                ("Aproximadamente 25% anual", False),
                ("Siempre pierde dinero", False),
                ("Aproximadamente 10% anual", True),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# LESSON 4
# ---------------------------------------------------------------------------
LESSON_4 = {
    "title": "Construyendo un Portafolio",
    "description": "Aprende a crear un portafolio diversificado usando la asignación de activos y el rebalanceo.",
    "estimated_time": 7,
    "content": """# Construyendo un Portafolio

Un **portafolio** (o cartera de inversión) es el conjunto de todos los activos en los que inviertes. Construir un buen portafolio no significa simplemente elegir las acciones más populares; requiere una estrategia clara basada en tus objetivos y perfil de riesgo.

## Asignación de Activos (Asset Allocation)

La asignación de activos es la decisión más importante que tomarás como inversor. Consiste en decidir qué porcentaje de tu dinero destinas a cada tipo de activo:

- **Renta Variable (Acciones/ETFs)**: Mayor potencial de crecimiento, mayor volatilidad.
- **Renta Fija (Bonos)**: Estabilidad y generación de ingresos predecibles.
- **Efectivo/Liquidez**: Para emergencias y oportunidades.

> Estudios demuestran que más del 90% de la variabilidad en los rendimientos de un portafolio se debe a la asignación de activos, no a la selección individual de valores.

## Regla del 110

Una regla sencilla para principiantes:

**Porcentaje en acciones = 110 - tu edad**

- Si tienes 25 años: 85% acciones, 15% bonos
- Si tienes 40 años: 70% acciones, 30% bonos
- Si tienes 60 años: 50% acciones, 50% bonos

Es una aproximación, pero refleja el principio de que los jóvenes pueden asumir más riesgo porque tienen más tiempo para recuperarse de caídas.

## Diversificación en la Práctica

Diversificar no es solo tener muchas acciones. Una buena diversificación incluye:

- **Por tipo de activo**: Acciones, bonos, inmobiliario, materias primas.
- **Por geografía**: No invertir solo en tu país. Incluir mercados internacionales.
- **Por sector**: Tecnología, salud, energía, consumo, finanzas...
- **Por tamaño de empresa**: Grandes (blue chips), medianas y pequeñas.

## Rebalanceo

Con el tiempo, los activos que mejor funcionan ocupan un porcentaje cada vez mayor de tu cartera, desequilibrando tu asignación original. El **rebalanceo** consiste en volver periódicamente a tus porcentajes objetivo.

Por ejemplo, si tu objetivo es 70/30 (acciones/bonos) y tras un buen año las acciones crecen hasta representar el 80%, venderías parte de las acciones y comprarías bonos para volver al 70/30.

- **Frecuencia recomendada**: Una o dos veces al año, o cuando la desviación supere el 5%.

## Ejemplo de Portafolio para Principiante

Un portafolio simple y efectivo podría ser:

- 60% ETF de acciones globales (ej: MSCI World)
- 25% ETF de bonos diversificados
- 10% ETF de mercados emergentes
- 5% Efectivo/liquidez

Con solo 3-4 fondos puedes tener una cartera bien diversificada a nivel mundial.
""",
    "quizzes": [
        {
            "question": "Según la 'Regla del 110', ¿qué porcentaje debería invertir en acciones una persona de 30 años?",
            "explanation": "La Regla del 110 sugiere restar tu edad de 110 para obtener el porcentaje en acciones: 110 - 30 = 80% en acciones y 20% en bonos.",
            "options": [
                ("30%", False),
                ("110%", False),
                ("80%", True),
                ("50%", False),
            ],
        },
        {
            "question": "¿Qué es el 'rebalanceo' de un portafolio?",
            "explanation": "El rebalanceo es ajustar periódicamente la composición del portafolio para volver a los porcentajes objetivo originales, vendiendo activos que han crecido mucho y comprando los que se quedaron cortos.",
            "options": [
                ("Vender todas las inversiones y empezar de cero", False),
                (
                    "Ajustar los porcentajes de la cartera para volver a la asignación objetivo",
                    True,
                ),
                ("Invertir solo en el activo que mejor ha funcionado", False),
                ("Cambiar de broker cada año", False),
            ],
        },
        {
            "question": "¿Qué factor determina más del 90% de la variabilidad en los rendimientos de un portafolio?",
            "explanation": "Múltiples estudios académicos han demostrado que la asignación de activos (cuánto pones en acciones, bonos, etc.) es el factor dominante, por encima de la selección individual de valores o el timing del mercado.",
            "options": [
                ("Comprar en el momento perfecto (market timing)", False),
                ("Elegir las acciones individuales correctas", False),
                ("Tener suerte", False),
                ("La asignación de activos (asset allocation)", True),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# LESSON 5
# ---------------------------------------------------------------------------
LESSON_5 = {
    "title": "Primeros Pasos",
    "description": "Guía práctica para dar tus primeros pasos como inversor: cuentas, cantidades y errores comunes.",
    "estimated_time": 6,
    "content": """# Primeros Pasos como Inversor

Ya conoces los fundamentos. Ahora es momento de pasar a la acción. En esta lección veremos los pasos concretos para empezar a invertir y los errores más comunes que debes evitar.

## Paso 1: Ordena tus Finanzas

Antes de invertir un solo euro, asegúrate de:

- Tener un **fondo de emergencia** de 3-6 meses de gastos esenciales.
- No tener deudas de alto interés (tarjetas de crédito, préstamos personales). Pagar estas deudas es la mejor "inversión" que puedes hacer.
- Tener un presupuesto claro para saber cuánto puedes destinar a inversión cada mes.

## Paso 2: Abre una Cuenta en un Broker

Un **broker** es la plataforma a través de la cual compras y vendes inversiones. Al elegir uno, fíjate en:

- **Comisiones**: Cuánto cobran por comprar/vender. Muchos brokers online ya ofrecen comisiones muy bajas o cero.
- **Productos disponibles**: ¿Ofrecen acciones, ETFs, bonos, fondos?
- **Regulación**: Que esté regulado por la CNMV (España), BaFin (Alemania) u otro organismo oficial.
- **Facilidad de uso**: Una interfaz clara y sencilla.

## Paso 3: Define tu Estrategia

Responde estas preguntas antes de comprar nada:

1. ¿Cuál es mi objetivo? (Jubilación, vivienda, libertad financiera...)
2. ¿Cuál es mi horizonte temporal? (5, 10, 20, 30 años)
3. ¿Cuánto puedo invertir cada mes de forma constante?
4. ¿Cuál es mi tolerancia al riesgo?

> Una buena estrategia es aburrida. Si tu inversión te genera ansiedad constante, probablemente estás asumiendo más riesgo del que puedes soportar.

## Paso 4: Empieza con Poco y Sé Constante

No necesitas grandes cantidades para empezar. Muchos brokers permiten invertir desde 10-50 €. Lo importante es la **constancia**:

- La estrategia del **DCA (Dollar Cost Averaging)** consiste en invertir la misma cantidad cada mes, independientemente de si el mercado sube o baja. Esto reduce el riesgo de invertir todo en el peor momento.

## Los 5 Errores más Comunes

1. **Intentar predecir el mercado**: Nadie sabe cuándo subirá o bajará. Invierte de forma constante.
2. **Dejarse llevar por las emociones**: El pánico lleva a vender en mínimos; la euforia a comprar en máximos.
3. **No diversificar**: Poner todo en una sola empresa o sector es extremadamente arriesgado.
4. **Ignorar las comisiones**: Comisiones altas pueden comerse gran parte de tus rendimientos a largo plazo.
5. **No empezar**: El mayor error es posponer la inversión. El tiempo es tu mayor aliado gracias al interés compuesto.

## Resumen del Módulo

En estas cinco lecciones has aprendido:

- Qué es invertir y por qué es importante
- Los principales tipos de activos (acciones, bonos, fondos, ETFs)
- La relación entre riesgo y rentabilidad
- Cómo construir un portafolio diversificado
- Los pasos prácticos para empezar

¡Ahora es tu turno! Usa el simulador de bolsa de FinLearn para practicar sin riesgo antes de invertir dinero real.
""",
    "quizzes": [
        {
            "question": "¿En qué consiste la estrategia DCA (Dollar Cost Averaging)?",
            "explanation": "DCA consiste en invertir la misma cantidad de dinero a intervalos regulares (ej: cada mes), sin importar el precio del mercado. Esto promedia el coste de compra y reduce el riesgo de invertir todo en un mal momento.",
            "options": [
                ("Invertir todo el dinero disponible de una sola vez", False),
                (
                    "Invertir la misma cantidad cada mes sin importar si el mercado sube o baja",
                    True,
                ),
                ("Solo comprar cuando el mercado está bajando", False),
                ("Vender todas las inversiones cada mes y volver a comprar", False),
            ],
        },
        {
            "question": "¿Cuál de estos NO es un error común al invertir?",
            "explanation": "Diversificar tu cartera entre diferentes activos y sectores es una buena práctica, no un error. Los errores comunes son intentar predecir el mercado, dejarse llevar por emociones, no diversificar e ignorar comisiones.",
            "options": [
                ("Intentar predecir cuándo subirá el mercado", False),
                ("Vender en pánico cuando el mercado baja", False),
                ("Ignorar las comisiones del broker", False),
                ("Diversificar tu cartera entre diferentes activos", True),
            ],
        },
        {
            "question": "Al elegir un broker, ¿cuál de estos factores es MÁS importante para tu seguridad como inversor?",
            "explanation": "La regulación por un organismo oficial (como la CNMV en España) garantiza que el broker cumple las leyes, protege tus fondos y opera de manera transparente. Es el factor más crítico para la seguridad.",
            "options": [
                ("Que tenga la aplicación más bonita", False),
                ("Que ofrezca criptomonedas", False),
                ("Que esté regulado por un organismo oficial (como la CNMV)", True),
                ("Que tenga oficinas físicas cerca de tu casa", False),
            ],
        },
    ],
}

ALL_LESSONS = [LESSON_1, LESSON_2, LESSON_3, LESSON_4, LESSON_5]


class Command(BaseCommand):
    help = (
        "Seed Module 1 'Introducción a la Inversión' — 5 full lessons with 15 quizzes."
    )

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
