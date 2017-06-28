# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    db_func.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mmorel <mmorel@student.42.us.org>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2017/06/27 21:04:07 by mmorel            #+#    #+#              #
#    Updated: 2017/06/27 21:04:08 by mmorel           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def get_db(database):
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(database)
        print ('Connection established')
    return db

def init_db(database):
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as file:
            db.cursor().executescript(file.read())
        db.commit()
