---
tags: proyect ia data-mining selenium 
name: QuiniAI
collaborators: Christian Adrian
---
# Todos:
- [ ] Leer datos con selenium
- [ ] Crear scripts de inicialización e instalación
- [ ] Crear docker compose
- [ ] Establecer conexión a BD
- [ ] Scripts iniciación de BD
- [ ] Hacer Magia

## Recolecta de Datos
Mining Data Webpage [FLASH SCORES](https://www.flashscore.com/football/spain/laliga/standings/#/SbZJTabs/over_under/overall/2.5)
Results Url (By Season): https://www.flashscore.com/football/spain/laliga-{START_YEAR}-{END_YEAR}/results/
Herramienta: **Selenium**

# BD
Postgres
## Esquemas Base de Datos
### Equipos
| id equipo | nombre_equipo |

### Temporada XXXX
|id equipo | posición liga |

### H2H
> Las Filas son los equipos locales, las columnas son los visitantes
> El factor es en función de la fila

fila por equipo (local)
columna por equipo
Contenido: Factor de peso en el head 2 head
Ejemplo:
	- Madrid vs Celta: 1.2 (probabilidad que gane el madrid en local vs celta visitante)
	- Celta vs Madrid: 0.8 (probabilidad que gane el celta en local vs madrid visitante)

### Factor Local vs Visitante
| id equipo |  factor_local |  factor_visitante | temporada

### Partidos de Liga 
> TABLA PRINCIPAL

| id_partido |  equipo_local | equipo_vist | goles_local | goles_visitante | fecha | jornada | temporada (año de comienzo) | 

### Partidos de Torneo
> SUDA

| id_partido |  equipo_local | equipo_vist | goles_local | goles_visitante | fecha | jornada | temporada (año de comienzo) | 

## Cálculo de Predicciones
1. Cálculo Estado del Equipo vista 3 años
2. Cálculo del H2H específico con todo el histórico
3. Hace rmagia y combinarlos (*asignado: Adri*)

## Lógicas a Tener en Cuenta
- [ ] Básicas (Goles a Favor, en Contra, Rachas de Partidos, Home vs Away)
- [ ] Si tienen partido próximo (temas de descansar el equipo, usar suplentes.. para no cansarlos para el siguiente partido)
- [ ]  Dificultad del equipo
