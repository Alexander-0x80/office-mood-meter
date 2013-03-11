<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Login</title>
        <link rel="stylesheet" href="css/style.css" type="text/css">
    </head>
    <body>
        <form id="login" action="/login" method="post">
                <img src="/img/key.png"/>
                <input name="username" type="text" placeholder="Username" autofocus required>
                <input name="password" type="password" placeholder="Password" required>
                <button class="btn"  type="submit" id="submit">Login</button>
        <form>
        <script src="js/login.js" type="text/javascript"></script>
    </body>
</html>