# vettel
A cli tool to fetch different statistics and info about formula 1 using [f1db](https://github.com/f1db/f1db)

## Features

- **Drivers statistics during year/all time: total points, poles, q3 apearences, average points, grid positions, diferent rates, streaks and much more**

- **Season tables (driver/constructor standings) in [wikipedia like style](https://en.wikipedia.org/wiki/2025_Formula_One_World_Championship#World_Drivers'_Championship_standings)**

- **Detailed info about season races, sprints, qualifications**

- **Pit stop times**

- **Season calendar**

- **Circuits all time records: best lap times, best qualification times, driver with most wins, most podiums.**

- **Fully offline: Info fetched from local database**

## Examples

<table><tr>
<td>
  
```sh
vet --no-delimiters circuit silverstone -mw -r=30
```
  
```
      Driver                  Total

  1    Lewis Hamilton          9
  2    Alain Prost             5
  3    Jim Clark               3
  4    Michael Schumacher      3
  5    Nigel Mansell           3
  6    Alberto Ascari          2
  7    David Coulthard         2
  8    Fernando Alonso         2
  9    Jackie Stewart          2
  10   Jacques Villeneuve      2
  11   José Froilán González   2
  12   Mark Webber             2
  13   Max Verstappen          2
  14   Sebastian Vettel        2
  15   Ayrton Senna            1
  16   Carlos Sainz Jr.        1
  17   Clay Regazzoni          1
  18   Damon Hill              1
  19   Emerson Fittipaldi      1
  20   Jack Brabham            1
  21   James Hunt              1
  22   John Watson             1
  23   Johnny Herbert          1
  24   Juan Manuel Fangio      1
  25   Juan Pablo Montoya      1
  26   Kimi Räikkönen          1
  27   Lando Norris            1
  28   Mika Häkkinen           1
  29   Nico Rosberg            1
  30   Nino Farina             1
```

</td>
<td>
  
```sh
vet calendar 2026 --utc
```
```
              R1 - Australia
  ----------------------------------------
  - Qualifying:        Mar 07 at 05:00 UTC
  - Race:              Mar 08 at 04:00 UTC

                R2 - China
  ----------------------------------------
  - Sprint qualifying: Mar 13 at 07:30 UTC
  - Sprint:            Mar 14 at 03:00 UTC
  - Qualifying:        Mar 14 at 07:00 UTC
  - Race:              Mar 15 at 07:00 UTC

                R3 - Japan
  ----------------------------------------
  - Qualifying:        Mar 28 at 06:00 UTC
  - Race:              Mar 29 at 05:00 UTC

                R4 - Miami
  ----------------------------------------
  - Sprint qualifying: May 01 at 20:30 UTC
  - Sprint:            May 02 at 16:00 UTC
  - Qualifying:        May 02 at 20:00 UTC
  - Race:              May 03 at 17:00 UTC

           -*- R5 - Canada -*-
  ----------------------------------------
  - Sprint qualifying: May 22 at 20:30 UTC
  - Sprint:            May 23 at 16:00 UTC
  - Qualifying:        May 23 at 20:00 UTC
  - Race:              May 24 at 20:00 UTC

                ....
```

</td>

<td>

```sh
vet race japan 2026
```
```
Finish    Driver              Points

  1         Kimi Antonelli      25
  2 (+1)    Oscar Piastri       18
  3 (+1)    Charles Leclerc     15
  4 (-2)    George Russell      12
  5         Lando Norris        10
  6         Lewis Hamilton      8
  7         Pierre Gasly        6
  8 (+3)    Max Verstappen      4
  9 (+5)    Liam Lawson         2
  10 (+2)   Esteban Ocon        1
  11 (+2)   Nico Hülkenberg
  12 (-4)   Isack Hadjar
  13 (-4)   Gabriel Bortoleto
  14 (-4)   Arvid Lindblad
  15 (+1)   Carlos Sainz Jr.
  16 (-1)   Franco Colapinto
  17 (+2)   Sergio Pérez
  18 (+3)   Fernando Alonso
  19 (+1)   Valtteri Bottas
  20 (-3)   Alexander Albon
  DNF       Lance Stroll
  DNF       Oliver Bearman

Fastest lap: Kimi Antonelli - 1:32.432 (lap 49)


--------------------------------------------------
Lance Stroll - Reason retired: Mechanical
Oliver Bearman - Reason retired: Accident
```

</td>
<td>

```sh
vet standings --flags
```
```
       Name                Nationality   Constructor    Points

  1    Kimi Antonelli      🇮🇹 ITA        Mercedes       156
  2    Lewis Hamilton      🇬🇧 GBR        Ferrari        115
  3    George Russell      🇬🇧 GBR        Mercedes       106
  4    Charles Leclerc     🇲🇨 MON        Ferrari        75
  5    Lando Norris        🇬🇧 GBR        McLaren        73
  6    Oscar Piastri       🇦🇺 AUS        McLaren        68
  7    Max Verstappen      🇳🇱 NED        Red Bull       55
  8    Pierre Gasly        🇫🇷 FRA        Alpine         41
  9    Isack Hadjar        🇫🇷 FRA        Red Bull       34
  10   Liam Lawson         🇳🇿 NZL        Racing Bulls   28
  11   Oliver Bearman      🇬🇧 GBR        Haas           18
  12   Franco Colapinto    🇦🇷 ARG        Alpine         16
  13   Arvid Lindblad      🇬🇧 GBR        Racing Bulls   13
  14   Carlos Sainz Jr.    🇪🇸 ESP        Williams       6
  15   Alexander Albon     🇹🇭 THA        Williams       5
  16   Esteban Ocon        🇫🇷 FRA        Haas           3
  17   Gabriel Bortoleto   🇧🇷 BRA        Audi           2
  18   Fernando Alonso     🇪🇸 ESP        Aston Martin   1
  19   Nico Hülkenberg     🇩🇪 GER        Audi           0
  20   Valtteri Bottas     🇫🇮 FIN        Cadillac       0
  21   Sergio Pérez        🇲🇽 MEX        Cadillac       0
  22   Lance Stroll        🇨🇦 CAN        Aston Martin   0    
```

</td>
<td>

```sh
vet sprint china 2026 --full
```
```
| Finish   | Driver            | Contructor   | Start | Gap     | Laps | Pts |
|----------|-------------------|--------------|-------|---------|------|-----|
| 1        | George Russell    | Mercedes     | 1     |         | 19   | 8   |
| 2 (+4)   | Charles Leclerc   | Ferrari      | 6     | +0.674  | 19   | 7   |
| 3 (+1)   | Lewis Hamilton    | Ferrari      | 4     | +2.554  | 19   | 6   |
| 4 (-1)   | Lando Norris      | McLaren      | 3     | +4.433  | 19   | 5   |
| 5 (-3)   | Kimi Antonelli    | Mercedes     | 2     | +5.688  | 19   | 4   |
| 6 (-1)   | Oscar Piastri     | McLaren      | 5     | +6.809  | 19   | 3   |
| 7 (+6)   | Liam Lawson       | Racing Bulls | 13    | +10.900 | 19   | 2   |
| 8 (+1)   | Oliver Bearman    | Haas         | 9     | +11.271 | 19   | 1   |
| 9 (-1)   | Max Verstappen    | Red Bull     | 8     | +11.619 | 19   |     |
| 10 (+2)  | Esteban Ocon      | Haas         | 12    | +13.887 | 19   |     |
| 11 (-4)  | Pierre Gasly      | Alpine       | 7     | +14.780 | 19   |     |
| 12 (+5)  | Carlos Sainz Jr.  | Williams     | 17    | +15.753 | 19   |     |
| 13 (+1)  | Gabriel Bortoleto | Audi         | 14    | +15.858 | 19   |     |
| 14 (+2)  | Franco Colapinto  | Alpine       | 16    | +16.393 | 19   |     |
| 15 (-5)  | Isack Hadjar      | Red Bull     | 10    | +16.430 | 19   |     |
| 16 (+6)  | Alexander Albon   | Williams     | 22    | +20.014 | 19   |     |
| 17 (+1)  | Fernando Alonso   | Aston Martin | 18    | +21.599 | 19   |     |
| 18 (+1)  | Lance Stroll      | Aston Martin | 19    | +21.971 | 19   |     |
| 19 (+2)* | Sergio Pérez      | Cadillac     | 21    | +28.241 | 19   |     |
| DNF      | Nico Hülkenberg   | Audi         | 11    |         | 12   |     |
| DNF      | Valtteri Bottas   | Cadillac     | 20    |         | 12   |     |
| DNF      | Arvid Lindblad    | Racing Bulls | 15    |         | 11   |     |

* - Sergio Pérez got 5.000s penalty

--------------------------------------------------
Nico Hülkenberg - Reason retired: Mechanical
Valtteri Bottas - Reason retired: Withdrew
Arvid Lindblad - Reason retired: Collision damage
```

</td>
</tr></table>

Season results table
```sh
vet season 2023 --flags >> README.md
```

| pos | name             | 🇧🇭 BHR | 🇸🇦 SAU | 🇦🇺 AUS | 🇦🇿 AZE | 🇺🇸 MIA | 🇲🇨 MCO | 🇪🇸 ESP | 🇨🇦 CAN | 🇦🇹 AUT | 🇬🇧 GBR | 🇭🇺 HUN | 🇧🇪 BEL | 🇳🇱 NLD | 🇮🇹 ITA | 🇸🇬 SGP | 🇯🇵 JPN | 🇶🇦 QAT | 🇺🇸 USA | 🇲🇽 MEX | 🇧🇷 SAO | 🇺🇸 LAS | 🇦🇪 ABD | pts |
|-----|------------------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|-----|
| 1   | Max Verstappen   | 1ᵖ     | 2ᶠ     | 1ᵖ     | 2      | 1ᶠ     | 1ᵖ     | 1ᵖᶠ    | 1ᵖ     | 1ᵖᶠ    | 1ᵖᶠ    | 1ᶠ     | 1      | 1ᵖ     | 1      | 5      | 1ᵖᶠ    | 1ᵖᶠ    | 1      | 1      | 1ᵖ     | 1      | 1ᵖᶠ    | 575 |
| 2   | Sergio Pérez     | 2      | 1ᵖ     | 5ᶠ     | 1      | 2ᵖ     | 16     | 4      | 6ᶠ     | 3      | 6      | 3      | 2      | 4      | 2      | 8      | DNF    | 10     | 4      | DNF    | 4      | 3      | 4      | 285 |
| 3   | Lewis Hamilton   | 5      | 5      | 2      | 6      | 6      | 4ᶠ     | 2      | 3      | 8      | 3      | 4ᵖ     | 4ᶠ     | 6      | 6      | 3ᶠ     | 5      | DNF    | DSQ    | 2ᶠ     | 8      | 7      | 9      | 234 |
| 4   | Charles Leclerc  | DNF    | 7      | DNF    | 3ᵖ     | 7      | 6      | 11     | 4      | 2      | 9      | 7      | 3ᵖ     | DNF    | 4      | 4      | 4      | 5      | DSQᵖ   | 3ᵖ     | DNS    | 2ᵖ     | 2      | 206 |
| 5   | Fernando Alonso  | 3      | 3      | 3      | 4      | 3      | 2      | 7      | 2      | 5      | 7      | 9      | 5      | 2ᶠ     | 9      | 15     | 8      | 6      | DNF    | DNF    | 3      | 9      | 7      | 206 |
| 6   | Lando Norris     | 17     | 17     | 6      | 9      | 17     | 9      | 17     | 13     | 4      | 2      | 2      | 7      | 7      | 8      | 2      | 2      | 3      | 2      | 5      | 2ᶠ     | DNF    | 5      | 205 |
| 7   | Carlos Sainz Jr. | 4      | 6      | 12     | 5      | 5      | 8      | 5      | 5      | 6      | 10     | 8      | DNF    | 5      | 3ᵖ     | 1ᵖ     | 6      | DNS    | 3      | 4      | 6      | 6      | 18     | 200 |
| 8   | George Russell   | 7      | 4      | DNF    | 8ᶠ     | 4      | 5      | 3      | DNF    | 7      | 5      | 6      | 6      | 17     | 5      | 16     | 7      | 4      | 5      | 6      | DNF    | 8      | 3      | 175 |
| 9   | Oscar Piastri    | DNF    | 15     | 8      | 11     | 19     | 10     | 13     | 11     | 16     | 4      | 5      | DNF    | 9      | 12ᶠ    | 7      | 3      | 2      | DNF    | 8      | 14     | 10ᶠ    | 6      | 97  |
| 10  | Lance Stroll     | 6      | DNF    | 4      | 7      | 12     | DNF    | 6      | 9      | 9      | 14     | 10     | 9      | 11     | 16     | DNS    | DNF    | 11     | 7      | 17     | 5      | 5      | 10     | 74  |
| 11  | Pierre Gasly     | 9      | 9      | 13     | 14     | 8      | 7      | 10     | 12     | 10     | 18     | DNF    | 11     | 3      | 15     | 6      | 10     | 12     | 6      | 11     | 7      | 11     | 13     | 62  |
| 12  | Esteban Ocon     | DNF    | 8      | 14     | 15     | 9      | 3      | 8      | 8      | 14     | DNF    | DNF    | 8      | 10     | DNF    | DNF    | 9      | 7      | DNF    | 10     | 10     | 4      | 12     | 58  |
| 13  | Alexander Albon  | 10     | DNF    | DNF    | 12     | 14     | 14     | 16     | 7      | 11     | 8      | 11     | 14     | 8      | 7      | 11     | DNF    | 13     | 9      | 9      | DNF    | 12     | 14     | 27  |
| 14  | Yuki Tsunoda     | 11     | 11     | 10     | 10     | 11     | 15     | 12     | 14     | 19     | 16     | 15     | 10     | 15     | DNS    | DNF    | 12     | 15     | 8ᶠ     | 12     | 9      | 18     | 8      | 17  |
| 15  | Valtteri Bottas  | 8      | 18     | 11     | 18     | 13     | 11     | 19     | 10     | 15     | 12     | 12     | 12     | 14     | 10     | DNF    | DNF    | 8      | 12     | 15     | DNF    | 17     | 19     | 10  |
| 16  | Nico Hülkenberg  | 15     | 12     | 7      | 17     | 15     | 17     | 15     | 15     | DNF    | 13     | 14     | 18     | 12     | 17     | 13     | 14     | 16     | 11     | 13     | 12     | 19     | 15     | 9   |
| 17  | Daniel Ricciardo |        |        |        |        |        |        |        |        |        |        | 13     | 16     |        |        |        |        |        | 15     | 7      | 13     | 14     | 11     | 6   |
| 18  | Guanyu Zhou      | 16ᶠ    | 13     | 9      | DNF    | 16     | 13     | 9      | 16     | 12     | 15     | 16     | 13     | DNF    | 14     | 12     | 13     | 9      | 13     | 14     | DNF    | 15     | 17     | 6   |
| 19  | Kevin Magnussen  | 13     | 10     | 17     | 13     | 10     | 19     | 18     | 17     | 18     | DNF    | 17     | 15     | 16     | 18     | 10     | 15     | 14     | 14     | DNF    | DNF    | 13     | 20     | 3   |
| 20  | Liam Lawson      |        |        |        |        |        |        |        |        |        |        |        |        | 13     | 11     | 9      | 11     | 17     |        |        |        |        |        | 2   |
| 21  | Logan Sargeant   | 12     | 16     | 16     | 16     | 20     | 18     | 20     | DNF    | 13     | 11     | 18     | 17     | DNF    | 13     | 14     | DNF    | DNF    | 10     | 16     | 11     | 16     | 16     | 1   |
| 22  | Nyck de Vries    | 14     | 14     | 15     | DNF    | 18     | 12     | 14     | 18     | 17     | 17     |        |        |        |        |        |        |        |        |        |        |        |        | 0   |

Other:
```sh
# Get 2023 max verstappen comprehensive overview/statistics:
vet driver max-verstappen 2023
```
```sh
# Show driver standings for current year
vet standings
```
```sh
# Get 2023 max verstappen race results table:
vet driver max-verstappen 2023 --races
```
```sh
# Get best lap time at suzuka circuit
vet circuit suzuka --best-lap
```
```sh
# Show driver with most wins, most podiums at silverstone circuit
vet circuit silverstone -mw -mp
```
```sh
# Show 2026 constructor standings
vet season 2026 --constructor
```
```sh
# Show 2026 miami sprint qualifying results
vet sprint miami 2026 -q
```
```sh
# Show full 2026 gp calendar with free practice and circuit name
vet calendar -f -fp -c
```
```sh
# Search database for driver with "max"
vet db --search -d max
```
```sh
# Execute some sql script for db
vet db --sql my_hacky.sql
```

> [!NOTE]
> To get new info, update database once in a while with:
> 
> ```sh
> vet db --update
> ```

## Installation

### AUR:
```sh
yay -S vettel # Or with any other aur helper like paru
```

### From source:

```sh
git clone https://github.com/cebem1nt/vettel.git
cd vettel
```

#### Using pip

```sh
pip install .
```

#### Using old setup.py

```sh
sudo python setup.py install
```

## Misc

```
usage: vet [-h] [-v] [--double-headers] [--no-delimiters] [--adjustment {left,center,right}] {circuit,driver,race,results,sprint,standings,season,calendar,search,db} ...

Different info, statistics, records, all time bests of Formula One

positional arguments:
  {circuit,driver,race,results,sprint,standings,season,calendar,search,db}
                        Available commands
    circuit             Get different records for a circuit
    driver              Different driver's statistics, data over the season or all time
    race                Show exact race result for given year
    results             Show results for all races/quali for given year
    sprint              Sprint results
    standings           Season driver standings
    season              Fancy wikipedia like season table for driver/constructor championship
    calendar            Calendar for a given season
    search              Search the database
    db                  Different database related commands

options:
  -h, --help            show this help message and exit
  -v, --version         Show vettel version and exit
  --double-headers      Print table headers twice (at the top and bottom)
  --no-delimiters       Do not print any separators for tables
  --adjustment {left,center,right}
                        Table text alignment
```
