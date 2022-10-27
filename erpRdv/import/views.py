from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rdv.models import  RendezVous,Bailleur,Locataire,Propriete,TypeIntervention,TypePropriete,RdvReporteAgent,RdvReporteDate
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
import xlwt, xlrd,random, string, json


class ImportApi(APIView):

    def post(self,request):
        fichier = request.FILES.get('fichier')
        data_=request.data
        data = None
        if not fichier.name.endswith('xls'):
            return JsonResponse({"status":1},status=401)
        try:
            data = xlrd.open_workbook(filename=None, file_contents=fichier.read(), formatting_info=True)
        except Exception as e:
            return JsonResponse({"status":2},status=401)

        table = data.sheets()[0]
        nligne = table.nrows
        ncolonnes = table.ncols
        colnames = table.row_values(0)
        liste_finale =[]
        for i in range(nligne):
            liste_temp = []
            for j in range(ncolonnes):
                cell_values = table.row_values(i)[j]
                liste_temp.append(cell_values)
            liste_finale.append(liste_temp)
        del(liste_finale[0])
        for liste in liste_finale: 
            #try:
            if int(data_["cible"]) == 1:
                CreatedDate = datetime(*xlrd.xldate_as_tuple(liste[3],data.datemode))
                type_ = TypeIntervention.objects.create(
                    id = liste[0],
                    type = liste[2],
                    statut = 1,
                    created_at  = CreatedDate,
                    updated_at = CreatedDate
                ) 
            if int(data_["cible"]) == 2:
                CreatedDate = datetime(*xlrd.xldate_as_tuple(liste[3],data.datemode))
                type_ = TypePropriete.objects.create(
                    id = liste[0],
                    type = liste[2],
                    statut = 1,
                    created_at  = CreatedDate,
                    updated_at = CreatedDate
                ) 
            if int(data_["cible"]) == 3:
                #return JsonResponse({"status":data_["agent"]},status=200) 
                if type(liste[11]) != float:
                    CreatedDate=datetime(1990,1,1,12,12)
                else:
                    CreatedDate = datetime(*xlrd.xldate_as_tuple(liste[11],data.datemode))

                if type(liste[39]) != float:
                    Createdat_=datetime(1990,2,2,12,12)
                else:
                    Createdat_ = datetime(*xlrd.xldate_as_tuple(liste[39],data.datemode))
                
                if type(liste[40]) != float:
                    updatedat_=datetime(1990,2,2,12,12)
                else:
                    updatedat_ = datetime(*xlrd.xldate_as_tuple(liste[40],data.datemode))
                
                for u in range(40):
                     if liste[u] == "NULL":
                        liste[u] = None
                with transaction.atomic():
                    if CreatedDate.year == 2022:
                        bailleur = Bailleur.objects.create(
                            nom = liste[14],
                            prenom = liste[15],
                            email = liste[16],
                            reference = liste[13],
                        )
                        locataire = Locataire.objects.create(
                            nom = liste[28],
                            prenom = liste[29],
                            email = liste[31],
                            telephone= liste[30],
                        )
                    
                        propriete = Propriete.objects.create(
                            surface = liste[18],
                            numero= liste[21],
                            numeroParking= liste[22],
                            adresse = liste[24],
                            codePostal= liste[26],
                            ville = liste[27],
                            adresseComplementaire= liste[25],
                            numeroCave =liste[23] ,
                            numeroSol = liste[20],
                            bailleur =bailleur,
                            locataire = locataire,
                            type = liste[19],
                            ancien_locataire = liste[32],
                        ) 

                        if liste[33] is not None:
                            propriete.date_sortie_ancien_locataire = datetime(*xlrd.xldate_as_tuple(liste[33],data.datemode))
                        else:
                            propriete.date_sortie_ancien_locataire = None

                        if liste[17] is not None:
                            propriete.type_propriete = TypePropriete.objects.filter(pk=int(liste[17])).first() 
                        else:
                            propriete.type_propriete = liste[17]
                                         
                        propriete.save()
                        
                        rdv = RendezVous.objects.create(
                            id = liste[0],
                            ref_lot = liste[9],
                            ref_rdv_edl = liste[10],
                            propriete = propriete,
                            #client = int(liste[1]),
                            date = CreatedDate,
                            #passeur = int(liste[3]),
                            #agent = int(liste[4]),
                            liste_document_recuperer = liste[34],
                            consignes_particuliere = liste[35],
                            info_diverses = liste[36],
                            #statut = int(liste[37]),
                            couleur = "red",
                            #ancien_client_id = int(liste[2]),
                            ancien_agent_trigramme = liste[5],
                            #agent_constat = int(liste[6]),
                            numero = liste[7],
                            ref_commande = liste[8],
                            last_update_by =liste[38], 
                            created_at= Createdat_,
                            updated_at = updatedat_,
                        ) 
                        if liste[1] is not None:
                            rdv.client = int(liste[1])
                        if liste[3] is not None:
                            rdv.passeur = int(liste[3])
                        if liste[4] is not None:
                            rdv.agent = int(liste[4])
                        if liste[37] is not None:
                            rdv.statut = int(liste[37])
                        if liste[2] is not None:
                            rdv.ancien_client_id = int(liste[2])
                        if liste[6] is not None:
                            rdv.agent_constat = int(liste[6])

                        if liste[4] is None:
                            rdv.agent = 690
                        #for agent in  data_["agent"]:
                            #if liste[4] is not None and agent[0] == int(liste[4]):
                                #rdv.agent = agent['agent']
                        rdv.save
                        if liste[12] is not None:
                            rdv.intervention = TypeIntervention.objects.filter(pk=int(liste[12])).first()
                        else:
                            rdv.intervention = liste[12]
                        
                        rdv.save()

                        if liste[1] is None:
                            rdv.delete()

            #except Exception as e:
                #return JsonResponse({"status":3},status=401)    
        return Response({},status=status.HTTP_200_OK)
