# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    populate_graph.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mmorel <mmorel@student.42.us.org>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2017/06/27 21:06:33 by mmorel            #+#    #+#              #
#    Updated: 2017/06/27 21:06:35 by mmorel           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def populateGraph():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("select humidity from humidity where strftime('%d', time) > '25' and strftime('%d', time) < '31'")
    r = c.fetchall()
    hum = []
    for member in r:
        hum.append(member[0])
    c.execute("select strftime('%m-%d %H:%M', time) from humidity where strftime('%d', time) > '25' and strftime('%d', time) < '31'")
    r = c.fetchall()
    time = []
    for member in r:
        time.append(member[0])
    c.close()
    trace_high = go.Scatter(
                    x=time,
                    y=hum,
                    name = "AAPL High",
                    line = dict(color = '#17BECF'),
                    opacity = 0.8)
    data = [trace_high]
    layout = dict(
        title = "Humidity History",
        xaxis = dict(
            range = ['2017-06-23','2017-06-30'],
            autotick = False,
            tick0 = 0,
            dtick = 6
            )
    )

    fig = dict(data=data, layout=layout)
    graph = plotly.offline.plot(fig, show_link=False, filename="humidity_graph.html", output_type='div', auto_open=False)
    
    return (graph)