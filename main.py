from flask import Flask, render_template, request, jsonify

from sql_request import ReqHandler

app = Flask(__name__)


user_hndlr = ReqHandler("mydb", "myuser", "mysecretpassword", "localhost", "5432")
queries = { 
           1: "SELECT * FROM users;",
           2: "SELECT surname, name, Fname, address FROM users ORDER BY address ASC",
           3: "SELECT surname, name, Fname, exp FROM users WHERE exp > 4;",
           }

messages = {
        1: "Нажата кнопка №1 (SELECT * FROM users;)",
        2: "Нажата кнопка №2 (адрес по возрастанию)",
        3: "Нажата кнопка №3 (сотрудники со стажем больше 4 лет)",
            }



class ParseSQL():
    def __init__(self, text):
        self.raw_text = text
        self.size = len(text)

    def generator(self):
        n = 0
        while n < self.size:
            yield self.raw_text[n]
            n += 1

    def get_header(self):
        return self.raw_text[0]

    def get_body(self):
        return self.raw_text[1:]

def get_mock_data(button_id):
    if button_id in (1, 2, 3):
        query_res = ParseSQL(user_hndlr.query(queries[button_id]))
        columns = query_res.get_header()
        rows = query_res.get_body()
        message = messages[button_id]
    else:
        columns = []
        rows = []
        message = 'Неизвестная кнопка'

    # Демонстрация: количество строк и столбцов определяется в этой функции
    print(f"Количество строк: {len(rows)}, количество столбцов: {len(columns) if columns else 0}")

    return {
        'columns': columns,
        'rows': rows,
        'message': message
    }

@app.route('/')
def index():
    """Главная страница с тремя кнопками и местом для таблицы."""
    return render_template('index.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    """
    Обработчик нажатия кнопки.
    Принимает JSON с номером кнопки, возвращает данные для таблицы и сообщение.
    """
    data = request.get_json()
    button_id = data.get('button_id')
    if not button_id:
        return jsonify({'error': 'Не указан button_id'}), 400

    result = get_mock_data(button_id)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
    for line in ParseSQL(user_hndlr.query("SELECT * FROM users;")).generator():
        print(line)


