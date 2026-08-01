# DatabaseFinal

This is my Database Design and Development final project - a relational database for a horse barn that does riding lessons.

## Use Intructions
To see the three queries written in queries.sql, put:

```
sqlite3 -header -column horse_barn.db < queries.sql
```

in the terminal. To see them one at a time, or to make your own, type:

```

sqlite3 horse_barn.db

.mode colunm
.headers on

<paste/type full query here>

.exit

```

To run our little interface and interact as a client (like our barn director), type:
```
python main.py
```
