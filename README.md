# DatabaseFinal

This is going to be the space for my Database Design and Development final project
I'm making my relational database system around a lesson horse barn

## Use Intructions
To see the three queries written in queries.sql, put:

```
sqlite3 -header -column horse_barn.db < queries.sql
```

in the terminal. To see them one at a time, or to make your own, type:

```

sqlite horse_barn.db

.mode colunm
.headers on

<paste/type full query here>

.exit

```

To run our little interface and interact as a client (like our barn director), type:
```
python main.py
```