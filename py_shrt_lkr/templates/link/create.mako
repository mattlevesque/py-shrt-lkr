<html>
<head>
  <!-- CSS -->
  <link rel="stylesheet" href="${request.static_url('deform:static/css/jquery.autocomplete.css')}" type="text/css" />
  <link rel="stylesheet" href="${request.static_url('deform:static/css/jquery-ui-timepicker-addon.css')}" type="text/css" />
  <link rel="stylesheet" href="${request.static_url('deform:static/css/form.css')}" type="text/css" />
  <!--link rel="stylesheet" href="${request.static_url('deform:static/css/beautify.css')}" type="text/css" /-->
  <!-- JavaScript -->
  <script type="text/javascript"
          src="${request.static_url('deform:static/scripts/jquery-1.7.2.min.js')}"></script>
  <script type="text/javascript"
          src="${request.static_url('deform:static/scripts/jquery.form.js')}"></script>
<script type="text/javascript"
          src="${request.static_url('deform:static/scripts/jquery.maskedinput-1.2.2.min.js')}"></script>
<script type="text/javascript"
          src="${request.static_url('deform:static/scripts/jquery.maskMoney-1.4.1.js')}"></script>
<script type="text/javascript"
          src="${request.static_url('deform:static/scripts/jquery-ui-1.8.11.custom.min.js')}"></script>
<script type="text/javascript"
          src="${request.static_url('deform:static/scripts/jquery-ui-timepicker-addon.js')}"></script>
<script type="text/javascript"
          src="${request.static_url('deform:static/scripts/modernizr.custom.input-types-and-atts.js')}"></script>

  <script type="text_deform/javascript"
          src="${request.static_url('deform:static/scripts/deform.js')}"></script>
    <script type="text/javascript"
          src="${request.static_url('deform:static/tinymce/jscripts/tiny_mce/tiny_mce.js')}"></script>

</head>
<body>


<h1>Create new link</h1>

<div>
${form|n}
</div>

${test|n}

    </body>
</html>