import datetime
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import cx_Oracle
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware

conn = cx_Oracle.connect('user1', '1', 'localhost:1521/xe')
cur = conn.cursor()

Secret_key = "12345"
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key=Secret_key)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/loginform", response_class=HTMLResponse)
def loginfrom(request: Request, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    cur.execute("select * from users where username = :username and password = :password",
                {'username': username, 'password': password})
    result = cur.fetchall()
    request.session['username'] = username
    if result:
        url = f"/dashboard/{username}"
        return RedirectResponse(url=url)
    else:
        message = "Invalid username or password"
        context = {"request": request, "message": message}
        return templates.TemplateResponse("login.html", context)


@app.get("/signup", response_class=HTMLResponse)
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/registerform", response_class=HTMLResponse)
def registerform(request: Request, username: Annotated[str, Form()], email: Annotated[str, Form()],
                 password: Annotated[str, Form()],
                 confirm_password: Annotated[str, Form()]):
    date = datetime.date.today()
    if username in ["deepan", "kushagra"]:
        role = "admin"
    else:
        role = "user"
    usernames = cur.execute("select username from users")
    for i in usernames:
        if username == i[0]:
            message = "Username already exists"
            return templates.TemplateResponse("signup.html", {"request": request, "message": message})

    if password != confirm_password:
        message = "Passwords do not match"
        return templates.TemplateResponse("signup.html", {"request": request, "message": message})
    else:
        cur.execute(
            "INSERT INTO users VALUES (:username, :password, :email, :role, SYSDATE,0)",
            {'username': username, 'email': email, 'password': password, 'role': role})
        conn.commit()
        return templates.TemplateResponse("login.html", {"request": request})


def total_balace(username):
    cur.callfunc('get_total_balance', float, [username])
    totbal = cur.var(cx_Oracle.NUMBER)
    cur.execute('BEGIN :result := get_total_balance(:username); END;', result=totbal, username=username)
    totbal = totbal.getvalue()
    return totbal


@app.post("/dashboard/{username}", response_class=HTMLResponse)
def dashboard(request: Request, username: str):
    result = total_balace(username)
    cur.callfunc('calculate_total_spending', float, [username, datetime.date.today()])
    dailymoneyspent = dailyspending(username, datetime.date.today())
    cur.execute(
        "SELECT * FROM Transactions WHERE Username = :username ORDER BY TransactionDate DESC FETCH FIRST 4 ROWS ONLY",
        {'username': username})
    transactions = cur.fetchall()
    data, labels = show_chart(username)
    context = {"request": request, "result": username, "balance": result, "dailyspent": dailymoneyspent,
               "transactions": transactions, "data": data, "labels": labels}
    return templates.TemplateResponse("index.html", context)


def dailyspending(username, date):
    cur.callfunc('calculate_total_spending', float, [username, date])
    dailyspent = cur.var(cx_Oracle.NUMBER)
    cur.execute('BEGIN :result := calculate_total_spending(:username, :today); END;',
                result=dailyspent, username=username, today=datetime.date.today())
    dailyspent = dailyspent.getvalue()
    return dailyspent


def get_category_id(category_name):
    cur.execute("select categoryid from categories where categoryname = :category", {'category': category_name})
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None


@app.post("/add_fund", response_class=HTMLResponse)
def add_funds(request: Request, amount: Annotated[float, Form()], category: Annotated[str, Form()]):
    amount = float(amount)
    print(category)
    category_id = get_category_id(category)
    print(category_id)
    username = request.session.get('username')
    transaction_type = category

    cur.execute("INSERT INTO Transactions (TransactionID, Username, CategoryID, Amount, Description, TransactionDate) "
                "VALUES (transaction_id.nextval, :username, :categoryid, :amount, :Description, SYSDATE)",
                {'username': username, 'categoryid': category_id, 'amount': amount, 'Description': transaction_type})
    conn.commit()
    url = f"/dashboard/{username}"
    return RedirectResponse(url=url)


@app.post("/add_expense", response_class=HTMLResponse)
def add_expense(request: Request, amount: Annotated[float, Form()], category: Annotated[str, Form()],
                description: Annotated[str, Form()]):
    amount = float(amount)
    category_id = get_category_id(category)
    username = request.session.get('username')
    cur.execute("INSERT INTO Transactions (TransactionID, Username, CategoryID, Amount, Description, TransactionDate) "
                "VALUES (transaction_id.nextval, :username, :categoryid, :amount, :Description, SYSDATE)",
                {'username': username, 'categoryid': category_id, 'amount': amount, 'Description': description})
    conn.commit()
    url = f"/dashboard/{username}"
    return RedirectResponse(url=url)


def show_chart(username):
    result_set_cursor = cur.var(cx_Oracle.CURSOR)
    cur.execute("BEGIN :result := get_expense_spending(:username); END;",
                result=result_set_cursor, username=username)
    result_set = result_set_cursor.getvalue()

    data = []
    labels = []

    for i in result_set:
        labels.append(i[0])
        data.append(i[1])

    return data, labels


@app.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    request.session.pop('username')
    return RedirectResponse(url="/")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4000)
