import sqlite3

def select_from_database_best():
  conn = sqlite3.connect('MPPR.sql')
  cur = conn.cursor()
  select_command = f"SELECT \
    CASE \
        WHEN Medieval_2__Total_War >= Empire__Total_War AND Medieval_2__Total_War >= Napoleon__Total_War AND Medieval_2__Total_War >= Total_War__Shogun_2 AND Medieval_2__Total_War >= Total_War__Rome_2 AND Medieval_2__Total_War >= Total_War__Attila AND Medieval_2__Total_War >= Total_War__Three_Kingdoms AND Medieval_2__Total_War >= Total_War__Warhammer THEN 'Medieval_2__Total_War' \
        WHEN Empire__Total_War >= Napoleon__Total_War AND Empire__Total_War >= Total_War__Shogun_2 AND Empire__Total_War >= Total_War__Rome_2 AND Empire__Total_War >= Total_War__Attila AND Empire__Total_War >= Total_War__Three_Kingdoms AND Empire__Total_War >= Total_War__Warhammer THEN 'Empire__Total_War' \
        WHEN Napoleon__Total_War >= Total_War__Shogun_2 AND Napoleon__Total_War >= Total_War__Rome_2 AND Napoleon__Total_War >= Total_War__Attila AND Napoleon__Total_War >= Total_War__Three_Kingdoms AND Napoleon__Total_War >= Total_War__Warhammer THEN 'Napoleon__Total_War' \
        WHEN Total_War__Shogun_2 >= Total_War__Rome_2 AND Total_War__Shogun_2 >= Total_War__Attila AND Total_War__Shogun_2 >= Total_War__Three_Kingdoms AND Total_War__Shogun_2 >= Total_War__Warhammer THEN 'Total_War__Shogun_2' \
        WHEN Total_War__Rome_2 >= Total_War__Attila AND Total_War__Rome_2 >= Total_War__Three_Kingdoms AND Total_War__Rome_2 >= Total_War__Warhammer THEN 'Total_War__Rome_2' \
        WHEN Total_War__Attila >= Total_War__Three_Kingdoms AND Total_War__Attila >= Total_War__Warhammer THEN 'Total_War__Attila' \
        WHEN Total_War__Three_Kingdoms >= Total_War__Warhammer THEN 'Total_War__Three_Kingdoms' \
        ELSE 'Total_War__Warhammer' \
    END AS max_game \
FROM games \
WHERE teleg_id = {385210730}"

  cur.execute(select_command)
  data = cur.fetchall()
  cur.close()
  conn.close()
  return data
print(select_from_database_best())
