
from django.db import models

# Create your models here.

class Bailleur(models.Model):
    nom = models.CharField("Nom du bailleur",max_length=100,null=True)
    prenom = models.CharField("prenom du bailleur",max_length=100,null=True)
    email = models.CharField("email du bailleur",max_length=100,null=True)
    reference = models.CharField("référence du bailleur",max_length=100,null=True)

    def __str__(self) -> str:
        return self.nom+" "+self.prenom

class Locataire(models.Model):
    nom = models.CharField("Nom du locataire",max_length=100,null=True)
    prenom = models.CharField("prénom du locataire",max_length=100,null=True)
    email = models.CharField("Email du locataire",max_length=100,null=True)
    telephone= models.CharField("Telephone du locataire",max_length=30,null=True)

    def __str__(self) -> str:
        return self.nom+" "+self.prenom

class TypePropriete(models.Model):
    type = models.CharField('Type',max_length=50)
    statut = models.IntegerField('statut du model')
    created_at= models.DateTimeField("Date de creation",auto_now_add=False)
    updated_at = models.DateTimeField("Date de modification", auto_now_add=True)

class Propriete(models.Model):
    surface = models.CharField("Surface du bien",max_length=100,null=True)
    numero= models.CharField('numéro de porte de la propriété',max_length=100,null=True)
    numeroParking= models.CharField("Numéro de parking",max_length=100,null=True)
    adresse = models.CharField("Adresse de la propriété", max_length=100,null=True)
    codePostal= models.CharField("Code postal de la propriété",max_length=100,null=True)
    ville = models.CharField("ville de la propriété",max_length=100,null=True)
    adresseComplementaire= models.CharField("Adresse complémentaire de la propriété",max_length=100,null=True)
    numeroCave = models.CharField("Numéro de cave de la propriété",max_length=100,null=True)
    numeroSol = models.CharField("Numéro de sol",max_length=100,null=True)
    bailleur = models.OneToOneField(Bailleur,on_delete=models.CASCADE,null=True,related_name="bailleur")
    locataire = models.OneToOneField(Locataire,on_delete=models.CASCADE,null=True,related_name="locataire")
    ancien_locataire = models.CharField("old locatire",max_length=80,null=True)
    date_sortie_ancien_locataire= models.DateTimeField("Date de creation",auto_now_add=False,null=True)
    type = models.CharField("Type de bien",max_length=50,null=True)
    type_propriete = models.ForeignKey(TypePropriete,on_delete=models.CASCADE,null=True,related_name="type_de_propriete")

class TypeIntervention(models.Model):
    type = models.CharField("Type d'intervention",max_length=50,null=True)
    statut = models.IntegerField("Statut",null=True)
    created_at= models.DateTimeField("Date de creation",auto_now_add=False)
    updated_at = models.DateTimeField("Date de modification", auto_now_add=True)

class RendezVous(models.Model):
    ref_lot = models.CharField('ref lot', max_length=100, null=True)
    ref_rdv_edl = models.CharField('reference rendez-vous EDL',max_length=100,null=True)
    intervention = models.ForeignKey(TypeIntervention,on_delete=models.CASCADE,null=True,related_name="type_intervention")
    propriete = models.OneToOneField(Propriete,on_delete=models.CASCADE,null=True,related_name="propriete")
    client = models.IntegerField("Client",null=True)
    date = models.DateTimeField("Date et heure du RDV",auto_now_add=False,null=True)
    passeur = models.BigIntegerField("Passeur",null=True)
    agent = models.IntegerField("Agent responsable du RDV",null=True)
    longitude = models.CharField("longitude",max_length=100,null=True)
    latitude = models.CharField("latitude",max_length=100,null=True)
    liste_document_recuperer = models.CharField("liste de document à recupérer",max_length=200,null=True)
    consignes_particuliere = models.CharField("Consignes particulière",max_length=200,null=True)
    info_diverses = models.CharField("Informations diverses",max_length=300,null=True)
    statut = models.CharField('Statut du RDV',max_length=30,default="Attente prise en charge",null=True)
    couleur = models.CharField('couleur du RDV',max_length=30,default="red",null=True)
    ancien_client_id = models.CharField("ancien client ID", max_length=50, null=True)
    ancien_agent_trigramme = models.CharField("Ancien agent trigramme",max_length=15,null=True)
    agent_constat = models.CharField("Agent constat",max_length=50,null=True)
    numero = models.CharField("Numero",max_length=20,null=True)
    ref_commande = models.CharField("Reference commande",max_length=40,null=True)
    last_update_by = models.IntegerField("Modifier par", null=True)
    audit_planneur = models.IntegerField("Audit planneur",null=True)
    created_at= models.DateTimeField("Date de creation",auto_now_add=False,null=True)
    updated_at = models.DateTimeField("Date de modification", auto_now_add=False,null=True)

class RdvReporteDate(models.Model):
    rdv = models.ForeignKey(RendezVous,on_delete=models.CASCADE,related_name="Rendez_vous_date")
    ancienneDate = models.DateTimeField("Ancienne date de RDV",auto_now_add=False)
    created_at = models.DateTimeField("Date de mise à jour",auto_now_add=True)

class RdvReporteAgent(models.Model):
    rdv = models.ForeignKey(RendezVous,on_delete=models.CASCADE,related_name="Rendez_vous_agent")
    ancien_agent = models.IntegerField("Ancien agent",null=False)
    created_at =  models.DateTimeField("Date de mise à jour",auto_now_add=True)


    

