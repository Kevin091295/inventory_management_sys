import random
import string
from django.core.management.base import BaseCommand
from dashboard.models import StockTransaction

class Command(BaseCommand):
    help = 'Update existing stock transaction reference numbers'

    def generate_reference_number(self):
        """
        Generate reference number in the format:
        2 alphabets + 3 numbers + 1 alphabet + 1 number + 1 alphabet
        """
        return (
            ''.join(random.choices(string.ascii_uppercase, k=2)) +  # 2 alphabets
            ''.join(random.choices(string.digits, k=3)) +           # 3 numbers
            random.choice(string.ascii_uppercase) +                 # 1 alphabet
            random.choice(string.digits) +                          # 1 number
            random.choice(string.ascii_uppercase)                   # 1 alphabet
        )

    def handle(self, *args, **kwargs):
        self.stdout.write("Updating stock transaction reference numbers...")

        transactions = StockTransaction.objects.all()
        for transaction in transactions:
            if not transaction.reference_number or len(transaction.reference_number) != 8:
                transaction.reference_number = self.generate_reference_number()
                transaction.save()
                self.stdout.write(f"Updated transaction {transaction.id} to {transaction.reference_number}")

        self.stdout.write("All transactions updated successfully!")
