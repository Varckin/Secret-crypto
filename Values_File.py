import sqlite3 as data_base
import Cryptodome.Hash.SHA3_256, Cryptodome.Cipher.AES, Cryptodome.Hash.SHA3_512, json
from base64 import b64encode, b64decode
Header_Labels = ('Header', 'Login', 'URL')
Sorting_Enabled = True
password = str
directory = ''
data_record = list
dict_data = dict

with open('Config.json', 'r', encoding='utf-8') as read_file:
    data = json.load(read_file)
    dict_data = dict(data)
    keys_data = list(dict(data)["Language"].keys())

def write_lang_config():
    with open('Config.json', 'w', encoding='utf-8') as write_file:
        dict_data.update({"lang": lang})
        json.dump(dict_data, write_file,ensure_ascii=False, indent=4)

lang = dict_data["lang"]
dict_lang = dict_data["Language"][lang]



def create_db(name_db=str, pswd=str):
    db = data_base.connect(name_db+'.db')
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Password (
            password TEXT NOT NULL PRIMARY KEY
            );
        """)
    save_pswd = 'INSERT INTO Password (password) VALUES (?)'
    cursor.execute(save_pswd, (pswd,))
    db.commit()

    create_new_table(name_db)


def create_new_table( name_db=str):
    db = data_base.connect(name_db+'.db')
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Storage (
            header TEXT NOT NULL PRIMARY KEY,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            url TEXT,
            note TEXT
            );
        """)
    db.commit()
    cursor.close()
    db.close()

def hash_pswrd(password):
    hash = Cryptodome.Hash.SHA3_512.new(password.encode()).hexdigest()
    print(hash)
    return hash

def encrypt(plain_text, password):
    key = Cryptodome.Hash.SHA3_256.new(password.encode()).digest()
    cipher = Cryptodome.Cipher.AES.new(key, Cryptodome.Cipher.AES.MODE_EAX)
    cipher_text, tag = cipher.encrypt_and_digest(bytes(plain_text, 'UTF-8'))
    nonce = cipher.nonce

    print(b64encode(nonce).decode()+'\n'+b64encode(tag).decode()+'\n'+b64encode(cipher_text).decode())

    # salt.nonce.tag.cipher_text
    encrypt_text = b64encode(nonce).decode()+b64encode(tag).decode()+b64encode(cipher_text).decode()

    return encrypt_text

def decrypt(encrypt_text, password):
    nonce = b64decode(encrypt_text[0:24])
    tag = b64decode(encrypt_text[24:48])
    cipher_text = b64decode(encrypt_text[48:])
    key = Cryptodome.Hash.SHA3_256.new(password.encode()).digest()
    print(nonce,tag,cipher_text)
    cipher = Cryptodome.Cipher.AES.new(key, Cryptodome.Cipher.AES.MODE_EAX, nonce=nonce)
    decrypt_text = cipher.decrypt_and_verify(cipher_text,tag)

    return decrypt_text.decode()