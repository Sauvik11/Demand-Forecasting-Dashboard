
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
 

class ForecastDashboardView(TemplateView):
    template_name = 'dashboard/assets/templates/index.html' 


    def get_forecast_demand(self, demand,version=1):
        # Set user's pk as the key for the forecast dataset.
        
       demand_data = cache.get(str(self.request.user), version=version)
       print("cache.get(self.request.user)",cache.get(self.request.user))
       if demand: 
            if  demand_data :
                print("demand_instance in cache", demand_data)

        
            if not  demand_data :
                print("demand_instance not in cache")
                temp_dict = dict(demand.__dict__.items())
                temp_dict.pop('_state',None)
                
                print("temp_dict",temp_dict)
                demand_instance=Forecast_Master(**temp_dict)
                demand_data = {'data':demand_instance, 'version':version}
                cache.set(str(self.request.user),  demand_data, 3600,version=version)
                
        
            return  demand_data.get('data')
        

    def current_forecast_version(self):
        version=cache.get('forecast_version')

        if not version :
            version=1
            cache.set('forecast_version',version,3600)
        return version


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
        corr_type= self.request.GET.get('w_correl_type', None)
        date = self.request.GET.get('date', None)
        corrdates =[]
        w_corr_date= self.request.GET.get('w_row', None)
        d_corr_date= self.request.GET.get('d_row', None)
        n_corr_date= self.request.GET.get('n_row', None)
        w1selected_cities =self.request.GET.getlist('w1city_selected', None)
        print("w1selected_cities", w1selected_cities)
        if w_corr_date  :
            corrdates.append(w_corr_date)
        if d_corr_date :
            corrdates.append(d_corr_date)
        if n_corr_date :
            corrdates.append(n_corr_date)

        print("corr_dates", corrdates )

        if date == '':
            date = datetime.now().date()
        print("date....", type(date))
        state_input = self.request.GET.get('state', 1)
        print("state_input....",type(state_input))

        if state_input == "3":
            if self.request.GET.get('zones'):
            
                getstate= list(StateZone.objects.filter(state=state_input,discom= self.request.GET.get('zones') ).values_list('unique_id', flat=True))
                print('zone if state and zone both')
                
            elif self.request.GET.get('discom'):
                getstate= list(StateZone.objects.filter(state=state_input,discom= self.request.GET.get('discom') ).values_list('unique_id', flat=True))
                print('zone if state and discom both')
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
        # print("getstate ...........", getstate)
        weather_date=self.request.GET.get('weather_date', None)
        refdate=self.request.GET.get('refdate', None)
        action = self.request.GET.get('Action', None)
        
        forecast_types=[]
        weather1 = None
        weather2 = None
        if "ftype" in self.request.GET:
            forecast_types = self.request.GET.getlist('ftype')
        else:
            forecast_types=''
        
        # print("forecast_types",forecast_types)
        # print("request.get",self.request.GET )
        if 'chart1_weather' in self.request.GET:
            weather1=self.request.GET.getlist('chart1_weather', None)
        elif 'chart1.2_weather' in self.request.GET:
             weather1=self.request.GET.get('chart1.2_weather', None)
             weather1 = ast.literal_eval(weather1) 
        if 'chart2_weather' in self.request.GET:     
            weather2=self.request.GET.getlist('chart2_weather', None)
        elif 'chart2.2_weather' in self.request.GET:
             weather2=self.request.GET.get('chart2.2_weather', None)
             weather2 = ast.literal_eval(weather2)     
        weather3=self.request.GET.getlist('chart3_weather', None)
        # print("request.get",self.request.GET.get )
        # print(" weather1", type(weather1))
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
            
            # print('n_by_dates',n_by_dates)

        
        print('date_corr',date,'corr_state',corr_state,'w_correl_type',corr_type )
        w_corr_data= list(corr_dates.objects.filter(Date=date, loc_ID=corr_state,Item_ID=corr_type).values_list('Ref_date').order_by('Rank')[:3])
        w_corr_data=[str(w[0]) for w in w_corr_data]
        # print('w_corr_data',w_corr_data)
        
        d_corr_data= list(corr_dates.objects.filter(Date=date,loc_ID=corr_state,Item_ID='Demand_corr').values_list('Ref_date').order_by('Rank')[:3])
        d_corr_data=[str(w[0]) for w in d_corr_data]
        # print('d_corr_data',d_corr_data)
        
        
            

        
        all_forecasttypes= list(Forecast_Master.objects.all().values_list('forecast_type', flat=True).distinct())
        date_choices = Forecast_Master.objects.all().exclude(
            date__isnull=True
        ).values_list('date', flat=True).order_by('-date').distinct()


        
        datasets=[]
        demand_datas= Forecast_Master.objects.filter(forecast_type__in=forecast_types,date=date,loc_ID__in=getstate).distinct()
        

        # corr demands
        corr_demands = Forecast_Master.objects.filter( forecast_type__iexact='ITD',date__in=corrdates,loc_ID=getstate[0]).distinct()
        # print("corr_demands....", corr_demands)
        if date:
            todays_date= datetime.strptime(str(date), '%Y-%m-%d')
            ensemble_date_time= todays_date +  timedelta(days=1)
            ensemble_date= ensemble_date_time.strftime('%Y-%m-%d')
            print("ensemble_date", ensemble_date)
            ensemble_demand = ensemble.objects.filter(ID=corr_state,date=ensemble_date,Type="Type_1" )
            print("ensemble_demand",ensemble_demand)
            
            scada_demand= None
            if state_input== "1":
                scada_demand =  Up_scada.objects.filter(date='2022-11-03')
            
            if scada_demand:    
                scada_blockvalues= []
                for demand in  scada_demand:
                    block_value= demand.volume
                    scada_blockvalues.append(block_value)
                print("ensemble block", scada_blockvalues )
                datasets.append({
                        'name': 'Scada',
                        # 'borderColor': color,
                        # 'borderWidth': 2, 
                        'data':scada_blockvalues,
                        # 'fill': False,
                        # 'borderDash': [5,2.5]
                })

            #ensemble demand
                ensemble_blockvalues= []
                for demand in  ensemble_demand:
                    block_value= demand.Final_forecast
                    ensemble_blockvalues.append(block_value)
                print("ensemble block", ensemble_blockvalues )
                datasets.append({
                        'name': 'Ensemble',
                        # 'borderColor': color,
                        # 'borderWidth': 2, 
                        'data': ensemble_blockvalues,
                        # 'fill': False,
                        # 'borderDash': [5,2.5]
                    })


        i=0
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
        
           



        print ("datasets",datasets)
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
        # print("weather2####", weather2, "refdate", refdate)
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
                
        # print("weather3_data1", weather3_data1[3])
      
        if self.request.GET.get('fromBlock') and  self.request.GET.get('fromBlock') is not None :
            forecast_version= self.current_forecast_version()
            demand_instance= Forecast_Master.objects.filter( forecast_type__iexact='TLD_Forecast',date=date,loc_ID=getstate[0]).first()
            # print("print demand blocks1",demand_instance)
            
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
                # print("print demand blocks",demand.block1,demand.block2)
                    block_values = attrgetter(*BLOCK_CONSTANTS)(demand)
                    block_values_dict= dict(zip(BLOCK_CONSTANTS,block_values))
                    # print("block_values_dict",block_values_dict)
                    from_block = int(self.request.GET.get('fromBlock'))
                    to_block= int(self.request.GET.get('toBlock'))
                    color = random.choice(border_colors)
                    from_value=float(self.request.GET.get('fromVal'))
                    to_value=float(self.request.GET.get('toVal'))
                    if action == "Add":
                        added_demand= add_action(demand, from_block, to_block, from_value, to_value)
                        block_values_dict.update(**added_demand)
                        self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                        # print("block_values_dictupdated",block_values_dict)
                        forecast_dataset= tuple(block_values_dict.values())
                        
                        datasets.append({
                            'name': "forecast",
                            # 'borderColor': 'red' ,
                            # 'borderWidth': 2, 
                            'data': forecast_dataset,
                            # 'fill': False
                        })
                        # print("added_demand", added_demand)
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
      
        cityweather_chartdata=[]
        # for f in weather1:
        #     cityweather_chartdata.append(
        #         {
        #         'label': f,
        #         'borderColor': 'red' ,
        #         'borderWidth': 2, 
        #         'data': [] ,

        #     }
        #     )
        
        # print("weather_data1", weather_data1)
        print("get_citieskeys", all_cities)
        context['weather_data_one'] =  weather_data1
        context['weather2_data_one']= weather2_data1
        context['weather3_data_one']= weather3_data1
        # context['cityweather_data'] = json.dumps(cityweather_data)
        context['all_cities'] = all_cities
        context['weather_data_one'] =  weather_data1
        context['datasets'] = json.dumps(datasets)
        context['labels'] = json.dumps([i for i in range(1, 97)])
        context['whther_labels'] = json.dumps([i for i in range(0, 25)])
        context['all_forecasttypes'] = all_forecasttypes
        context['forecast_types'] = forecast_types
        context['date_choices'] = date_choices
        context['n_by_dates'] = n_by_dates
        context['w_corr_data'] = w_corr_data
        context['d_corr_data'] = d_corr_data
        context['zones'] = zones
        context['weather1']= weather1
        context['weather2']= weather2
        context['weather3']= weather2
        # context['weather_datasets']= json.dumps(weather_datasets) 
        
        context['weather_parameters']= weather_parameters
        # context['DW_datasets']= json.dumps(DW_datasets)
        context['actions']= actions
        context['form']= form
        context['formz']= formz
        return context
    
class LoginView(auth_views.LoginView):
    print("in login view")

class test(TemplateView):
    template_name = 'dashboard/assets/templates/test.html' 