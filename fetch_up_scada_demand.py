from dateutil import parser as date_parser
from django.utils import timezone
from pymongo import MongoClient
from dashboard.models import Up_scada
connection_string = "mongodb://ITTeam:memi%40123456@103.239.139.244:27017"
client = MongoClient(connection_string)

db = client.admin

scada_demand_collection = db['UP_Scada_Data']

scada_demand_instances= []
print("code before 1st query")
curr_date= Up_scada.objects.latest("date")

sort_date=curr_date.date.strftime("%Y%m%d")
for data in scada_demand_collection.find({'date_int':{'$gt':int(sort_date)}}).limit(1000):
     date= data.get('date_int',None)
     dem_date= None 
     if date:
        dem_date= timezone.datetime.strptime(str(date), "%Y%m%d")
     scada_data = {
          'block':data['block'],
          'date':dem_date,
          'volume': data['volume'],
     }
     scada_demand_instances.append(scada_data)

Up_scada.objects.bulk_create(scada_demand_instances)