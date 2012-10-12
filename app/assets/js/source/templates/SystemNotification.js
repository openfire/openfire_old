<div id="openfire-notification" class="notification {{=level}}" style="opacity: 0; display: none;">
    <h1>{{=title}}</h1>
    <p>{{=message}}</p>
    {{confirm}}
    <button id="notification-yes">yes</button>
    <button id="notification-no">no</button>
    {{/confirm}}
    {{alert}}
    <button id="notification-ok">ok</button>
    {{/alert}}
</div>