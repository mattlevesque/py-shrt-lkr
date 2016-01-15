<h1>Link list!!!</h1>
${data}


<%def name="buildrow(item, odd=True)">
    %if odd:
        <tr class="odd">
    %else:
        <tr class="even">
    % endif
        <td>
</%def>

<table class="paginator"><tr><th>id</th><th>Date</th><th>Description</th><th>Expenses</th><th>Income</th><th>Balance</th><th>Actions</th></tr>
<% odd=False %>
% for item in data:
     ${buildrow(item, odd)}
    <% odd = not(odd) %>
% endfor
</table>