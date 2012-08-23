{% macro social_naked() %}
		_gap1i = 'plusone', _gap1r = 'https://apis.google.com/js/plusone.js', _fbi = 'fbsdk',
		_fbr = 'https://connect.facebook.net/en_US/all.js#xfbml=1&appId=257586781019220',
		undefined = _ofinject.appendChild(_.create_doc_frag(_.create_element_string(_dfeln, {
			'id': ['js', _gap1i].join('-'), 'async': '', 'type': _dfelt, 'src': _gap1r, }, JSON.stringify({{ {'lang': 'en-US', 'parsetags': 'explicit'}|json|safe }})))),
		_p1onload = _ofinject.lastChild.onload = function (ev) { gapi.plusone.render(_gap1i); },
		_fbs = _ofinject.appendChild(_.create_doc_frag(_.create_element_string(_dfeln, {
			'id': ['js', _fbi].join('-'), 'async': '', 'type': _dfelt, 'src': _fbr,
		}, ''))), _fbonload = window.fbAsyncInit = function (ev) {
			FB.init({appId: '257586781019220', status: true, cookie: true, xfbml: true, channelUrl: '{{ util.request.get('environ', {}).get('HTTP_SCHEME', 'http://') }}{% if util.handler.force_hostname %}{{ util.handler.force_hostname }}{% else %}{{ util.request.get('environ', {}).get("HTTP_HOST", 'localhost:8080') }}{% endif %}/channel.html'});
			FB.Event.subscribe('edge.create', function(targetUrl) { $.openfire.analytics.track.social('facebook', 'like', {}, '/'); });
		},
{%- endmacro -%}