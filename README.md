STATUS :
1/ OK-CMDB-ASSET-ID : Match entre les assets_id des tables : assets / IT_equipment
2/ 'ASSET_ID OK / SHORT_NAME MISMATCH' : Match des ASSETS ID avec des noms courts différents
3/ /!\ Asset_ID affiché : Seulement pour les serveurs, match entre les noms courts de IT_equipment et celui 
d'assets avec les 3 derniers caracteres en moins. Exemple : IT_equipment.nom = SU941, assets.nom_court = SU941AOS
4/OK-POSITION : Position entre asset.DALLE et IT_equipment.REPERAGE_ID qui match

--- PROBLEME
Nom court / long '%FRC2' sont mal référencé sur les deux tables ils sont contenus dans le dossier Mismatch

LES EXTENSIONS :
- FEX
- NETAPP / NETAPPS