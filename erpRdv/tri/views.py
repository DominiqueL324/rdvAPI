from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rdv.models import  RendezVous,Bailleur,Locataire,Propriete,TypeIntervention,TypePropriete,RdvReporteAgent,RdvReporteDate
from rdv.serializer import RdvReporteDateSerializer,RdvReporteAgentSerializer, RendezVousSerializer,BailleurSerializer,LocataireSerializer,TypeProprieteSerializer,ProprieteSerializer,TypeInterventionSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import datetime, random, string
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from datetime import date, datetime,time,timedelta
from django.db import transaction, IntegrityError
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination
from django.core.mail import send_mail
from django.db.models import Q

class RDVApi(APIView):

    pagination_class=PageNumberPagination
    paginator = pagination_class()
    
    def get(self,request):
        final_ = RendezVous.objects.none()
        #user c'est la personne qui fait la requête il peut être AS,AC,SAL,Client et Admin
        user = request.GET.get('user',None)

        #role c'est le role du user qui fait la requête il peut être AS,AC,SAL,Client et Admin
        role__ = request.GET.get('role',None)

        #groupe de celui qui envoit la requete
        #

        #filtre (requette)
        query = Q()

        if request.GET.get('salarie',None) is not None:
            salarie = request.GET.get('salarie',None)
            query |= Q(passeur=int(salarie)) 
 
        #cas d'un agent seulement
        if(request.GET.get('role',None) is not None):
            role_ = request.GET.get('role',None)
            query &= Q(role_=user)

        #cas d'un agent admin client salarie
        if(request.GET.get('statut',None) is not None):
            statut_ = request.GET.get('statut',None)
            query &= Q(statut=int(statut_))
        
        #cas d'un agent admin client
        if(request.GET.get('client',None) is not None):
            client = request.GET.get('client',None)
            query &= Q(client=int(client))

        #cas d'un admin qui veut les RDV
        if(request.GET.get('agent',None) is not None):
            agent = request.GET.get('agent',None)
            query &= Q(agent=int(agent))
            """query |= Q(agent_constat=int(agent))
            query |= Q(audit_planneur=int(agent))
            query |= Q(agent=float(agent))
            query |= Q(agent_constat=float(agent))
            query |= Q(audit_planneur=float(agent))"""

        if(request.GET.get('debut',None) is not None):
            query &= Q(date__gte=datetime.strptime(request.GET.get("debut"),'%Y-%m-%d'))
        
        if(request.GET.get('fin',None) is not None):
            query &= Q(date__lte=datetime.strptime(request.GET.get("fin"),'%Y-%m-%d'))
        
        query_set=RendezVous.objects.filter(query)
        page = self.paginator.paginate_queryset(query_set,request,view=self)
        serializer = RendezVousSerializer(page,many=True)
        return self.paginator.get_paginated_response(serializer.data)