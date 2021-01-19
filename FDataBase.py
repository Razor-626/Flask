import math, time, sqlite3

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print('Ошибка чтения БД')
        return []

    def addPost(self, title, description):

        try:
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO posts VALUES(NULL, ?, ?, ?)', (title, description, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления статьи в БД' + str(e))
            return False

        return True

    def getPost(self, postId):
        try:
            self.__cur.execute(f"SELECT title, description FROM posts WHERE id = {postId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка получения статьи из БД' + str(e))

        return(False, False)

    def getPosts(self):
        try:
            self.__cur.execute(f"SELECT id, title, description FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print('Ошибка получения статей из БД' + str(e))

        return []

    def addUser(self, username, email, password):

        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE `{email}`")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь с таким email ужк существует')
                return False

            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO users VALUES(NULL, ?, ?, ?, ?)', (username, email, password, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления в БД' + str(e))
            return False

        return True

    def authorization(self, username, password):

        try:
            self.__cur.execute(f"SELECT id, username from users WHERE username = {username} and password = {password}")
            res = self.__cur.fetchone()
            print(res)
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка авторизации. 1' + str(e))