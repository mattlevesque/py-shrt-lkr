<html>
    <head>
        <title><%block name="title" /></title>
    </head>
    <body>
        <%block name="header">
        <h2>${self.title()}</h2>
        %if len(request.session.peek_flash())>0:
        <div class="flash-msg">
            %for msg in request.session.pop_flash():
                <p>${msg}</p>
            %endfor
        </div>
        %endif
        </%block>
        ${self.body()}
    </body>
</html>