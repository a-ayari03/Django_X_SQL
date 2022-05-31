## Version

V1 : It_equipment
V2 : It_equipment
V3 : Olivier_it
V4 : It_equipment

___


## STATUS
 1. OK-CMDB-ASSET-ID : Match entre les assets_id des tables : assets / IT_equipment
 2. /!\ Asset_ID affiché : Seulement pour les serveurs, match entre les noms courts de IT_equipment et celui 
d'assets avec les 3 derniers caracteres en moins. Exemple : IT_equipment.nom = SU941, assets.nom_court = SU941AOS
 3. OK-POSITION : Position entre asset.DALLE et IT_equipment.REPERAGE_ID qui match
	 3.2.  MATCH-POSITION : nombre de match par position entre IT_equipment et la CMDB non filtree : 'ok-position:1'	
 4. NOM DU FABRICANT : ASSET_ID : Regroupe les NAS et leur extension lorsqu'ils sont dans le même Rack (NetAPP)
 5.  'CMDB-OK-OLD' : equipments avec l'extension _OLD/-OLD dans la CMDB mais pas dans IT_Equipment
 6. ~~'MISMATCH_TIRET' : equipments avec un tiret manquant et/ou différents entre les deux bases~~
 7. FEX : ASSET_ID : Regroupe les FEX et ses extensions même s'ils ne sont pas dans le meme rack
 8. EXADATA : No match 
 9. Netapp : No match
 10. PCP : No Match
 11. HDS : [asset_id sur la base CMDB] sinon 'No match' : regroupement des equipments HDS / Hitachi en se basant sur les 5 premiers charactères 
 12. MATCH-CMDB : HORS Status Install : Si aucun status et qu'il y a match enetre les noms et/ou position sur la cmdb non filtrée
 13. DXI : ASSET_ID : Regroupe les FEX et ses extensions même s'ils ne sont pas dans le meme rack

## STATUS_3 
Status inspiré d'olivier_it, lorsque `STATUS` est non null, alors `status_3` = 'Identifiable'. Permet de voir plus rapidement les equipements non identifiable


## ASSET_ID_OK_POSITION
On cherche tous les OK-position:1 et on rajoute dans la colonne `ASSET_ID_OK_POSITION` l'asset id correspondant dans la CMDB


AUDIT :
12. Mise à jour des notes et création de colonne qui référence l'équipement de la CMDB
1.1 Patch_Panel : Equipments du type Patch Panel
1.2 Linked_equipment : On fait le lien entre la cmdb et notes associées à une audit, généralement le bon asset_id est référencé dans la colonne asset_id_to_add

13. Ajout d'une nouvelle colonne. On essaye de retracer pour quelle raison il n'y a pas eu de match initialement
2.1 OK-Position : Si le status ok:position existe c'est qu'il y a plusieurs match sur une seule position. Impossible de faire le choix sans controle des bases et/ou controle physique
2.2 Wrong position : Oublie de position / mauvaise position renseigné = Recherche manuel de l'asset-id et de l'équipement
2.3 Wrong Salle  : Mauvaise salle ou salle avec extension dans la CMDB



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

------
