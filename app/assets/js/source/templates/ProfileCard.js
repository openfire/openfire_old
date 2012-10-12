<div class="profile-card">
	<a href="{{=url}}">
		<div class="avatar" data-name="{{=name}}">
			<img src="{{=avatar_url}}">
		</div>
	</a>
	<div class="accounts">
		{{>accounts}}
			<a class="icon {{=service}}" href="{{=url}}"></a>
		{{/accounts}}
	</div>
</div>