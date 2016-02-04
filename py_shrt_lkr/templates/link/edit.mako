<%inherit file="../base/main.mako"/>
<%block name="title">Edit link</%block>


<div>
The link : ${tags.Link(link, url=link)}
</div>
<div>
${form|n}
</div>
