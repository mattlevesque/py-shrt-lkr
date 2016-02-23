<%inherit file="../base/main.mako"/>
<%block name="title">Edit link</%block>

<script>
    jQuery(document).ready(function() {
        $('input.tagit').tagit({
            allowSpaces: true
        });
    });
</script>


<div>
The link : ${tags.Link(link, url=link)}
Hits: ${hits}
</div>
<div>
${form|n}
</div>



