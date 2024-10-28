from django.core.management.base import BaseCommand
from personalityperfume.models import PersonalityPerfume

class Command(BaseCommand):
    help = 'Populate the PersonalityPerfume table'

    def handle(self, *args, **kwargs):
        perfumes = [
            ("Rêveur (Imagineur)", "Floral", "Soft and dreamy scents that evoke creativity."),
            ("Empathique", "Fruity", "Fresh and vibrant fragrances that uplift the spirit."),
            ("Persévérant", "Woody", "Earthy and grounded scents that convey stability."),
            ("Travaillomane (Analyseur)", "Oriental", "Complex and rich fragrances that stimulate the senses."),
            ("Promoteur", "Citrus", "Bright and zesty perfumes that energize and invigorate."),
            ("Rebelle (Energiseur)", "Spicy", "Bold and daring scents that express individuality."),
        ]

        for personality_type, perfume_type, characteristics in perfumes:
            PersonalityPerfume.objects.create(
                personality_type=personality_type,
                perfume_type=perfume_type,
                characteristics=characteristics
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated PersonalityPerfume table'))
