{%- macro build_native_page_object(page, transport, security) -%}
{{ {

	'platform': {
		'name': util.config.project.name,
		'version': sys.version,
		'origindc': util.appengine.datacenter,
		'instance': util.appengine.instance,
		'debug': true if api.users.is_current_user_admin() else false
	},

	'debug': {
		'logging': (util.config.debug or api.users.is_current_user_admin()),
		'eventlog': util.config.debug,
		'verbose': util.config.debug,
		'strict': false
	} if util.config.debug else null,

	'push': {
		'token': transport.realtime.channel if transport.realtime.enabled else '',
		'timeout': transport.realtime.timeout if transport.realtime.enabled else 0
	} if transport.realtime.enabled else {},

	'user': {
		'k': util.handler.encrypt(security.current_user.key.urlsafe()),
		'username': security.current_user.username,
		'firstname': security.current_user.firstname,
		'lastname': security.current_user.lastname,
		'email': security.current_user.email[0].id(),
		'is_user_admin': api.users.is_current_user_admin(),
		'custom_url': security.current_user.get_custom_url(),
		'avatar': util.handler.encrypt(security.current_user.avatar.urlsafe()) if security.current_user.has_avatar() else false,
		'avatar_asset': util.handler.encrypt(security.current_user.avatar.id()) if security.current_user.has_avatar() else false
	} if security.current_user != none else false,

	'services': {

		'endpoint': '://'.join(['https', transport.services.endpoint]) if transport.services.secure else '://'.join(['http', transport.services.endpoint]),
		'consumer': transport.services.consumer,
		'scope': transport.services.scope,
		'apis': transport.services.make_object(page.services)

	}

}|json|safe }}
{%- endmacro -%}

{%- macro build_page_object(services, config, page) -%}

$(document).ready(function (){

	{% block platform_statement %}
		$.apptools.sys.platform = {
			name: '{{ util.config.project.name }}', version: '{{ sys.version }}', origindc: '{{ util.appengine.datacenter }}', instance: '{{ util.appengine.instance }}',
			{%- if api.users.is_current_user_admin() -%}
			debug: {% autoescape off %}{{ util.converters.json.dumps(util.config.debug) }}{% endautoescape %}
			{%- endif -%}
		};
		{%- if util.config.debug or api.users.is_current_user_admin() -%}
			$.apptools.dev.setDebug({logging: true, eventlog: true, verbose: true});
		{%- else -%}
			$.apptools.dev.setDebug({logging: false, eventlog: false, verbose: false});
		{%- endif -%}
	{% endblock %}

	{% if services != null %}
	$.apptools.api.rpc.factory([
		{%- for service, action, cfg, opts in services -%}
			{
				name: '{{ service }}',
				base_uri: '{{ action }}',
				methods: [{%- for i, method in enumerate(cfg.methods) -%}'{{ method }}'{%- if i != (len(cfg.methods) - 1) %},{%- endif -%}{%- endfor -%}],
				config: {{ util.converters.json.dumps(opts)|safe }}
			}{%- if not loop.last -%},{%- endif -%}
		{%- endfor -%}
	]);
	{% endif %}

	{% if page.open_channel %}
	{% if page.channel_token %}
		$.apptools.push.channel.establish("{{ page.channel_token }}").listen();
	{% endif %}
	{% endif %}

	{% block userobj %}
		{%- if userapi != none -%}

			$.apptools.user.setUserInfo({

				{%- if api.users.get_current_user() != none -%}
					{%- set userobj = api.users.get_current_user() -%}
					current_user: {
						nickname: "{{ userobj.nickname() }}",
						email: "{{ userobj.email() }}"
					},
					is_user_admin: {{ util.converters.json.dumps(api.users.is_current_user_admin()) }}
				{%- else -%}
					current_user: null,
					is_user_admin: false
				{%- endif -%}

			});
		{%- endif -%}
	{% endblock %}

	$.apptools.events.trigger('API_READY');

});

{%- endmacro -%}
