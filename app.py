from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = request.form['email']
        passw = request.form['password']
        if not user or not passw:
            return render_template_string(template, warning='Missing input value')
        result = Cookie(user, passw)
        return render_template_string(template, result=result)
    return render_template_string(template)

def Cookie(user, passw):
    import requests
    import re
    session = requests.Session()
    headers = {
        'authority': 'free.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'dpr': '3',
        'origin': 'https://free.facebook.com',
        'referer': 'https://free.facebook.com/login/?email=%s' % (user),
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-full-version-list': '"Not-A.Brand";v="99.0.0.0", "Chromium";v="124.0.6327.1"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        'viewport-width': '980',
    }
    getlog = session.get(f'https://free.facebook.com/login.php')
    idpass = {
        "lsd": re.search('name="lsd" value="(.*?)"', str(getlog.text)).group(1),
        "jazoest": re.search('name="jazoest" value="(.*?)"', str(getlog.text)).group(1),
        "m_ts": re.search('name="m_ts" value="(.*?)"', str(getlog.text)).group(1),
        "li": re.search('name="li" value="(.*?)"', str(getlog.text)).group(1),
        "try_number": "0",
        "unrecognize_tries": "0",
        "email": user,
        "pass": passw,
        "login": "Log In",
        "bi_xrwh": re.search('name="bi_xrwh" value="(.*?)"', str(getlog.text)).group(1),
    }
    comp = session.post("https://free.facebook.com/login/device-based/regular/login/?shbl=1&refsrc=deprecated",
                        headers=headers, data=idpass, allow_redirects=False)
    jopl = session.cookies.get_dict().keys()
    cookie = ";".join([key + "=" + value for key, value in session.cookies.get_dict().items()])
    if "c_user" in jopl:
        return f"**Cookie:**\n{cookie}"
    elif "checkpoint" in jopl:
        return "Account checkpoint"
    else:
        return "Invalid username or password"

template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cookie Getter</title>
</head>
<body>
    <h1>Cookie Getter</h1>
    <form method="post">
        <label for="email">Email/ID/Number:</label>
        <input type="text" id="email" name="email">
        <br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password">
        <br>
        <input type="submit" value="Get cookie">
    </form>
    <div>
        {% if warning %}
            <p style="color: red;">{{ warning }}</p>
        {% endif %}
        {% if result %}
            <p>{{ result }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
      
