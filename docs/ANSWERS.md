# Réponses du test

## _Utilisation de la solution (étape 1 à 3)_

Dans ce projet, il était demandé d'élaborer et d'implémenter un flux de données qui récupère quotidiennement les données
provenant de l'api fournie.

Pour cela, j'ai décidé de créer un dossier supplémentaire dans le répertoire src, afin de bien séparer les fichiers de 
l'api et ceux du flux de données pour gagner en lisibilité et en organisation. Ce dossier est nommé datapipeline et contient : 
- un fichier python nommé data_functions.py qui contient toutes les fonctions nécessaires à l'execution du script
- un autre fichier python nommé datapipeline.py qui correspond au script qui sera réellement executé

Le fichier data_functions contient donc trois fonctions principales : 
- la fonction call_api qui prend en paramètres l'url vers l'api et le nom de la route à appeler ("users" par exemple). Cette fonction aura pour
objectif, comme son nom l'indique, des appels à l'API. Nous allons décrire plus en détail comment elle fonctionne : 

    Tout d'abord, afin de pouvoir joindre l'api, cette fonction utilise la librairie requests. Dans ce cas d'utilisation
nous ne faisons que récupérer des données, donc nous n'utiliserons que la fonction requests.get. Cette fonction prend
en entrée l'url à interroger, que nous avons ici découpé en deux parties : l'adresse du serveur de l'api (ici le localhost) et la route spécifique contenu dans le paramètre "route". 
Cela nous permet de ne pas dupliquer le code d'appel à l'api trois fois (une fonction pour chaque route). Premièrement, parce que cela impliquerait de la 
duplication de code, chose à éviter à tout prix car en cas de changement quelconque dans la fonction il faudrait reporter les changements
plusieurs fois mais également parce que si nous avions plus d'appels différents à réaliser ce serait ni maintenable ni lisible.
Ensuite, pour s'assurer que nous n'avons pas de problème à contacter l'api, ce qui pourrait arriver pour diverses raisons, comme l'utilisation d'une route
inexistante ou erronée par exemple. Nous sécurisons notre appel à l'aide du mot clé "try". Ce qui va nous permettre ensuite d'appeler la function 
raise_for_status() qui lèvera une exception si la réponse contient un code de statut d'erreur. Cela permet à notre fonction d'avoir un comportement approprié 
si une erreur survient. 
Pour finir, si l'appel se déroule correctement et qu'aucune exception n'est levée, nous allons utiliser la fonction .json() afin de transformer la réponse de l'api
en données sous le format json, ce qui nous sera utile pour la suite. 

- Nous arrivons donc dans la fonction suivante : transform_to_df(). Cette fonction a pour objectif de prendre en entrée les données json, fournies par la fonction que 
nous avons décrite précédemment, et de les transformer en dataFrame. Cela, selon moi, nous apporte plusieurs avantages. Pour commencer, un dataframe est un type de données
qui est facilement exploitable. Effectivement, dans ce cas précis nous récupérons les données brutes et nous n'appliquons aucune trasnformation à celles-ci, mais dans un cas
réel ce ne sera certainement pas le cas. Travailler et transformer un json est compliqué et peu intuitif. Ici, nous avons utiliser pandas pour générer le dataFrame car les
jeux de données sont de petites tailles mais nous aurions pu également utiliser spark. Spark nous aurait permit de traiter plus efficacement et de manière distribuée les jeux 
de données très massifs que serait en réalité le type de données que nous utilisons dans ce problème. De plus, les transformations que je viens de décrire peuvent être très utiles
en cas déboguage du flux de données. On peut facilement afficher, filtrer, etc. les données.

- Ensuite, nous passons par la fonction suivante save_to_database(), qui, dans un cas réel, permettrait d'enregistrer les données fraîchement récupérées et traitées vers sa base de
données. Ici, je n'ai pas implémenté cette fonction pour le faire car cela ne rentrait pas dans les contraintes de ce test. À la place, à des fins de tests, j'ai quand même
enregistré les données dans des fichiers csv en local. Ce qui nous est utile à des fins de test. 

Pour finir avec le code source de ce flux de données, nous allons nous intéresser au deuxième fichier du package : datapipeline.py
Ce fichier, comme je l'ai dis précédemment, sera le script executable. Il est donc composé d'une seule et unique fonction fetch_data() qui se chargera de réaliser les appels aux
différentes fonctions que je viens de décrire pour les 3 cas dont nous avions besoin.
Cette fonction doit être appelée quotidiennement. J'ai donc utilisé la librairie schedule afin de planifier le lancement de cette fonction tous les jours à 2h du matin par exemple.
C'est par souci de simplicité pour ce test que j'ai choisi cette librairie mais dans un cas réel, il serait préférable d'utiliser un outil d'orchestration tel que Apache Airflow qui
est plus complet et plus adapté à un flux de données. 
Afin que le script ne s'arrête pas après son execution et qu'il perdure dans le temps nous avons du rajouter une boucle infinie due à l'utilisation de schedule.

Dans le cas précis du test technique, il était demandé de réaliser un flux pour récupérer les différentes données. Cependant, je pense que dans une utilisation concrète il serait préférable que chaque donnée
ait son propre flux. Cela pourrait permettre par exemple de paralléliser les traitements et de gagner en efficacité si les ressources le permettent. Cela pourrait donner également plus
d'indépendance à chaque flux. Si nous avons eu un problème avec les users par exemple, plusieurs flux distincts nous permettraient de ne relancer que celui dont nous avons besoin et donc
d'économiser en temps et ressources. De même lors du développement de nouvelles features et des tests. 

Pour ce qui est des tests unitaires, j'ai ajouté un script test_datapipeline.py dans le dossier test. J'ai testé les différentes fonctions décrites dans le fichier data_functions afin de m'assurer 
que les résultats soient bien les résultats escomptés. Pour la première fonction call_api, j'ai écris 4 tests, un pour chacune des trois routes (afin d'être sûre que j'arrive à y accéder) et un cas 
default contenant une requête qui ne doit pas aboutir pour voir comment se comporte ma fonction dans ce cas. J'ai appliqué ce même principe pour la fonction suivante transform_to_df dans laquelle j'ai
également réaliser une vérification du schéma de données attendu. Pour la dernière fonction, il ne m'a pas semblé nécessaire de tester l'écriture de fichier pour les 3 routes j'ai donc pris une route
comme exemple tout en gardant le test "bad request".

## Questions (étapes 4 à 7)

### Étape 4

Pour ce qui est de la base de données j'utiliserais une base de données relationnelle SQL car dans notre cas d'utilisation, les données ont besoins d'être reliées les unes aux autres. Les données provenant
de l'API ont un schéma et des attributs fixes. Cela nous permet également de réaliser des jointures complexes indispensables à notre système de recommendation.

Pour ce qui est des tables, je garderai une structure similaire à ce que nous rend l'API en en créant trois : users, tracks et listen_history.
Les tables users et tracks auraient les attributs que l'on devine facilement avec la structure des données provenant de l'API : 
- Pour tracks : ['id' Primary key, 'name', 'artist', 'songwriters', 'duration', 'genres', 'album', 'created_at', 'updated_at']
- Pour users : ['id' Primary key, 'first_name', 'last_name', 'email', 'gender', 'favorite_genres', 'created_at', 'updated_at']

C'est ensuite pour la table dernière table listen_history que je ferais les choses un peu différement. 
En analysant les données renvoyées par l'API je vois que nous avons une ligne par utilisateur. À chaque utilisateur est associé un array de tracks_id, une date de création et une date de mise à jour.
Je trouve l'utilisation d'un array très peu propice à ce que nous voulons faire avec les données. Comme dit précédemment, notre système de recommendation nécessite un lien fort en les différentes tables.
Cet array ne nous permet pas de faire facilement et efficacement des jointures. Par exemple, si nous voulons tout simplement récupérer les noms de toutes les chansons écoutées par un utilisateur en joignant avec 
la table tracks ou si nous voulons déterminer l'artiste le plus écouté du moment. 
Dans la question précédente, lors que j'expliquais comment j'avais réaliser ma solution je parlais de transformations qui pouvaient être appliquées sur les données avant leur enregistrement dans la base de données.
Je propose donc ici la mise en place d'un traitement qui viendrait "exploser" les lignes de cette table (ce qui est très facilement faisable avec un dataframe pandas ou spark). Nous aurions donc une ligne par écoute 
plutôt qu'une ligne par utilisateur. Ce qui donnerait un schéma comme ceci : 
- listen_history : ['user_id' Foreign key, 'track_id' Foreign key]

La table listen_history agirait donc comme une table d'association entre les deux tables précédentes. Cela fait beaucoup de sens car un même utilisateur va très probablement écouter plusieurs musiques mais chaque 
musique sera également amenée à être écouté par grand nombre d'utilisateurs. 
Effectivement, cela va engendrer une multiplication du nombre de lignes dans la table ce qui pourrait poser des problèmes de performances même si cela simplifie considérablement les requêtes.
Pour réduire cela, nous pouvons par exemple, indexer la table sur les deux clés étrangères user_id et track_id.

### Étape 5

Afin de s'assurer de la bonne santé de notre pipeline de données, nous pouvons surveiller quelques métriques intéressantes :
- réussite de l'execution : s'assurer chaque jour que la pipeline se soit exécuté sans échec 
- le temps d'execution de la pipeline : si nous savons que l'execution de notre flux prend environ 1h par exemple nous pouvons mettre une alerte si le temps passé dépasse un certain seuil.
- le volume des données : de même que pour le temps d'execution, un volume de données trop petit ou trop important par rapport au volume habituellement traité peut representer un moyen
simple et efficace de déceler des anomalies dans le flux.

Ces différentes vérifications peuvent être executées à la main chaque jour mais il est préférable tout de même de l'automatiser afin de limiter les erreurs humaines et ne pas faire
"perdre du temps" à un humain pour les réaliser. 
Nous pouvons utiliser des outils qui permettent d'analyser les logs en sortie de notre pipeline et d'envoyer des notifications (par email par exemple) à l'équipe en cas de problème.

### Étape 6

Pour automatiser le calcul de recommandation, je pense qu'il serait préférable de créer une autre pipeline de données.
Ce flux devra être en mesure de venir récupérer les données contenues dans notre base et de calculer les nouvelles recommandations avant de les envoyer aux utilisateurs par le biais d'une API.
Pour ce qui est de la planification de ce flux, plusieurs choix peuvent être interessants : 
- Nous pouvons planifier périodiquement le lancement de cette pipeline avec Airflow comme nous l'avons décrit précédemment pour notre flux.
La périodicté pourrait dépendre des besoins du client : une ou deux fois par semaine par exemple. Ce choix est intéressant car il permet une grande flexibilité pour le client
quant au service qu'il veut fournir à ces utilisateurs en fonction des ressources nécessaires au calcul.
- Si la pipeline doit être executée tous les jours, elle pourrait être déclenchée à la suite de notre flux d'ingestion de données. Ce qui serait pertinent car cela permet de s'assurer
que la pipeline d'ingestion ait bien finit sa tâche et que les données ait bien été fraîchement mises à jour. Si les deux pipelines s'overlap cela poserait de grand soucis quant à la stabilité
de celles-ci
- Enfin, nous pourrions potentiellement imaginer une solution très poussée du point de vue de l'expérience utilisateur. Le but ici serait de relancer le calcul de recommandation de manière plus 
personnalisé en ne calculant qu'après x nouvelles écoutes. Cela permettrait à l'utilisateur de voir ses recommandations évoluées de manière intelligente au fil de ses écoutes. Cela pourrait également
permettre de ne pas recalculer de recommandations à un utilisateur inactif.

Pour résumé, je pense que si le calcul de nouvelles recommendations n'est pas trop gourmand en temps et en ressources, la solution numéro 2 est la plus adaptée à notre problème actuel car elle est un
bon compromis entre l'expérience utilisateur dans laquelle ils voient leurs recommandations mises à jour régulièrement et la contrainte qui est la récupération des données quotidienne.
Sinon dans le cas contraire, la solution numéro 1 serait plus adaptée. 
Le système 3 aurait plus de sens, selon moi, dans un système plus "streaming" où nous récupérons et traitons les données au fil des écoutes des utilsateurs.

### Étape 7

Afin d'automatiser le réentrainement du modèle les choix qui s'offrent sont très similaires aux choix précédemment décrits. 
Il faudrait créer une autre pipeline qui se chargerait de venir récupérer les données et d'entrainer le modèle. 
Cette pipeline serait automatisée à l'aide d'Airflow tout comme les deux autres et pourrait être déclenchée périodiquement, une fois par semaine ou toutes les deux semaines par exemple. 
Si notre client souhaite des recommandations intelligentes qui évoluent vite on pourrait imaginer réentrainer le modèle tous les jours, ce qui pourrait donner un traitement quotidien comme ceci :

Flux d'ingestion de données déclenche le ré-entrainement du modèle qui déclenche lui-même le calcul des nouvelles recommandations. 

Je pense que ce traitement est lourd pour une pipeline quotidienne car, l'entrainement d'un modèle est quelque chose de complexe et qui prend beaucoup de temps. 
Dans ce cas-ci, il est plus judicieux d'utiliser la solution numéro une et de ré-entraîner le modèle moins souvent. 
Pour commencer, un même modèle fournira différents résultats de recommandations et peut donc être ré-utilisé plusieurs fois pour générer des recommandations différentes.
D'un point de vue de coût et de temps de traitement, c'est la solution la plus adaptée sachant qu'il n'est pas nécessaire d'avoir un nouveau modèle plus d'une fois par semaine selon moi.


