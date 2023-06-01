
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import F
from django.contrib.auth import views as auth_views
# Create your views here.
import json
from dashboard.utils.helper import *
from django.core.cache import cache
import ast
import random
from operator import attrgetter
import itertools
from itertools import chain
# from chartjs.views.lines import BaseLineChartView
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q
from .models import *
from .forms import *
from locations.models import *
from datetime import datetime
from datetime import timedelta
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.contrib.auth import login, logout, authenticate
import operator
from django.views import View
from dateutil.parser import parse
from django.http import JsonResponse

print("this view")
BLOCK_CONSTANTS = [
     'block1', 'block2', 'block3', 'block4', 'block5', 'block6', 'block7', 'block8', 'block9', 'block10', 'block11',
     'block12', 'block13', 'block14', 'block15', 'block16', 'block17', 'block18', 'block19', 'block20', 'block21',
     'block22', 'block23', 'block24', 'block25', 'block26', 'block27', 'block28', 'block29', 'block30', 'block31',
     'block32', 'block33', 'block34', 'block35', 'block36', 'block37', 'block38', 'block39', 'block40', 'block41',
     'block42', 'block43', 'block44', 'block45', 'block46', 'block47', 'block48', 'block49', 'block50', 'block51',
     'block52', 'block53', 'block54', 'block55', 'block56', 'block57', 'block58', 'block59', 'block60', 'block61',
     'block62', 'block63', 'block64', 'block65', 'block66', 'block67', 'block68', 'block69', 'block70', 'block71',
     'block72', 'block73', 'block74', 'block75', 'block76', 'block77', 'block78', 'block79', 'block80', 'block81',
     'block82', 'block83', 'block84', 'block85', 'block86', 'block87', 'block88', 'block89', 'block90', 'block91',
     'block92', 'block93', 'block94', 'block95', 'block96'
 ]

BLOCK_CONSTANTS_weather = ['block0',
     'block1', 'block2', 'block3', 'block4', 'block5', 'block6', 'block7', 'block8', 'block9', 'block10', 'block11',
     'block12', 'block13', 'block14', 'block15', 'block16', 'block17', 'block18', 'block19', 'block20', 'block21',
     'block22', 'block23']

border_colors = [
            'indianred', 'salmon', 'darksalmon', 'crimson', 'red', 'darkred', 'pink', 'hotpink', 'deeppink',
            'palevioletred', 'coral', 'tomato', 'orangered', 'darkorange', 'orange', 'gold', 'palegoldenrod',
            'darkkhaki', 'thistle', 'plum', 'violet', 'orchid', 'fuchsia', 'magenta', 'rebeccapurple', 'blueviolet',
            'darkviolet', 'darkorchid', 'darkmagenta', 'purple', 'indigo', 'slateblue', 'darkslateblue', 'greenyellow',
            'lawngreen', 'limegreen', 'springgreen', 'seagreen', 'forestgreen', 'green', 'darkgreen', 'yellowgreen',
            'olivedrab', 'darkolivegreen', 'darkseagreen', 'darkcyan', 'teal', 'cyan', 'aquamarine', 'turquoise',
            'darkturquoise', 'cadetblue', 'steelblue', 'powderblue', 'skyblue', 'deepskyblue', 'dodgerblue',
            'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'navy', 'midnightblue', 'burlywood', 'tan', 'rosybrown',
            'sandybrown', 'goldenrod', 'darkgoldenrod', 'peru', 'chocolate', 'saddlebrown', 'sienna', 'brown', 'maroon',
             'darkgray', 'darkslategray', 'black'
        ]
weather_parameters= ['cloud_cover','precip_chance','pressure_mean_sea_level','qpf','qpf_snow',
                        'relative_humidity','temperature','temperature_dew_point','temperature_feels_like',
                        'temperature_heat_index','temperature_wind_chill','uv_index','visibility','wind_direction',
                        'wind_gust','wind_speed','wx_severity']
zones= {'Central':'CZ','East':'EZ','West': 'WZ','South':'SZ','North': 'NZ'}
discoms={'Madhya Pradesh': 'MP'}


class WeatherPostView(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax(): 
         state_input = self.request.POST.get('state',1)
         weather1=[]
         w1selected_cities =self.request.POST.get('w1city_selected', None)
         w1selected_cities = json.loads(w1selected_cities)
         weather_date = self.request.POST.get('wdate', '2021-08-23')
         refdate=self.request.POST.get('wdate_ref', '2021-08-24') 
         p1= self.request.POST.get('p1', 'temperature')  
         p2= self.request.POST.get('p2', 'temperature_dew_point')
         if not p1:
             p1='temperature'
         if not p2:
             p2='temperature_dew_point'
         weather1.append(p1)
         weather1.append(p2)
         weather_data0_ref=[]
         weather_data0=[]
         weather_data1=[]
         if state_input:
            state_weather= State.objects.get(id=state_input).code
            state= State.objects.get(id=state_input)
            get_cities= dict(state.city_set.values_list('name', 'geocode'))     
         else:
            get_cities={}
       

        all_cities=list(get_cities.keys())
        selected_cities = {}
        #for selected cities dictionary
        if w1selected_cities:
            for city in w1selected_cities: 
                selected_cities[city]= get_cities[city]            
        city_labels= []
        for city in all_cities:
            weather_label= [i for i in range(1, 25)]
            label= city + ';' +  str(weather_label)
            city_labels.append(label)


        weather_date = self.request.GET.get('weather_date', '2021-08-23')
       
        if weather1:
            for f in weather1: 
                if weather_date is not '' and weather_date is not None : 
                    if len(w1selected_cities)> 0 :
                       weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=selected_cities.values())
                       weather_data_date = list(weather_qs.filter(geo_code__in=list(selected_cities.values())).order_by('city','block').distinct('city','block').values('block',f,'date',city_name=F('city__name'),))
                    #    print("weather_data_date", weather_data_date )
                    else:
                        weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=get_cities.values())
                        weather_data_date = list(weather_qs.filter(geo_code__in=list(get_cities.values())).order_by('city','block').distinct('city','block').values('block',f,'date',city_name=F('city__name'),)) 
                    weather_data0.append(weather_data_date)
                    # print("weather_data0", weather_data0)
                if refdate is not '' and refdate is not  None:
                    # print("refdate", refdate)
                    if len(w1selected_cities)> 0 :
                        weather_qs = Weather.objects.filter(date=refdate, geo_code__in=selected_cities.values())
                        weather_data_ref = list(weather_qs.filter(geo_code__in=list(selected_cities.values())).order_by('city','block').distinct('city','block').values('block',f, 'date',city_name=F('city__name'))) 
                    else: 
                        weather_qs = Weather.objects.filter(date=refdate, geo_code__in=get_cities.values())
                        weather_data_ref = list(weather_qs.filter(geo_code__in=list(get_cities.values())).order_by('city','block').distinct('city','block').values('block',f, 'date',city_name=F('city__name')))   
                    weather_data0_ref.append(weather_data_ref)
            weather_data_one= weather_data0 + weather_data0_ref
            return JsonResponse(weather_data_one,safe=False)
        else:
            # your code to handle non-AJAX POST requests
            pass

class Weather2PostView(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax(): 
         state_input = self.request.POST.get('state',1)
         weather1=[]
         weather_date = self.request.POST.get('wdate', '2021-08-23')
         w1selected_cities =self.request.POST.get('w1city_selected', None)
         w1selected_cities = json.loads(w1selected_cities)
         
         refdate=self.request.POST.get('wdate_ref', '2021-08-24') 
         p1= request.POST.get('p1', 'temperature')  
         p2= request.POST.get('p2', 'temperature_dew_point')
         if not p1:
             p1='temperature'
         if not p2:
             p2='temperature_dew_point'
         weather1.append(p1)
         weather1.append(p2)
        
        
         weather_data0_ref=[]
         weather_data0=[]
         weather_data1=[]
         if state_input:
            state_weather= State.objects.get(id=state_input).code
            state= State.objects.get(id=state_input)
            get_cities= dict(state.city_set.values_list('name', 'geocode'))     

         else:
            get_cities={}
       

        all_cities=list(get_cities.keys())
        selected_cities = {}
        #for selected cities dictiona
        if w1selected_cities:
            for city in w1selected_cities: 
               selected_cities[city]= get_cities[city]
        

        
            
        city_labels= []
        for city in all_cities:
            weather_label= [i for i in range(1, 25)]
            label= city + ';' +  str(weather_label)
            city_labels.append(label)
       
        if weather1:
            for f in weather1: 
                if weather_date is not '' and weather_date is not None : 
                    if len(w1selected_cities)> 0 :
                       weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=selected_cities.values())
                       
                       weather_data_date = list(weather_qs.filter(geo_code__in=list(selected_cities.values())).order_by('city','block').distinct('city','block').values('block',f,'date',city_name=F('city__name'),))
                       print("weather_data_date", weather_data_date )
                    else:
                        weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=get_cities.values())
                        weather_data_date = list(weather_qs.filter(geo_code__in=list(get_cities.values())).order_by('city','block').distinct('city','block').values('block',f,'date',city_name=F('city__name'),)) 
                    weather_data0.append(weather_data_date)
                    # print("weather_data0", weather_data0)
                if refdate is not '' and refdate is not  None:
                    # print("refdate", refdate)
                    if len(w1selected_cities)> 0 :
                        weather_qs = Weather.objects.filter(date=refdate, geo_code__in=selected_cities.values())
                        weather_data_ref = list(weather_qs.filter(geo_code__in=list(selected_cities.values())).order_by('city','block').distinct('city','block').values('block',f, 'date',city_name=F('city__name'))) 
                    else: 
                        weather_qs = Weather.objects.filter(date=refdate, geo_code__in=get_cities.values())
                        weather_data_ref = list(weather_qs.filter(geo_code__in=list(get_cities.values())).order_by('city','block').distinct('city','block').values('block',f, 'date',city_name=F('city__name')))   
                    weather_data0_ref.append(weather_data_ref)
            weather2_data_one= weather_data0 + weather_data0_ref
            
           
            return JsonResponse(weather2_data_one,safe=False)
        else:
            # your code to handle non-AJAX POST requests
            pass

class Weather3PostView(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax(): 
         state_input = self.request.POST.get('state',1)
         weather1=[]
         weather_date = self.request.POST.get('wdate', '2021-08-23')
         w1selected_cities =self.request.POST.get('w1city_selected', None)
         w1selected_cities = json.loads(w1selected_cities)
         
        
         refdate=self.request.POST.get('wdate_ref', '2021-08-24')
         p1= self.request.POST.get('p1', 'temperature')  
         p2= self.request.POST.get('p2', 'temperature_dew_point')
         if not p1:
             p1='temperature'
         if not p2:
             p2='temperature_dew_point'
         weather1.append(p1)
         weather1.append(p2)
         weather_data0_ref=[]
         weather_data0=[]
         weather_data1=[]
         if state_input:
            state_weather= State.objects.get(id=state_input).code
            state= State.objects.get(id=state_input)
            get_cities= dict(state.city_set.values_list('name', 'geocode'))     
            print("get_cities_initial", get_cities)
         else:
            get_cities={}
        print("weather1........",weather1)

        all_cities=list(get_cities.keys())
        selected_cities = {}
        #for selected cities dictionary
       
        if w1selected_cities:
            for city in w1selected_cities: 
               selected_cities[city]= get_cities[city]
        
        print("selected cities",selected_cities, "len(w1selected_cities)", len(w1selected_cities) )
            
        city_labels= []
        for city in all_cities:
            weather_label= [i for i in range(1, 25)]
            label= city + ';' +  str(weather_label)
            city_labels.append(label)
        
        if weather1:
            for f in weather1: 
                if weather_date is not '' and weather_date is not None : 
                    if len(w1selected_cities)> 0 :
                       weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=selected_cities.values())
                       print("weatherqs", weather_qs )
                       weather_data_date = list(weather_qs.filter(geo_code__in=list(selected_cities.values())).order_by('city','block').distinct('city','block').values('block',f,'date',city_name=F('city__name'),))
                       print("weather_data_date", weather_data_date )
                    else:
                        weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=get_cities.values())
                        weather_data_date = list(weather_qs.filter(geo_code__in=list(get_cities.values())).order_by('city','block').distinct('city','block').values('block',f,'date',city_name=F('city__name'),)) 
                    weather_data0.append(weather_data_date)
                    # print("weather_data0", weather_data0)
                if refdate is not '' and refdate is not  None:
                    # print("refdate", refdate)
                    if len(w1selected_cities)> 0 :
                        weather_qs = Weather.objects.filter(date=refdate, geo_code__in=selected_cities.values())
                        weather_data_ref = list(weather_qs.filter(geo_code__in=list(selected_cities.values())).order_by('city','block').distinct('city','block').values('block',f, 'date',city_name=F('city__name'))) 
                    else: 
                        weather_qs = Weather.objects.filter(date=refdate, geo_code__in=get_cities.values())
                        weather_data_ref = list(weather_qs.filter(geo_code__in=list(get_cities.values())).order_by('city','block').distinct('city','block').values('block',f, 'date',city_name=F('city__name')))   
                    weather_data0_ref.append(weather_data_ref)
            weather_data_one= weather_data0 + weather_data0_ref
            
            # print("weather_data_one",weather_data_one)
            
           
            return JsonResponse(weather_data_one,safe=False)
        else:
            # your code to handle non-AJAX POST requests
            pass




class ForecastDashboardView(TemplateView):
    print("in function")
    template_name = 'dashboard/assets/templates/index.html'

    def current_forecast_version(self):
        version=cache.get('forecast_version')

        if not version :
            version=1
            cache.set('forecast_version',version,3600)
        return version


    def post(self, request, *args, **kwargs):
        action = request.POST.get('Action')
        corr_data=request.POST.get('corr_data')
        corr_data_clr=request.POST.get('corrdata_clr')
        scadaflag=request.POST.get('scada')
        actualflag=request.POST.get('actual')
        memiflag=request.POST.get('memi')
        ensmbleflag=request.POST.get('ensmbl')
        todays_date="2023-05-19"
        tomorrow_date=datetime.strptime(todays_date, '%Y-%m-%d') + timedelta(days=1)
        tomorrow_date = tomorrow_date.strftime('%Y-%m-%d')
        print(memiflag,"memiflag")
        if action:
           
            from_val = request.POST.get('fromVal')
            to_val = request.POST.get('toVal')
            from_block = request.POST.get('fromBlock')
            to_block = request.POST.get('toBlock')
            action = request.POST.get('Action')
            date = request.POST.get('Date')
            state = request.POST.get('state')
            demand = request.POST.get('chartdata')
            demand =json.loads(demand)
            forecast_dict = next(i for i in demand if i['name'] == 'forecast')
            
            
               
            if demand is not None:
                    block_values = forecast_dict['data']
                    block_values_dict= dict(zip(BLOCK_CONSTANTS,block_values))
                    from_block = int(from_block)
                    to_block= int(to_block)
                    from_value=float(from_val)
                    to_value=float(to_val)
                      
                    if action == "Multiply": 
                        multipled_demand= multiply_action(block_values_dict, from_block, to_block, from_value, to_value)
                        block_values_dict.update(**multipled_demand)
                        # self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                        forecast_dataset= list(block_values_dict.values())
                        
                        for d in demand:
                            if d['name']=='forecast':
                                d['data']=forecast_dataset
                       
                       
                    if action == "Average": 
                        avgdate=  self.request.POST.get('avgdate') 
                       
                        averageref=  Actual_demands.objects.filter( state__iexact="Uttar Pradesh",date=avgdate).order_by('block')
                        averageref_blockValues= []
                        
                        for d in averageref: 
                             block_values = d.demand
                             averageref_blockValues.append(block_values)
                        averageref_dict=dict(zip(BLOCK_CONSTANTS,averageref_blockValues))
                        
                        
                        average_demand= average_action(block_values_dict,averageref_dict, from_block, to_block, from_value, to_value)
                        block_values_dict.update(**average_demand)
                        # self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                        forecast_dataset= list(block_values_dict.values())
                        for d in demand:
                            if d['name']=='forecast':
                                d['data']=forecast_dataset
                    if action == "Shift left":
                        Shiftleft_demand= shift_left_action(block_values_dict, from_block, to_block, from_value, to_value)
                        
                        block_values_dict.update(**Shiftleft_demand)
                        # self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                        forecast_dataset= list(block_values_dict.values())
                        for d in demand:
                            if d['name']=='forecast':
                                d['data']=forecast_dataset
                    if action == "Shift right":
                        Shiftright_demand= shift_right_action(block_values_dict, from_block, to_block, from_value, to_value)
                        block_values_dict.update(**Shiftright_demand)
                        # self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                        forecast_dataset= list(block_values_dict.values())
                        for d in demand:
                            if d['name']=='forecast':
                                d['data']=forecast_dataset
                    if action == "Smooth":
                        smooth_demand= smooth_action(block_values_dict, from_block, to_block, from_value, to_value)
                        block_values_dict.update(**smooth_demand)
                        # self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                        forecast_dataset= list(block_values_dict.values())
                        for d in demand:
                            if d['name']=='forecast':
                                d['data']=forecast_dataset

            demand=json.dumps(demand)
                
            return JsonResponse(demand,safe=False)
        if corr_data:
             actDates= self.request.POST.getlist('actDates[]')
             tempdate= self.request.POST.getlist('tempdate[]')
             tempfdate= self.request.POST.getlist('tempfdate[]')
             demcorrdate=self.request.POST.getlist('actDates[]')
             demand = self.request.POST.get('chartdata')
             demand =json.loads(demand)
             all_corrdates= list(set(actDates+tempdate+tempfdate+demcorrdate))

             for date in all_corrdates:
               corr_demands= Actual_demands.objects.filter( state__iexact="Uttar Pradesh",date=date)
               corr_demand_blockValues=[]
               for d in corr_demands:
                   block_values = d.demand
                   corr_demand_blockValues.append(block_values)
               demand.append({
                   'name': "corrdate" +" "+ date ,
                   'data': corr_demand_blockValues,
                   })
    
             demand=json.dumps(demand)
             return JsonResponse(demand,safe=False)
        if corr_data_clr:
           demand= request.POST.get('chartdata')
           demand =json.loads(demand)
          
           demand = [d for d in demand if not d.get("name", "").startswith("corrdate")]
           print("chartdata", demand)
           demand=json.dumps(demand)
           return JsonResponse(demand,safe=False)
        if scadaflag:
           
            if scadaflag == "scadaon":
               demand= request.POST.get('chartdata')
               demand =json.loads(demand)
               scadademand=Up_scada.objects.filter(date=todays_date)
               scada_blockvalues= []

               for d in  scadademand:
                        block_value= d.volume
                        scada_blockvalues.append(block_value)
                    
               demand.append({
                            'name': 'Scada',
                            'data':scada_blockvalues,
                    })
               
            else:   
              demand= request.POST.get('chartdata')
              demand =json.loads(demand)
              demand = [d for d in demand if not d.get("name", "").startswith("Scada")]
            demand=json.dumps(demand)  
            return JsonResponse(demand,safe=False)
        if actualflag:
           
            if actualflag == "actualon":
               demand= request.POST.get('chartdata')
               demand =json.loads(demand)
               actualdemand=Actual_demands.objects.filter( state__iexact="Uttar Pradesh",date=todays_date).order_by('block')
               actual_demand_blockValues= []
               for d in actualdemand: 
                    block_values = d.demand
                    actual_demand_blockValues.append(block_values)
               demand.append({
                    'name': 'Actual'+':' +" "+ str(todays_date) ,
                    'data': actual_demand_blockValues,  
                })
               
            else:   
              demand= request.POST.get('chartdata')
              demand =json.loads(demand)
              print(demand,"sauvik")
              demand = [d for d in demand if not d.get("name", "").startswith("Actual")]
            demand=json.dumps(demand)  
            return JsonResponse(demand,safe=False)
        
        if memiflag:
          
            if memiflag == "memion":
               demand= request.POST.get('chartdata')
               demand =json.loads(demand)
               memi_today_blks=[]
               memidemand=Forecast_Master.objects.filter( forecast_type__iexact='Manual',date=todays_date,forecast_term='DAM',loc_ID="INDUP000000").first()
               block_values = list(attrgetter(*BLOCK_CONSTANTS)(memidemand))
               memi_today_blks.extend(block_values)
               demand.append({
                                   'name': 'MEMI',
                                   'data':memi_today_blks,
                           })
               
            else:   
             
              demand= request.POST.get('chartdata')
              demand =json.loads(demand)
             
              demand = [d for d in demand if not d.get("name", "").startswith("MEMI")]
            demand=json.dumps(demand)  
            return JsonResponse(demand,safe=False)
        if ensmbleflag:
            print("sauvik ens")
            if ensmbleflag == "ensmblon":
               print("ensmblon sauvik")
               demand= request.POST.get('chartdata')
               demand =json.loads(demand)
               ensemble_blockvalues= []
               print(demand,"sauvik1")
               ensmbldemand=ensemble.objects.filter(ID="INDUP000000",date=tomorrow_date,Type="Type_1" )
               for d in  ensmbldemand:
                    block_value= d.Final_forecast
                    ensemble_blockvalues.append(block_value)
                
               demand.append({
                'name': 'Ensemble',
                
                'data': ensemble_blockvalues,
                
                })
               print(demand,"sauvik2") 
            else:   
             
              demand= request.POST.get('chartdata')
        
              demand =json.loads(demand)
             
              demand = [d for d in demand if not d.get("name", "").startswith("Ensemble")]

            demand=json.dumps(demand)  
            print(demand,"after rem")
            return JsonResponse(demand,safe=False)



        if request.is_ajax():
            print("request.POST",request.POST)
            state = request.POST.get('state')
            zones = request.POST.get('zones')
            date = request.POST.get('date')
            ftype = request.POST.get('ftype')
            ftype = json.loads(ftype)
            datasets=request.POST.get('chartdata')
            datasets=json.loads( datasets)
            
            
            if state == "3":
                if zones is not None:
                    getstate= list(StateZone.objects.filter(state=state,discom= zones ).values_list('unique_id', flat=True))
                else:
                    getstate= list(StateZone.objects.filter(state=state).values_list('unique_id', flat=True))
            else: 
                print('stateinput not 3')
                getstate= list(StateZone.objects.filter(state=state).values_list('unique_id', flat=True))  
            print('ftype',ftype)
            print('date',date)
            print('getstate',getstate)
           
            demand_datas= Forecast_Master.objects.filter(forecast_type__in=ftype,date=date,loc_ID__in=getstate).distinct()
            for demand_data in demand_datas:

                block_values = attrgetter(*BLOCK_CONSTANTS)(demand_data)
                print("block_values_demand",block_values)
              
                datasets.append({
                    'name': demand_data.forecast_type,
                    # 'borderColor': color,
                    # 'borderWidth': 2, 
                    'data': block_values,
                    # 'fill': False,
                    # 'borderDash': [5,2.5]
                })
            datasets=json.dumps(datasets)
            return JsonResponse(datasets, safe=False)
        else:
            # your code to handle non-AJAX POST requests
            pass
    def GET(self, request, *args, **kwargs):
     if request.is_ajax():
        print("doc ready")
        data = {
            'message': 'This is a message from the server!',
            'value': 42,
            'success': True
        }
        return JsonResponse(data) 
     else:
           print("doc not ready")
           pass       


    def get_forecast_demand(self, demand,version=1):
        # Set user's pk as the key for the forecast dataset.
        
       demand_data = cache.get(str(self.request.user), version=version)
       print(demand,"get forecast demand")
       if demand: 
            if  demand_data :
                print("demand_instance in cache", demand_data)

        
            if not  demand_data :
                temp_dict = dict(demand.__dict__.items())
               
                temp_dict.pop('_state',None)

                demand_instance=Forecast_Master(**temp_dict)
                demand_data = {'data':demand_instance, 'version':version}
                cache.set(str(self.request.user),  demand_data, 3600,version=version)

            return  demand_data.get('data')

    def is_date(self,string, fuzzy=False):
        try: 
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False 
        

   

    def update_forecast_demand(self,demand,block_values,version=1):

        demand = self.get_forecast_demand(demand,version=version)
        version+=1
        temp_dict = dict(demand.__dict__.items())
        temp_dict.pop('_state',None)
        temp_dict.pop('_django_version',None)   
        temp_dict.update(**block_values)
        # print("temp_dict.......",temp_dict)
        demand = Forecast_Master(**temp_dict)
        print("demand.......",demand)
        cache.set(str(self.request.user), {'data':demand, 'version':version}, 3600,version=version)
        cache.set('forecast_version',version,3600)
        return demand

    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        form= StateForm()
        formz=DiscomForm()
        base_demand= self.request.GET.get('base', None)
        avg_ref_demand=self.request.GET.get('avgRef', None)
        # todays_date= datetime.today().strftime('%Y-%m-%d')
        todays_date="2023-05-19"
        tomorrow_date=datetime.strptime(todays_date, '%Y-%m-%d') + timedelta(days=1)
        tomorrow_date = tomorrow_date.strftime('%Y-%m-%d')
     
        Actual_date= self.request.GET.getlist('Actual', None)
        Actual_date= Actual_date if Actual_date else todays_date
        print("todays_date Actual_date",Actual_date)
        Actual_date= datetime.strptime(Actual_date, '%Y-%m-%d').date()
        corr_type= self.request.GET.get('w_correl_type', None)
        date = self.request.GET.get('date', '2022-07-27')
        corrdates =[]
        t_corr_date= self.request.GET.getlist('t_correl_date', None)
        tf_corr_date= self.request.GET.getlist('tf_correl_date', None)
        d_corr_date= self.request.GET.getlist('d_row', None)
        n_corr_date= self.request.GET.getlist('n_row', None)
        w1selected_cities =self.request.GET.getlist('w1city_selected', None)
        scada_flag = self.request.GET.get('enable_scada',None)
        ensemble_flag= self.request.GET.get('enable_ensemble',None)
        print("w1selected_cities", w1selected_cities)
        print("scada_flag...", scada_flag)
        print("ensemble_flag...", ensemble_flag)
        if tf_corr_date  :
            corrdates.extend(tf_corr_date)
        if t_corr_date  :
            corrdates.extend(t_corr_date)
        if d_corr_date :
            corrdates.extend(d_corr_date)
        if n_corr_date :
            corrdates.extend(n_corr_date)


        if date == '':
            date = datetime.now().date()
        print("date....", type(date))
        state_input = self.request.GET.get('state', 1)
        print("state_input....",state_input)
        
        if state_input == "3":
            if self.request.GET.get('zones'):
            
                getstate= list(StateZone.objects.filter(state=state_input,discom= self.request.GET.get('zones') ).values_list('unique_id', flat=True))
                print('zone if state and zone both')
                
            else:
                getstate= list(StateZone.objects.filter(state=state_input).values_list('unique_id', flat=True))
                print(' zone if state only')
        else: 
            print('stateinput not 3')
            getstate= list(StateZone.objects.filter(state=int(state_input)).values_list('unique_id', flat=True))
        

        if state_input:
            state_weather= State.objects.get(id=state_input).code
            state= State.objects.get(id=state_input)
            get_cities= dict(state.city_set.values_list('name', 'geocode'))     
            print("get_cities_initial", get_cities)
        else:
            get_cities={}

       

        all_cities=list(get_cities.keys())
        
       
        print("get_cities", get_cities)   
        print("allselected_cities",all_cities)
        selected_cities = {}
        #for selected cities dictionary
        for city in w1selected_cities:
            selected_cities[city]= get_cities[city]
        
        print("selected cities",selected_cities, "len(w1selected_cities)", len(w1selected_cities) )
            
        city_labels= []
        for city in all_cities:
            weather_label= [i for i in range(1, 25)]
            label= city + ';' +  str(weather_label)
            city_labels.append(label)
        print("citylabel", city_labels)
        weather_date = self.request.GET.get('weather_date', '2021-08-23')
        print("weather_date....",weather_date)
    
        refdate=self.request.GET.get('refdate', '2021-08-24')
        print("ref_date....",refdate)
        action = self.request.GET.get('Action', None)

        
        forecast_types=[]
        weather1 = None
        weather2 = None
        
        forecast_types = self.request.GET.getlist('ftype','TLD_Forecast')
       
        
        print("forecast_types",forecast_types)
        # print("request.get",self.request.GET )
        if 'chart1_weather' in self.request.GET:
            weather1=self.request.GET.getlist('chart1_weather')
        else: 
              weather1 = ['temperature_heat_index', 'temperature_feels_like']

        if 'chart2_weather' in self.request.GET:     
            weather2=self.request.GET.getlist('chart2_weather', None)
        else: 
            weather2 = ['temperature_heat_index', 'temperature_feels_like']   
       
        weather3=self.request.GET.getlist('chart3_weather', ['temperature_heat_index', 'temperature_feels_like'])
        # print("request.get",self.request.GET.get )
        print(" weather1", weather1)
        # print(" weather2", weather2)
        if len(getstate) != 0 and "MP" not in getstate[0] :
             print("in 5 slice")
             corr_state = getstate[0]
             corr_state= corr_state[:5]
        elif "INDMP"== getstate[0][:5]:
            print("in 7 slice")
            corr_state = getstate[0]
            corr_state= corr_state[:7]
        else:
            corr_state=''
       
       # nearby and corr dates
        n_by_dates= ''
        if date :
            n_date=datetime.strptime(str(date), '%Y-%m-%d')
            # print('n_date',n_date)
            n_by_dates= []
            nearby_date_1= n_date -  timedelta(days=1,)
            nearby_date_1= nearby_date_1.strftime('%Y-%m-%d')
            nearby_date_2= n_date -  timedelta(days=2,)
            nearby_date_2= nearby_date_2.strftime('%Y-%m-%d')
            nearby_date_3= n_date -  timedelta(days=3,)
            nearby_date_3= nearby_date_3.strftime('%Y-%m-%d')
            n_by_dates.extend([nearby_date_1,nearby_date_2,nearby_date_3])
            
        print('n_by_dates',n_by_dates)

        
        print('date_corr',date,'corr_state',corr_state,'w_correl_type',corr_type )
        temp_corr_data= list(corr_dates.objects.filter(Date=tomorrow_date, loc_ID=corr_state,Item_ID="temp_Corr").values_list('Ref_date').order_by('Rank')[:3])
        tempf_corr_data= list(corr_dates.objects.filter(Date=tomorrow_date, loc_ID=corr_state,Item_ID="tempf_Corr").values_list('Ref_date').order_by('Rank')[:3])
        temp_corr_data=[str(w[0]) for w in temp_corr_data]
        tempf_corr_data=[str(w[0]) for w in tempf_corr_data]
       
        
        d_corr_data= list(corr_dates.objects.filter(Date=tomorrow_date,loc_ID=corr_state,Item_ID='Demand_corr').values_list('Ref_date').order_by('Rank')[:3])
        d_corr_data=[str(w[0]) for w in d_corr_data]
        
        
            

        
        all_forecasttypes= list(Forecast_Master.objects.all().values_list('forecast_type', flat=True).distinct())
        date_choices = Forecast_Master.objects.all().exclude(
            date__isnull=True
        ).values_list('date', flat=True).order_by('-date').distinct()
        actual_date_choices=  Actual_demands.objects.all().exclude(
            date__isnull=True
        ).values_list('date', flat=True).order_by('-date').distinct()
        print(actual_date_choices,"actual_date_choices values")
        


        
        datasets=[]
        print("demand line date", date)
        print("demand line forecast_types", forecast_types)
        print("demand line state", getstate)
        demand_datas= Forecast_Master.objects.filter(forecast_type__in=forecast_types,date=date,loc_ID__in=getstate).distinct()
        print(demand_datas,"demand_datas123")
        # fetching Actual demand
        # if Actual_date:
        #     Actual_date_conv=[] 
        #     for d in Actual_date:
        #          try : 
        #                 Actual_date =  datetime.strptime(d, '%b. %d, %Y').strftime('%Y-%m-%d')
        #                 Actual_date_conv.append(Actual_date)
        #                 print("Actual_date converted",Actual_date)
        #          except: 
        #                 Actual_date =  datetime.strptime(d, '%b %d, %Y').strftime('%Y-%m-%d')
        #                 Actual_date_conv.append(Actual_date)
            # print("Actual_date converted",Actual_date_conv)
      
        if state_input == 1 :
                print("state_input",state_input)
                state_act= 'Uttar Pradesh'
        elif state_input == 2:
                    state_act= 'bihar'
        elif state_input == 3:
                    state_act= 'Madhya Pradesh'
        elif state_input == 4:
                    state_act= 'West Bengal' 
        print("state_act",state_act)   
        
        demand_instance_actual= Actual_demands.objects.filter( state__iexact=state_act,date=todays_date).order_by('block')
        actual_demand_blockValues= []
        print("demand_instance_actual",len(demand_instance_actual))
        for demand in demand_instance_actual: 
             block_values = demand.demand
             actual_demand_blockValues.append(block_values)
        print(actual_demand_blockValues,"actual_demand_blockValues")
        datasets.append({
                    'name': 'Actual'+':' +" "+ str(todays_date) ,
                    'data': actual_demand_blockValues,  
                })
        

         # fetching correct base demand
        if base_demand:

            if self.is_date(base_demand) and state_input is not None :
                    try: 
                        try:
                            date =  datetime.strptime(base_demand, '%b. %d, %Y').strftime('%Y-%m-%d')
                        except :
                            date =  datetime.strptime(base_demand, '%Y-%m-%d').strftime('%Y-%m-%d')
                    except: 
                        date =  datetime.strptime(base_demand, '%B %d, %Y').strftime('%Y-%m-%d')
                    
                    
                        
                    print("dateNOw",date)
                    if state_input == '1':
                        state= 'Uttar Pradesh'
                    elif state_input == '2':
                        state= 'bihar'
                    elif state_input == '3':
                        state= 'Madhya Pradesh'
                    elif state_input == '4':
                        state= 'West Bengal' 
                    print("state is ",state)
                    demand_instance= Actual_demands.objects.filter( state__iexact=state,date=date)
                    

                    base_demand_blockValues=[]
                    print("demand_instance actual",demand_instance)
                    for demand in demand_instance: 
                        block_values = demand.demand
                        base_demand_blockValues.append(block_values)
                        # print("block_values_demand actual",block_values)
                        color = random.choice(border_colors)
                        # print(block_values)
                        # if f=='ITD':
                        #     dataset1.append(block_values)
                    datasets.append({
                        'name': "Baseline : " + date ,
                        # 'borderColor': color,
                        # 'borderWidth': 2, 
                        'data': base_demand_blockValues,
                        # 'fill': False,
                        # 'borderDash': [5,2.5]
                    })
            elif self.is_date(base_demand)== False and date is not None : 
                    print("in else baseee",base_demand)
                    print("baseline date",date)
                    print("baseline loc",getstate[0])
                    base_demand_blockValues=[]
                    demand_instance= Forecast_Master.objects.filter( forecast_type__iexact=base_demand,date=date,loc_ID=getstate[0]).first()
                    if demand_instance != None: 
                        block_values = attrgetter(*BLOCK_CONSTANTS)(demand_instance)
                        base_demand_blockValues.append(block_values)
                        print("block_values_demand",block_values)
                        color = random.choice(border_colors)
                            # print(block_values)
                            # if f=='ITD':
                            #     dataset1.append(block_values)
                        datasets.append({
                            'name': "Baseline : " + demand_instance.forecast_type,
                            # 'borderColor': color,
                            # 'borderWidth': 2, 
                            'data': block_values,
                            # 'fill': False,
                            # 'borderDash': [5,2.5]
                        })
            else:
                demand_instance= Forecast_Master.objects.filter( forecast_type__iexact='TLD_Forecast',date=date,loc_ID=getstate[0]).first()
                # print("Forecast_Master object normal",demand_instance.block1)
                block_values = attrgetter(*BLOCK_CONSTANTS)(demand_instance)
                base_demand_blockValues.append(block_values)
                # print(block_values)
                # if f=='ITD':
                #     dataset1.append(block_values)
                datasets.append({
                    'name': "Baseline : " + demand_instance.forecast_type,
                    # 'borderColor': color,
                    # 'borderWidth': 2, 
                    'data': block_values,
                    # 'fill': False,
                    # 'borderDash': [5,2.5]
                })
            
        # print("demand_instance",demand_instance)
        
        # if demand_instance:
            # for demand in demand_instance: 
            #     block_values = demand.demand
            #     base_demand_blockValues.append(block_values)
            #     print("block_values_demand",block_values)
            #     color = random.choice(border_colors)
            #     # print(block_values)
            #     # if f=='ITD':
            #     #     dataset1.append(block_values)
            #     datasets.append({
            #         'name': "Baseline : " + demand_instance.forecast_type,
            #         # 'borderColor': color,
            #         # 'borderWidth': 2, 
            #         'data': block_values,
            #         # 'fill': False,
            #         # 'borderDash': [5,2.5]
            #     })
            
            
        #reference demand for average
        if avg_ref_demand: 
            if self.is_date(avg_ref_demand) and state_input is not None :
                try : 
                        date =  datetime.strptime(avg_ref_demand, '%b. %d, %Y').strftime('%Y-%m-%d')
                except: 
                        date =  datetime.strptime(avg_ref_demand, '%B %d, %Y').strftime('%Y-%m-%d')
                print("dateNOw",date)
                if state_input == '1':
                    state= 'Uttar Pradesh'
                elif state_input == '2':
                    state= 'bihar'
                elif state_input == '3':
                    state= 'Madhya Pradesh'
                elif state_input == '4':
                    state= 'West Bengal' 
                print("state is ",state)
                demand_instanceAvg_ref= Actual_demands.objects.filter( state__iexact=state,date=date)
            elif self.is_date(avg_ref_demand)== False and date is not None : 
                demand_instanceAvg_ref= Forecast_Master.objects.filter( forecast_type__iexact=base_demand,date=date,loc_ID=getstate[0]).first()

        corr_demands = Forecast_Master.objects.filter( forecast_type__iexact='ITD',date__in=corrdates,loc_ID=getstate[0]).distinct()
      
        # if date :
            # todays_date= datetime.strptime(str(date), '%Y-%m-%d')
            # ensemble_date_time= todays_date +  timedelta(days=1)
            # ensemble_date= ensemble_date_time.strftime('%Y-%m-%d')
            # print("ensemble_date", ensemble_date)
            # ensemble_demand = ensemble.objects.filter(ID=corr_state,date=ensemble_date,Type="Type_1" )
            
            # if scada_flag == "on":
            #     scada_demand= None
            #     if state_input== "1":
        scada_demand = Up_scada.objects.filter(date=todays_date)
        print(scada_demand,"scada_demand");  
        if scada_demand:    
                    scada_blockvalues= []
                    for demand in  scada_demand:
                        block_value= demand.volume
                        scada_blockvalues.append(block_value)
                    
                    datasets.append({
                            'name': 'Scada',
                            # 'borderColor': color,
                            # 'borderWidth': 2, 
                            'data':scada_blockvalues,
                            # 'fill': False,
                            # 'borderDash': [5,2.5]
                    })
        memi_today_blks=[]            
        memi_today=Forecast_Master.objects.filter( forecast_type__iexact='Manual',date=todays_date,forecast_term='DAM',loc_ID=getstate[0]).first()   
        block_values = list(attrgetter(*BLOCK_CONSTANTS)(memi_today))
        memi_today_blks.extend(block_values)
        datasets.append({
                            'name': 'MEMI',
                            # 'borderColor': color,
                            # 'borderWidth': 2, 
                            'data':memi_today_blks,
                            # 'fill': False,
                            # 'borderDash': [5,2.5]
                    })
        
        ensemble_demand = ensemble.objects.filter(ID=getstate[0],date=tomorrow_date,Type="Type_1" )
        # if ensemble_flag == "on":
        ensemble_blockvalues= []
        for demand in  ensemble_demand:
            block_value= demand.Final_forecast
            ensemble_blockvalues.append(block_value)
        datasets.append({
                'name': 'Ensemble',
                
                'data': ensemble_blockvalues,
                
                })
        
        

        for demand in corr_demands:
            block_values = attrgetter(*BLOCK_CONSTANTS)(demand)
            datasets.append({
                'name': 'correlation demand' +' ' + corrdates[i] ,
                # 'borderColor': '#00008B',
                # 'borderWidth': 2, 
                'data': block_values,
                # 'fill': False,
                # 'borderDash': [5,2.5]
            })
            i+=1
        
        for demand_data in demand_datas:
            block_values = attrgetter(*BLOCK_CONSTANTS)(demand_data)
            print("block_values_demand",block_values)
            color = random.choice(border_colors)
            # print(block_values)
            # if f=='ITD':
            #     dataset1.append(block_values)
            datasets.append({
                'name': demand_data.forecast_type,
                # 'borderColor': color,
                # 'borderWidth': 2, 
                'data': block_values,
                # 'fill': False,
                # 'borderDash': [5,2.5]
            })
        
           



       
        #DW chart ==>
        dw_weather= ['temperature', 'temperature_feels_like','wind_speed', 'cloud_cover', 'precip_chance', 'wind_gust']
        DW_datasets=[]

        for label in dw_weather:
            dw_data= Weather.objects.filter(date=date, state_code=state_weather).values_list(label).order_by('-block')[:24]
            block_values = tuple(dw_data)
            block_values = tuple(list(itertools.chain(*block_values)))
            color = random.choice(border_colors)
            DW_datasets.append({
                    'label':  label,
                    'borderColor': color,
                    'borderWidth': 2,
                    'data': block_values,
                    'fill': False
                })
              
        # print("DW_datasets",DW_datasets)
        weather_data0_ref=[]
        weather_data0=[]
        weather_data1=[]
        if weather1:
            for f in weather1: 
                if weather_date is not '' and weather_date is not None : 
                    if len(w1selected_cities)> 0 :
                       weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=selected_cities.values())
                       print("weatherqs", weather_qs )
                       weather_data_date = list(weather_qs.filter(geo_code__in=list(selected_cities.values())).order_by('city','block').distinct('city','block').values('block',f,'date',city_name=F('city__name'),))
                       print("weather_data_date", weather_data_date )
                    else:
                        weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=get_cities.values())
                        weather_data_date = list(weather_qs.filter(geo_code__in=list(get_cities.values())).order_by('city','block').distinct('city','block').values('block',f,'date',city_name=F('city__name'),)) 
                    weather_data0.append(weather_data_date)
                    # print("weather_data0", weather_data0)
                if refdate is not '' and refdate is not  None:
                    # print("refdate", refdate)
                    if len(w1selected_cities)> 0 :
                        weather_qs = Weather.objects.filter(date=refdate, geo_code__in=selected_cities.values())
                        weather_data_ref = list(weather_qs.filter(geo_code__in=list(selected_cities.values())).order_by('city','block').distinct('city','block').values('block',f, 'date',city_name=F('city__name'))) 
                    else: 
                        weather_qs = Weather.objects.filter(date=refdate, geo_code__in=get_cities.values())
                        weather_data_ref = list(weather_qs.filter(geo_code__in=list(get_cities.values())).order_by('city','block').distinct('city','block').values('block',f, 'date',city_name=F('city__name')))   
                    weather_data0_ref.append(weather_data_ref)
            weather_data1= weather_data0 + weather_data0_ref
        
        # print("weather_data1", weather_data1)
        weather2_data0_ref=[]
        weather2_data0=[]
        weather2_data1=[]
        if weather2 is not None:
            for f in weather2:
                if f != '':
                     if len(w1selected_cities)> 0 :
                        weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=selected_cities.values())
                        weather_data_date = list(weather_qs.filter(geo_code__in=list(selected_cities.values())).order_by('city','block').distinct('city','block').values('block',f,'date',city_name=F('city__name'),)) 
                     else:
                        weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=get_cities.values())
                        weather_data_date = list(weather_qs.filter(geo_code__in=list(get_cities.values())).order_by('city','block').distinct('city','block').values('block',f,'date',city_name=F('city__name'),))                       
                     weather2_data0.append(weather_data_date)
                if refdate is not None:
                    if len(w1selected_cities)> 0 :
                        weather_qs_ref = Weather.objects.filter(date=refdate, geo_code__in=selected_cities.values())
                        weather_data_ref = list(weather_qs_ref.filter(geo_code__in=list(selected_cities.values())).order_by('city','block').distinct('city','block').values('block',f, 'date',city_name=F('city__name'))) 
                    else:
                        weather_qs_ref = Weather.objects.filter(date=refdate, geo_code__in=get_cities.values())
                        weather_data_ref = list(weather_qs_ref.filter(geo_code__in=list(get_cities.values())).order_by('city','block').distinct('city','block').values('block',f, 'date',city_name=F('city__name')))    
                    weather2_data0_ref.append(weather_data_ref)
            
        weather2_data1= weather2_data0 + weather2_data0_ref
        # print("weather2",weather2_data1)
        weather3_data0_ref=[]
        weather3_data0=[]
        weather3_data1=[]
        if weather3:
            for f in weather3:
                if f is not '':
                    if len(w1selected_cities)> 0 :
                        weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=selected_cities.values())
                        weather_data_date = list(weather_qs.filter(geo_code__in=list(selected_cities.values())).order_by('city','block').distinct('city','block').values('block',f,'date',city_name=F('city__name'),))
                    else:
                        weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=get_cities.values())
                        weather_data_date = list(weather_qs.filter(geo_code__in=list(get_cities.values())).order_by('city','block').distinct('city','block').values('block',f,'date',city_name=F('city__name'),)) 
                    weather3_data0.append(weather_data_date)
                if refdate is not None:
                    if len(w1selected_cities)> 0 :
                        weather_qs_ref = Weather.objects.filter(date=refdate, geo_code__in=selected_cities.values())
                        weather_data_ref = list(weather_qs_ref.filter(geo_code__in=list(selected_cities.values())).order_by('city','block').distinct('city','block').values('block',f, 'date',city_name=F('city__name')))     
                    else:
                        weather_qs_ref = Weather.objects.filter(date=refdate, geo_code__in=get_cities.values())
                        weather_data_ref = list(weather_qs_ref.filter(geo_code__in=list(get_cities.values())).order_by('city','block').distinct('city','block').values('block',f, 'date',city_name=F('city__name')))
                    weather3_data0_ref.append(weather_data_ref) 
                    # print("weatherdata", len(list(weatherdata)))
            weather3_data1= weather3_data0 + weather3_data0_ref
                    # weather3_data1.append(weather_data_ref)
                
        
        
        for d in datasets:
            if d['name']=='Ensemble':
               
             datasets.append({
                         'name': "forecast",
                         # 'borderColor': 'red' ,
                         # 'borderWidth': 2, 
                         'data': d['data'],
                         # 'fill': False
                     }) 
        
        # demand_instance= Forecast_Master.objects.filter( forecast_type__iexact='TLD_Forecast',date=date,loc_ID=getstate[0]).first()

        forecast_dict = next(i for i in datasets if i['name'] == 'forecast')

        if self.request.GET.get('fromBlock') and  self.request.GET.get('fromBlock') is not None :

            forecast_version= self.current_forecast_version()
            
            
            
            if 'undo' in self.request.GET:
                forecast_version-= 1 
                demand=self.get_forecast_demand(demand_instance,version=forecast_version)
                block_values = attrgetter(*BLOCK_CONSTANTS)(demand)
                datasets.append({
                        'name': "forecast",
                        # 'borderColor': 'red' ,
                        # 'borderWidth': 2, 
                        'data': block_values,
                        # 'fill': False
                    })
                cache.set('forecast_version', forecast_version, 3600)
            elif 'clearall' in self.request.GET:    
                forecast_version = 1 
                demand=self.get_forecast_demand(demand_instance,version=forecast_version)
                block_values = attrgetter(*BLOCK_CONSTANTS)(demand)
                datasets.append({
                        'name': "forecast",
                        # 'borderColor': 'red' ,
                        # 'borderWidth': 2, 
                        'data': block_values,
                        # 'fill': False
                    })
                cache.set('forecast_version', forecast_version, 3600)
            else:
                # forecast_version += 1
                # cache.set('forecast_version', forecast_version, 3600)
                demand=self.get_forecast_demand(demand_instance,version=forecast_version)
              
                if demand is not None:
                    block_values = forecast_dict['data']
                    block_values_dict= dict(zip(BLOCK_CONSTANTS,block_values))
                    from_block = int(self.request.GET.get('fromBlock'))
                    to_block= int(self.request.GET.get('toBlock'))
                    color = random.choice(border_colors)
                    from_value=float(self.request.GET.get('fromVal'))
                    to_value=float(self.request.GET.get('toVal'))
                    if action == "Add":
                        added_demand= add_action(demand, from_block, to_block, from_value, to_value)
                        block_values_dict.update(**added_demand)
                        self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                        forecast_dataset= tuple(block_values_dict.values())
                        
                        datasets.append({
                            'name': "forecast",
                            # 'borderColor': 'red' ,
                            # 'borderWidth': 2, 
                            'data': forecast_dataset,
                            # 'fill': False
                        })
                    if action == "Multiply": 
                      
                        multipled_demand= multiply_action(demand, from_block, to_block, from_value, to_value)
                        
                        block_values_dict.update(**multipled_demand)
                        self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                        forecast_dataset= list(block_values_dict.values())
                        datasets.append({
                             'name': "forecast",
                            # 'borderColor': 'red' ,
                            # 'borderWidth': 2, 
                            'data': forecast_dataset,
                            # 'fill': False
                        })
                    if action == "Average": 
                        average_demand= average_action(demand, from_block, to_block, from_value, to_value)
                        block_values_dict.update(**average_demand)
                        self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                        forecast_dataset= list(block_values_dict.values())
                        datasets.append({
                             'name': "forecast",
                            # 'borderColor': 'red' ,
                            # 'borderWidth': 2, 
                            'data': forecast_dataset,
                            # 'fill': False
                        })
                    if action == "Shift left":
                        Shiftleft_demand= shift_left_action(demand, from_block, to_block, from_value, to_value)
                        block_values_dict.update(**Shiftleft_demand)
                        self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                        forecast_dataset= list(block_values_dict.values())
                        datasets.append({
                            'name': "forecast",
                            # 'borderColor': 'red' ,
                            # 'borderWidth': 2, 
                            'data': forecast_dataset,
                            # 'fill': False
                        })
                    if action == "Shift right":
                        Shiftright_demand= shift_right_action(demand, from_block, to_block, from_value, to_value)
                        block_values_dict.update(**Shiftright_demand)
                        self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                        forecast_dataset= list(block_values_dict.values())
                        datasets.append({
                            'name': "forecast",
                            # 'borderColor': 'red' ,
                            # 'borderWidth': 2, 
                            'data': forecast_dataset,
                            # 'fill': False
                        })    

                    if action == "Smooth":
                        smooth_demand= smooth_action(demand, from_block, to_block, from_value, to_value)
                        block_values_dict.update(**smooth_demand)
                        self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                        forecast_dataset= list(block_values_dict.values())
                        datasets.append({
                            'name': "forecast",
                            # 'borderColor': 'red' ,
                            # 'borderWidth': 2, 
                            'data': forecast_dataset,
                            # 'fill': False
                        })    
        actions = ['Add','Multiply','Average','Shift left','Shift right','Smooth']    
        # weatherlabels=  [[i for i in range(0, 25)] for j in range(0,len(city_labels))]
        # print("weatherlabels", weatherlabels)
       
        
        
        context['actual_date_choices'] = actual_date_choices
        context['scada_flag'] = scada_flag
        context['ensemble_flag'] = ensemble_flag
        context['weather_data_one'] = weather_data1
        context['weather2_data_one']= weather2_data1
        context['weather3_data_one']= weather3_data1
        # context['cityweather_data'] = json.dumps(cityweather_data)
        context['all_cities'] = all_cities
       
        context['datasets'] = json.dumps(datasets)
        context['labels'] = json.dumps([i for i in range(1, 97)])
        context['whther_labels'] = json.dumps([i for i in range(0, 25)])
        context['all_forecasttypes'] = all_forecasttypes
        context['forecast_types'] = forecast_types
        context['date_choices'] = date_choices
        context['n_by_dates'] = n_by_dates
        context['temp_corr_data'] = temp_corr_data
        context['tempf_corr_data'] = tempf_corr_data
        # context['w_corr_data'] = w_corr_data
        context['d_corr_data'] = d_corr_data
        context['zones'] = zones
        context['weather1']= weather1
        context['weather2']= weather2
        context['weather3']= weather2
        context['weather_date']= weather_date
        context['refdate']= refdate
        context['state_input']= state_input
        
        # context['weather_datasets']= json.dumps(weather_datasets) 
        
        context['weather_parameters']= weather_parameters
        # context['DW_datasets']= json.dumps(DW_datasets)
        context['actions']= actions
        context['form']= form
        context['formz']= formz
        context['date']= date
        
        return context
    

class LoginView(auth_views.LoginView):
    print("in login view")

class test(TemplateView):
    template_name = 'dashboard/assets/templates/test.html' 