<%inherit file="../base/main.mako"/>
<%block name="title">Link list</%block>

<%def name="buildrow(item, odd=True)">
    %if odd:
        <tr class="odd">
    %else:
        <tr class="even">
    % endif
        <td>${item.description}</td>
        <td>${item.url}</td>
        <td>${item.shorty}</td>
        <td>
            ${tags.Link("Edit", url=request.route_url('link_edit', id=item.id))} |
            ${tags.Link("Delete", url=request.route_url('link_delete', id=item.id))}
        </td>
</%def>

<table class="paginator"><tr><th>Description</th><th>Link to</th><th>Shorty</th><th>Actions</th></tr>
<% odd=False %>
% for item in linkLst:
     ${buildrow(item, odd)}
    <% odd = not(odd) %>
% endfor
</table>