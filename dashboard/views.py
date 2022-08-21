from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import F
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
        corr_type= self.request.GET.get('correl_type', None)
        date = self.request.GET.get('date', None)
        if date == '':
            date = datetime.now().date()
        print("date....",date)
        state_input = self.request.GET.get('state', None)
        print("state_input....",state_input)
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
            getstate= list(StateZone.objects.filter(state=state_input).values_list('unique_id', flat=True))

        if state_input:
            state_weather= State.objects.get(id=state_input).code
            state= State.objects.get(id=state_input)
            get_cities= dict(state.city_set.values_list('name', 'geocode'))     
            print("get_cities", get_cities)
        else:
            get_cities={}

        
        all_cities=list(get_cities.keys())

        print("all_citiesnow", all_cities) 
        city_labels= []
        for city in all_cities:
            weather_label= [i for i in range(1, 25)]
            label= city + ';' +  str(weather_label)
            city_labels.append(label)
        print("citylabel", city_labels)
        print("getstate and state_weather", getstate)
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
        
        print("forecast_types",forecast_types)
        print("request.get",self.request.GET )
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
        print("request.get",self.request.GET.get )
        # print(" weather1", type(weather1))
        # print(" weather2", weather2)
        if len(getstate) != 0:
             corr_state = getstate[0]
             corr_state= corr_state[:5]
        else:
            corr_state=''
            
        w_corr_data= list(corr_dates.objects.filter(Date=date,loc_ID=corr_state,Item_ID=corr_type).values_list('Ref_date').order_by('Rank')[:3])
        w_corr_data=[str(w[0]) for w in w_corr_data]
        print('w_corr_data',w_corr_data)
        print('date',date,'corr_state',corr_state,'corr_type',corr_type )
    
        all_forecasttypes= list(Forecast_Master.objects.all().values_list('forecast_type', flat=True).distinct())
        date_choices = Forecast_Master.objects.all().exclude(
            date__isnull=True
        ).values_list('date', flat=True).order_by('-date').distinct()

        datasets=[]
        demand_datas= Forecast_Master.objects.filter( forecast_type__in=forecast_types,date=date,loc_ID__in=getstate).distinct()
        print("demanddatass" , demand_datas)
        
        for demand_data in demand_datas:
            block_values = attrgetter(*BLOCK_CONSTANTS)(demand_data)
            print("block_values_demand",block_values)
            color = random.choice(border_colors)
            print(block_values)
            # if f=='ITD':
            #     dataset1.append(block_values)
            datasets.append({
                'label': demand_data.forecast_type,
                'borderColor': color,
                'borderWidth': 2, 
                'data': block_values,
                'fill': False,
                'borderDash': [5,2.5]
            })
      
        print ("weather_date224",weather_date)
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
              
        print("DW_datasets",DW_datasets)
        weather_datasets1=[]
        weather_dataset1_ref=[]
        for f in weather1: 
              if weather_date is not '' and weather_date is not None : 
                weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=get_cities.values())
                weather_data = list(weather_qs.filter(geo_code__in=list(get_cities.values())).order_by('city','block').distinct('city','block').values('block',f,city_name=F('city__name'))) 
                print("weatherDATA", weather_data)
                # print("weather_date222",  weather_date)
                color = random.choice(border_colors)
                weatherdata= Weather.objects.filter(date=weather_date, state_code=state_weather,geo_code= city[1]).values_list(f).order_by('-block')[:24]
                # print("weatherdata",  weatherdata)
                block_values = tuple(weatherdata)
                block_values = tuple(list(itertools.chain(*block_values)))
                # print("weather_dataaaaa",  block_values)
                weather_datasets1.append({
                    'label':  f +' '+ weather_date,
                    'borderColor': color,
                    'borderWidth': 2,
                    'data': block_values,
                    'fill': False,
                    'XaxisID':city[0]
                })
              if refdate is not None:
                # print("refdate", refdate)
                weatherdata_ref= Weather.objects.filter(date=refdate,geo_code= city[1]).values_list(f).order_by('-block')[:24]   
                # print("weatherdata", len(list(weatherdata)))
                # print("weatherdata", weatherdata)
                block_values_weather_ref=tuple(weatherdata_ref)
                block_values_weather_ref=tuple(list(itertools.chain(*block_values_weather_ref)))
                # print("block_values",block_values)  , state_code=sta
                # print("block_values_weather_ref",block_values_weather_ref)               
                color = random.choice(border_colors)
                
                weather_dataset1_ref.append({
                    'label':  refdate,
                    'borderColor': color,
                    'borderWidth': 2,
                    'data': block_values_weather_ref,
                    'fill': False,
                    'borderDash': [3,1.5],
                    'XaxisID':city[0]
                })
        weather_datasets = weather_datasets1 + weather_dataset1_ref 



        if weather1 is not None :
            for f in weather1: 
                weatherdata= Weather.objects.filter(date=weather_date, geo_code__in=get_cities.values()).values_list(f).order_by('-block')
                print("weatherdata_new",  len(weatherdata))
        all_cities=list(get_cities.keys())

        weather_datasets1=[]
        weather_dataset1_ref=[]
        cityweather_data=[]
        if weather1 is not None :
            for f in weather1: 
              if weather_date is not '' and weather_date is not None :  
                print("state[1]",f, weather_date,"state_weather")
                print("weather_date222",  weather_date)
                #new
                # weather_qs = Weather.objects.filter(date=weather_date, geo_code__in=get_cities.values())
                # weather_data = list(weather_qs.filter(city__name__in=list(get_cities.keys())).order_by('geo_code','block').distinct('geo_code','block').values('block',f,city_name=F('city__name')))
                # print("weather_data_new",weather_data)
                color = random.choice(border_colors)
                weatherdata= Weather.objects.filter(date=weather_date,state_code=state_weather, geo_code__in=get_cities.values()).values_list(f).order_by('-block')[:24]
                print("weatherdatacity231", weatherdata) 
                print("weatherdatacity233", weatherdata)
                # for city,geocode in get_cities.items():
                #     citydata= weather_qs.filter(geo_code=geocode).order_by('block').values_list(f, flat=True)
                #     cityweather_data.append(
                #         {
                #             "city": city,
                #             "data": list(citydata)
                #         }
                #     )
                # print("cityweather_data", cityweather_data)
                block_values = tuple(weatherdata)
                block_values = tuple(list(itertools.chain(*block_values)))
                # print("weather_dataaaaa",  block_values)
                weather_datasets1.append({
                    'label':  f +' '+ weather_date,
                    'borderColor': color,
                    'borderWidth': 2,
                    'data': block_values,
                    'fill': False
                })
              if refdate is not None:
                print("refdate", refdate)
                weatherdata_ref= Weather.objects.filter(date=refdate, state_code=state_weather).values_list(f).order_by('-block')[:24]   
                # print("weatherdata", len(list(weatherdata)))
                # print("weatherdata", weatherdata)
                block_values_weather_ref=tuple(weatherdata_ref)
                block_values_weather_ref=tuple(list(itertools.chain(*block_values_weather_ref)))
                # print("block_values",block_values)  
                print("block_values_weather_ref",block_values_weather_ref)               
                color = random.choice(border_colors)
                
                weather_dataset1_ref.append({
                    'label':  refdate,
                    'borderColor': color,
                    'borderWidth': 2,
                    'data': block_values_weather_ref,
                    'fill': False,
                    'borderDash': [3,1.5]
                })
        weather_datasets = weather_datasets1 + weather_dataset1_ref


       
        print("weather_datasets", weather_datasets)
        weather_datasets2=[]
        weather_datasets2_ref=[]
        if weather2 is not None:
            for f in weather2:
                if f is not '':
                    print("state[1]",f, date)
                    print("date",  date)
                    weatherdata= Weather.objects.filter(date=weather_date, state_code=state_weather).values_list(f).order_by('-block')[:24]
                    if refdate is not None:
                        weatherdata_ref= Weather.objects.filter(date=date, state_code=state_weather).values_list(f).order_by('-block')[:24]  
                    # print("weatherdata", len(list(weatherdata)))
                    print("weatherdata", weatherdata)
                    block_values = tuple(weatherdata)
                    block_values = tuple(list(itertools.chain(*block_values)))
                    block_values_weather_ref=tuple(weatherdata_ref)
                    block_values_weather_ref=tuple(list(itertools.chain(*block_values_weather_ref)))
                    print("block_values",block_values) 
                    
                    color = random.choice(border_colors)
                    weather_datasets2.append({
                        'label':  f +' '+ weather_date,
                        'borderColor': color,
                        'borderWidth': 2,
                        'data': block_values,
                        'fill': False
                    })
                    weather_datasets2_ref.append({
                        'label': f +' '+ refdate,
                        'borderColor': color,
                        'borderWidth': 2,
                        'data': block_values,
                        'fill': False,
                        'borderDash': [3,1.5]
                    })
        weather2_datasets= weather_datasets2 +  weather_datasets2_ref
        
        
        
        weather_datasets3=[]
        weather_datasets3_ref=[]
        for f in weather3:
            if f is not '':
                print("state[1]",  f, date)
                print("date",  date)
                weatherdata= Weather.objects.filter(date=weather_date, state_code=state_weather).values_list(f).order_by('-block')[:24]
                if refdate is not None:
                        weatherdata_ref= Weather.objects.filter(date=refdate, state_code=state_weather).values_list(f).order_by('-block')[:24]  
                # print("weatherdata", len(list(weatherdata)))
                print("weatherdata", weatherdata)
                block_values = tuple(weatherdata)
                block_values = tuple(list(itertools.chain(*block_values)))
                block_values_weather_ref=tuple(weatherdata_ref)
                block_values_weather_ref=tuple(list(itertools.chain(*block_values_weather_ref)))
                print("block_values",block_values) 
                
                color = random.choice(border_colors)
                weather_datasets3.append({
                    'label': f +' '+ weather_date,
                    'borderColor': color,
                    'borderWidth': 2,
                    'data': block_values,
                    'fill': False
                })
                weather_datasets3_ref.append({
                    'label': f +' '+ refdate,
                    'borderColor': color,
                    'borderWidth': 2,
                    'data': block_values,
                    'fill': False,
                    'borderDash': [3,1.5]
                })
                
        weather3_datasets= weather_datasets3 + weather_datasets3_ref
    
        if self.request.GET.get('fromBlock') and  self.request.GET.get('fromBlock') is not None :
            forecast_version= self.current_forecast_version()
            demand_instance= Forecast_Master.objects.filter( forecast_type__iexact='ITD',date=date,loc_ID=getstate).first()
            print("print demand blocks1",demand_instance)
            
            if 'undo' in self.request.GET:
                forecast_version-= 1 
                demand=self.get_forecast_demand(demand_instance,version=forecast_version)
                block_values = attrgetter(*BLOCK_CONSTANTS)(demand)
                datasets.append({
                        'label': "forecast",
                        'borderColor': 'red' ,
                        'borderWidth': 2, 
                        'data': block_values,
                        'fill': False
                    })
                cache.set('forecast_version', forecast_version, 3600)
            elif 'clearall' in self.request.GET:
                forecast_version = 1 
                demand=self.get_forecast_demand(demand_instance,version=forecast_version)
                block_values = attrgetter(*BLOCK_CONSTANTS)(demand)
                datasets.append({
                        'label': "forecast",
                        'borderColor': 'red' ,
                        'borderWidth': 2, 
                        'data': block_values,
                        'fill': False
                    })
                cache.set('forecast_version', forecast_version, 3600)
            else:
                # forecast_version += 1
                # cache.set('forecast_version', forecast_version, 3600)
                demand=self.get_forecast_demand(demand_instance,version=forecast_version)
                print("print demand blocks",demand.block1,demand.block2)
                block_values = attrgetter(*BLOCK_CONSTANTS)(demand)
                block_values_dict= dict(zip(BLOCK_CONSTANTS,block_values))
                print("block_values_dict",block_values_dict)
                from_block = int(self.request.GET.get('fromBlock'))
                to_block= int(self.request.GET.get('toBlock'))
                color = random.choice(border_colors)
                from_value=float(self.request.GET.get('fromVal'))
                to_value=float(self.request.GET.get('toVal'))
                if action == "Add":
                    added_demand= add_action(demand, from_block, to_block, from_value, to_value)
                    block_values_dict.update(**added_demand)
                    self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                    print("block_values_dictupdated",block_values_dict)
                    forecast_dataset= tuple(block_values_dict.values())
                    
                    datasets.append({
                        'label': "forecast",
                        'borderColor': 'red' ,
                        'borderWidth': 2, 
                        'data': forecast_dataset,
                        'fill': False
                    })
                    print("added_demand", added_demand)
                if action == "Multiply": 
                    multipled_demand= multiply_action(demand, from_block, to_block, from_value, to_value)
                    block_values_dict.update(**multipled_demand)
                    self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                    forecast_dataset= list(block_values_dict.values())
                    datasets.append({
                        'label': "forecast",
                        'borderColor': 'red' ,
                        'borderWidth': 2, 
                        'data': forecast_dataset,
                        'fill': False
                    })
                if action == "Average": 
                    average_demand= average_action(demand, from_block, to_block, from_value, to_value)
                    block_values_dict.update(**average_demand)
                    self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                    forecast_dataset= list(block_values_dict.values())
                    datasets.append({
                        'label': "forecast",
                        'borderColor': 'red' ,
                        'borderWidth': 2, 
                        'data': forecast_dataset,
                        'fill': False
                    })
                if action == "Shift left":
                    Shiftleft_demand= shift_left_action(demand, from_block, to_block, from_value, to_value)
                    block_values_dict.update(**Shiftleft_demand)
                    self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                    forecast_dataset= list(block_values_dict.values())
                    datasets.append({
                        'label': "forecast",
                        'borderColor': 'red' ,
                        'borderWidth': 2, 
                        'data': forecast_dataset,
                        'fill': False
                    })
                if action == "Shift right":
                    Shiftright_demand= shift_right_action(demand, from_block, to_block, from_value, to_value)
                    block_values_dict.update(**Shiftright_demand)
                    self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                    forecast_dataset= list(block_values_dict.values())
                    datasets.append({
                        'label': "forecast",
                        'borderColor': 'red' ,
                        'borderWidth': 2, 
                        'data': forecast_dataset,
                    })    

                if action == "Smooth":
                    smooth_demand= smooth_action(demand, from_block, to_block, from_value, to_value)
                    block_values_dict.update(**smooth_demand)
                    self.update_forecast_demand(demand,block_values_dict,version=forecast_version)
                    forecast_dataset= list(block_values_dict.values())
                    datasets.append({
                        'label': "forecast",
                        'borderColor': 'red' ,
                        'borderWidth': 2, 
                        'data': forecast_dataset,
                    })    
        actions = ['Add','Multiply','Average','Shift left','Shift right','Smooth']    
        # weatherlabels=  [[i for i in range(0, 25)] for j in range(0,len(city_labels))]
        # print("weatherlabels", weatherlabels)
        print("datasets",datasets)
        cityweather_chartdata=[]
        for f in weather1:
            cityweather_chartdata.append(
                {
                'label': f,
                'borderColor': 'red' ,
                'borderWidth': 2, 
                'data': [] ,

            }
            )

        context['weather_data'] =  weather_data
        context['cityweather_data'] = json.dumps(cityweather_data)
        context['citylabels'] = get_cities.keys()
        context['datasets'] = json.dumps(datasets)
        context['labels'] = json.dumps([i for i in range(1, 97)])
        context['whther_labels'] = json.dumps([i for i in range(0, 25)])
        context['all_forecasttypes'] = all_forecasttypes
        context['forecast_types'] = forecast_types
        context['date_choices'] = date_choices
        context['w_corr_data'] = w_corr_data
        context['zones'] = zones
        context['weather1']= weather1
        context['weather2']= weather2
        context['weather3']= weather2
        context['weather_datasets']= json.dumps(weather_datasets) 
        context['weather2_datasets']= json.dumps(weather2_datasets)
        context['weather3_datasets']= json.dumps(weather3_datasets) 
        context['weather_parameters']= weather_parameters
        # context['DW_datasets']= json.dumps(DW_datasets)
        context['actions']= actions
        context['form']= form
        context['formz']= formz
        return context
    
     
    #  [{'label': 'temperature_dew_point', 'borderColor': 'peru', 'borderWidth': 2, 'data': [(26.1,), (26.1,), (25.1,), (26.9,), (27.0,), (25.6,), (25.9,), (26.1,), (25.8,), (26.6,), (27.1,), (27.1,), (26.1,), (26.9,), (27.0,), (25.6,), (25.6,), (25.6,), (26.3,), (26.6,), (26.4,), (26.1,), (27.1,), (26.6,)]}, {'label': 'temperature_feels_like', 'borderColor': 'darkgray', 'borderWidth': 2, 'data': [(34.4,), (34.5,), (33.2,), (33.7,), (33.8,), (34.3,), 
    #  [{'label': 'ITD', 'borderColor': 'cyan', 'borderWidth': 2, 'data': (21957.10494, 21799.03, 21783.02, 22133.32058, 22030.97606, 21578.62724, 21479.61388, 20648.18184, 20844.76, 20712.15, 20717.56391, 20745.80395, 20605.77251, 20518.52092, 20299.59782, 20184.99332, 20050.9264, 19950.00824, 19942.29887, 19834.6192, 19778.04036, 19683.34763, 19398.36169, 19213.11412, 18342.80341, 17626.61746, 17154.10053, 17090.01473, 16633.16535, 16478.14184, 16344.94243, 16530.03834, 16461.94552, 17002.33176, 16800.42813, 16984.12436, 17773.42287, 18086.8372, 18434.03025, 19038.81677, 19950.08009, 21049.42549, 21059.20127, 21612.56512, 21080.22374, 21214.30635, 21404.11901, 21146.86959, 21245.95724, 20531.34439, 20440.81502, 20378.01479, 20181.39, 20345.11631, 19809.164, 20367.67493, 21430.31716, 21444.66494, 21172.20588, 21290.6915, 21193.92969, 21040.6127, 20925.08347, 20348.8419, 19604.61, 19654.93833, 18944.97059, 18608.53211, 17875.49989, 18602.10377, 18637.63142, 18330.38, 18796.70392, 19544.83796, 20321.84145, 21627.86815, 21555.83, 22412.81, 22910.42209, 23170.28079, 23215.54976, 23201.61087, 22802}]