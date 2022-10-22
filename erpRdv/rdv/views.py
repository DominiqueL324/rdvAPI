from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import  RendezVous,Bailleur,Locataire,Propriete,TypeIntervention,TypePropriete,RdvReporteAgent,RdvReporteDate
from .serializer import RdvReporteDateSerializer,RdvReporteAgentSerializer, RendezVousSerializer,BailleurSerializer,LocataireSerializer,TypeProprieteSerializer,ProprieteSerializer,TypeInterventionSerializer
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
    serializer_class= RendezVousSerializer
    queryset = RendezVous.objects.all()
    paginator = pagination_class()

    def get(self,request):

        if(request.GET.get('clientcount',None) is not None):
            val_ = request.GET.get("clientcount",None)
            rdv = RendezVous.objects.filter(client=int(val_)).count()
            return JsonResponse({"Rdv":rdv},status=200)

        if(request.GET.get('agentcount',None) is not None):
            val_ = request.GET.get("agentcount",None)
            rdv = RendezVous.objects.filter(agent=int(val_)).count()
            return JsonResponse({"Rdv":rdv},status=200)

        if(request.GET.get('salariecount',None) is not None):
            val_ = request.GET.get("salariecount",None)
            rdv = RendezVous.objects.filter(passeur=int(val_)).count()
            return JsonResponse({"Rdv":rdv},status=200)

        if(request.GET.get('agentcountconst',None) is not None):
            val_ = request.GET.get("agentcountconst",None)
            rdv = RendezVous.objects.filter(agent_constat=val_).count()
            return JsonResponse({"Rdv":rdv},status=200)

        if(request.GET.get('admincount',None) is not None):
            rdv = RendezVous.objects.count()
            return JsonResponse({"Rdv":rdv},status=200)


        if(request.GET.get("user",None) is not None):
            val_ = request.GET.get("user",None)
            query_set=""
            if request.GET.get("debut",None) is not None and request.GET.get("fin",None) is not None:
                query_set = RendezVous.objects.filter(client=int(val_),date__gte=datetime.strptime(request.GET.get("debut"),'%Y-%m-%d'),date__lte=datetime.strptime(request.GET.get("fin"),'%Y-%m-%d'))
            else:
                query_set = RendezVous.objects.filter(client=int(val_))
            
            if request.GET.get("paginated",None) is not None:
                serializer = RendezVousSerializer(query_set,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)

            page = self.paginator.paginate_queryset(query_set,request,view=self)
            serializer = RendezVousSerializer(page,many=True)
            return self.paginator.get_paginated_response(serializer.data)

        if(request.GET.get("agent",None) is not None):
            val_ = request.GET.get("agent",None)
            query_set=""
            if request.GET.get("debut",None) is not None and request.GET.get("fin",None) is not None:
                 query_set = RendezVous.objects.filter(Q(agent=int(val_)) | Q(agent_constat=int(val_))| Q(audit_planneur=int(val_)),date__gte=datetime.strptime(request.GET.get("debut"),'%Y-%m-%d'),date__lte=datetime.strptime(request.GET.get("fin"),'%Y-%m-%d'))
            else:
                query_set = RendezVous.objects.filter( Q(agent=int(val_)) | Q(agent_constat=int(val_))| Q(audit_planneur=int(val_)) )
            
            if request.GET.get("paginated",None) is not None:
                serializer = RendezVousSerializer(query_set,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)

            page = self.paginator.paginate_queryset(query_set,request,view=self)
            serializer = RendezVousSerializer(page,many=True)
            return self.paginator.get_paginated_response(serializer.data)

        if(request.GET.get("constat",None) is not None):
            val_ = request.GET.get("constat",None)
            query_set=""
            if request.GET.get("debut",None) is not None and request.GET.get("fin",None) is not None:
                 query_set = RendezVous.objects.filter(Q(agent=int(val_)) | Q(agent_constat=int(val_))| Q(audit_planneur=int(val_)),date__gte=datetime.strptime(request.GET.get("debut"),'%Y-%m-%d'),date__lte=datetime.strptime(request.GET.get("fin"),'%Y-%m-%d'))
            else:
                query_set = RendezVous.objects.filter(Q(agent=int(val_)) | Q(agent_constat=int(val_))| Q(audit_planneur=int(val_)))
            
            if request.GET.get("paginated",None) is not None:
                serializer = RendezVousSerializer(query_set,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)

            page = self.paginator.paginate_queryset(query_set,request,view=self)
            serializer = RendezVousSerializer(page,many=True)
            return self.paginator.get_paginated_response(serializer.data)

        if(request.GET.get("planneur",None) is not None):
            val_ = request.GET.get("constat",None)
            query_set=""
            if request.GET.get("debut",None) is not None and request.GET.get("fin",None) is not None:
                 query_set = RendezVous.objects.filter(Q(agent=int(val_)) | Q(agent_constat=int(val_))| Q(audit_planneur=int(val_)),date__gte=datetime.strptime(request.GET.get("debut"),'%Y-%m-%d'),date__lte=datetime.strptime(request.GET.get("fin"),'%Y-%m-%d'))
            else:
                query_set = RendezVous.objects.filter(Q(agent=int(val_)) | Q(agent_constat=int(val_))| Q(audit_planneur=int(val_)))
            
            if request.GET.get("paginated",None) is not None:
                serializer = RendezVousSerializer(query_set,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)

            page = self.paginator.paginate_queryset(query_set,request,view=self)
            serializer = RendezVousSerializer(page,many=True)
            return self.paginator.get_paginated_response(serializer.data)

        if(request.GET.get("passeur",None) is not None):
            val_ = request.GET.get("passeur",None)
            query_set=""
            if request.GET.get("debut",None) is not None and request.GET.get("fin",None) is not None:
                query_set = RendezVous.objects.filter(passeur=int(val_),date__gte=datetime.strptime(request.GET.get("debut"),'%Y-%m-%d'),date__lte=datetime.strptime(request.GET.get("fin"),'%Y-%m-%d'))
            else:
                query_set = RendezVous.objects.filter(passeur=int(val_))
            
            if request.GET.get("paginated",None) is not None:
                serializer = RendezVousSerializer(query_set,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)

            page = self.paginator.paginate_queryset(query_set,request,view=self)
            serializer = RendezVousSerializer(page,many=True)
            return self.paginator.get_paginated_response(serializer.data)

        if request.GET.get("debut",None) is not None and request.GET.get("fin",None) is not None:
            query_set = RendezVous.objects.filter(date__gte=datetime.strptime(request.GET.get("debut"),'%Y-%m-%d'),date__lte=datetime.strptime(request.GET.get("fin"),'%Y-%m-%d'))
            page = self.paginator.paginate_queryset(query_set,request,view=self)
            serializer = RendezVousSerializer(page,many=True)
            if request.GET.get("paginated",None) is not None:
                serializer = RendezVousSerializer(query_set,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return self.paginator.get_paginated_response(serializer.data)

        page = self.paginator.paginate_queryset(self.queryset,request,view=self)
        """if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)"""
        #rdv = RendezVous.objects.all()
        serializer = RendezVousSerializer(page,many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self,request):
        data = request.data
        with transaction.atomic():
            #création du bailleur
            bailleur = Bailleur.objects.create(
                nom=data['nom_bailleur'],
                prenom=data['prenom_bailleur'],
                email=data['email_bailleur'],
                reference=data['reference_bailleur'],
            )

            #création de l'occupant 
            occupant= Locataire.objects.create(
                nom=data['nom_locataire'],
                prenom=data['prenom_locataire'],
                email=data['email_locataire'],
                telephone=data['telephone_locataire'],
            )

            #création de la propriété
            propriete = Propriete.objects.create(
                surface = data["surface_propriete"],
                numero = data["numero_propriete"],
                numeroParking = data["numero_parking_propriete"],
                adresse = data["adresse_propriete"],
                codePostal = data["code_postal_propriete"],
                ville = data["ville_propriete"],
                adresseComplementaire = data["adresse_complementaire_propriete"],
                numeroCave = data["numero_cave_propriete"],
                numeroSol = data["numero_sol_propriete"],
                bailleur = bailleur,
                locataire = occupant,
                type = data["type"],
                ancien_locataire = data['ancien_locataire'],
                type_propriete = TypePropriete.objects.filter(pk=int(data['type_propriete'])).first()
            )
            couleur = ""
            statut_=""
            if int(data['statut']) == 1:
                statut_ = "Attente prise en charge"
                couleur="red"
            elif int(data['statut']) == 2:
                statut_ = "Prise en charge Attente horaire"
                couleur="orange"
            elif int(data['statut']) == 3:
                statut_ = "Action requise"
                couleur="blue"
            elif int(data['statut']) == 4:
                statut_ = "Annule"
                couleur="yellow"
            else:
                statut_ = "Organise"
                couleur="green"


            #création du RDV
            rdv = RendezVous.objects.create(
                ref_lot = data['ref_lot'],
                ref_rdv_edl = data['ref_edl'],
                intervention = TypeIntervention.objects.filter(pk=int(data['intervention'])).first(),
                propriete = propriete,
                client = int(data['client']),
                date = data['date'],
                #passeur = int(data['passeur']),
                #agent = request.POST.get(),
                #longitude = data['longitude'],
                #latitude = data['latitude'],
                consignes_particuliere = data['consignes_part'],
                liste_document_recuperer= data['list_documents'],
                info_diverses = data['info_diverses'],
                statut=data['statut'],
                couleur = couleur
            )
            if request.POST.get("passeur",None) is not None:
                rdv.passeur = int(data['passeur'])
            
            if request.POST.get("longitude",None) is not None:
                rdv.longitude = int(data['longitude'])
            
            if request.POST.get("latitude",None) is not None:
                rdv.latitude = int(data['latitude'])
            
            if request.POST.get("agent",None) is not None:
                rdv.agent = int(data['agent'])
            
            if request.POST.get("agent_constat",None) is not None:
                rdv.agent_constat = int(data['agent_constat'])

            if request.POST.get("audit_planneur",None) is not None:
                rdv.passeur = int(data['audit_planneur'])



            rdv.save()
                
            rdv = RendezVous.objects.filter(pk=rdv.id)
            serializer = RendezVousSerializer(rdv,many=True)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    """@property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self,queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self,data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)"""

class RDVApiDetails(APIView):

    def get(self,request,id):
        rdv = RendezVous.objects.filter(pk=id)
        if rdv.exists():
            serializer = RendezVousSerializer(rdv,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"status":"none"}, status=status.HTTP_204_NO_CONTENT)


    def put(self,request,id):
        data = request.data
        rdv = RendezVous.objects.filter(pk=id)
        if rdv.exists():
            rdv = rdv.first()
            propriete = rdv.propriete
            locataire = rdv.propriete.locataire
            bailleur = propriete.bailleur
            old_date = rdv.date
            old_agent = rdv.agent
            if(request.POST.get("cas",None) is not None):
                rdv.agent_constat = int(data['agent_constat'])
                rdv.audit_planneur = int(data['audit_planneur'])
                rdv.save()
                rdv = RendezVous.objects.filter(pk=id)
                serializer = RendezVousSerializer(rdv,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)

            if(request.POST.get("final",None) is not None):
                rdv.date = data['date']
                rdv.statut = 4
                rdv.couleur = "green"
                rdv.save()
                rdv = RendezVous.objects.filter(pk=id)
                serializer = RendezVousSerializer(rdv,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)

            with transaction.atomic():
                #edition du bailleur
                bailleur.nom=data['nom_bailleur']
                bailleur.prenom=data['prenom_bailleur']
                bailleur.email=data['email_bailleur']
                bailleur.reference=data['reference_bailleur']
                bailleur.save()

                #edition du locataire
                locataire.nom=data['nom_locataire']
                locataire.prenom=data['prenom_locataire']
                locataire.email=data['email_locataire']
                locataire.telephone=data['telephone_locataire']
                locataire.save()

                #edition de la propriété
                propriete.surface = data["surface_propriete"]
                propriete.numero = data["numero_propriete"]
                propriete.numeroParking = data["numero_parking_propriete"]
                propriete.adresse = data["adresse_propriete"]
                propriete.codePostal = data["code_postal_propriete"]
                propriete.ville = data["ville_propriete"]
                propriete.adresseComplementaire = data["adresse_complementaire_propriete"]
                propriete.numeroCave = data["numero_cave_propriete"]
                propriete.numeroSol = data["numero_sol_propriete"]
                propriete.bailleur = bailleur
                propriete.locataire = locataire
                propriete.type_propriete = TypePropriete.objects.filter(pk=int(data['type_propriete'])).first()
                propriete.save()

                statut_=""
                couleur = ""
                if int(data['statut']) == 1:
                    statut_ = "Attente prise en charge"
                    couleur="red"
                elif int(data['statut']) == 2:
                    statut_ = "Prise en charge Attente horaire"
                    couleur="orange"
                elif int(data['statut']) == 3:
                    statut_ = "Action requise"
                    couleur="blue"
                elif int(data['statut']) == 4:
                    statut_ = "Organise"
                    couleur="green"
                else:
                    statut_ = "Annulé"
                    couleur="yellow"

                #edition du RDV
                rdv.ref_lot = data['ref_lot']
                rdv.statut = data['statut']
                rdv.couleur = couleur
                rdv.ref_rdv_edl = data['ref_edl']
                rdv.intervention = TypeIntervention.objects.filter(pk=int(data['intervention'])).first()
                rdv.propriete = propriete
                rdv.client = int(data['client'])
                rdv.date = data['date']
                #rdv.passeur = request.POST.get("passeur",None)
                #rdv.agent = request.POST.get("agent",None)
                #rdv.longitude = data['longitude']
                #rdv.latitude = data['latitude']
                rdv.liste_document_recuperer = data['consignes_part'] 
                rdv.consignes_particuliere = data['list_documents']
                rdv.info_diverses = data['info_diverses']
                rdv.save()

                if request.POST.get("passeur",None) is not None:
                    rdv.passeur = int(data['passeur'])
                
                if request.POST.get("agent",None) is not None:
                    rdv.agent = int(data['agent'])
                
                if request.POST.get("agent_constat",None) is not None:
                    rdv.agent_constat = int(data['agent_constat'])

                if request.POST.get("audit_planneur",None) is not None:
                    rdv.passeur = int(data['audit_planneur'])

                """if rdv.agent != old_agent:
                    RdvReporteAgent.objects.create(
                        rdv= rdv,
                        ancien_agent = old_agent
                    )
                if rdv.date != old_date:
                    RdvReporteDate.objects.create(
                        rdv = rdv,
                        ancienneDate = old_date
                    )"""

                rdv = RendezVous.objects.filter(pk=id)
                serializer = RendezVousSerializer(rdv,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"status":"none"},status=status.HTTP_204_NO_CONTENT)

    def delete(self,request,id):
        rdv = RendezVous.objects.filter(pk=id)
        if rdv.exists():
            propriete = rdv.first().propriete
            bailleur = propriete.bailleur
            pro = propriete.locataire
            rdv.delete()
            bailleur.delete()
            pro.delete()
            propriete.delete()
            
            return Response({"status":"done"},status=status.HTTP_200_OK)
        return Response({"status":"none"}, status=status.HTTP_204_NO_CONTENT)

class RDVReportedApi(APIView):

    pagination_class=PageNumberPagination
    serializer_class= RdvReporteDateSerializer
    queryset = ""
    paginator =  pagination_class() 
    
    def get(self,request):
        data = request.data 
        id = request.GET.get("rdv",None)
        if id is not None:
            self.queryset = RdvReporteDate.objects.filter(rdv=RendezVous.objects.filter(pk=int(id)).first())
            page = self.paginator.paginate_queryset(self.queryset,request,view=self)
            #if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)
            #if reported.exists():
                #serializer = RdvReporteDateSerializer(reported,many=True)
                #return Response(serializer.data,status = status.HTTP_200_OK)
            #else:
                #return Response({"status":"none"},status = status.HTTP_200_OK)
        self.queryset = RdvReporteDate.objects.all()
        page = self.paginator.paginate_queryset(self.queryset,request,view=self)
        #if page is not None:
        serializer = self.serializer_class(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)
        #reported = 
        #serializer = RdvReporteDateSerializer(reported,many=True)
        #return Response(serializer.data,status = status.HTTP_200_OK)
    """@property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self,queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self,data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)"""

class RDVReportedAgentApi(APIView):

    pagination_class=PageNumberPagination
    serializer_class= RdvReporteAgentSerializer
    queryset = ""
    paginator = pagination_class()

    def get(self,request):
        data = request.data 
        id = request.GET.get("rdv",None)
        if id is not None:
            self.queryset = RdvReporteAgent.objects.filter(rdv=RendezVous.objects.filter(pk=int(id)).first() )
            #reported = 
            page = self.paginator.paginate_queryset(self.queryset,request,view=self)
            #if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)
            """if reported.exists():
                serializer = RdvReporteAgentSerializer(reported,many=True)
                return Response(serializer.data,status = status.HTTP_200_OK)
            else:
                return Response({"status":"none"},status = status.HTTP_200_OK)"""
        self.queryset = RdvReporteAgent.objects.all()
        page = self.paginator.paginate_queryset(self.queryset,request,view=self)
        #if page is not None:
        serializer = self.serializer_class(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

        #serializer = RdvReporteAgentSerializer(reported,many=True)
        #return Response(serializer.data,status = status.HTTP_200_OK)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self,queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self,data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


