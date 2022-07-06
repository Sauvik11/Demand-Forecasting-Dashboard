from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
import json
from dashboard.utils.helper import *

import ast
import random
from operator import attrgetter
import itertools
# from chartjs.views.lines import BaseLineChartView
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q
from .models import *
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
            'aliceblue', 'darkgray', 'darkslategray', 'black'
        ]
weather_parameters= ['cloud_cover','precip_chance','pressure_mean_sea_level','qpf','qpf_snow',
                        'relative_humidity','temperature','temperature_dew_point','temperature_feels_like',
                        'temperature_heat_index','temperature_wind_chill','uv_index','visibility','wind_direction',
                        'wind_gust','wind_speed','wx_severity']
 

class ForecastDashboardView(TemplateView):
    template_name = 'dashboard/assets/templates/index.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.request.GET.get('date', None)
        action = self.request.GET.get('Action', None)
        state_input = self.request.GET.get('state', None)
        print("date",date)
        statewther=self.request.GET.get('chart1_weather_state', None)
        weather1 = None
        weather2 = None
        forecast_types = self.request.GET.getlist('ftype')
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
        print(" weather2", weather2)
        states = {'Uttar Pradesh': ('INDUP000000', 'UP0'), 'Madhya Pradesh': ('INDMPMP0000','MP0'),
              'Madhya Pradesh East Zone': ('INDMPEZ0000','MP0'), 'Madhya Pradesh West Zone': ('INDMPWZ0000','MP0'),
              'Madhya Pradesh Central Zone': ('INDMPCZ0000','MP0'), 'Bihar': ('INDBH000000','BH0')}
        state=''
        if state_input is not None:
            state= states[state_input]
        if statewther is not None:
            state= states[statewther]  
        # print("state",state)
        # demand_dataAll= Forecast_Master.objects.all()

        all_forecasttypes= list(Forecast_Master.objects.all().values_list('forecast_type', flat=True).distinct())
        date_choices = Forecast_Master.objects.all().exclude(
            date__isnull=True
        ).values_list('date', flat=True).order_by('-date').distinct()
        datasets=[]
        test_data= Forecast_Master.objects.filter(date='2021-08-21', loc_ID='INDUP000000').values_list('forecast_type', flat=True)
        print("test_data",test_data)

        
        # data_action=list(dataset1[0])
        for f in forecast_types:
            demand_data= Forecast_Master.objects.filter( forecast_type__iexact=f,date=date,loc_ID=state[0]).first()
            print("demand_data",demand_data.forecast_type)
            block_values = attrgetter(*BLOCK_CONSTANTS)(demand_data)
            print("ffff",f)
            print("block_values",block_values)
            color = random.choice(border_colors)
            print(block_values)
            # if f=='ITD':
            #     dataset1.append(block_values)
            datasets.append({
                'label': demand_data.forecast_type,
                'borderColor': color,
                'borderWidth': 2, 
                'data': block_values
            })
        dataset1 =[]
        for q in datasets:
            if q['label']=='ITD':
                dataset1.append(q['data'])
        print("dataset",dataset1)
        weather_datasets=[]
        if weather1 is not None:
            for f in weather1: 
                print("state[1]",  state[1],f, date)
                print("date",  date)
                weatherdata= Weather.objects.filter(date=date, state_code=state[1]).values_list(f).order_by('-block')[:24]
                # print("weatherdata", len(list(weatherdata)))
                print("weatherdata", weatherdata)
                block_values = tuple(weatherdata)
                block_values = tuple(list(itertools.chain(*block_values)))
                print("block_values",block_values)                 
                color = random.choice(border_colors)
                weather_datasets.append({
                    'label': f,
                    'borderColor': color,
                    'borderWidth': 2,
                    'data': block_values,
                })
        weather2_datasets=[]
        if weather2 is not None:
            for f in weather2:
                if f is not '':
                    print("state[1]",  state[1],f, date)
                    print("date",  date)
                    weatherdata= Weather.objects.filter(date=date, state_code=state[1]).values_list(f).order_by('-block')[:24]
                    # print("weatherdata", len(list(weatherdata)))
                    print("weatherdata", weatherdata)
                    block_values = tuple(weatherdata)
                    block_values = tuple(list(itertools.chain(*block_values)))
                    print("block_values",block_values) 
                    
                    color = random.choice(border_colors)
                    weather2_datasets.append({
                        'label': f,
                        'borderColor': color,
                        'borderWidth': 2,
                        'data': block_values,
                    })

        weather3_datasets=[]
        
        for f in weather3:
            if f is not '':
                print("state[1]",  state[1],f, date)
                print("date",  date)
                weatherdata= Weather.objects.filter(date=date, state_code=state[1]).values_list(f).order_by('-block')[:24]
                # print("weatherdata", len(list(weatherdata)))
                print("weatherdata", weatherdata)
                block_values = tuple(weatherdata)
                block_values = tuple(list(itertools.chain(*block_values)))
                print("block_values",block_values) 
                
                color = random.choice(border_colors)
                weather3_datasets.append({
                    'label': f,
                    'borderColor': color,
                    'borderWidth': 2,
                    'data': block_values,
                })
        current_block= 1
        if self.request.GET.get('fromBlock') and  self.request.GET.get('toBlock') is not None :
            for demand in dataset1:
                from_block =self.request.GET.get('fromBlock')
                to_block= self.request.GET.get('toBlock')
                from_value=self.request.GET.get('fromVal')
                to_value=self.request.GET.get('toVal')
                current_value = calculate_current_value(current_block, from_block, to_block, from_value, to_value)
                print("current_value", current_value)
                min_block_val= get_min_block_value(demand)
            
        # print("weather3_datasets",weather3_datasets)
        # print("datasets",datasets)
        context['datasets'] = json.dumps(datasets)
        context['labels'] = json.dumps([i for i in range(1, 97)])
        context['whther_labels'] = json.dumps([i for i in range(0, 26)])
        context['all_forecasttypes'] = all_forecasttypes
        context['forecast_types'] = forecast_types
        context['date_choices'] = date_choices
        context['states'] = states
        context['state']= state
        context['weather1']= weather1
        context['weather2']= weather2
        context['weather3']= weather2
        context['weather_datasets']= json.dumps(weather_datasets) 
        context['weather2_datasets']= json.dumps(weather2_datasets)
        context['weather3_datasets']= json.dumps(weather3_datasets) 
        context['weather_parameters']= weather_parameters
        return context
    
     
    #  [{'label': 'temperature_dew_point', 'borderColor': 'peru', 'borderWidth': 2, 'data': [(26.1,), (26.1,), (25.1,), (26.9,), (27.0,), (25.6,), (25.9,), (26.1,), (25.8,), (26.6,), (27.1,), (27.1,), (26.1,), (26.9,), (27.0,), (25.6,), (25.6,), (25.6,), (26.3,), (26.6,), (26.4,), (26.1,), (27.1,), (26.6,)]}, {'label': 'temperature_feels_like', 'borderColor': 'darkgray', 'borderWidth': 2, 'data': [(34.4,), (34.5,), (33.2,), (33.7,), (33.8,), (34.3,), 
    #  [{'label': 'ITD', 'borderColor': 'cyan', 'borderWidth': 2, 'data': (21957.10494, 21799.03, 21783.02, 22133.32058, 22030.97606, 21578.62724, 21479.61388, 20648.18184, 20844.76, 20712.15, 20717.56391, 20745.80395, 20605.77251, 20518.52092, 20299.59782, 20184.99332, 20050.9264, 19950.00824, 19942.29887, 19834.6192, 19778.04036, 19683.34763, 19398.36169, 19213.11412, 18342.80341, 17626.61746, 17154.10053, 17090.01473, 16633.16535, 16478.14184, 16344.94243, 16530.03834, 16461.94552, 17002.33176, 16800.42813, 16984.12436, 17773.42287, 18086.8372, 18434.03025, 19038.81677, 19950.08009, 21049.42549, 21059.20127, 21612.56512, 21080.22374, 21214.30635, 21404.11901, 21146.86959, 21245.95724, 20531.34439, 20440.81502, 20378.01479, 20181.39, 20345.11631, 19809.164, 20367.67493, 21430.31716, 21444.66494, 21172.20588, 21290.6915, 21193.92969, 21040.6127, 20925.08347, 20348.8419, 19604.61, 19654.93833, 18944.97059, 18608.53211, 17875.49989, 18602.10377, 18637.63142, 18330.38, 18796.70392, 19544.83796, 20321.84145, 21627.86815, 21555.83, 22412.81, 22910.42209, 23170.28079, 23215.54976, 23201.61087, 22802}]