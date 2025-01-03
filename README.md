# Algorytmy wyznaczania trasy w systemach nawigacyjnych

Projekt realizowany w ramach kursu Programowanie aplikacji geoinformacyjnych (2024). Głównym celem projektu jest implementacja algorytmów wyznaczania tras w sieci drogowej przy użyciu języka Python i integracja z systemem GIS. Dodatkowo projekt będzie rozszerzony o funkcję **wyznaczania zasięgu**, co pozwoli określić punkty, do których można dotrzeć w określonym czasie.

Autorzy: Adrian Fabisiewicz (@affq), Julia Gomulska (@julka3110)

## Realizacja
Stworzono dwa toole do ArcGIS-a Pro, pozwalające na wyznaczenie najszybszej i najkrótszej trasy oraz obszaru, do jakiego można dotrzeć w określonym czasie.

### Narzędzie do wyznaczania tras
#### Interfejs

<div align="center">
  <img src="https://github.com/user-attachments/assets/6a9f7b42-cb78-4d1a-a159-7fdecf5b40c8" width="300" height="auto"/>
</div>

#### Przykład działania
Trasy wyznaczone przez narzędzie: na zielono - trasa najkrótsza, na różowo - najszybsza

<div align="center">
  <img src="https://github.com/user-attachments/assets/8f00656a-8fe4-4f03-8587-99c4c96092da" width="500" height="auto"/>
</div>

### Narzędzie do wyznaczania zasięgu
#### Interfejs

<div align="center">
  <img src="https://github.com/user-attachments/assets/b3194648-59a1-4d28-8b64-c1c4899e96b2" width="300" height="auto"/>
</div>

#### Przykład działania
Trasy możliwe do pokonania w ciągu 7 minut z punktu startowego przy Bibliotece Uniwersyteckiej w Toruniu

<div align="center">
  <img src="https://github.com/user-attachments/assets/dcdc9582-939c-4c93-a777-26b196c44148" width="500" height="auto"/>
</div>
