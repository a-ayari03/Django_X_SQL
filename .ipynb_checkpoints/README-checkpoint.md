
Le dossier contient la présence de 2 workflows :

    1/ Olivier_it_Workflow.ipynb : mise à jour des tables relatifs à la CMDB, IT_equipments et Olivier_IT
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
Workflow permettant la mise à jour de la table `IT_equipments_unique_equipments`.

`IT_Equipment_unique_records` : table regroupant tous les asset_id unique, une ligne par equipments avec tous les attribus prédifinis auquel on rajoute : 
    
    - First_occurence : première d'ajout d'un fichier
    - last_move_date : date du dernier changement de position
    - last_move : dernier changement de position
    - last_move_salle : Salle du dernier changement de position
    - Clean date : Si un equipment est jugé clean, la date du dernier ajout est affiché 


