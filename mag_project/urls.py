from django.contrib import admin
from django.urls import include, path

from ilmirapp import views
from rest_framework.response import Response
from rest_framework.views import APIView

import math 
from sympy import *
import numpy as np

class Gradient(APIView):
    def get(self, request):
        print(request.GET)
        lat = request.GET['latitude']
        lon = request.GET['longitude']

        la = float(lat)
        lo = float(lon)

        r = symbols('r')
        q = symbols('q')
        fi = symbols('fi')

        a = 6371.03 
        g01 = -30100
        g11 = -2013
        h11 = 5675

        V = (a ** 3 / r ** 2) * (g01 * cos(q) + g11 * cos(fi) * sin(q) + h11 * sin(fi)*sin(q))

        B1 = -diff(V,r)
        B2 = -(1/r)*diff(V,q)
        B3 = - 1/(r*sin(q)) * diff(V,fi)

        B_r_r = diff(V, r, 2)

        B_r_q =  1 / r * diff(V,r,q) - 1 / r**2 * diff(V,q)

        B_r_fi = (1 / (r * sin(q))) * diff(V,fi,r) - (1 / (r ** 2 * sin(q)) * diff(V,fi))

        B_q_q = 1 / r * diff(V,r) + 1 / r**2 * diff(V,q,2)

        B_q_fi = (1 / (r**2 * sin(q))) * diff(V,q,fi) + (cos(q) / (r ** 2 * sin(q)) * diff(V,q))

        B_fi_fi =  1 / r * diff(V,r) + cos(q) / (r**2 *sin(q)) * diff(V,q) + 1 / (r**2 * sin(q**2)) *  diff(V,fi,2)
        
        lati, long = np.deg2rad(la), np.deg2rad(lo)
        R = 6371 # radius of the earth
        x = R * np.cos(lati) * np.cos(long)
        y = R * np.cos(lati) * np.sin(long)
        z = R *np.sin(lati)

    #перевод в сферические координаты
        r_num = math.sqrt(x **2 + y **2 + z **2)
        q_num = math.atan(math.sqrt((x**2 + y**2) / z)) 
        fi_num = math.atan(y/x) 

        tensor_list = []

        B_r_r_result =  B_r_r.evalf(subs={r : r_num, q : q_num,fi : fi_num})

        B_r_q_result = B_r_q.evalf(subs={r : r_num, q : q_num,fi : fi_num})

        B_r_fi_result = B_r_fi.evalf(subs={r : r_num, q : q_num,fi : fi_num})

        B_q_q_result = B_q_q.evalf(subs={r : r_num, q : q_num,fi : fi_num})

        B_q_fi_result = B_q_fi.evalf(subs={r : r_num, q : q_num,fi : fi_num})

        B_fi_fi_result = B_fi_fi.evalf(subs={r : r_num, q : q_num,fi : fi_num})

        tensor_list.append(str(B_r_r_result))
        tensor_list.append(str(B_r_q_result))
        tensor_list.append(str(B_r_fi_result))
        tensor_list.append(str(B_q_q_result))
        tensor_list.append(str(B_q_fi_result))
        tensor_list.append(str(B_fi_fi_result))

        B1 = -diff(V,r)
        B2 = -(1/r)*diff(V,q)
        B3 = - 1/(r*sin(q)) * diff(V,fi)

        grad_list = []
        B1_result =  B1.evalf(subs={r : r_num, q : q_num,fi : fi_num})
        B2_result =  B2.evalf(subs={r : r_num, q : q_num,fi : fi_num})
        B3_result =  B3.evalf(subs={r : r_num, q : q_num,fi : fi_num})

        grad_list.append(str(B1_result))
        grad_list.append(str(B2_result))
        grad_list.append(str(B3_result))

        return Response({"tensor": tensor_list, "gradient": grad_list})

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", views.index),
    path('api/gradient/', Gradient.as_view())
]