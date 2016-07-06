from django.core.management.base import BaseCommand
import datetime
import sys
sys.path.insert(0, 'C:/Pythondjango/Firstdjango/firstapp/')

from models import Mail, VerCode, CreateAccount

class Command(BaseCommand):

    help = 'Expires event objects which are out-of-date'

    def handle(self, *args, **options):
        print VerCode.objects.filter(date__lt=datetime.datetime.now()).delete()
        print Mail.objects.filter(date__lt=datetime.datetime.now()).delete()
        print CreateAccount.objects.filter(date__lt=datetime.datetime.now()).delete()