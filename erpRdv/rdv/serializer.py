#from tkinter.tix import Tree
from unittest import result
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.relations import method_overridden
from .models import Bailleur, Locataire, TypeIntervention,TypePropriete,Propriete, RendezVous, RdvReporteAgent,RdvReporteDate

class BailleurSerializer(serializers.ModelSerializer):
    class Meta:
        model= Bailleur
        fields = '__all__'

class LocataireSerializer(serializers.ModelSerializer):
    class Meta:
        model= Locataire
        fields = '__all__'

class TypeProprieteSerializer(serializers.ModelSerializer):
    class Meta:
        model= TypePropriete
        fields = '__all__'

class TypeInterventionSerializer(serializers.ModelSerializer):
    class Meta:
        model= TypeIntervention
        fields = '__all__'

class TrackListingFieldBailleur(serializers.RelatedField):
    def to_representation(self, value):
        result = {
            "nom":value.nom,
            "prenom":value.prenom,
            "email":value.email,
            "reference":value.reference,
            "id":value.id
        }
        return result

class TrackListingFieldLocataire(serializers.RelatedField):
    def to_representation(self, value):
        result = {
            "nom":value.nom,
            "prenom":value.prenom,
            "email":value.email,
            "telephone":value.telephone,
            "id":value.id
        }
        return result

class TrackListingFieldTypePropriete(serializers.RelatedField):
    def to_representation(self, value):
        result = {
            "type":value.type,
            "statut":value.statut,
            "created_at":value.created_at,
            "id":value.id
        }
        return result

class TrackListingFieldTypeIntervention(serializers.RelatedField):
    def to_representation(self, value):
        result = {
            "type":value.type,
            "statut":value.statut,
            "created_at":value.created_at,
            "id":value.id
        }
        return result

class ProprieteRepresentation(serializers.RelatedField):
    def to_representation(self, value):
        result = {
            "id":value.id,
            "surface": value.surface,
            "numero": value.numero,
            "numeroParking": value.numeroParking,
            "adresse":value.adresse,
            "codePostal": value.codePostal,
            "ancien_locataire": value.ancien_locataire,
            "date_sortie_ancien_locataire": value.date_sortie_ancien_locataire,
            "ville":value.ville,
            "adresseComplementaire": value.adresseComplementaire,
            "numeroCave":value.numeroCave,
            "type":value.type,
            "numeroSol":  value.numeroSol,
            'bailleur':{"nom":value.bailleur.nom,"prenom":value.bailleur.prenom,"email":value.bailleur.email,"reference":value.bailleur.reference},
            'locataire':{"nom":value.locataire.nom,"prenom":value.locataire.prenom,"email":value.locataire.email,"telephone":value.locataire.telephone},
            "type_propriete": {"type": value.type_propriete.type,"statut":value.type_propriete.statut,"id":value.type_propriete.id },

        }
        return result

class ProprieteSerializer(serializers.ModelSerializer):
    bailleur = TrackListingFieldBailleur(read_only=True,many=False)
    locataire = TrackListingFieldLocataire(read_only=True,many=False)
    type_propriete = TrackListingFieldTypePropriete (read_only=True,many=True)
    class Meta:
        model= Propriete
        fields = '__all__'

class RendezVousSerializer(serializers.ModelSerializer):
    propriete = ProprieteRepresentation(read_only=True,many=False)
    intervention = TrackListingFieldTypeIntervention(read_only=True,many=False)
    class Meta:
        model= RendezVous
        fields = '__all__'


class rendezVousRepresentation(serializers.RelatedField):
    def to_representation(self, value):
        result = {
            "id":value.id,
            "ref_lot" : value.ref_lot,
            "ref_rdv_edl": value.ref_rdv_edl,
            "intervention" :{"type":value.intervention.type,"id":value.intervention.id},
            "propriete" :{
                            "id":value.propriete.id,
                            "surface": value.propriete.surface,
                            "numero": value.propriete.numero,
                            "numeroParking": value.propriete.numeroParking,
                            "adresse":value.propriete.adresse,
                            "codePostal": value.propriete.codePostal,
                            "ville":value.propriete.ville,
                            "type": value.propriete.type,
                            "adresseComplementaire": value.propriete.adresseComplementaire,
                            "ancien_locataire": value.ancien_locataire,
                            "date_sortie_ancien_locataire": value.date_sortie_ancien_locataire,
                            "numeroCave":value.propriete.numeroCave,
                            "numeroSol":  value.propriete.numeroSol,
                            "type" : value.propriete.type,
                            "bailleur" : {"nom": value.propriete.bailleur.nom,"prenom":value.propriete.bailleur.prenom,"email":value.propriete.bailleur.email,"id":value.propriete.bailleur.id },
                            "locataire" :{"nom": value.propriete.locataire.nom,"prenom":value.propriete.locataire.prenom,"email":value.propriete.locataire.email,"telephone":value.propriete.locataire.telephone,"id":value.propriete.locataire.id },
                            "type_propriete": {"type": value.propriete.type_propriete.type,"statut":value.propriete.type_propriete.statut,"id":value.propriete.type_propriete.id },
                        },
            "client" : value.client,
            "passeur":value.passeur,
            "agent":value.agent,
            "longitude":value.longitude,
            "latitude" : value.latitude
        }
        return result
    
class RdvReporteDateSerializer(serializers.ModelSerializer):
    rdv = rendezVousRepresentation(read_only=True,many=False)
    class Meta:
        model= RdvReporteDate
        fields = '__all__'

class RdvReporteAgentSerializer(serializers.ModelSerializer):
    rdv = rendezVousRepresentation(read_only=True,many=False)
    class Meta:
        model= RdvReporteAgent
        fields = '__all__'