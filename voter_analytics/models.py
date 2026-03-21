# File: voter_analytics/models.py
# Author: Abdul Rafay (rafaya@bu.edu), 3/20/2026
# Description: Model definition for Voter and function to load data from CSV.

from django.db import models
import csv
from datetime import datetime

class Voter(models.Model):
    '''
    Store/represent the data from one registered voter in Newton, MA.
    '''
    # identification
    last_name = models.TextField()
    first_name = models.TextField()
    
    # residential address
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True, null=True)
    zip_code = models.TextField()
    
    # dates
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    
    # party and precinct
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.TextField()
    
    # election participation
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    
    # voter score
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.street_number} {self.street_name}, Precinct {self.precinct_number})'

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    
    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()

    filename = '/Users/abdulrafay/Desktop/django/newton_voters.csv'
    
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            try:
                # helper to convert TRUE/FALSE string to boolean
                def to_bool(val):
                    return val.strip().upper() == 'TRUE'
                
                # handle integer conversions safely
                def to_int(val):
                    try:
                        return int(val)
                    except ValueError:
                        return 0 # or some default

                voter = Voter(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_number=to_int(row['Residential Address - Street Number']),
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row['Residential Address - Apartment Number'],
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=row['Date of Birth'],
                    date_of_registration=row['Date of Registration'],
                    party_affiliation=row['Party Affiliation'].strip(),
                    precinct_number=row['Precinct Number'],
                    v20state=to_bool(row['v20state']),
                    v21town=to_bool(row['v21town']),
                    v21primary=to_bool(row['v21primary']),
                    v22general=to_bool(row['v22general']),
                    v23town=to_bool(row['v23town']),
                    voter_score=to_int(row['voter_score']),
                )
                voter.save()
            except Exception as e:
                # print(f"Skipped row due to error: {e}. Row: {row}")
                pass
    
    print(f'Done. Created {Voter.objects.count()} Voters.')
