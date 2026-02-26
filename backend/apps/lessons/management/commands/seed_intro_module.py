"""
Management command to seed the first module "Introducción a la Inversión"
with the first lesson (full content + quizzes) and placeholder lessons 2-5.
Matches the sample data from frontend/src/i18n/translations.js.
"""

from django.core.management.base import BaseCommand
from apps.lessons.models import Module, Lesson, Quiz, QuizOption


MODULE_DATA = {
    "title": "Introducción a la Inversión",
    "description": "Aprende los fundamentos de la inversión, incluyendo acciones, bonos y fondos mutuos. Perfecto para principiantes que comienzan su camino financiero.",
    "icon": "📈",
    "color": "#6366f1",
    "difficulty": "beginner",
    "order": 0,
    "xp_reward": 500,
}

LESSON_1_CONTENT = """# ¿Qué es Invertir?

Invertir es el acto de asignar dinero o recursos con la expectativa de generar ingresos o ganancias a lo largo del tiempo. A diferencia del ahorro, donde simplemente guardas dinero, invertir pone tu dinero a trabajar.

## ¿Por qué Invertir?

1. **Superar la Inflación**: Tu dinero pierde valor con el tiempo debido a la inflación. Invertir ayuda a que tu patrimonio crezca más rápido que la inflación.

2. **Construir Riqueza**: A través del poder del interés compuesto, incluso pequeñas inversiones pueden crecer significativamente con el tiempo.

3. **Alcanzar Metas**: Ya sea la jubilación, comprar una casa o financiar la educación, invertir puede ayudarte a alcanzar tus objetivos financieros.

## Conceptos Clave

### Riesgo y Rentabilidad
Generalmente, mayores rendimientos potenciales vienen con mayor riesgo. Entender tu tolerancia al riesgo es crucial.

### Diversificación
No pongas todos los huevos en la misma cesta. Distribuir las inversiones entre diferentes activos reduce el riesgo.

### Horizonte Temporal
Cuanto más tiempo puedas dejar tu dinero invertido, más tiempo tendrá para crecer y recuperarse de las fluctuaciones del mercado.
"""

QUIZZES_LESSON_1 = [
    {
        "question": "¿Cuál es la principal diferencia entre ahorrar e invertir?",
        "order": 0,
        "xp_reward": 10,
        "explanation": "Mientras que ahorrar típicamente significa guardar dinero en cuentas seguras, invertir implica asignar dinero en activos que pueden potencialmente crecer en valor con el tiempo.",
        "options": [
            ("Ahorrar implica poner dinero en un banco, invertir no", False),
            ("Invertir pone tu dinero a trabajar para generar rendimientos", True),
            ("No hay diferencia", False),
            ("Ahorrar es más arriesgado que invertir", False),
        ],
    },
    {
        "question": "¿Qué es la diversificación?",
        "order": 1,
        "xp_reward": 10,
        "explanation": "La diversificación significa distribuir tus inversiones entre varios tipos de activos, sectores y regiones geográficas para reducir el riesgo.",
        "options": [
            ("Invertir todo tu dinero en una sola acción", False),
            ("Distribuir inversiones entre diferentes activos para reducir el riesgo", True),
            ("Solo invertir en empresas de tecnología", False),
            ("Mantener todo tu dinero en efectivo", False),
        ],
    },
    {
        "question": "¿Por qué es importante el horizonte temporal en la inversión?",
        "order": 2,
        "xp_reward": 10,
        "explanation": "Un horizonte temporal más largo le da a tus inversiones más tiempo para crecer a través del interés compuesto y recuperarse de caídas temporales del mercado.",
        "options": [
            ("Determina cuándo abre el mercado de valores", False),
            ("Horizontes más largos permiten más tiempo de recuperación ante fluctuaciones del mercado", True),
            ("Solo importa para traders diarios", False),
            ("El horizonte temporal no tiene impacto en la inversión", False),
        ],
    },
]

LESSONS_2_TO_5 = [
    ("Tipos de Inversiones", "Conoce acciones, bonos, fondos mutuos y más.", ""),
    ("Riesgo y Rentabilidad", "Entiende la relación entre riesgo y rendimiento.", ""),
    ("Construyendo un Portafolio", "Aprende a diversificar y construir un portafolio.", ""),
    ("Primeros Pasos", "Cómo dar tus primeros pasos como inversor.", ""),
]


class Command(BaseCommand):
    help = "Seed the first module 'Introducción a la Inversión' with lesson 1 (full content + quizzes) and placeholder lessons 2-5."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing 'Introducción a la Inversión' module and its lessons before seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted = Module.objects.filter(title=MODULE_DATA["title"]).delete()
            if deleted[0]:
                self.stdout.write(
                    self.style.WARNING(
                        f"Deleted existing module and {deleted[1].get('lessons.Module', 0)} related objects."
                    )
                )

        if Module.objects.filter(title=MODULE_DATA["title"]).exists():
            self.stdout.write(
                self.style.WARNING(
                    "Module 'Introducción a la Inversión' already exists. Use --clear to replace it."
                )
            )
            return

        module = Module.objects.create(**MODULE_DATA)
        self.stdout.write(self.style.SUCCESS(f"Created module: {module.title}"))

        # Lesson 1: full content + quizzes
        lesson1 = Lesson.objects.create(
            module=module,
            title="¿Qué es Invertir?",
            description="Aprende los conceptos fundamentales de la inversión y por qué es importante para tu futuro financiero.",
            content=LESSON_1_CONTENT.strip(),
            order=0,
            xp_reward=50,
            estimated_time=5,
        )
        self.stdout.write(self.style.SUCCESS(f"  Created lesson: {lesson1.title}"))

        for q_data in QUIZZES_LESSON_1:
            quiz = Quiz.objects.create(
                lesson=lesson1,
                question=q_data["question"],
                order=q_data["order"],
                xp_reward=q_data["xp_reward"],
                explanation=q_data["explanation"],
            )
            for i, (text, is_correct) in enumerate(q_data["options"]):
                QuizOption.objects.create(
                    quiz=quiz,
                    text=text,
                    is_correct=is_correct,
                    order=i,
                )
        self.stdout.write(f"    Added {len(QUIZZES_LESSON_1)} quizzes with options.")

        # Lessons 2-5: placeholders
        for i, (title, description, content) in enumerate(LESSONS_2_TO_5, start=2):
            Lesson.objects.create(
                module=module,
                title=title,
                description=description,
                content=content or f"Contenido de la lección '{title}' (próximamente).",
                order=i - 1,
                xp_reward=50,
                estimated_time=5,
            )
            self.stdout.write(self.style.SUCCESS(f"  Created lesson: {title}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Module has {module.lessons_count} lessons. Run the app and complete lesson 1 to earn XP."
            )
        )
