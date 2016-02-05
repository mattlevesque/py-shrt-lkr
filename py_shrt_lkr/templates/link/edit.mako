<%inherit file="../base/main.mako"/>
<%block name="title">Edit link</%block>


<div>
The link : ${tags.Link(link, url=link)}
Hits: ${hits}
</div>
<div>
${form|n}
</div>
