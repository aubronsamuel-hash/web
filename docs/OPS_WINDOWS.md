# OPS Windows

## Prerequis

* PowerShell 5.1+ ou PowerShell 7+
* Git
* Python 3.11+ et Node LTS (prochaines etapes)

## Scripts

```powershell
# Generer/maj docs
.\scripts\ps1\New-Docs.ps1

# Formater fichiers simples (fin de ligne, trimming)
.\scripts\ps1\Format-Docs.ps1

# Verifier presence fichiers, ASCII, lignes > 120
.\scripts\ps1\Test-Docs.ps1
```

## Codes retour

0 OK; 1 USAGE_INVALIDE; 2 PREREQUIS_MANQUANTS; 10 ERREUR_INTERNE.
