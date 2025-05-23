
# 🧭 Guide de gestion des environnements Django : DEV / VIP / PROD

## 📁 Structure des environnements

| Environnement | Objectif                           | Autorisations                     |
|---------------|-------------------------------------|------------------------------------|
| **DEV**       | Développement de nouvelles features | ✅ `makemigrations`<br>✅ `migrate` |
| **VIP**       | Test / QA / Pré-prod                | ❌ `makemigrations`<br>✅ `migrate` |
| **PROD**      | Environnement de production         | ❌ `makemigrations`<br>✅ `migrate` |

---

## 🔄 Refaire proprement l'environnement VIP (RAZ)

### Étapes à suivre

#### 1. 📦 Sauvegarder ce qui doit l’être *(optionnel)*
```bash
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > vip_backup.json
```

---

#### 2. 🗑️ Supprimer la base VIP
- **PostgreSQL** :
  ```bash
  dropdb nom_base_vip
  createdb nom_base_vip
  ```
- **SQLite** :
  Supprimer le fichier `.sqlite3`.
- **Docker** :
  ```bash
  docker-compose down -v
  docker-compose up -d
  ```

---

#### 3. 🧹 Nettoyer les migrations locales
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
git checkout origin/dev -- */migrations/
```

---

#### 4. 🧱 Recréer les tables et appliquer les migrations
```bash
python manage.py migrate
```

---

#### 5. 🧪 Recharger les données de test (si besoin)
```bash
python manage.py loaddata vip_backup.json
```

---

## 🔒 Prévention : Interdire les `makemigrations` en VIP

### Option : blocage dans `manage.py`
```python
import sys
if 'makemigrations' in sys.argv:
    print("❌ ERREUR : makemigrations interdit en VIP. Fais-le uniquement en DEV.")
    sys.exit(1)
```

---

## ⚙️ Adapter les données entre environnements avec un script Python

Crée une commande personnalisée dans `yourapp/management/commands/adapt_env.py` :

```python
from django.core.management.base import BaseCommand
from yourapp.models import MyModel

class Command(BaseCommand):
    help = 'Adapte les données selon l’environnement (vip, prod)'

    def add_arguments(self, parser):
        parser.add_argument('--env', type=str, help='dev / vip / prod', required=True)

    def handle(self, *args, **options):
        env = options['env']

        if env == 'vip':
            self.stdout.write("🔧 Adaptation pour VIP en cours...")
            self.adapt_for_vip()
        elif env == 'prod':
            self.stdout.write("🔒 Préparation PROD en cours...")
            self.adapt_for_prod()
        else:
            self.stdout.write(self.style.ERROR("❌ Environnement non reconnu."))

    def adapt_for_vip(self):
        for obj in MyModel.objects.all():
            obj.label = obj.label.upper()
            obj.save()
        self.stdout.write(self.style.SUCCESS("✅ Données adaptées pour VIP."))

    def adapt_for_prod(self):
        for obj in MyModel.objects.filter(validated_by__isnull=False):
            obj.sync_status = 'ready'
            obj.save()
        self.stdout.write(self.style.SUCCESS("✅ Données préparées pour PROD."))
```

---

### ▶️ Exécution

```bash
python manage.py adapt_env --env=vip
python manage.py adapt_env --env=prod
```

---

## 🧠 Rappels essentiels

- Les migrations sont **du code versionné** ➜ uniquement générées en **DEV**.
- Toujours **tester les migrations en VIP** avant de les appliquer en PROD.
- En PROD : **jamais de `makemigrations`**, et **toujours une sauvegarde** avant toute migration.
- Pour synchroniser : **DEV → VIP → PROD**, jamais l’inverse.
