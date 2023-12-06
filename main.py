import telebot;
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from questions_and_answers import answer_options, questions
from API import KEY


bot = telebot.TeleBot(KEY)



def create_keyboard(text : list, question_number : int):
  keyboard = InlineKeyboardMarkup(); #наша клавиатура

  for i, word in enumerate(text):
    callback_data = f"{question_number}_{i+1}"
    key = InlineKeyboardButton(text=word, callback_data=callback_data)
    keyboard.add(key); #добавляем кнопку в клавиатуру

  return keyboard


@bot.callback_query_handler(func=lambda call: call.data)
def callHandler1(call):
    
    question_number, answer_option = map(int, call.data.split('_'))
    print(answer_option)
    print(call.message.chat.id)

    if(question_number == 20):
      best_result = select_from_database_best(call.message.chat.id)
      bot.send_message(call.message.chat.id, f'Вам больше всего подошла бы: {best_result}')
      delete_table_from_database()
    
    else:
      update_sum_in_game(answer_options[question_number][answer_option], call.message.chat.id)   
      keyboard = create_keyboard(['Да', 'Нет'], question_number + 1)
      bot.send_message(call.message.chat.id, questions[question_number], reply_markup=keyboard)
      print(question_number, questions[question_number])


@bot.message_handler(commands=['start'])
def start_command(message):
  delete_table_from_database()
  create_database()
  #print(message.from_user.id)
  insert_in_database(message.from_user.id)
  keyboard = create_keyboard(['Да', 'Конечно'], 1)
  bot.send_message(message.from_user.id, "Приступим?", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
  
  if message.text:
    bot.send_message(message.from_user.id, "Напиши /start")
  
  else:
    bot.send_message(message.from_user.id, "Какая-то ошибка")


def create_database():
    conn = sqlite3.connect('MPPR.sql')
    cur = conn.cursor()

    # Создание таблицы "games"
    create_games_table = '''
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teleg_id INTEGER,
        Medieval_2__Total_War INTEGER,
        Empire__Total_War INTEGER,
        Napoleon__Total_War INTEGER,
        Total_War__Shogun_2 INTEGER,
        Total_War__Rome_2 INTEGER,
        Total_War__Attila INTEGER,
        Total_War__Three_Kingdoms INTEGER,
        Total_War__Warhammer INTEGER
    )
    '''
    cur.execute(create_games_table)

    conn.commit()
    cur.close()
    conn.close()


def insert_in_database(teleg_id : int):
  conn = sqlite3.connect('MPPR.sql')
  cur = conn.cursor()
  insert_command = f"INSERT INTO games \
                    (teleg_id, Medieval_2__Total_War, Empire__Total_War, Napoleon__Total_War, Total_War__Shogun_2, Total_War__Rome_2, Total_War__Attila, Total_War__Three_Kingdoms, Total_War__Warhammer) \
              VALUES ({teleg_id}, 0, 0, 0, 0, 0, 0, 0, 0)"
  cur.execute(insert_command)
  conn.commit()
  cur.close()
  conn.close()


def delete_table_from_database():
    try:
        conn = sqlite3.connect('MPPR.sql')
        cur = conn.cursor()

        # Delete the specified table
        delete_table_command = f"DROP TABLE IF EXISTS games"
        cur.execute(delete_table_command)

        conn.commit()
        cur.close()
        conn.close()
        print(f"Successfully deleted the table games from the database.")
    except Exception as e:
        print(f"An error occurred: {e}")


def update_sum_in_game(info_for_update : dict, teleg_id : int):
    conn = sqlite3.connect('MPPR.sql')
    cur = conn.cursor()
    update_command = f'\
    UPDATE games \
    SET \
      Medieval_2__Total_War = Medieval_2__Total_War + {info_for_update[0]}, \
      Empire__Total_War = Empire__Total_War + {info_for_update[1]}, \
      Napoleon__Total_War = Napoleon__Total_War + {info_for_update[2]}, \
      Total_War__Shogun_2 = Total_War__Shogun_2 + {info_for_update[3]}, \
      Total_War__Rome_2 = Total_War__Rome_2 + {info_for_update[4]}, \
      Total_War__Attila = Total_War__Attila + {info_for_update[5]}, \
      Total_War__Three_Kingdoms = Total_War__Three_Kingdoms + {info_for_update[6]}, \
      Total_War__Warhammer = Total_War__Warhammer + {info_for_update[7]} \
    WHERE teleg_id = {teleg_id};'
    cur.execute(update_command)
    conn.commit()
    cur.close()
    conn.close()


def select_from_database_best(telegId):
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
WHERE teleg_id = {telegId}"

  cur.execute(select_command)
  data = cur.fetchall()
  cur.close()
  conn.close()
  return data[0][0]


if __name__ == '__main__':
  bot.infinity_polling()
  