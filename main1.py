import sqlite3

def add_server(server_id,status,role_id):
    con = sqlite3.connect("date.db")
    sql = f"insert into servers(server_id,status,role) values({server_id},'{status}','{role_id}');"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def all_servers():
    con = sqlite3.connect("date.db")
    sql = f"select * from servers;"
    cur = con.cursor()
    cur.execute(sql)
    servers = cur.fetchall()
    con.close()
    return servers

def get_server(id):
    con = sqlite3.connect("date.db")
    sql = f"select * from servers where server_id = {id};"
    cur = con.cursor()
    cur.execute(sql)
    server = cur.fetchone()
    con.close()
    return server

def delete_server(id):
    con = sqlite3.connect("date.db")
    sql = f"delete from servers where server_id = {id};"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def get_warns():
    con = sqlite3.connect("date.db")
    sql = f"select * from warns;"
    cur = con.cursor()
    cur.execute(sql)
    warns = cur.fetchall()
    con.close()
    return warns

def add_warn(server_id):
    con = sqlite3.connect("date.db")
    sql = f"insert into warns(server_id,amount) values({server_id},1);"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def add_amount(server_id):
    con = sqlite3.connect("date.db")
    sql = f"select * from warns where server_id = {server_id};"
    cur = con.cursor()
    cur.execute(sql)
    info = cur.fetchone()
    amount = info[2] + 1
    sql1 = f"update warns set amount = {amount} where server_id = {server_id};"
    cur.execute(sql1)
    con.commit()
    con.close()

def get_amount(server_id):
    con = sqlite3.connect("date.db")
    sql = f"select * from warns where server_id = {server_id};"
    cur = con.cursor()
    cur.execute(sql)
    info = cur.fetchone()
    con.commit()
    con.close()
    return info[2]

def get_greet():
    con = sqlite3.connect("date.db")
    sql = f"select * from greet;"
    cur = con.cursor()
    cur.execute(sql)
    servers = cur.fetchall()
    con.close()
    return servers

def add_greet(server_id,channel_id):
    con = sqlite3.connect("date.db")
    sql = f"insert into greet(server_id,channel_id,greetdel) values({server_id},{channel_id},4);"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def remove_greet(channel_id):
    con = sqlite3.connect("date.db")
    sql = f"delete from greet where channel_id = {channel_id};"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def get_users():
    con = sqlite3.connect("date.db")
    sql = f"select * from economy;"
    cur = con.cursor()
    cur.execute(sql)
    users = cur.fetchall()
    con.close()
    return users

def add_user(user_id):
    con = sqlite3.connect("date.db")
    sql = f"insert into economy(user_id,balance,inventory) values({user_id},0,'Computer');"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def add_money(user_id,money):
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    sql = f"select * from economy where user_id == {user_id}"
    cur.execute(sql)
    user = cur.fetchone()
    moneys = user[2]
    full_money = moneys + money
    sql1 = f"update economy set balance = {full_money} where user_id = {user_id}"
    cur.execute(sql1)
    con.commit()
    con.close()

def share_money(user_id,user_ids,money):
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    user = get_info(user_ids)
    moneys = user[2]
    full_money = moneys + money
    sql1 = f"update economy set balance = {full_money} where user_id = {user_ids}"
    cur.execute(sql1)
    sql3 = f"select * from economy where user_id = {user_id}"
    cur.execute(sql3)
    user = cur.fetchone()
    moneys = user[2]
    full_money = moneys - money
    sql2 = f"update economy set balance = {full_money} where user_id = {user_id}"
    cur.execute(sql2)
    con.commit()
    con.close()

def get_info(user_id):
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    sql = f"select * from economy where user_id == {user_id}"
    cur.execute(sql)
    user = cur.fetchone()
    con.close()
    return user

def give_money(user_ids,money):
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    user = get_info(user_ids)
    moneys = user[2]
    full_money = moneys + money
    sql1 = f"update economy set balance = {full_money} where user_id = {user_ids}"
    cur.execute(sql1)
    con.commit()
    con.close()

def remove_money(user_id,amount):
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    user = get_info(user_id)
    moneys = user[2]
    full_money = moneys - amount
    sql1 = f"update economy set balance = {full_money} where user_id = {user_id}"
    cur.execute(sql1)
    con.commit()
    con.close()

def add_inventory(user_id,name):
    con = sqlite3.connect("date.db")
    sql = f"update economy set inventory = {name} where user_id = {user_id};"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def update_greet(channel_id, time):
    con = sqlite3.connect("date.db")
    sql = f"update greet set greetdel = {time} where channel_id = {channel_id}"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
  


def add_funcmd(user_id):
    con = sqlite3.connect("date.db")
    sql = f"insert into funcmd(user_id) values({user_id})"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def get_funcmd():
    con = sqlite3.connect("date.db")
    sql = f"select * from funcmd;"
    cur = con.cursor()
    cur.execute(sql)
    users = cur.fetchall()
    con.close()
    return users

def remove_funcmd(user_id):
    con = sqlite3.connect("date.db")
    sql = f"delete from funcmd where user_id = {user_id}"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def add_chatbot(channel_id):
    con = sqlite3.connect("date.db")
    sql = f"insert into chatbot(channel_id) values({channel_id})"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def get_chatbot():
    con = sqlite3.connect("date.db")
    sql = f"select * from chatbot;"
    cur = con.cursor()
    cur.execute(sql)
    channels = cur.fetchall()
    con.close()
    return channels

def remove_chatbot(channel_id):
    con = sqlite3.connect("date.db")
    sql = f"delete from chatbot where channel_id = {channel_id}"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def get_join_channels():
    con = sqlite3.connect("date.db")
    sql = f"select * from joinchannel;"
    cur = con.cursor()
    cur.execute(sql)
    channels = cur.fetchall()
    con.close()
    return channels

def add_joinchannel(guild_id,channel_id):
    con = sqlite3.connect("date.db")
    sql = f"insert into joinchannel(guild_id,channel_id) values({guild_id},{channel_id})"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def remove_joinchannel(channel_id):
    con = sqlite3.connect("date.db")
    sql = f"delete from joinchannel where channel_id = {channel_id}"
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()