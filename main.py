from datetime import datetime
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


@app.get("/", response_class=HTMLResponse)  # home page
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# login ,signup and logout
@app.get("/login", response_class=HTMLResponse)  # login page
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
            "INSERT INTO users VALUES (:username, :password, :email, :role, SYSDATE)",
            {'username': username, 'email': email, 'password': password, 'role': role})
        conn.commit()
        return templates.TemplateResponse("login.html", {"request": request})


@app.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    request.session.pop('username')
    return RedirectResponse(url="/")


@app.post("/resetpassword", response_class=HTMLResponse)
async def reset_password(request: Request, email: str = Form(...),
                         password: str = Form(...),
                         confirm_password: str = Form(...)):
    print(email, password, confirm_password)
    cur.execute("select username from users where email = :email", {'email': email})
    result = cur.fetchone()
    if not result:
        message = "Email not found"
        return templates.TemplateResponse("forgotpass.html", {"request": request, "message": message})
    else:
        username = result[0]
        if password != confirm_password:
            message = "Passwords do not match"
            return templates.TemplateResponse("forgotpass.html", {"request": request, "message": message})
        else:
            cur.execute("update users set password = :password where email = :email",
                        {'password': password, 'email': email})
            conn.commit()
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/forgotpassword", response_class=HTMLResponse)
def forgot_password(request: Request):
    return templates.TemplateResponse("forgotpass.html", {"request": request})


def total_balace(username):
    cur.callfunc('get_total_balance', float, [username])
    totbal = cur.var(cx_Oracle.NUMBER)
    cur.execute('BEGIN :result := get_total_balance(:username); END;', result=totbal, username=username)
    totbal = totbal.getvalue()
    return totbal  # total balance


# dashboard
@app.post("/dashboard/{username}", response_class=HTMLResponse)
def dashboard(request: Request, username: str):
    result = total_balace(username)
    # cur.callfunc('calculate_total_spending', float, [username, datetime.date.today()])
    dailymoneyspent = dailyspending(username, datetime.today().date())
    cur.execute(
        "SELECT * FROM Transactions WHERE Username = :username ORDER BY TransactionDate DESC FETCH FIRST 4 ROWS ONLY",
        {'username': username})
    transactions = cur.fetchall()
    data, labels = show_chart(username)
    cur.execute("""SELECT TRUNC(TransactionDate) AS TransactionDay,
                SUM(Amount) AS TotalExpense FROM Transactions
            WHERE CategoryID IN (3, 4, 5, 6, 7, 8) 
                AND TransactionDate >= TRUNC(SYSDATE) - 7
                AND USERNAME = :username
            GROUP BY
                TRUNC(TransactionDate) 
            ORDER BY
                TRUNC(TransactionDate) DESC""", {'username': username})
    result_set = cur.fetchall()
    days = []
    expenses = []
    for i in result_set:
        days.append(i[0].strftime("%A"))
        expenses.append(i[1])
    days.reverse()
    expenses.reverse()
    print(days, expenses)
    context = {"request": request, "result": username, "balance": result, "dailyspent": dailymoneyspent,
               "transactions": transactions, "data": data, "labels": labels, "days": days, "expenses": expenses}
    return templates.TemplateResponse("index2.html", context)


def dailyspending(username, date):
    cur.callfunc('calculate_total_spending', float, [username, date])
    dailyspent = cur.var(cx_Oracle.NUMBER)
    cur.execute('BEGIN :result := calculate_total_spending(:username, :today); END;',
                result=dailyspent, username=username, today=datetime.today().today())
    dailyspent = dailyspent.getvalue()
    return dailyspent


def get_category_id(category_name):
    cur.execute("select categoryid from categories where categoryname = :category", {'category': category_name})
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None


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
    # print(data, labels)
    return data, labels


# transactions
@app.get("/transactions/{username}", response_class=HTMLResponse)
def transactions(request: Request, username: str):
    cur.execute("SELECT * FROM Transactions WHERE Username = :username ORDER BY TransactionDate DESC",
                {'username': username})
    transactions1 = cur.fetchall()
    tot_bal = total_balace(username)
    category_names = {
        1: "Salary",
        2: "Deposits",
        3: "Food",
        4: "Transportation",
        5: "Bills",
        6: "Toiletries",
        7: "Gifts",
        8: "Others"
    }
    dailyspend = dailyspending(username, datetime.today().date())
    context = {"request": request, "transactions": transactions1, "result": username, "balance": tot_bal,
               "dailyspent": dailyspend, "category_names": category_names}
    return templates.TemplateResponse("transactions.html", context)


@app.get("/dashboard/{username}", response_class=HTMLResponse)
def dashboard(request: Request, username: str):
    result = total_balace(username)
    # cur.callfunc('calculate_total_spending', float, [username, datetime.date.today()])
    dailymoneyspent = dailyspending(username, datetime.today().date())
    cur.execute(
        "SELECT * FROM Transactions WHERE Username = :username ORDER BY TransactionDate DESC FETCH FIRST 4 ROWS ONLY",
        {'username': username})
    transactions = cur.fetchall()
    data, labels = show_chart(username)
    cur.execute("""SELECT TRUNC(TransactionDate) AS TransactionDay,
                SUM(Amount) AS TotalExpense FROM Transactions
            WHERE CategoryID IN (3, 4, 5, 6, 7, 8) 
                AND TransactionDate >= TRUNC(SYSDATE) - 7
                AND USERNAME = :username
            GROUP BY
                TRUNC(TransactionDate) 
            ORDER BY
                TRUNC(TransactionDate) DESC""", {'username': username})
    result_set = cur.fetchall()
    days = []
    expenses = []
    for i in result_set:
        days.append(i[0].strftime("%A"))
        expenses.append(i[1])
    days.reverse()
    expenses.reverse()
    print(days, expenses)
    context = {"request": request, "result": username, "balance": result, "dailyspent": dailymoneyspent,
               "transactions": transactions, "data": data, "labels": labels, "days": days, "expenses": expenses}
    return templates.TemplateResponse("index2.html", context)


# analytics


@app.post("/transactions/{username}", response_class=HTMLResponse)
def transactions(request: Request, username: str):
    cur.execute("SELECT * FROM Transactions WHERE Username = :username ORDER BY TransactionDate DESC",
                {'username': username})
    transactions1 = cur.fetchall()
    tot_bal = total_balace(username)
    dailyspend = dailyspending(username, datetime.today().date())
    category_names = {
        1: "Salary",
        2: "Deposits",
        3: "Food",
        4: "Transportation",
        5: "Bills",
        6: "Toiletries",
        7: "Gifts",
        8: "Others"
    }
    context = {"request": request, "transactions": transactions1, "result": username, "balance": tot_bal,
               "dailyspent": dailyspend, "category_names": category_names}
    return templates.TemplateResponse("transactions.html", context)


@app.post("/submit-transaction", response_class=HTMLResponse)
async def submit_transaction(request: Request, transactionName: str = Form(...),
                             transactionAmount: float = Form(...),
                             transactionCategory: str = Form(...)):
    print(transactionName, transactionAmount, transactionCategory)
    # Process the form data as needed, such as saving to a database
    category_id = get_category_id(transactionCategory)
    username = request.session.get('username')
    cur.execute(
        "INSERT INTO Transactions (TransactionID, Username, CategoryID, Amount, Description, TransactionDate) "
        "VALUES (transaction_id.nextval, :username, :categoryid, :amount, :Description, SYSDATE)",
        {'username': username, 'categoryid': category_id, 'amount': transactionAmount, 'Description': transactionName})
    conn.commit()
    # Redirect to a success page or another URL
    return RedirectResponse(url=f"/dashboard/{username}")


@app.post("/updatetransaction", response_class=HTMLResponse)
async def update(request: Request, transactionId: int = Form(...), transactionName: str = Form(...),
                 transactionAmount: float = Form(...), transactionCategory: str = Form(...)):
    print(transactionId, transactionName, transactionAmount, transactionCategory)
    username = request.session.get('username')
    category_id = get_category_id(transactionCategory)
    cur.execute(
        "Update Transactions set Description = :transactionName, Amount = :transactionAmount, CategoryID = :transactionCategory where TransactionID = :transactionId",
        {'transactionName': transactionName, 'transactionAmount': transactionAmount, 'transactionCategory': category_id,
         'transactionId': transactionId})
    conn.commit()
    return RedirectResponse(url=f'/transactions/{username}')


@app.post("/deletetransaction", response_class=HTMLResponse)
async def delete(request: Request, transactionId: int = Form(...)):
    username = request.session.get('username')
    cur.execute("Delete from Transactions where TransactionID = :transactionId", {'transactionId': transactionId})
    conn.commit()
    return RedirectResponse(url=f'/transactions/{username}')


@app.get("/statistics/{username}", response_class=HTMLResponse)
def statistics(request: Request, username: str):
    cur.execute("""SELECT CategoryId, SUM(Amount) AS TotalExpense
                    FROM Transactions
                    WHERE CategoryId NOT IN (1,2) AND Username = :username
                    GROUP BY CategoryId""",
                {'username': username})
    result_set = cur.fetchall()
    data = []
    labels = []
    category_names = {
        3: "Food",
        4: "Transportation",
        5: "Bills",
        6: "Toiletries",
        7: "Gifts",
        8: "Others"
    }
    for i in result_set:
        labels.append(category_names[i[0]])
        data.append(i[1])

    tot_sum = sum(data)
    data_per = [round((i / tot_sum) * 100, 2) for i in data]
    print(data, labels)
    cur.execute("""SELECT TO_CHAR(TransactionDate, 'YYYY-MM') AS Month, SUM(Amount) AS TotalExpense
                    FROM Transactions
                    WHERE CategoryId NOT IN (1, 2) -- Assuming CategoryId 1 and 2 are for funds
                    AND EXTRACT(YEAR FROM TransactionDate) = EXTRACT(YEAR FROM SYSDATE) 
                    AND Username = :username
                    GROUP BY TO_CHAR(TransactionDate, 'YYYY-MM')
                    ORDER BY TO_CHAR(TransactionDate, 'YYYY-MM')
                    """, {'username': username})
    result_set = cur.fetchall()
    data1 = []
    labels1 = []
    for i in result_set:
        labels1.append(datetime.strptime(i[0], '%Y-%m').strftime('%B'))
        data1.append(i[1])
    cur.execute("""SELECT TO_CHAR(TransactionDate, 'YYYY-MM') AS Month, SUM(Amount) AS TotalExpense
                        FROM Transactions
                        WHERE CategoryId IN (1, 2) -- Assuming CategoryId 1 and 2 are for funds
                        AND EXTRACT(YEAR FROM TransactionDate) = EXTRACT(YEAR FROM SYSDATE) 
                        AND Username = :username
                        GROUP BY TO_CHAR(TransactionDate, 'YYYY-MM')
                        ORDER BY TO_CHAR(TransactionDate, 'YYYY-MM')
                        """, {'username': username})
    result_set = cur.fetchall()
    data2 = []
    labels2 = []
    for i in result_set:
        labels2.append(datetime.strptime(i[0], '%Y-%m').strftime('%B'))
        data2.append(i[1])
    cur.execute("""
        SELECT SUM(amount) AS total_expenses
        FROM Transactions
        WHERE TransactionDate >= TRUNC(SYSDATE, 'MM') - INTERVAL '12' MONTH
          AND TransactionDate < TRUNC(SYSDATE, 'MM')
          AND CategoryId NOT IN (1, 2) AND Username = :username
        """, {'username': username})
    result = cur.fetchone()
    total_expenses = result[0] or 0
    context = {"request": request, "result": username, "data": data, "labels": labels, "data1": data1,
               "labels1": labels1,
               "data2": data2, "labels2": labels2, "total_expenses": total_expenses, "data_per": data_per}
    return templates.TemplateResponse("statistics.html", context)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
