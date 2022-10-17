from dateutil import parser as date_parser
from django.utils import timezone
from pymongo import MongoClient

from dashboard.models import Weather, corr_dates

connection_string = "mongodb://ITTeam:memi%40123456@103.239.139.244:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-256"

client = MongoClient(connection_string)

db = client.admin

corr_dates_collection = db['Correlation_table']

current_date = corr_dates.objects.latest('Date').Date

corr_dates_list = [i for i in corr_dates_collection.find({'Date':{'$gte':str(current_date)} })]

corr_dates.objects.bulk_create([
corr_dates(
loc_ID=data['ID'],Date=timezone.datetime.strptime(data['Date'],"%d-%m-%Y"),Item_ID=data['Item_ID'],Rank=data['Rank'],Ref_date=timezone.datetime.strptime(data['Ref_date'],"%d-%m-%Y"),Correlation=data['Correlation']
) for data in corr_dates_list])
 