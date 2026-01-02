# f1-stats
A cli tool to fetch different statistics about formula 1 using [f1db]()

## Features
You can fetch plenty of different tables and statistics: 

- Season tables (driver/constructor standings) in wikipedia like style

- Detailed info about season races, qualifications, pit stop times

- circuits all time records: best lap times, best qualification times, driver with most wins, most podiums. 

## Examples

```sh
# The season tables
python f1_stats.py --gp-flags season 2023 >> README.md
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

```sh
# Season overview (different statistics)
python f1_stats.py driver fernando-alonso 2012 -o
```

```
Season overview — fernando-alonso, 2012
--------------------------------------------------
Races: 20  Finished: 18  Not finished/started: 2  (rate: 10.0%)

Points
- Total pts: 278 pts (2 place)
- Team pts share: 69.50%
- Pts per race: 13.90 pts
- Avg pts when scoring: 15.44 pts
- Points volatility (std): 7.59 pts

Qualifying & starts
- Poles: 2  (Pole rate: 10.0%)
- Q1, Q2 eliminations: 3 (rate: 15.0%)
- Q3 appearances: 17
- Pole conversion (poles / Q3s): 11.8%
- Avg grid position: 6.10
- Median grid position: 6.00
- Most common grid position: 2
- Penalties: 0

Results & rates
- Wins: 3  (Win rate: 15.0%)
- Podiums: 13  (Podium rate: 65.0%)
- Scoring finishes: 18  (Scoring rate: 90.0%)
- Fastest laps: 0  (Fastest-lap rate: 0.0%)
- Finish rate: 90.0%
- Avg finish position: 3.28
- Median finish position: 3.00
- Most common finish position: 2
- Finish position CV (coefficient of variation): 0.660

Pit stops & strategy
- Avg pit stops per race: 1.94
- Avg pit stops time: 21.91s
- Problematic pit stops: 0

Not started/finished/classified, disqualified:
- DNF: 2 (10.0%)
  * belgium - Collision
  * japan - Collision
- DNS: 0 (0.0%)
- DSQ: 0 (0.0%)
- NC: 0 (0.0%)

Race progress
- Avg positions gained per race: 3.47
- % races net gain: 72.2%
- % races net loss: 11.1%
- % races no change: 16.7%
- Longest podium streak: 5
- Longest win streak: 1
- Longest points streak: 11
```

```sh
# Circuit records
python f1_stats.py circuit monza --best-lap
```

|    | year | driver             | finish | lap | time     | tyre        | engine     | constructor |
|----|------|--------------------|--------|-----|----------|-------------|------------|-------------|
| 1  | 2025 | Lando Norris       | 2      | 53  | 1:20.901 | pirelli     | mercedes   | mclaren     |
| 2  | 2025 | Max Verstappen     | 1      | 52  | 1:21.003 | pirelli     | honda-rbpt | red-bull    |
| 3  | 2004 | Rubens Barrichello | 1      | 41  | 1:21.046 | bridgestone | ferrari    | ferrari     |
| 4  | 2025 | Oscar Piastri      | 3      | 47  | 1:21.245 | pirelli     | mercedes   | mclaren     |
| 5  | 2025 | Charles Leclerc    | 4      | 53  | 1:21.294 | pirelli     | ferrari    | ferrari     |
| 6  | 2004 | Michael Schumacher | 2      | 35  | 1:21.361 | bridgestone | ferrari    | ferrari     |
| 7  | 2025 | Alexander Albon    | 7      | 53  | 1:21.368 | pirelli     | mercedes   | williams    |
| 8  | 2024 | Lando Norris       | 3      | 53  | 1:21.432 | pirelli     | mercedes   | mclaren     |
| 9  | 2005 | Kimi Räikkönen     | 4      | 51  | 1:21.504 | michelin    | mercedes   | mclaren     |
| 10 | 2024 | Lewis Hamilton     | 5      | 53  | 1:21.512 | pirelli     | mercedes   | mercedes    |
| 11 | 2025 | Lewis Hamilton     | 6      | 50  | 1:21.546 | pirelli     | ferrari    | ferrari     |
| 12 | 2025 | Carlos Sainz Jr.   | 11     | 47  | 1:21.740 | pirelli     | mercedes   | williams    |
| 13 | 2024 | Max Verstappen     | 6      | 43  | 1:21.745 | pirelli     | honda-rbpt | red-bull    |
| 14 | 2019 | Lewis Hamilton     | 3      | 51  | 1:21.779 | pirelli     | mercedes   | mercedes    |
| 15 | 2025 | George Russell     | 5      | 45  | 1:21.800 | pirelli     | mercedes   | mercedes    |

```sh
# Constructor standings
python f1_stats.py season 2025 --constructor >> README.md
```

| pos | name         | AUS | CHN | JPN | BHR | SAU | MIA | EMR | MCO | ESP | CAN | AUT | GBR | BEL | HUN | NLD | ITA | AZE | SGP | USA | MEX | SAO | LAS  | QAT | ABD | pts |
|-----|--------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|-----|-----|-----|
| 1   | McLaren      | 1ᵖᶠ | 2ᶠ  | 2   | 3   | 4ᶠ  | 2ᶠ  | 2   | 1ᵖᶠ | 2   | 18  | 1ᵖ  | 1   | 2ᵖ  | 1   | 18  | 2ᶠ  | 7   | 3   | 2   | 1ᵖ  | 1ᵖ  | DSQᵖ | 4   | 3   | 833 |
| 1   | McLaren      | 9   | 1ᵖ  | 3   | 1ᵖᶠ | 1   | 1   | 3ᵖ  | 3   | 1ᵖᶠ | 4   | 2ᶠ  | 2ᶠ  | 1   | 2   | 1ᵖᶠ | 3   | DNF | 4   | 5   | 5   | 5   | DSQ  | 2ᵖᶠ | 2   | 833 |
| 2   | Mercedes     | 3   | 3   | 5   | 2   | 5   | 3   | 7   | 11  | 4   | 1ᵖᶠ | 5   | 10  | 5   | 3ᶠ  | 4   | 5   | 2   | 1ᵖ  | 6   | 7ᶠ  | 4   | 2    | 6   | 5   | 469 |
| 2   | Mercedes     | 4   | 6   | 6ᶠ  | 11  | 6   | 6   | DNF | 18  | DNF | 3   | DNF | DNF | 16ᶠ | 10  | 16  | 9   | 4   | 5   | 13ᶠ | 6   | 2   | 3    | 5   | 15  | 469 |
| 3   | Red Bull     | 2   | 4   | 1ᵖ  | 6   | 2ᵖ  | 4ᵖ  | 1ᶠ  | 4   | 10  | 2   | DNF | 5ᵖ  | 4   | 9   | 2   | 1ᵖ  | 1ᵖᶠ | 2   | 1ᵖ  | 3   | 3   | 1ᶠ   | 1   | 1ᵖ  | 451 |
| 3   | Red Bull     | DNF | 12  | 17  | 16  | 12  | DNF | 14  | 8   | 11  | DNF | 6   | DNF | 8   | 8   | 12  | 14  | 5   | 15  | 11  | DNF | 7   | 14   | 9   | 18  | 451 |
| 4   | Ferrari      | 8   | DSQ | 4   | 4   | 3   | 7   | 6   | 2   | 3   | 5   | 3   | 14  | 3   | 4ᵖ  | DNF | 4   | 9   | 6   | 3   | 2   | DNF | 4    | 8   | 4ᶠ  | 398 |
| 4   | Ferrari      | 10  | DSQ | 7   | 5   | 7   | 8   | 4   | 5   | 6   | 6   | 4   | 4   | 7   | 12  | DNF | 6   | 8   | 8ᶠ  | 4   | 8   | DNF | 8    | 12  | 8   | 398 |
| 5   | Williams     | 5   | 7   | 9   | 12  | 9   | 5   | 5   | 9   | DNF | DNF | DNF | 8   | 6   | 15  | 5   | 7   | 13  | 14  | 14  | 12  | 11ᶠ | DNF  | 11  | 16  | 137 |
| 5   | Williams     | DNF | 10  | 14  | DNF | 8   | 9   | 8   | 10  | 14  | 10  | DNS | 12  | 18  | 14  | 13  | 11  | 3   | 10  | DNF | 17  | 13  | 5    | 3   | 13  | 137 |
| 6   | Racing Bulls | DNF | 11  | 8   | 13  | 10  | 11  | 9   | 6   | 7   | 16  | 12  | DNF | 20  | 11  | 3   | 10  | 10  | 11  | 16  | 13  | 8   | 6    | 18  | 17  | 92  |
| 6   | Racing Bulls | DNF | 12  | 17  | 16  | 12  | DNF | 14  | 8   | 11  | DNF | 6   | DNF | 8   | 8   | 12  | 14  | 5   | 15  | 11  | DNF | 7   | 14   | 9   | 18  | 92  |
| 7   | Aston Martin | DNF | DNF | 11  | 15  | 11  | 15  | 11  | DNF | 9   | 7   | 7   | 9   | 17  | 5   | 8   | DNF | 15  | 7   | 10  | DNF | 14  | 11   | 7   | 6   | 89  |
| 7   | Aston Martin | 6   | 9   | 20  | 17  | 16  | 16  | 15  | 15  | DNS | 17  | 14  | 7   | 14  | 7   | 7   | 18  | 17  | 13  | 12  | 14  | 16  | DNF  | 17  | 10  | 89  |
| 8   | Haas         | 14  | 8   | 10  | 10  | 13  | DNF | 17  | 12  | 17  | 11  | 11  | 11  | 11  | DNF | 6   | 12  | 12  | 9   | 9   | 4   | 6   | 10   | DNF | 12  | 79  |
| 8   | Haas         | 13  | 5   | 18  | 8   | 14  | 12  | DNF | 7   | 16  | 9   | 10  | 13  | 15  | 16  | 10  | 15  | 14  | 18  | 15  | 9   | 12  | 9    | 15  | 7   | 79  |
| 9   | Kick Sauber  | 7   | 15  | 16  | DSQ | 15  | 14  | 12  | 16  | 5   | 8   | 9   | 3   | 12  | 13  | 14  | DNS | 16  | 20  | 8   | DNF | 9   | 7    | DNF | 9   | 70  |
| 9   | Kick Sauber  | DNF | 14  | 19  | 18  | 18  | DNF | 18  | 14  | 12  | 14  | 8   | DNF | 9   | 6   | 15  | 8   | 11  | 17  | 18  | 10  | DNF | DNF  | 13  | 11  | 70  |
| 10  | Alpine       | 11  | DSQ | 13  | 7   | DNF | 13  | 13  | DNF | 8   | 15  | 13  | 6   | 10  | 19  | 17  | 16  | 18  | 19  | 19  | 15  | 10  | 13   | 16  | 19  | 22  |
| 10  | Alpine       |     |     |     |     |     |     | 16  | 13  | 15  | 13  | 15  | DNS | 19  | 18  | 11  | 17  | 19  | 16  | 17  | 16  | 15  | 15   | 14  | 20  | 22  |

## Installation

```sh
git clone https://github.com/cebem1nt/f1-stats.git
cd f1-stats
./install # Set up the db
```

## Misc

```
python f1_stats.py --help
usage: f1_stats.py [-h] [--double-headers] [--no-delimiters] [--adjustment {left,center,right}] [--gp-flags] {circuit,driver,season,search,db} ...

Diferrent charts, statistics, records, all time bests of Formula One

positional arguments:
  {circuit,driver,season,search,db}
                        Available commands
    circuit             Get different records for a circuit
    driver              Different driver's statistics, data over the season
    season              Fancy wikipedia like season table for driver/constructor championship
    search              Search for different rows in tables by name
    db                  Different database related commands

options:
  -h, --help            show this help message and exit
  --double-headers      Print table headers twice (at the top and bottom)
  --no-delimiters       Do not print any separators for tables
  --adjustment {left,center,right}
                        Table text alignment
  --gp-flags            Add emoji flags to grand prix

# You can also use --help for each subcommand: 
python f1_stats.py driver --help
usage: f1_stats.py driver [-h] [-r] [-s] [-q] [-p] [-o] ID YEAR

positional arguments:
  ID                Driver id
  YEAR              Season year

options:
  -h, --help        show this help message and exit
  -r, --races       Get a table of driver season races
  -s, --sprints     Get a table of driver season sprints
  -q, --qualifying  Get a table of driver qualifyings
  -p, --pit-stops   Get a table of pit stops for each race
  -o, --overview    An overview, driver statistics for a season
```