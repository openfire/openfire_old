{% macro google_analytics_naked(config, multitrack=false, anonymize=false, account_ids={}) %}
{%- if config.enable -%}
{% if util.config.debug %}
	{%- set __ = account_ids.update({'openfire': config.account_id.dev}) -%}
	{%- set __ = config.update({'selected_client': config.webclient.dev}) -%}
{% else %}
	{%- if (util.request.get('environ', {}).get('HTTPS', {}) != 'off') and not (util.handler.force_https) -%}
		{%- set __ = config.update({'selected_client': config.webclient.https}) -%}
	{%- else -%}
		{%- set __ = config.update({'selected_client': config.webclient.http}) -%}
	{%- endif -%}
	{%- if 'staging' in util.request.host -%}
		{%- set __ = account_ids.update({'openfire': config.account_id.staging}) -%}
	{%- else -%}
		{%- set __ = account_ids.update({'openfire': config.account_id.production}) -%}
	{%- endif -%}
{% endif %}
		_gac = {multitrack: {% if multitrack %}true{%- else -%}false{%- endif -%}, anonymize: {% if anonymize %}true{%- else -%}false{%- endif -%}, account_ids: {{ util.converters.json.dumps(account_ids)|safe }}},
		undefined = _ofinject.appendChild(_.create_doc_frag(_.create_element_string(_dfeln, {'id': 'js-analytics', 'async': '', 'type': _dfelt,
		'src': '{{ config.selected_client }}', 'data-hostname':{%- if util.handler.force_hostname -%} '{{ util.handler.force_hostname }}'{%- else -%} '{{ util.request.host }}'{%- endif -%}}, ''))),
		_gacol = _ofinject.lastChild.onload = function (ev) { $.apptools.analytics.internal.initialize(window._gaq, window._gat, _gac, ev); },
{%- endif -%}
{% endmacro %}
{% macro google_analytics_async(config, multitrack=false, anonymize=false, account_ids={}) %}
	{%- if config.enable -%}

	{%- if util.config.debug -%}
		{%- set __ = account_ids.update({'openfire': config.account_id.dev}) -%}
		{%- set __ = config.update({'selected_client': config.webclient.dev}) -%}
	{%- else -%}
		{%- if (util.request.get('environ', {}).get('HTTPS', 'off') != 'off') and not (util.handler.force_https) -%}
			{%- set __ = config.update({'selected_client': config.webclient.https}) -%}
		{%- else -%}
			{%- set __ = config.update({'selected_client': config.webclient.http}) -%}
		{%- endif -%}
		{%- if 'staging' in util.request.host -%}
			{%- set __ = account_ids.update({'openfire': config.account_id.staging}) -%}
		{%- else -%}
			{%- set __ = account_ids.update({'openfire': config.account_id.production}) -%}
		{%- endif -%}
	{%- endif -%}

	_.ready(function (w) {
		var _gaq = _gaq || [], _gat = _gat || {},
			_gac = {multitrack: {% if multitrack %}true{%- else -%}false{%- endif -%}, anonymize: {% if anonymize %}true{%- else -%}false{%- endif -%}, account_ids: {{ util.converters.json.dumps(account_ids)|safe }}},
			aswc = _.create_doc_frag(_.create_element_string('script', {
				'async': '', 'type': 'text/javascript', 'src': '{{ config.selected_client }}',
				'data-hostname':{%- if util.handler.force_hostname -%} '{{ util.handler.force_hostname }}'{%- else -%} '{{ util.request.host }}'{%- endif -%}
			}, '')),
			scpr = document.getElementsByTagName('script')[0],
			iscp = aswc.lastChild;
			iscp.onload = function (ev) { $.apptools.analytics.internal.initialize(w._gaq, w._gat, _gac, ev); }
			scpr.parentNode.insertBefore(aswc);
	});

	{%- endif -%}
{% endmacro %}