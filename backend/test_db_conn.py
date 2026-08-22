import pymysql

passwords_to_try = ['', 'root', '123456', 'admin', '1234', 'mysql', 'password', 'root123', 'admin123', 'root@123', '12345678', '123456789', 'password123', '123']
for p in passwords_to_try:
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password=p,
            port=3306,
            charset='utf8mb4'
        )
        print(f"SUCCESS: Connected with user='root' and password='{p}'")
        conn.close()
        break
    except Exception as e:
        print(f"Password '{p}': {e}")
