



MàJ 04/10/2022 
Le dossier contient la présence de 5 workflows :

    1/ Olivier_it_Workflow.ipynb : mise à jour des tables relatifs à la CMDB, IT_equipments et Olivier_IT. Série de traitement permettant de déterminer les équipements bien localisés et ceux qui présentent des anomalies
    2/ Vision_spatial.ipynb  : Ajout des equipements manquants à Olivier_it
    3/ IT_Equipment_Workflow.ipynb : Ajout des equipements manquants à IT_equipemnts et série de traitement permettant de déterminer les équipements bien localisés et ceux qui présentent des anomalies
    4/ Equipment_move_workflow.ipynb : mise à jour des equipments de la table IT_equipments. Taracking des déplacements d'équipements
    5/ Simulateur_espace.ipynb : Simule l'espace disponible et identifie les slot vides sur chacun des racks afin de permettre une projection des équipes dans le déplacement du matériel.
    
# Liste des indicateurs en sortie : 
    
   - IT_Equipment_unique_records : table avec les équipements unique
   - indicator_it_equipment_count_per_salle (http://127.0.0.1:8000/show_indicator_room/)
   - indicator_it_equipment_count_per_type_per_salle (http://127.0.0.1:8000/show_indicator_type_room/)
   - indicator_it_equipment_simulateur_espace (descriptif des attribues dans la section : **#3/ Simulateur_espace**) (http://127.0.0.1:8000/show_simulateur_espace/): Simulation de l'espace disponible dans le datacenter après le calcul de tous les équipements
   - indicator_it_equipment_simulateur_masterplan (http://127.0.0.1:8000/show_simulateur_espace_mp/)
   - indicator_it_equipment_simulateur_avant_apres_masterplan (http://127.0.0.1:8000/show_simulateur_espace_before_after_mp/)
   - IT_Equipment_x_olivier_it : Ajout des commentaires et attribues d'olivier_it sur 6sigma (workflow IT_Equipment_Workflow)
   - 6SIGMA_report (descriptif des attribues dans la section : **#5 IT_Equipment_Workflow_rapport** ): Rapport servant aux équipes de 6SIGMA d'insérer leurs commentaires/analyses et d'éffectuer directement le traitement de 6sigma sur le meme rapport  
 

 Le fonctionnement des workflows est assurés par la présence de fichier dans ses 4 dossiers : 
	 - Downloads/ : Présence des scripts permettant le bon fonctionnement des workflows
	 - Downloads/raw_file : Présence des **fichiers csv permettant la mise à jour des bases de données**
	 - Downloads/historique : Historique de tous les fichiers ayant servi aux bases de données
	 - Downloads/query_folder : Présence des scripts permettant le bon fonctionnement des workflows

# Pipeline 

**INPUT** : Les fichiers csv (généralement asset_new, IT_Equipment et/ou Olivier_it) doivent être standardisés et glissés dans le dossier ***Downloads/raw_file***  au format qui suit :
	- <nom_de_la_base>_<date_au_format : dd.mm.yy>.csv . Exemple : fichier en rapport à la base de donnée IT_Equipment se nommera ***IT_Equipment.04.02.2022.csv***
**OUTPUT** : Une fois la mise à jour effectuée, les fichiers csv seront transférés sous le dossier **Downloads/historique**. Un fichier exporté contenant tous les traitements sera crée sous le dossier **Downloads/resultat/année_mois_jour/**.

1. Lancement du script `Update_olivier_it.py` afin de mettre à jour les bases de données (CMDB, Olivier_it, 6Sigma) et initialiser les workflows Olivier_it_Workflow et Vision_spatial

>  cd Downloads/

> python3 Update_olivier_it.py

2. Lancement du script `Update_IT_Equipment.py` afin de mettre à jour la base de donnée (6Sigma) et initialiser le workflow IT_Equipment_Workflow.ipynb

>  cd Downloads/

> python3 Update_IT_Equipment.py

3. Lancement du script `Update_It_equipment_records.py` afin de mettre à jour la base de données IT_equipement et initialiser le workflow Equipment_move_workflow. Seul les fichiers csv contenus dans le dossier **Downloads/historique** serviront au fonctionnement du workflow.

>  cd Downloads/

> python3 Update_It_equipment_records.py
> 
4. Lancement du script `Update_IT_Equipment_report.py` : création d'un rapport au format olivier_it. Nécessite la présence du dernier rapport en cours `Claude_it` dans le dossier **Downloads/raw_file** pour fonctionner. Il est possible de rajouter des attributs/colonnes en modifiant le schema de creation de la table dans le fichier suivant /home/alexandre/Downloads/query_folder/olivier_it_2_sql_query.txt. Attention, l'ordre doit correspondre au rapport 6SIGMA généré par les query du workflow IT_Equipment

>  cd Downloads/

> python3 Update_IT_Equipment_report.py

5. Execution du script `Update_simulateur_spatial.py` afin de mettre à jour la simulation de l'espace avec et sans la prise en compte le master plan disponible dans les racks
>  cd Downloads/

> python3 Update_simulateur_spatial.py

6. Execution du script `export_csv.py` permettant d'enregistrer au format csv n'importe quel table disponible dans la database :

> cd Downloads/

> python3 export_csv.py <nom_de_la_table>

Un fichier exporté contenant tous les traitements sera crée sous le dossier **Downloads/resultat/année_mois_jour/<nom_de_la_table>**
    
# 1/ Olivier_it_Workflow (non requis)

Le workflow repose sur la mise à jour des fichiers csv IT_equipments, Assets_new (CMDB) ainsi que Olivier_it afin de constater les écarts entre les différentes base de données.
Le workflow est scindé en deux fichiers : Vision_spatial.ipynb ainsi que Olivier_it_Workflow.ipynb :

- **Vision_spatial** : Lance une série de requêtes visant à comparer les équipements présents sur les 3 bases de données dans le but d'avoir une liste des équipements manquant à Olivier_it. Une fois identifiés, les équipements sont rajoutés à la base Olivier_it afin d'appliquer des traitements du workflow olivier_it_workflow.
- **Olivier_it_Workflow** : Série de traitement permettant de déterminer les équipements bien localisés et ceux qui présentent des anomalies.

Une fois inséré, la description détaillée des traitements effectués est disponible sur le fichier Olivier_it_Workflow .ipnyb (Jupyter Notebook).
Plusieurs attributs sont ainsi générés : 

- attribut `status_6sigma`: 
	-  OK : asset id présent sur 6Sigma
	- KO : Non présent

- attribut `status_CMDB`: 
	-  OK : asset id présent sur CMDB
	- KO : Non présent

- attribut `status_position_6sigma`: Salle + Rack + 1er slot de l'équipement
	-  OK : Position présente sur 6Sigma
	- KO : Non présent

- attribut `status_position_CMDB`: Salle + Rack + 1er slot de l'équipement
	-  OK :Position présente sur CMDB
	- KO : Non présent

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


`indicator_it_equipment_count_per_salle` : résumé du nombre d'equipment par salle et par mois

     - P1_P2: sommes des équipements dans les salles P1 et P2
     - P3_P4: sommes des équipements dans les salles P3 et P4
     - P1: nb d'equipement P1
     - P2: nb d'equipement P2
     - P3: nb d'equipement P3
     - P4: nb d'equipement P4

`indicator_it_equipment_count_per_type_per_salle` : résumé du nombre d'equipment par salle, type et par mois

     - P1_P2: sommes des équipements dans les salles P1 et P2
     - P3_P4: sommes des équipements dans les salles P3 et P4
     - P1: nb d'equipement P1
     - P2: nb d'equipement P2
     - P3: nb d'equipement P3
     - P4: nb d'equipement P4

# 3/ Simulateur_espace.ipynb

Ce workflow a pour but de simuler l'espace disponible sur chacun des racks afin de permettre une projection des équipes dans le déplacement du matériel. Deux variantes du workflow existent (Simulateur_espace_with_master_plan_remove.ipynb)

1. `indicator_it_equipment_simulateur_espace `: **indicateur de l'espace disponible pour tous les rack** par rapport à la somme des hauteurs de chaque équipement renseigné sur la CMDB sans prendre en considération les futures équipements retirer  :

	- rack capacity : nombre de slot disponble par rack (par défaut -1)
		- Si la valeur affichée est -1 sela signifie que les attribues du rack ne sont pas disponible dans le fichier `Cabinet.csv`
	- quantity slot occupied : nombre de slot utilisé
	- quantity available occupied : nombre de slot disponible
	- available slot : position des slots disponible
	- number of alimentation : nombre d'alimentation disponible par rack d'après le fichier `Cabinet.csv` 

2.  `indicator_it_equipment_simulateur_espace_mp` : simuler l'espace disponible en tenant compte des futurs équipements (de la salle P2 uniquement pour l'instant) sensés être retirer d'après le Master Plan.
			- rack capacity : nombre de slot disponble par rack (par défaut -1)
			- Si la valeur affichée est -1 sela signifie que les attribues du rack ne sont pas disponible dans le fichier `Cabinet.csv`
		- quantity slot occupied : nombre de slot utilisé
		- quantity available occupied : nombre de slot disponible
		- available slot : position des slots disponible
		- number of alimentation : nombre d'alimentation disponible par rack d'après le fichier `Cabinet.csv` 


# 4/ IT_Equipment_Workflow.ipynb

Le workflow repose sur la mise à jour des fichiers csv IT_equipments (6SIGMA ), Assets_new (CMDB) ainsi que Olivier_it afin de constater les écarts entre les différentes base de données et de rajouter les équipements manquant de la CMDB à 6SIGMA 

Une fois inséré, la description détaillée des traitements effectués est disponible sur le fichier IT_Equipment_Workflow.ipnyb (Jupyter Notebook).
Plusieurs attributs sont ainsi générés : 

- attribut `status_CMDB`: 
	-  OK : asset id présent sur CMDB
	- KO : Non présent

- attribut `status_position_CMDB`: Salle + Rack + 1er slot de l'équipement
	-  OK :Position présente sur CMDB
	- KO : Non présent

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

# 5/ IT_Equipment_Workflow_rapport.ipynb

Le workflow repose sur la mise à jour des fichiers csv IT_equipments (6SIGMA ), Assets_new (CMDB) ainsi que Olivier_it afin de constater les écarts entre les différentes base de données et de rajouter les équipements manquant de la CMDB à 6SIGMA. Il permet en outre de générer un rapport des équipements présent sur 6SIGMA et CMDB à destinations des équipes

Les fichiers en sortie : **6SIGMA** et **CMDB** sont constitués des attribues suivants :

- Les attribues de `Modele` à `Nom_de_la_salle` sont générés automatiquement lors du traitement et proviennent de la base 6SIGMA

- Les attribues de `End_Move_Target` à `Index_CC` sont récupérés à chaque traitement du fichier initial 

- attribut `from_source`: 
	-  6SIGMA: équipement présent sur la base 6SIGMA
	-  CMDB:  équipement uniquement présent sur la CMDB
	
- attribut `status_CMDB`: 
	- OK : asset id présent sur CMDB
	- KO : Non présent

- attribut `status_position_CMDB`: Salle + Rack + 1er slot de l'équipement
	-  OK :Position présente sur CMDB
	- KO : Non présent

- attribut `status_asset_id` : 
    - "Trouvé - bon asset id"
    - "Non Trouvé - Mauvais Asset ID" impossibilité de trouver l'asset_id dans la CMDB (assets_filtrée)
    
- attribut `status_position` : 
    - "Bonne localisation"
    - "KO localisation" : impossibilité de trouver la position dans la CMDB (assets_filtrée)

- attribut `status_name` : Priorisation du status affiché 
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

- attribut `status_global` : agrégation des status asset_id, de position, de nom et de l’état de l’équipement

- attribut `status_etat` : Si un équipement est repéré (par son asset_id et/ou sa position ) 
    - "Trouvé - bon asset id"
    - "Non Trouvé - Mauvais Asset ID"
    - "KO Etat" - Aucun ou plusieurs equipments sur la même position, impossible d'établir le lien

- attribut `status_etat_hpe` : agrégation des status asset_id et de position
    1- pas asset id & pas de localisation
    2- pas asset id & localisation
    3- assed id & localisation => status
    4- asset id & pas localisation ==> "assetid"
    5- PCP ==> "PCP"
    6- Patch Panel => "Patch Panel"
- attribut `status_status` : Agrégation de tous les attributs
- attribut `status_CC` : Agrégation de tous les attributs avec mots clés

- attribut `status_spec` : attribut spécial dépendant de certains équipements
    - "Patch Panel"
    - "PCP"
    - 'PCP : KO' uniquement pour les équipements des rack I11->O11
    
- Les attribues de `status_cc` à `Hauteur_U` sont générés automatiquement lors du traitement et proviennent de la base 6SIGMA

- attribut `date_apparition` : date d'apparition de l'équipement pour la première fois (d'après la CMDB) par rapport à son asset_id et son nom

-  attribut `date_dernier_mouvement` : date du dernier mouvement de l'équipement (d'après la CMDB) par rapport à son asset_id et son nom
- attribut `date_clean` : 
	- NULL : L'équipement est toujours présent dans la base 6SIGMA
	- Si une date est affichée selon correspond à la date de nettoyage 

### Un fichier : `CMDB_TO_FILTER.csv` est disponible dans le dossier ***Downloads/query_folder***  et permet de manuellement ajouter des modèles d'équipement à supprimer dans le rapport final CMDB
