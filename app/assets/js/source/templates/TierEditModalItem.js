<div id="{{<type}}-editing-{{<index}}" class="{{&1}}">
	<div class="left" style="margin-right: 10px; max-width: 35%">
		{{amount}}
		amount: <input type="text" id="{{&1}}-amount-{{&2}}" class="{{&1}}-field amount" data-validation="number" data-label="amount" contenteditable=true placeholder="{{=amount}}"></input>
		<br>
		{{/amount}}
		name: <input type="text" id="{{&1}}-name-{{&2}}" class="{{&1}}-field name" data-validation="alpha" data-label="name" contenteditable=true placeholder="{{=name}}"></input>
		<br>
	</div>
	description:
	<br>
	<textarea id="{{&1}}-description-{{&2}}" class="rounded {{&1}}-field description" data-label="description" contenteditable=true>{{description}}{{=description}}{{/description}}{{summary}}{{=summary}}{{/summary}}</textarea>
	<br>
	{{>buttons}}
		{{+Button}}
	{{/buttons}}
</div>