# Scale-Invariant Feature Transform (SIFT)

Projekt ma na celu zaprezentowanie algorytmu SIFT oraz eksperymentów na nim przeprowadzonych na potrzeby przedmiotu `Analiza Danych Obrazowych i Multimedialnych` w semestrze `2026L`.

## Zespół

* Cong Minh Vu
* Mateusz Szulc
* Szymon Ochnio
* Mateusz Kwiatkowski

## Zawartość repozytorium

* `demo/demo.ipynb` - główna prezentacja algorytmu: wstęp teoretyczny, wizualizacja kolejnych etapów, opis własnej biblioteki pomocniczej, demonstracja dopasowania obrazów i podsumowanie wniosków z eksperymentów.
* `experiments/experiments<1-4>.ipynb` - eksperymenty na czterech różnych zestawach danych dla trzech konfiguracje parametrów SIFT (baseline, wysoka czułość, optymalizacja szybkości): dopasowanie par obrazów, niezmienniczość na obrót i skalę, estymacja homografii (RANSAC) oraz porównanie SIFT z ORB.

## Konfiguracja środowiska

Wymagana wersja Pythona: 3.12+

### 1. Utwórz wirtualne środowisko

```bash
python -m venv .venv
```

### 2. Aktywuj wirtualne środowisko

Windows (PowerShell):

```powershell
. .\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Zainstaluj zależności

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Uruchomienie

Po instalacji otwórz jeden z notebooków projektu i uruchom komórki lub przeglądaj zapisane już wyniki.
