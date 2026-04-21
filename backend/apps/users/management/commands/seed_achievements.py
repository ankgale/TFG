"""
Management command to seed the initial set of achievements.
"""

from django.core.management.base import BaseCommand

from apps.users.models import Achievement

ACHIEVEMENTS = [
    # Learning milestones
    {
        "name": "Primera Lección",
        "description": "Completa tu primera lección",
        "icon": "📖",
        "category": "learning",
        "xp_reward": 50,
        "condition_type": "lessons_completed",
        "condition_value": 1,
    },
    {
        "name": "Estudiante Dedicado",
        "description": "Completa 5 lecciones",
        "icon": "📚",
        "category": "learning",
        "xp_reward": 100,
        "condition_type": "lessons_completed",
        "condition_value": 5,
    },
    {
        "name": "Experto en Formación",
        "description": "Completa 10 lecciones",
        "icon": "🎓",
        "category": "learning",
        "xp_reward": 200,
        "condition_type": "lessons_completed",
        "condition_value": 10,
    },
    {
        "name": "Primer Módulo",
        "description": "Completa tu primer módulo",
        "icon": "🏅",
        "category": "learning",
        "xp_reward": 150,
        "condition_type": "modules_completed",
        "condition_value": 1,
    },
    # Streak milestones
    {
        "name": "Racha de 3 Días",
        "description": "Mantén una racha de actividad de 3 días",
        "icon": "🔥",
        "category": "streak",
        "xp_reward": 75,
        "condition_type": "streak_days",
        "condition_value": 3,
    },
    {
        "name": "Racha Semanal",
        "description": "Mantén una racha de actividad de 7 días",
        "icon": "💪",
        "category": "streak",
        "xp_reward": 200,
        "condition_type": "streak_days",
        "condition_value": 7,
    },
    {
        "name": "Racha Mensual",
        "description": "Mantén una racha de actividad de 30 días",
        "icon": "⭐",
        "category": "streak",
        "xp_reward": 500,
        "condition_type": "streak_days",
        "condition_value": 30,
    },
    # Trading milestones
    {
        "name": "Primera Operación",
        "description": "Realiza tu primera compra o venta de acciones",
        "icon": "📊",
        "category": "trading",
        "xp_reward": 50,
        "condition_type": "trades_executed",
        "condition_value": 1,
    },
    {
        "name": "Trader Activo",
        "description": "Realiza 10 operaciones en el simulador",
        "icon": "📈",
        "category": "trading",
        "xp_reward": 150,
        "condition_type": "trades_executed",
        "condition_value": 10,
    },
    {
        "name": "Trader Veterano",
        "description": "Realiza 50 operaciones en el simulador",
        "icon": "🏆",
        "category": "trading",
        "xp_reward": 300,
        "condition_type": "trades_executed",
        "condition_value": 50,
    },
    # XP / Level milestones
    {
        "name": "Nivel 2",
        "description": "Alcanza el nivel 2",
        "icon": "🌟",
        "category": "special",
        "xp_reward": 100,
        "condition_type": "level_reached",
        "condition_value": 2,
    },
    {
        "name": "Nivel 5",
        "description": "Alcanza el nivel 5",
        "icon": "💎",
        "category": "special",
        "xp_reward": 250,
        "condition_type": "level_reached",
        "condition_value": 5,
    },
]


class Command(BaseCommand):
    help = "Seed the database with predefined achievements."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing achievements before seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = Achievement.objects.all().delete()
            self.stdout.write(f"Deleted {deleted} existing achievements.")

        created = 0
        for data in ACHIEVEMENTS:
            _, was_created = Achievement.objects.get_or_create(
                name=data["name"],
                defaults=data,
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {created} new achievements ({len(ACHIEVEMENTS)} total defined)."
            )
        )
