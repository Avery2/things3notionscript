
    # inbox shape:
    # print(f"{inbox[0]=}")
    # inbox[0]= {
    #     'uuid': '3g8ZTzH5b4tUUSGpy3ypSW',
    #     'type': 'to-do', 'title': '',
    #     'status': 'incomplete',
    #     'notes': 'The Boltzmann brain paradox - Fabio Pacucci - YouTube\nhttps://www.youtube.com/watch?v=OpohbXB_JZU',
    #     'start': 'Inbox',
    #     'start_date': None,
    #     'deadline': None,
    #     'stop_date': None,
    #     'checklist': True,
    #     'created': '2022-11-20 00:02:54',
    #     'modified': '2022-11-20 16:22:42',
    #     'index': -50541,
    #     'today_index': 0
    # }
    # >>> import things
    # >>> things.todos()
    # [{'uuid': '2Ukg8I2nLukhyEM7wYiBeb',
    # 'type': 'to-do',
    # 'title': 'Make reservation for dinner',
    # 'project': 'bNj6TPdKYhY6fScvXWVRDX',
    # ...},
    # {'uuid': 'RLZroza3jz0XPs3uAlynS7',
    # 'type': 'to-do',
    # 'title': 'Buy a whiteboard and accessories',
    # 'project': 'w8oSP1HjWstPin8RMaJOtB',
    # 'notes': "Something around 4' x 3' that's free-standing, two-sided, and magnetic.",
    # 'checklist': True,
    # ...
    # >>> things.todos('RLZroza3jz0XPs3uAlynS7')
    # {'uuid': 'RLZroza3jz0XPs3uAlynS7',
    # 'type': 'to-do',
    # 'title': 'Buy a whiteboard and accessories',
    # ...
    # 'checklist': [
    #     {'title': 'Cleaning Spray', 'status': 'completed', ...},
    #     {'title': 'Magnetic Eraser', 'status': 'incomplete', ...},
    #     {'title': 'Round magnets', 'status': 'incomplete', ...}
    # ]
    # ...
    # }
