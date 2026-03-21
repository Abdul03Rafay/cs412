import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs412.settings')
django.setup()

from voter_analytics.models import Voter

count = Voter.objects.count()
print(f"Total Voters: {count}")

if count > 0:
    first_voter = Voter.objects.first()
    print(f"First Voter: {first_voter}")
