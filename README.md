STATUS :
1/ OK-CMDB-ASSET-ID : Match entre les assets_id des tables : assets / IT_equipment
2/ 'ASSET_ID OK / SHORT_NAME MISMATCH' : Match des ASSETS ID avec des noms courts différents
3/ /!\ Asset_ID affiché : Seulement pour les serveurs, match entre les noms courts de IT_equipment et celui 
d'assets avec les 3 derniers caracteres en moins. Exemple : IT_equipment.nom = SU941, assets.nom_court = SU941AOS
4/OK-POSITION : Position entre asset.DALLE et IT_equipment.REPERAGE_ID qui match
5/ NOM DU FABRICANT : ASSET_ID : Regroupe les NAS et leur extension lorsqu'ils sont dans le même Rack (NetAPP)
6/ 'CMDB-OK-OLD' : equipments avec l'extension _OLD/-OLD dans la CMDB mais pas dans IT_Equipment
7/ 'MISMATCH_TIRET' : equipments avec un tiret manquant et/ou différents entre les deux bases
8/ FEX : ASSET_ID : Regroupe les FEX et ses extensions même s'ils ne sont pas dans le meme rack
 9/
  1. EXADATA : No match 
  2. Netapp : No match
  3. PCP : No Match
10 / HDS : [asset_id sur la base CMDB] sinon 'No match' : regroupement des equipments HDS / Hitachi en se basant sur les 5 premiers charactères 
11 / MATCH-POSITION : nombre de match par position entre IT_equipment et la CMDB non filtree
12 / MATCH-CMDB : HORS Status Install : Si aucun status et qu'il y a match enetre les noms et/ou position sur la cmdb non filtrée


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
it_build_system_HANA : regroupement des equipements HANA (soit avec le nom/nom de baie : hana), une ligne par rack oú le status n'est pas null
it_build_system_RING : regroupement des equipements "NA9TCR" avec un status non null, une ligne par rack
IT_Equipment_OLD : regroupement des equipements qui match avec equipements 'XXX_OLD' de la table `asset_new` et représente les equipements qui ne doivent pas être la mais qui y sont quand meme
IT_Equipment_FEX: regroupement des equipements cisco de type switch qui disposent d'extension mais pas forcement dans le meme rack, ex : SWC3PC27-FEX105 est rattache à l'equipement SWC3PC27
IT_Equipment_cleaning_Hitachi : regroupement et nettoyage des noms correspondants au fabricant Hitachi avec de faciliter la jointure et reduire la taille de la query 
it_equipment_all_retired_asset : regroupement des matchs de position et/ou nom entre IT_equipment et la cmdb filtré avec un status Etat = 'Retired'
IT_Equipment_match_position_reduced : Version condensée de IT_Equipment + jointure avec asset_new uniquement sur la position
IT_Equipment_match_position : Regroupement de tous les matchs de position et/ou nom entre IT_equipment sans filtre avec rajout du nombre de match par equipment : Exemple, nom = CH002 correspond à une seule ligne sur IT_Equipment mais à 32 lignes sur Asset = 32 lignes générés avec toutes les infos essentielles
IT_Equipment_match_no_proliant_c7000 : Regroupement de tous les matchs de position et/ou nom entre IT_equipment sans filtre où le status est nulle (rajout du status MATCH-CMDB : HORS Status Install)