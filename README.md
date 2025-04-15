# Accessibilité

## Création des branches dev et preprod

### preprod
La branche `preprod` est utilisée pour les environnements de pré-production.

Pour créer et basculer sur la branche `preprod` :
```bash
git checkout -b preprod
git push origin preprod
```
### dev
La branche dev est utilisée pour le développement et dépend de la branche preprod.

Pour créer et basculer sur la branche dev à partir de preprod :

```bash
git checkout -b dev
git push origin dev
```
### Étape 7 : Commit et push les modifications du README

Ajoutez, committez et poussez les modifications du fichier README :

```bash
git add README.md
git commit -m "Ajout des instructions pour les branches preprod et dev"
git push origin dev