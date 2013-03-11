<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Office Mood Meter</title>
        <link rel="stylesheet" href="css/style.css" type="text/css">
    </head>
    <body>
        <div id="topbar">
            %if user.get("name"):
                <form action="/logout" method="post">
                    <button class="btn right"  type="submit" id="submit">Logout</button>
                </form>
            %else:
                <form action="/login" method="get">
                    <button class="btn right">Login</button>
                </form>
            %end
        </div>
        <div id="charts">
            <!-- d3.js chart -->
        </div>
        %if user.get("name"):
            
            <div id="level">
                <div class="red"   >5</div>
                <div class="orange">4</div>
                <div class="yellow">3</div>
                <div class="blue"  >2</div>
                <div class="green" >1</div>
            </div>
            <img id="avatar" src="{{user.get('img')}}"/>
            <h2 style="text-align:center">How hungry are you ?</h2>
        %end
        <script src="http://d3js.org/d3.v3.min.js" type="text/javascript"></script>
        <script src="js/client.js" type="text/javascript"></script>
    </body>
</html>
