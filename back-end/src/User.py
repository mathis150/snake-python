import DataBase
import bcrypt
import uuid

class User:
    def init(self):
        self.__database = DataBase.DataBase()
        self.__database.connect()
        self.session_token = None

    def __del__(self):
        self.__database.close()
        self.session_token = None

    def register_user(self, username, email, password):
        cursor = self.__database.connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            self.__database.connection.commit()
            print("User registered successfully.")
        except Exception as e:
            print(f"Error: {e}")
            self.__database.connection.rollback()
        finally:
            cursor.close()

        try:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            
            if user:
                print("Connexion réussie.")
                user_id = user[0]

                session_token = str(uuid.uuid4())

                self.session_token = session_token

                cursor.execute("UPDATE users SET session_token = %s WHERE id = %s", (session_token, user_id))
                self.__database.connection.commit()

                print("Connexion réussie. Token de session :", session_token)
            else:
                print("Nom d'utilisateur ou mot de passe invalide.")
        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            cursor.close()

    def verify_password(self, password1, password2):
        if password1 == password2:
            return True
        else:
            return False
    
    def hache_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    def verify_session_token(self, session_token):
        cursor = self.__database.connection.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE session_token = %s", (session_token,))
            user = cursor.fetchone()
            
            if user:
                print("Token de session valide.")
                return True
            else:
                print("Token de session invalide.")
                return False
        except Exception as e:
            print(f"Erreur : {e}")
            return False
        finally:
            cursor.close()

    def login_user(self, username, password):
        cursor = self.__database.connection.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode(), user[3].encode()):
                print("Connexion réussie.")
                user_id = user[0]

                session_token = str(uuid.uuid4())

                self.session_token = session_token

                cursor.execute("UPDATE users SET session_token = %s WHERE id = %s", (session_token, user_id))
                self.__database.connection.commit()

                print("Connexion réussie. Token de session :", session_token)
                return True
            else:
                print("Nom d'utilisateur ou mot de passe invalide.")
                return False
        except Exception as e:
            print(f"Erreur : {e}")
            return False
        finally:
            cursor.close()
    

    def logout_user(self, session_token):
        cursor = self.__database.connection.cursor()
        try:
            cursor.execute("UPDATE users SET session_token = NULL WHERE session_token = %s", (session_token,))
            self.__database.connection.commit()
            print("Déconnexion réussie.")
        except Exception as e:
            print(f"Erreur : {e}")
            self.__database.connection.rollback()
        finally:
            cursor.close()