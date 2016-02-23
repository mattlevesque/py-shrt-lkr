<html>
    <head>
        <title><%block name="title" /> - ShrtLkr</title>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" type="text/javascript" charset="utf-8"></script>
        <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.9.2/jquery-ui.min.js" type="text/javascript" charset="utf-8"></script>

        <script src="${request.static_url('py_shrt_lkr:static/js/tag-it.min.js')}" type="text/javascript" charset="utf-8"></script>

        <link href="${request.static_url('py_shrt_lkr:static/css/jquery.tagit.css')}" rel="stylesheet" type="text/css">
        <link href="${request.static_url('py_shrt_lkr:static/css/tagit.ui-zendesk.css')}" rel="stylesheet" type="text/css">
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