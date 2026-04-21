"""
Management command to seed Module 3: "Finanzas Personales Básicas"
4 full lessons with rich content and 3 quizzes each (12 quizzes total).
Correct-answer positions are distributed across A/B/C/D.
"""

from django.core.management.base import BaseCommand

from apps.lessons.models import Lesson, Module, Quiz, QuizOption

MODULE_DATA = {
    "title": "Finanzas Personales Básicas",
    "description": (
        "Domina los conceptos básicos de finanzas personales incluyendo presupuesto, "
        "ahorro y gestión de deudas de manera efectiva."
    ),
    "icon": "💰",
    "color": "#f59e0b",
    "difficulty": "beginner",
    "order": 2,
    "xp_reward": 450,
}

# ---------------------------------------------------------------------------
# LESSON 1
# ---------------------------------------------------------------------------
LESSON_1 = {
    "title": "Creando un Presupuesto",
    "description": "Aprende a crear y mantener un presupuesto personal que te permita controlar tus gastos y alcanzar tus metas financieras.",
    "estimated_time": 7,
    "content": """# Creando un Presupuesto

Un presupuesto es la herramienta más poderosa de las finanzas personales. No se trata de privarte de cosas, sino de **saber exactamente a dónde va tu dinero** y decidir conscientemente cómo usarlo.

## ¿Por qué necesitas un presupuesto?

Sin un presupuesto, es casi imposible saber si estás gastando más de lo que ganas. Muchas personas se sorprenden al descubrir cuánto gastan en pequeñas compras diarias que, sumadas, representan miles de euros al año.

> Un presupuesto no restringe tu libertad — te da el control para gastar en lo que realmente te importa.

## La Regla del 50/30/20

Una de las guías más populares para distribuir tus ingresos es la regla **50/30/20**:

- **50% — Necesidades**: Vivienda, alimentación, transporte, seguros, servicios básicos. Son gastos que no puedes evitar.
- **30% — Deseos**: Ocio, restaurantes, suscripciones, ropa no esencial, vacaciones. Son gastos que mejoran tu calidad de vida pero no son imprescindibles.
- **20% — Ahorro e Inversión**: Fondo de emergencia, planes de pensiones, inversiones, pago acelerado de deudas.

### Ejemplo práctico

Si ganas 2.000 € netos al mes:
1. Necesidades: hasta 1.000 € (alquiler, comida, transporte, seguros)
2. Deseos: hasta 600 € (ocio, restaurantes, suscripciones)
3. Ahorro: al menos 400 € (fondo de emergencia, inversión)

## Cómo crear tu presupuesto paso a paso

### Paso 1: Registra tus ingresos
Anota todos los ingresos netos mensuales: salario, freelance, rentas, etc.

### Paso 2: Clasifica tus gastos
Revisa tus extractos bancarios de los últimos 3 meses. Categoriza cada gasto como necesidad, deseo o ahorro.

### Paso 3: Establece límites
Basándote en la regla 50/30/20 (o la proporción que mejor se adapte a tu situación), establece un tope para cada categoría.

### Paso 4: Haz seguimiento
Revisa tu presupuesto semanalmente durante el primer mes. Después, una revisión quincenal suele ser suficiente.

### Paso 5: Ajusta
Un presupuesto no es estático. Adáptalo cuando cambien tus circunstancias (subida de sueldo, nuevo gasto fijo, cambio de vivienda).

## Herramientas útiles

- **Hojas de cálculo**: Google Sheets o Excel son gratuitas y muy flexibles.
- **Apps de finanzas**: Fintonic, Monefy o YNAB te ayudan a categorizar gastos automáticamente.
- **Sobres digitales**: Asigna cantidades fijas a categorías y no las sobrepases.

## Errores comunes

- **No incluir gastos irregulares**: Seguro del coche, revisión médica anual, regalos de Navidad. Divídelos entre 12 y réservalos cada mes.
- **Ser demasiado restrictivo**: Un presupuesto irreal se abandona rápido. Deja margen para imprevistos.
- **No revisarlo**: Un presupuesto que no se revisa es papel mojado.
""",
    "quizzes": [
        {
            "question": "Según la regla 50/30/20, ¿qué porcentaje de tus ingresos debería destinarse al ahorro e inversión?",
            "explanation": "La regla 50/30/20 sugiere destinar el 50% a necesidades, el 30% a deseos y el 20% al ahorro e inversión.",
            "options": [
                ("10%", False),
                ("20%", True),
                ("30%", False),
                ("50%", False),
            ],
        },
        {
            "question": "Si ganas 2.000 € netos al mes, ¿cuánto deberías dedicar a necesidades según la regla 50/30/20?",
            "explanation": "El 50% de 2.000 € son 1.000 €, que es la cantidad máxima recomendada para necesidades (vivienda, alimentación, transporte, seguros).",
            "options": [
                ("600 €", False),
                ("800 €", False),
                ("1.000 €", True),
                ("1.500 €", False),
            ],
        },
        {
            "question": "¿Cuál de estos es un error común al hacer un presupuesto?",
            "explanation": "No incluir gastos irregulares (seguro anual, regalos, revisiones médicas) es un error muy frecuente que provoca que el presupuesto falle. Hay que dividirlos entre 12 meses y reservar la cantidad cada mes.",
            "options": [
                ("Revisar el presupuesto semanalmente", False),
                ("Usar una hoja de cálculo", False),
                ("Dejar margen para imprevistos", False),
                ("No incluir gastos irregulares como el seguro anual del coche", True),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# LESSON 2
# ---------------------------------------------------------------------------
LESSON_2 = {
    "title": "Fondo de Emergencia",
    "description": "Descubre por qué necesitas un fondo de emergencia, cuánto debería tener y cómo construirlo paso a paso.",
    "estimated_time": 6,
    "content": """# Fondo de Emergencia

Un fondo de emergencia es dinero apartado específicamente para **gastos imprevistos**: una avería del coche, una reparación en casa, una baja médica o incluso una pérdida de empleo. Es tu red de seguridad financiera.

## ¿Por qué es tan importante?

Sin un fondo de emergencia, cualquier imprevisto te obliga a recurrir a deuda (tarjeta de crédito, préstamo personal), que tiene intereses altos y puede generar un efecto bola de nieve.

> El fondo de emergencia no es un lujo — es la base sobre la que construyes el resto de tu vida financiera.

### Datos que preocupan

- El 40% de los españoles no podría afrontar un gasto imprevisto de 1.000 € sin endeudarse.
- Una avería de coche media cuesta entre 300 € y 2.000 €.
- El tiempo medio para encontrar empleo en España es de 3 a 6 meses.

## ¿Cuánto necesitas?

La recomendación general es tener entre **3 y 6 meses de gastos esenciales** ahorrados:

- **3 meses**: Si tienes un empleo estable, pocas responsabilidades y buena empleabilidad.
- **6 meses o más**: Si eres autónomo, tienes familia a cargo, o tu sector tiene alta incertidumbre.

### Cálculo rápido

1. Suma tus gastos esenciales mensuales (vivienda, comida, transporte, seguros, suministros).
2. Multiplica por el número de meses que elijas (3, 4, 5 o 6).

Ejemplo: Si tus gastos esenciales son 1.200 €/mes → Fondo objetivo = 1.200 × 6 = **7.200 €**

## ¿Dónde guardar el fondo?

El fondo de emergencia debe ser:

- **Líquido**: Que puedas acceder a él en 24-48 horas.
- **Seguro**: Sin riesgo de perder el capital.
- **Separado**: En una cuenta distinta a la del día a día, para no gastarlo sin querer.

Opciones recomendadas:
- Cuenta de ahorro remunerada (la más habitual).
- Depósito a corto plazo con liquidez anticipada.
- Fondo monetario (algo más de rentabilidad, sigue siendo muy seguro).

## Cómo construirlo paso a paso

### 1. Empieza con una meta pequeña
Tu primera meta: **1.000 €**. Este colchón mínimo ya cubre la mayoría de imprevistos menores.

### 2. Automatiza el ahorro
Configura una transferencia automática el día que cobras. Si no ves el dinero, no lo gastas.

### 3. Usa "dinero extra"
Destina al fondo cualquier ingreso extraordinario: paga extra, devolución de Hacienda, regalos monetarios.

### 4. Recorta temporalmente
Mientras construyes el fondo, reduce gastos no esenciales: menos comer fuera, pausar suscripciones que no uses.

### 5. No lo toques (salvo emergencias reales)
Una oferta de viaje no es una emergencia. Una lavadora rota sí lo es.

## ¿Qué es y qué NO es una emergencia?

- **SÍ**: Pérdida de empleo, avería del coche necesario para trabajar, gasto médico urgente, reparación imprescindible del hogar.
- **NO**: Vacaciones, un teléfono nuevo, ropa en rebajas, un capricho.
""",
    "quizzes": [
        {
            "question": "¿Cuántos meses de gastos esenciales se recomienda tener en un fondo de emergencia?",
            "explanation": "La recomendación estándar es tener entre 3 y 6 meses de gastos esenciales, dependiendo de la estabilidad laboral y responsabilidades familiares.",
            "options": [
                ("1 mes", False),
                ("Entre 3 y 6 meses", True),
                ("12 meses exactos", False),
                ("No importa la cantidad, cualquier ahorro vale", False),
            ],
        },
        {
            "question": "¿Cuál de estas características NO debería tener un fondo de emergencia?",
            "explanation": "Un fondo de emergencia debe ser seguro, líquido y estar separado de la cuenta diaria. Invertirlo en acciones implica riesgo de perder capital justo cuando más lo necesitas.",
            "options": [
                ("Estar en una cuenta separada de la del día a día", False),
                ("Ser accesible en 24-48 horas", False),
                ("Estar invertido en acciones para maximizar rentabilidad", True),
                ("No tener riesgo de perder el capital", False),
            ],
        },
        {
            "question": "¿Cuál de estos gastos SÍ justifica usar el fondo de emergencia?",
            "explanation": "Una avería del coche necesario para ir a trabajar es un gasto imprevisto e imprescindible — exactamente para lo que existe el fondo de emergencia. Vacaciones, ropa en rebajas o un móvil nuevo son deseos, no emergencias.",
            "options": [
                ("Unas vacaciones de última hora muy baratas", False),
                ("Ropa en rebajas a muy buen precio", False),
                ("Un smartphone nuevo que acaba de salir", False),
                ("Una avería del coche que necesitas para trabajar", True),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# LESSON 3
# ---------------------------------------------------------------------------
LESSON_3 = {
    "title": "Gestión de Deudas",
    "description": "Aprende a distinguir entre deuda buena y mala, y conoce las estrategias más efectivas para eliminar deudas.",
    "estimated_time": 7,
    "content": """# Gestión de Deudas

No todas las deudas son iguales. Entender la diferencia entre **deuda productiva** y **deuda destructiva** es esencial para tomar buenas decisiones financieras.

## Deuda buena vs. deuda mala

### Deuda buena (productiva)
Es aquella que te ayuda a generar riqueza o ingresos a largo plazo:
- **Hipoteca**: Compras un activo que normalmente se revaloriza.
- **Préstamo para estudios**: Aumenta tu capacidad de generar ingresos.
- **Préstamo para un negocio**: Con un plan sólido, puede generar beneficios superiores al coste de la deuda.

### Deuda mala (destructiva)
Es aquella que financia consumo o activos que pierden valor:
- **Tarjeta de crédito sin pagar al 100%**: Intereses del 18-25% anual.
- **Financiación de electrónica o vacaciones**: Pagas intereses por algo que ya consumiste.
- **Créditos rápidos (minicréditos)**: TAE que puede superar el 1.000%.

> Regla de oro: si lo que compras pierde valor y el interés es alto, probablemente es deuda mala.

## El coste real de la deuda

Una deuda de 3.000 € en tarjeta de crédito al 20% TAE, pagando solo el mínimo mensual (30 €):
- Tardarás más de **15 años** en pagarla.
- Pagarás más de **4.500 €** en intereses — más que la propia deuda.

## Estrategias para eliminar deudas

### Método Avalancha (matemáticamente óptimo)
1. Ordena tus deudas por **tipo de interés de mayor a menor**.
2. Paga el mínimo en todas excepto la de mayor interés.
3. Destina todo el dinero extra a la deuda con más interés.
4. Cuando la eliminas, pasa a la siguiente.

**Ventaja**: Pagas menos intereses en total.

### Método Bola de Nieve (psicológicamente efectivo)
1. Ordena tus deudas por **cantidad de menor a mayor**.
2. Paga el mínimo en todas excepto la más pequeña.
3. Destina todo el dinero extra a la deuda más pequeña.
4. Cuando la eliminas, pasas a la siguiente.

**Ventaja**: Las victorias rápidas al eliminar deudas pequeñas te motivan a seguir.

### ¿Cuál elegir?
- Si eres disciplinado y quieres ahorrar al máximo en intereses → **Avalancha**.
- Si necesitas motivación y victorias tempranas → **Bola de Nieve**.
- Ambos funcionan. Lo importante es elegir uno y ser constante.

## La trampa del pago mínimo

Las entidades financieras calculan el pago mínimo para que tardes el máximo tiempo posible en pagar. Pagar solo el mínimo es la forma más cara de devolver una deuda.

### Consejos prácticos

- **Nunca pagues solo el mínimo** de la tarjeta de crédito. Si puedes, paga el 100% cada mes.
- **Consolida deudas** si puedes conseguir un interés menor que el promedio de tus deudas actuales.
- **Negocia con tu banco**: A veces pueden reducir el tipo de interés o ofrecer un plan de pagos.
- **No adquieras nueva deuda** mientras pagas la existente.
""",
    "quizzes": [
        {
            "question": "¿Cuál de estas se considera generalmente una 'deuda buena'?",
            "explanation": "Una hipoteca se considera deuda productiva porque financias un activo (vivienda) que normalmente se revaloriza con el tiempo, y los intereses suelen ser relativamente bajos.",
            "options": [
                ("Deuda de tarjeta de crédito para comprar ropa", False),
                ("Una hipoteca para comprar tu vivienda", True),
                ("Un minicrédito para unas vacaciones", False),
                ("Financiar un televisor a 24 meses", False),
            ],
        },
        {
            "question": "¿En qué consiste el método Bola de Nieve para eliminar deudas?",
            "explanation": "El método Bola de Nieve ordena las deudas de menor a mayor importe y prioriza pagar primero la más pequeña. Las victorias rápidas generan motivación para seguir eliminando deudas.",
            "options": [
                ("Pagar primero la deuda con mayor tipo de interés", False),
                ("Pagar todas las deudas a partes iguales", False),
                ("Pedir un préstamo grande para cubrir todas las deudas", False),
                (
                    "Pagar primero la deuda más pequeña para generar motivación con victorias rápidas",
                    True,
                ),
            ],
        },
        {
            "question": "Si tienes 3.000 € en tarjeta de crédito al 20% TAE y pagas solo el mínimo, ¿qué ocurre?",
            "explanation": "Pagando solo el mínimo de una tarjeta de crédito al 20% TAE, tardarás más de 15 años en liquidarla y pagarás más de 4.500 € en intereses — más que el propio capital prestado.",
            "options": [
                ("La pagarás en unos 3 años sin problemas", False),
                ("Tardarás más de 15 años y pagarás más de 4.500 € en intereses", True),
                ("El banco te condonará la deuda después de 5 años", False),
                ("Los intereses se reducen automáticamente cada año", False),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# LESSON 4
# ---------------------------------------------------------------------------
LESSON_4 = {
    "title": "Estrategias de Ahorro",
    "description": "Descubre técnicas prácticas y probadas para ahorrar más dinero sin sacrificar tu calidad de vida.",
    "estimated_time": 6,
    "content": """# Estrategias de Ahorro

Ahorrar no significa vivir peor. Significa **gastar de forma consciente** y eliminar gastos que no aportan valor real a tu vida. Con las estrategias adecuadas, puedes ahorrar significativamente sin sentir que te privas de nada.

## El principio fundamental: Págate a ti primero

La mayoría de la gente intenta ahorrar lo que sobra a final de mes. El problema es que rara vez sobra algo. La estrategia correcta es al revés:

1. Cobras tu salario.
2. **Inmediatamente** transfieres tu cantidad de ahorro a otra cuenta.
3. Vives con el resto.

> "No ahorres lo que te sobra después de gastar. Gasta lo que te sobra después de ahorrar." — Warren Buffett

## Técnicas de ahorro probadas

### 1. Automatización
Configura una transferencia automática el día de cobro. Si no ves el dinero, no lo echas de menos.

### 2. Reto de las 52 semanas
- Semana 1: ahorra 1 €
- Semana 2: ahorra 2 €
- Semana 52: ahorra 52 €
- **Total al año: 1.378 €**

### 3. Regla de las 24/48 horas
Antes de cualquier compra no esencial superior a 50 €, espera 24-48 horas. Si después sigues queriéndolo, cómpralo. Muchas compras impulsivas se evitan así.

### 4. Auditoría de suscripciones
Revisa todas tus suscripciones (streaming, gym, apps, revistas). ¿Las usas todas? Cancelar 3-4 suscripciones innecesarias puede ahorrarte 30-60 € al mes (360-720 € al año).

### 5. La regla del coste por uso
Antes de comprar algo, calcula su coste por uso. Unos zapatos de 120 € que usas 200 veces cuestan 0,60 €/uso. Un vestido de 80 € que usas 2 veces cuesta 40 €/uso. El artículo más caro no siempre es el peor negocio.

## Ahorro en gastos fijos

Los gastos fijos son donde más puedes ahorrar porque el efecto es mensual y permanente:

- **Seguros**: Compara cada año. Cambiar de aseguradora puede ahorrarte 200-500 €/año.
- **Telefonía e internet**: Negocia o cambia de operador. La competencia es feroz y hay buenas ofertas.
- **Energía**: Compara tarifas eléctricas. Usa electrodomésticos en horas valle si tienes discriminación horaria.
- **Alimentación**: Planifica menús semanales, haz lista de la compra y ve al súper sin hambre.

## La cuenta de ahorro con objetivo

Tener una meta concreta multiplica tu motivación:

- "Vacaciones 2026: 1.800 €" = 150 €/mes durante 12 meses
- "Entrada del piso: 20.000 €" = 555 €/mes durante 3 años
- "Fondo de emergencia: 6.000 €" = 250 €/mes durante 2 años

### Consejo final

El mejor momento para empezar a ahorrar fue hace 10 años. El segundo mejor momento es **hoy**. Empieza con lo que puedas, aunque sean 20 € al mes. El hábito es más importante que la cantidad.
""",
    "quizzes": [
        {
            "question": "¿Qué significa el principio de 'pagarte a ti primero'?",
            "explanation": "Pagarte a ti primero significa apartar tu ahorro ANTES de empezar a gastar. Si esperas a final de mes para ahorrar lo que sobra, rara vez sobra algo.",
            "options": [
                ("Gastar libremente y ahorrar lo que sobre a fin de mes", False),
                ("Pagar todas tus deudas antes de ahorrar", False),
                (
                    "Transferir tu cantidad de ahorro nada más cobrar, antes de gastar en nada",
                    True,
                ),
                ("Comprarte algo bonito cada mes como recompensa", False),
            ],
        },
        {
            "question": "¿Cuánto ahorrarías al completar el Reto de las 52 semanas?",
            "explanation": "El Reto de las 52 semanas consiste en ahorrar 1 € la primera semana, 2 € la segunda, y así sucesivamente hasta 52 € en la última semana. La suma total es 1.378 €.",
            "options": [
                ("520 €", False),
                ("1.000 €", False),
                ("1.378 €", True),
                ("2.500 €", False),
            ],
        },
        {
            "question": "¿Cuál de estas técnicas ayuda a evitar compras impulsivas?",
            "explanation": "La regla de las 24/48 horas consiste en esperar un día o dos antes de hacer compras no esenciales superiores a 50 €. Muchas compras impulsivas se evitan porque el deseo inicial pasa.",
            "options": [
                (
                    "Esperar 24-48 horas antes de compras no esenciales superiores a 50 €",
                    True,
                ),
                ("Llevar siempre efectivo en lugar de tarjeta", False),
                ("Comprar todo online para comparar precios", False),
                ("Ir de compras solo los fines de semana", False),
            ],
        },
    ],
}

ALL_LESSONS = [LESSON_1, LESSON_2, LESSON_3, LESSON_4]


class Command(BaseCommand):
    help = (
        "Seed Module 3 'Finanzas Personales Básicas' — 4 full lessons with 12 quizzes."
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
