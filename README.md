STATUS :
1/ OK-CMDB-ASSET-ID : Match entre les assets_id des tables : assets / IT_equipment
2/ 'ASSET_ID OK / SHORT_NAME MISMATCH' : Match des ASSETS ID avec des noms courts différents
3/ /!\ Asset_ID affiché : Seulement pour les serveurs, match entre les noms courts de IT_equipment et celui 
d'assets avec les 3 derniers caracteres en moins. Exemple : IT_equipment.nom = SU941, assets.nom_court = SU941AOS
4/OK-POSITION : Position entre asset.DALLE et IT_equipment.REPERAGE_ID qui match
5/ NOM DU FABRICANT : ASSET_ID : Regroupe les NAS et leur extension lorsqu'ils sont dans le même Rack (NetAPP)



--- PROBLEME
Nom court / long '%FRC2' sont mal référencé sur les deux tables ils sont contenus dans le dossier Mismatch

LES EXTENSIONS :
- FEX
- NETAPP / NETAPPS 
- P-Class : power supply + computer ont une ligne différante

NA0VLB05/06 -> Rack X29 : toutes les extensions en anomalie entre CMDB et 6-Sigma
---------------------
Netapp :  Exemple sur NA0VLB05/06 -> Rack X29 : toutes les extensions en anomalie entre CMDB et 6-Sigma

    ATTO : Netapp à ajouter

  -> 139 d'extensions Netapp à corrigés

Cisco : FEX Extender : non rattachés avec leur switch maitre

  -> 72 cas 

  => stratégie à valider : toute extension est reliée avec son controleur maitre ??? (CC)


Scality : NA9TCR-FERME -> 35 en NULL pour NOM = 'NA9TCR'

  


  -> Patch Panel : aucun interêt -> 205 lignes


-------
VIEWS :
it_built_system_NAS : NAS principal (netapp, ATTO, Brocade) sans les extensions
it_built_system_storage_analytics_by_rack : regroupement des systems storage (System 2-en-1 avec chassis + server) classé par rack
it_build_system_EXADATA: regroupement des equipements avec comme fabricant Oracle
it_build_system_HPC : regroupement des equipements HPC, une ligne par FERME (même s'ils sont plusieurs par rack/salle en vrai) pour ratacher les fermes sans status 
a