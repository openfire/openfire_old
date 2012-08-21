{%- macro google_analytics_async(config, multitrack=false, anonymize=false, account_ids={}) -%}

	{% set __ = account_ids.update({'openfire': config.account_id}) %}
	{%- if config.enable -%}

		_.ready(function (w) {
			var _gaq = _gaq || [], _gat = _gat || {},
				_gac = {multitrack: {% if multitrack %}true{%- else -%}false{%- endif -%}, anonymize: {% if anonymize %}true{%- else -%}false{%- endif -%}, account_ids: {{ util.converters.json.dumps(account_ids)|safe }}},
				aswc = _.create_doc_frag(_.create_element_string('script', {
					'async': '', 'type': 'text/javascript', 'src': '{{ config.webclient }}',
					'data-hostname':{%- if util.handler.force_hostname -%} '{{ util.handler.force_hostname }}'{%- else -%} '{{ util.request.host }}'{%- endif -%}, 'data-tracker-id': '{{ config.account_id }}'
				}, '')),
				scpr = document.getElementsByTagName('script')[0],
				iscp = aswc.lastChild;
				iscp.onload = function (ev) {
					$.apptools.dev.verbose('OF:Analytics', 'Loaded Google Analytics webclient.', ev);
					$.openfire.analytics.internal.initialize(w._gaq, w._gat, _gac, ev);
				}
				scpr.parentNode.insertBefore(aswc);
		});

	{%- endif -%}

{%- endmacro -%}