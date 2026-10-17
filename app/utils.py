from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()

def password_hash(password: str):
    return password_hasher.hash(password)

def verify_password(plain, hash):
    return password_hasher.verify(plain, hash)

if __name__ == "__main__":
    from getpass import getpass

    password = getpass("Enter admin password: ")
    print(password_hash(password))