
Le dossier contient la présence de 3 workflows :

    1/ Olivier_it_Workflow.ipynb : mise à jour des tables relatifs à la CMDB, IT_equipments et Olivier_IT. 
    2/ Equipment_move_workflow.ipynb : mise à jour des equipments de la table IT_equipments. Taracking des déplacements d'équipements
 
 Le fonctionnement des workflows est assurés par la présence de fichier dans ses 4 dossiers : 
	 - Downloads/ : Présence des scripts permettant le bon fonctionnement des workflows
	 - Downloads/raw_file : Présence des **fichiers csv permettant la mise à jour des bases de données**
	 - Downloads/historique : Historique de tous les fichiers ayant servi aux bases de données
	 - Downloads/query_folder : Présence des scripts permettant le bon fonctionnement des workflows

# Pipeline 

1. Les fichiers csv (généralement asset_new, IT_Equipment et/ou Olivier_it) doivent être standardisés et glissés dans le dossier ***Downloads/raw_file***  au format qui suit :
	- <nom_de_la_base>_<date_au_format : dd.mm.yy>.csv . Exemple : fichier en rapport à la base de donnée IT_Equipment se nommera ***IT_Equipment.04.02.2022.csv***

2. Lancement du script `Query_launcher.py` afin de mettre à jour la base de données IT_equipement et initialiser le workflow Equipment_move_workflow. Seul les fichiers csv contenus dans le dossier **Downloads/historique*** serviront au fonctionnement du workflow.


>  cd Downloads/

> python3 Query_launcher.py

3. Une fois la mise à jour effectuée, les fichiers csv seront transférés sous le dossier ***Downloads/historique***. Un fichier exporté contenant tous les traitements sera crée sous le dossier ***Downloads/resultat***.

4. Lancement du script `Update_It_equipment_records.py` afin de mettre à jour les bases de données et initialiser le workflow Olivier_it_Workflow
	
>  cd Downloads/

> python3 Update_It_equipment_records.py

5. Lancement des scripts spécifiques (en cours de construction) :
    - Olivier_it_only_index_launcher.ipynb
    - Vision_spatial_launcher.ipynb
    
# 1/ Olivier_it_Workflow 

Le workflow repose sur la mise à jour des fichiers csv IT_equipments, Assets_new (CMDB) ainsi que Olivier_it afin de constater les écarts entre les différentes base de données.
Une fois inséré, la description détaillée des traitements effectués est disponible sur le fichier Olivier_it_Workflow .ipnyb (Jupyter Notebook).
Plusieurs attributs sont ainsi générés : 
- attribut `Status` :
    - Commun : Equipment present sur fichier Olivier_it & It_equipment
    - Non trouvé : Equipment non present sur It_equipment
    
- attribut `status_asset_id` : 
    - "Trouvé - bon asset id"
    - "Non Trouvé - Mauvais Asset ID" impossibilité de trouver l'asset_id dans la CMDB (assets_filtrée)
    
- attribut `status_position` : 
    - "Bonne localisation"
    - "KO localisation" : impossibilité de trouver la position dans la CMDB (assets_filtrée)

- attribut `status_nom_court` : Priorisation du status affiché 
    
    1. Présence d'asset d'id
        1. "nom_court type OLD"
        2. "nom_long type OLD" 
        3. "OK nom_court"
        4. "OK nom_long"
        5. "Mauvais nom" : nom court/long non présent dans la cmdb
    2. Non présence d'asset d'id
        1. "nom_court type OLD"
        2. "nom_long type OLD" 
        3. "OK nom_court"
        4. "OK nom_long"
        5. "Mauvais nom" : nom court/long non présent dans la cmdb
       
- attribut `status_etat` : Si un équipment est repéré (par son asset_id et/ou sa position ) 
    - "Trouvé - bon asset id"
    - "Non Trouvé - Mauvais Asset ID"
    - "KO Etat" - Aucun ou plusieurs equipments sur la même position, impossible d'établir le lien

- attribut `status_spec` : attribut spécial dépendant de certains équipements
    - "Patch Panel"
    - "PCP"
    
- attribut `status_etat_hpe` : agrégation des status asset_id et de position

    1- pas asset id & pas de localisation
    2- pas asset id & localisation
    3- assed id & localisation => status
    4- asset id & pas localisation ==> "assetid"
    5- PCP ==> "PCP"
    6- Patch Panel => "Patch Panel"
- attribut `status_status` : Agrégation de tous les attributs
- attribut `status_CC` : Agrégation de tous les attributs avec mots clés


# 2/ Equipment_move_workflow.ipynb 
Workflow permettant la mise à jour de la table `IT_equipments_unique_equipments` et la création d'indicateur permettant de tracker le nombre d'equipments et de déplacements par salle

`IT_Equipment_unique_records` : table regroupant tous les asset_id unique, une ligne par equipments avec tous les attribus prédifinis auquel on rajoute : 
    
    - First_occurence : première d'ajout d'un fichier
    - last_move_date : date du dernier changement de position
    - last_move : dernier changement de position
    - last_move_salle : Salle du dernier changement de position
    - Clean date : Si un equipment est jugé clean, la date du dernier ajout est affiché 


`indicateur_equipment_per_salle` : Suit le nombre d'equipment unique par salle

     - first_occurence : nb d'equipement dans la première occurence
     - last_occurence : nb d'equipement dans la dernière occurence
     - in_equipment : nb d'equipement entrée
     - out_equipment : nb d'equipement sortie

Liste des fichiers en sortie : 
    
    - IT_Equipment_unique_records : table avec les équipements unique
    - indicator_it_equipment_count_per_salle : résumé du nombre d'equipment par salle et par mois
    - indicator_it_equipment_count_per_type_per_salle : résumé du nombre d'equipment par salle, type et par mois

    
# 3/ Vision_spatial
Le workflow propose une série de query visant à comparer les résultats de la base de donnée Olivier_it par rapport aux bases 6Sigma et/ou CMDB afin de constater les différences entre les trois principales bases.
Vérification de la présence des equipements Olivier_it simultanément sur 6Sigma et sur la CMDB :

    - Controle de l'asset_id
    - Controle de Position 
    - listes des équipements de 6Sigma et CMDB non présent sur Olivier_it (olivier_it_eq_not_in_6sigma.csv, olivier_it_eq_not_in_cmdb.csv)

liste des fichiers en sortie : 

    - **olivier_it_vision_spatial_date_du_jour_resultat.csv** : Fichier contenant le traitement du workflow
    - **olivier_it_eq_not_in_6sigma.csv** : Liste des équipements 6sigma non présent sur Olivier_it
    - **olivier_it_eq_not_in_CMDB.csv** : Liste des équipements CMDB non présent sur Olivier_it

MàJ 06/07/2022 : 
Liste de fichier provenant du workflow equipment_move_workflow et permettant de mettre en lumière certains problèmes : 

    - **query_meme_nom_resultat_diff.csv** : comparaisons des equipments entre le 04/02/22 et le 17/06/2022 qui ont des noms similaires et des asset_id ou id_systeme_asset différent (sensé être unique et propre à chaque equipment
    - **IT_Equipment_move_salle_name_match.csv** : comparaisons des equipments entre le 04/02/22 et le 17/06/2022 qui ont des noms similaires **ET UNIQUE** . Permet d'observer les déplacements entre les salles
    - **IT_Equipment_non_unique_nom.csv** : comparaisons des equipments du 17/06/22 ayant des noms non unique
    - `IT_Equipment_move_no_asset` : Si un id_systeme_asset n'est pas dispo dans le dernier fichier csv on procède à un check des noms. S'il y a concordence des noms dans le dernier fichier c'est que id_systeme_asset a été modifié. Les deux positions sont ainsi affichées.
