
(function() {
  var AppException, AppTools, AppToolsCollection, AppToolsException, AppToolsModel, AppToolsRouter, AppToolsView, BlogManagerAPI, ContentManagerAPI, CoreAPI, CoreAdminAPI, CoreAgentAPI, CoreDevAPI, CoreDispatchAPI, CoreEventsAPI, CoreException, CoreInterface, CoreModelAPI, CoreObject, CorePushAPI, CoreRPCAPI, CoreRenderAPI, CoreStorageAPI, CoreUserAPI, CoreWidget, CoreWidgetAPI, Expand, Find, IndexedDBDriver, IndexedDBEngine, KeyEncoder, LocalStorageDriver, LocalStorageEngine, Milk, Modal, ModalAPI, Model, PageManagerAPI, Parse, PushDriver, QueryDriver, RPCAPI, RPCDriver, RPCRequest, RPCResponse, RenderDriver, Scroller, ScrollerAPI, SessionStorageDriver, SessionStorageEngine, SimpleKeyEncoder, SiteManagerAPI, StorageAdapter, StorageDriver, Tabs, TabsAPI, Template, TemplateCache, Util, WebSQLDriver, WebSQLEngine, _simple_key_encoder,
    __slice = [].slice,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; },
    _this = this;

  this.__apptools_preinit = {};

  TemplateCache = {};

  Find = function(name, stack, value) {
    var ctx, i, part, parts, _i, _j, _len, _ref, _ref1;
    if (value == null) {
      value = null;
    }
    if (name === '.') {
      return stack[stack.length - 1];
    }
    _ref = name.split(/\./), name = _ref[0], parts = 2 <= _ref.length ? __slice.call(_ref, 1) : [];
    for (i = _i = _ref1 = stack.length - 1; _ref1 <= -1 ? _i < -1 : _i > -1; i = _ref1 <= -1 ? ++_i : --_i) {
      if (stack[i] == null) {
        continue;
      }
      if (!(typeof stack[i] === 'object' && name in (ctx = stack[i]))) {
        continue;
      }
      value = ctx[name];
      break;
    }
    for (_j = 0, _len = parts.length; _j < _len; _j++) {
      part = parts[_j];
      value = Find(part, [value]);
    }
    if (value instanceof Function) {
      value = (function(value) {
        return function() {
          var val;
          val = value.apply(ctx, arguments);
          return (val instanceof Function) && val.apply(null, arguments) || val;
        };
      })(value);
    }
    return value;
  };

  Expand = function() {
    var args, f, obj, tmpl;
    obj = arguments[0], tmpl = arguments[1], args = 3 <= arguments.length ? __slice.call(arguments, 2) : [];
    return ((function() {
      var _i, _len, _results;
      _results = [];
      for (_i = 0, _len = tmpl.length; _i < _len; _i++) {
        f = tmpl[_i];
        _results.push(f.call.apply(f, [obj].concat(__slice.call(args))));
      }
      return _results;
    })()).join('');
  };

  Parse = function(template, delimiters, section) {
    var BuildRegex, buffer, buildInterpolationTag, buildInvertedSectionTag, buildPartialTag, buildSectionTag, cache, content, contentEnd, d, error, escape, isStandalone, match, name, parseError, pos, sectionInfo, tag, tagPattern, tmpl, type, whitespace, _name, _ref, _ref1, _ref2;
    if (delimiters == null) {
      delimiters = ['{{', '}}'];
    }
    if (section == null) {
      section = null;
    }
    cache = (TemplateCache[_name = delimiters.join(' ')] || (TemplateCache[_name] = {}));
    if (template in cache) {
      return cache[template];
    }
    buffer = [];
    BuildRegex = function() {
      var tagClose, tagOpen;
      tagOpen = delimiters[0], tagClose = delimiters[1];
      return RegExp("([\\s\\S]*?)([" + ' ' + "\\t]*)(?:" + tagOpen + "\\s*(?:(!)\\s*([\\s\\S]+?)|(=)\\s*([\\s\\S]+?)\\s*=|({)\\s*(\\w[\\S]*?)\\s*}|([^0-9a-zA-Z._!={]?)\\s*([\\w.][\\S]*?))\\s*" + tagClose + ")", "gm");
    };
    tagPattern = BuildRegex();
    tagPattern.lastIndex = pos = (section || {
      start: 0
    }).start;
    parseError = function(pos, msg) {
      var carets, e, endOfLine, error, indent, key, lastLine, lastTag, lineNo, parsedLines, tagStart;
      (endOfLine = /$/gm).lastIndex = pos;
      endOfLine.exec(template);
      parsedLines = template.substr(0, pos).split('\n');
      lineNo = parsedLines.length;
      lastLine = parsedLines[lineNo - 1];
      tagStart = contentEnd + whitespace.length;
      lastTag = template.substr(tagStart + 1, pos - tagStart - 1);
      indent = new Array(lastLine.length - lastTag.length + 1).join(' ');
      carets = new Array(lastTag.length + 1).join('^');
      lastLine = lastLine + template.substr(pos, endOfLine.lastIndex - pos);
      error = new Error();
      for (key in e = {
        "message": "" + msg + "\n\nLine " + lineNo + ":\n" + lastLine + "\n" + indent + carets,
        "error": msg,
        "line": lineNo,
        "char": indent.length,
        "tag": lastTag
      }) {
        error[key] = e[key];
      }
      return error;
    };
    while (match = tagPattern.exec(template)) {
      _ref = match.slice(1, 3), content = _ref[0], whitespace = _ref[1];
      type = match[3] || match[5] || match[7] || match[9];
      tag = match[4] || match[6] || match[8] || match[10];
      contentEnd = (pos + content.length) - 1;
      pos = tagPattern.lastIndex;
      isStandalone = (contentEnd === -1 || template.charAt(contentEnd) === '\n') && ((_ref1 = template.charAt(pos)) === (void 0) || _ref1 === '' || _ref1 === '\r' || _ref1 === '\n');
      if (content) {
        buffer.push((function(content) {
          return function() {
            return content;
          };
        })(content));
      }
      if (isStandalone && (type !== '' && type !== '&' && type !== '{')) {
        if (template.charAt(pos) === '\r') {
          pos += 1;
        }
        if (template.charAt(pos) === '\n') {
          pos += 1;
        }
      } else if (whitespace) {
        buffer.push((function(whitespace) {
          return function() {
            return whitespace;
          };
        })(whitespace));
        contentEnd += whitespace.length;
        whitespace = '';
      }
      switch (type) {
        case '!':
          break;
        case '':
        case '&':
        case '{':
          buildInterpolationTag = function(name, is_unescaped) {
            return function(context) {
              var value, _ref2;
              if ((value = (_ref2 = Find(name, context)) != null ? _ref2 : '') instanceof Function) {
                value = Expand.apply(null, [this, Parse("" + (value()))].concat(__slice.call(arguments)));
              }
              if (!is_unescaped) {
                value = this.escape("" + value);
              }
              return "" + value;
            };
          };
          buffer.push(buildInterpolationTag(tag, type));
          break;
        case '>':
          buildPartialTag = function(name, indentation) {
            return function(context, partials) {
              var partial;
              partial = partials(name).toString();
              if (indentation) {
                partial = partial.replace(/^(?=.)/gm, indentation);
              }
              return Expand.apply(null, [this, Parse(partial)].concat(__slice.call(arguments)));
            };
          };
          buffer.push(buildPartialTag(tag, whitespace));
          break;
        case '#':
        case '^':
          sectionInfo = {
            name: tag,
            start: pos,
            error: parseError(tagPattern.lastIndex, "Unclosed section '" + tag + "'!")
          };
          _ref2 = Parse(template, delimiters, sectionInfo), tmpl = _ref2[0], pos = _ref2[1];
          sectionInfo['#'] = buildSectionTag = function(name, delims, raw) {
            return function(context) {
              var parsed, result, v, value;
              value = Find(name, context) || [];
              tmpl = value instanceof Function ? value(raw) : raw;
              if (!(value instanceof Array)) {
                value = [value];
              }
              parsed = Parse(tmpl || '', delims);
              context.push(value);
              result = (function() {
                var _i, _len, _results;
                _results = [];
                for (_i = 0, _len = value.length; _i < _len; _i++) {
                  v = value[_i];
                  context[context.length - 1] = v;
                  _results.push(Expand.apply(null, [this, parsed].concat(__slice.call(arguments))));
                }
                return _results;
              }).apply(this, arguments);
              context.pop();
              return result.join('');
            };
          };
          sectionInfo['^'] = buildInvertedSectionTag = function(name, delims, raw) {
            return function(context) {
              var value;
              value = Find(name, context) || [];
              if (!(value instanceof Array)) {
                value = [1];
              }
              value = value.length === 0 ? Parse(raw, delims) : [];
              return Expand.apply(null, [this, value].concat(__slice.call(arguments)));
            };
          };
          buffer.push(sectionInfo[type](tag, delimiters, tmpl));
          break;
        case '/':
          if (section == null) {
            error = "End Section tag '" + tag + "' found, but not in section!";
          } else if (tag !== (name = section.name)) {
            error = "End Section tag closes '" + tag + "'; expected '" + name + "'!";
          }
          if (error) {
            throw parseError(tagPattern.lastIndex, error);
          }
          template = template.slice(section.start, contentEnd + 1 || 9e9);
          cache[template] = buffer;
          return [template, pos];
        case '=':
          if ((delimiters = tag.split(/\s+/)).length !== 2) {
            error = "Set Delimiters tags should have two and only two values!";
          }
          if (error) {
            throw parseError(tagPattern.lastIndex, error);
          }
          escape = /[-[\]{}()*+?.,\\^$|#]/g;
          delimiters = (function() {
            var _i, _len, _results;
            _results = [];
            for (_i = 0, _len = delimiters.length; _i < _len; _i++) {
              d = delimiters[_i];
              _results.push(d.replace(escape, "\\$&"));
            }
            return _results;
          })();
          tagPattern = BuildRegex();
          break;
        default:
          throw parseError(tagPattern.lastIndex, "Unknown tag type -- " + type);
      }
      tagPattern.lastIndex = pos != null ? pos : template.length;
    }
    if (section != null) {
      throw section.error;
    }
    if (template.length !== pos) {
      buffer.push(function() {
        return template.slice(pos);
      });
    }
    return cache[template] = buffer;
  };

  Milk = {
    VERSION: '1.2.0',
    helpers: [],
    partials: null,
    escape: function(value) {
      var entities;
      entities = {
        '&': 'amp',
        '"': 'quot',
        '<': 'lt',
        '>': 'gt'
      };
      return value.replace(/[&"<>]/g, function(ch) {
        return "&" + entities[ch] + ";";
      });
    },
    render: function(template, data, partials) {
      var context;
      if (partials == null) {
        partials = null;
      }
      if (!((partials || (partials = this.partials || {})) instanceof Function)) {
        partials = (function(partials) {
          return function(name) {
            if (!(name in partials)) {
              throw "Unknown partial '" + name + "'!";
            }
            return Find(name, [partials]);
          };
        })(partials);
      }
      context = this.helpers instanceof Array ? this.helpers : [this.helpers];
      return Expand(this, Parse(template), context.concat([data]), partials);
    }
  };

  if (this.__apptools_preinit != null) {
    this.__apptools_preinit.abstract_base_classes = [];
    this.__apptools_preinit.deferred_core_modules = [];
    this.__apptools_preinit.abstract_feature_interfaces = [];
    this.__apptools_preinit.deferred_library_integrations = [];
  } else {
    this.__apptools_preinit = {
      abstract_base_classes: [],
      deferred_core_modules: [],
      abstract_feature_interfaces: [],
      deferred_library_integrations: []
    };
  }

  CoreAPI = (function() {

    function CoreAPI() {}

    return CoreAPI;

  })();

  this.__apptools_preinit.abstract_base_classes.push(CoreAPI);

  CoreObject = (function() {

    function CoreObject() {}

    return CoreObject;

  })();

  this.__apptools_preinit.abstract_base_classes.push(CoreObject);

  CoreInterface = (function() {

    function CoreInterface() {}

    return CoreInterface;

  })();

  this.__apptools_preinit.abstract_base_classes.push(CoreInterface);

  CoreException = (function(_super) {

    __extends(CoreException, _super);

    function CoreException(module, message, context) {
      this.module = module;
      this.message = message;
      this.context = context;
    }

    CoreException.prototype.toString = function() {
      return '[' + this.module + '] CoreException: ' + this.message;
    };

    return CoreException;

  })(Error);

  this.__apptools_preinit.abstract_base_classes.push(CoreException);

  AppException = (function(_super) {

    __extends(AppException, _super);

    function AppException() {
      return AppException.__super__.constructor.apply(this, arguments);
    }

    AppException.prototype.toString = function() {
      return '[' + this.module + '] AppException: ' + this.message;
    };

    return AppException;

  })(CoreException);

  AppToolsException = (function(_super) {

    __extends(AppToolsException, _super);

    function AppToolsException() {
      return AppToolsException.__super__.constructor.apply(this, arguments);
    }

    AppToolsException.prototype.toString = function() {
      return '[' + this.module + '] AppToolsException: ' + this.message;
    };

    return AppToolsException;

  })(CoreException);

  this.__apptools_preinit.abstract_base_classes.push(AppException);

  this.__apptools_preinit.abstract_base_classes.push(AppToolsException);

  if (this.Backbone != null) {
    AppToolsView = (function(_super) {

      __extends(AppToolsView, _super);

      function AppToolsView() {
        return AppToolsView.__super__.constructor.apply(this, arguments);
      }

      return AppToolsView;

    })(Backbone.View);
    AppToolsModel = (function(_super) {

      __extends(AppToolsModel, _super);

      function AppToolsModel() {
        return AppToolsModel.__super__.constructor.apply(this, arguments);
      }

      return AppToolsModel;

    })(Backbone.Model);
    AppToolsRouter = (function(_super) {

      __extends(AppToolsRouter, _super);

      function AppToolsRouter() {
        return AppToolsRouter.__super__.constructor.apply(this, arguments);
      }

      return AppToolsRouter;

    })(Backbone.Router);
    AppToolsCollection = (function(_super) {

      __extends(AppToolsCollection, _super);

      function AppToolsCollection() {
        return AppToolsCollection.__super__.constructor.apply(this, arguments);
      }

      return AppToolsCollection;

    })(Backbone.Collection);
  } else {
    AppToolsView = (function() {

      function AppToolsView() {}

      return AppToolsView;

    })();
    AppToolsModel = (function() {

      function AppToolsModel() {}

      return AppToolsModel;

    })();
    AppToolsRouter = (function() {

      function AppToolsRouter() {}

      return AppToolsRouter;

    })();
    AppToolsCollection = (function() {

      function AppToolsCollection() {}

      return AppToolsCollection;

    })();
  }

  this.__apptools_preinit.abstract_base_classes.push(AppToolsView);

  this.__apptools_preinit.abstract_base_classes.push(AppToolsModel);

  this.__apptools_preinit.abstract_base_classes.push(AppToolsRouter);

  this.__apptools_preinit.abstract_base_classes.push(AppToolsCollection);

  Util = (function() {
    var _this = this;

    Util.mount = 'util';

    Util.events = [];

    Util.prototype.is = function(thing) {
      return !this.in_array(thing, [false, null, NaN, void 0, 0, {}, [], '', 'false', 'False', 'null', 'NaN', 'undefined', '0', 'none', 'None']);
    };

    Util.prototype.is_function = function(object) {
      return typeof object === 'function';
    };

    Util.prototype.is_object = function(object) {
      return typeof object === 'object';
    };

    Util.prototype.is_raw_object = function(object) {
      if (!object || typeof object !== 'object' || object.nodeType || (typeof object === 'object' && __indexOf.call(object, 'setInterval') >= 0)) {
        return false;
      }
      if ((object.constructor != null) && !object.hasOwnProperty('constructor') && !object.constructor.prototype.hasOwnProperty('isPrototypeOf')) {
        return false;
      }
      return true;
    };

    Util.prototype.is_empty_object = function(object) {
      var key, _i, _len;
      for (_i = 0, _len = object.length; _i < _len; _i++) {
        key = object[_i];
        return false;
      }
      return true;
    };

    Util.prototype.is_array = Array.isArray || function(object) {
      return typeof object === 'array' || Object.prototype.toString.call(object) === '[object Array]';
    };

    Util.prototype.in_array = function(item, array) {
      var it, matches, _fn, _i, _len,
        _this = this;
      if (array.indexOf != null) {
        return !!~array.indexOf(item);
      }
      matches = [];
      _fn = function(it) {
        if (it === item) {
          return matches.push(it);
        }
      };
      for (_i = 0, _len = array.length; _i < _len; _i++) {
        it = array[_i];
        _fn(it);
      }
      return matches.length > 0;
    };

    Util.prototype.to_array = function(node_or_token_list) {
      var array;
      array = [];
      for (i = node_or_token_list.length; i--; array.unshift(node_or_token_list[i]));

      if (array !== []) {
        return array;
      } else {
        return null;
      }
    };

    Util.prototype.get = function(query, node) {
      var cls, id, tg;
      if (node == null) {
        node = document;
      }
      if (query.nodeType) {
        return query;
      }
      if ((id = document.getElementById(query)) != null) {
        return id;
      } else {
        if ((cls = node.getElementsByClassName(query)).length > 0) {
          return this.to_array(cls);
        } else {
          if ((tg = node.getElementsByTagName(query)).length > 0) {
            return this.to_array(tg);
          } else {
            return null;
          }
        }
      }
    };

    Util.prototype.get_offset = function(elem) {
      var offL, offT;
      offL = offT = 0;
      while (true) {
        offL += elem.offsetLeft;
        offT += elem.offsetTop;
        if (!(elem = elem.offsetParent)) {
          break;
        }
      }
      return {
        left: offL,
        top: offT
      };
    };

    Util.prototype.has_class = function(element, cls) {
      var _ref;
      return ((_ref = element.classList) != null ? typeof _ref.contains === "function" ? _ref.contains(cls) : void 0 : void 0) || element.className && new RegExp('\\s*' + cls + '\\s*').test(element.className);
    };

    Util.prototype.is_id = function(str) {
      if (str.charAt(0) === '#' || document.getElementById(str !== null)) {
        return true;
      } else {
        return false;
      }
    };

    Util.prototype.bind = function(element, event, fn, prop) {
      var el, ev, func, _i, _len, _results, _results1,
        _this = this;
      if (prop == null) {
        prop = false;
      }
      if (this.is_array(element)) {
        _results = [];
        for (_i = 0, _len = element.length; _i < _len; _i++) {
          el = element[_i];
          _results.push((function(el) {
            return _this.bind(el, event, fn, prop);
          })(el));
        }
        return _results;
      } else if (this.is_raw_object(event)) {
        _results1 = [];
        for (ev in event) {
          func = event[ev];
          _results1.push((function(ev, func) {
            return _this.bind(element, ev, func, prop);
          })(ev, func));
        }
        return _results1;
      } else {
        return element.addEventListener(event, fn, prop);
      }
    };

    Util.prototype.unbind = function(element, event) {
      var el, els, ev, item, _i, _j, _k, _len, _len1, _len2, _results, _results1, _results2,
        _this = this;
      if (this.is_array(element)) {
        _results = [];
        for (_i = 0, _len = element.length; _i < _len; _i++) {
          el = element[_i];
          _results.push((function(el) {
            return _this.unbind(el, event);
          })(el));
        }
        return _results;
      } else if (this.is_array(event)) {
        _results1 = [];
        for (_j = 0, _len1 = event.length; _j < _len1; _j++) {
          ev = event[_j];
          _results1.push((function(ev) {
            return _this.unbind(element, ev);
          })(ev));
        }
        return _results1;
      } else if (this.is_raw_object(element)) {
        _results2 = [];
        for (el in element) {
          ev = element[el];
          _results2.push((function(el, ev) {
            return _this.unbind(el, ev);
          })(el, ev));
        }
        return _results2;
      } else if (element.constructor.name === 'NodeList') {
        els = [];
        for (_k = 0, _len2 = element.length; _k < _len2; _k++) {
          item = element[_k];
          els.push(item);
        }
        return this.unbind(els, event);
      } else {
        return element.removeEventListener(event);
      }
    };

    Util.prototype.block = function(async_method, object) {
      var result, _done;
      if (object == null) {
        object = {};
      }
      console.log('[Util] Enforcing blocking at user request... :(');
      _done = false;
      result = null;
      async_method(object, function(x) {
        result = x;
        return _done = true;
      });
      while (true) {
        if (_done !== false) {
          break;
        }
      }
      return result;
    };

    Util.prototype.now = function() {
      return new Date();
    };

    Util.prototype.timestamp = function(d) {
      if (d == null) {
        d = new Date();
      }
      return [[d.getMonth() + 1, d.getDate(), d.getFullYear()].join('-'), [d.getHours(), d.getMinutes(), d.getSeconds()].join(':')].join(' ');
    };

    Util.prototype.prep_animation = function(t, e, c) {
      var options;
      options = !(t != null) ? {
        duration: 400
      } : ((t != null) && this.is_object(t) ? this.extend({}, t) : {
        complete: c || (!c && e) || (is_function(t && t)),
        duration: t,
        easing: (c && e) || (e && !is_function(e))
      });
      return options;
    };

    Util.prototype.throttle = function(fn, buffer, prefire) {
      var last, timer;
      if (buffer == null) {
        buffer = 150;
      }
      timer = null;
      last = 0;
      return function() {
        var args, clear, elapsed, go,
          _this = this;
        args = arguments;
        elapsed = Util.now() - last;
        clear = function() {
          return timer = null;
        };
        go = function() {
          last = Util.now();
          return fn.apply(_this, args);
        };
        if (prefire && !timer) {
          go();
        }
        if (!!timer) {
          clearTimeout(timer);
        }
        if (!(prefire != null) && elapsed >= buffer) {
          return go();
        } else {
          return timer = setTimeout((prefire ? clear : go), !(prefire != null) ? buffer - elapsed : buffer);
        }
      };
    };

    Util.prototype.debounce = function(fn, buffer, prefire) {
      if (buffer == null) {
        buffer = 200;
      }
      if (prefire == null) {
        prefire = false;
      }
      return this.throttle(fn, buffer, prefire);
    };

    Util.prototype.extend = function() {
      var arg, args, deep, i, len, target, _fn, _i, _len,
        _this = this;
      target = arguments[0] || {};
      i = 1;
      deep = false;
      len = arguments.length;
      if (typeof target === 'boolean') {
        deep = target;
        target = arguments[1] || {};
        i++;
      }
      if (!this.is_object(target) && !this.is_function(target)) {
        target = {};
      }
      args = Array.prototype.slice.call(arguments, i);
      _fn = function(arg) {
        var a, clone, copied_src, o, option, options, src, value, _results;
        options = arg;
        _results = [];
        for (option in options) {
          value = options[option];
          if (target === value) {
            continue;
          }
          o = String(option);
          clone = value;
          src = target[option];
          if (deep && (clone != null) && (_this.is_raw_object(clone) || (a = _this.is_array(clone)))) {
            if (a != null) {
              a = false;
              copied_src = src && (_this.is_array(src) ? src : []);
            } else {
              copied_src = src && (_this.is_raw_object(src) ? src : {});
            }
            _results.push(target[option] = _this.extend(deep, copied_src, clone));
          } else if (clone != null) {
            _results.push(target[option] = clone);
          } else {
            _results.push(void 0);
          }
        }
        return _results;
      };
      for (_i = 0, _len = args.length; _i < _len; _i++) {
        arg = args[_i];
        _fn(arg);
      }
      return target;
    };

    Util.prototype.to_hex = function(color) {
      var b, c, g, r;
      if (color.match(/^#?[0-9A-F]{6}|[0-9A-F]{3}$\/i/)) {
        if (color.charAt(0 === '#')) {
          return color;
        } else {
          return '#' + color;
        }
      } else if (color.match(/^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$/)) {
        c = [parseInt(RegExp.$1, 10), parseInt(RegExp.$2, 10), parseInt(RegExp.$3, 10)];
        if (c.length === 3) {
          r = this.zero_fill(c[0].toString(16, 2));
          g = this.zero_fill(c[1].toString(16, 2));
          b = this.zero_fill(c[2].toString(16, 2));
          return '#' + r + g + b;
        }
      } else {
        return false;
      }
    };

    Util.prototype.to_rgb = function(color) {
      var b, c, g, r;
      if (color.match(/^rgb\(\s*\d{1,3}\s*,\s\d{1,3}\s*,\s*\d{1,3}\s*\)$/)) {
        return color;
      } else if (color.match(/^#?([0-9A-F]{1,2})([0-9A-F]{1,2})([0-9A-F]{1,2})$\/i/)) {
        c = [parseInt(RegExp.$1, 16), parseInt(RegExp.$2, 16), parseInt(RegExp.$3, 16)];
        r = c[0].toString(10);
        g = c[1].toString(10);
        b = c[2].toString(10);
        return 'rgb(' + r + ',' + g + ',' + b + ')';
      } else {
        return false;
      }
    };

    Util.prototype.wrap = function(e, fn) {
      var args, i;
      i = 2;
      if (e.preventDefault != null) {
        e.preventDefault();
        e.stopPropagation();
      } else {
        fn = e;
        i--;
      }
      args = Array.prototype.slice.call(arguments, i);
      return function() {
        return fn.apply(this, args);
      };
    };

    Util.prototype.zero_fill = function(num, length) {
      return (Array(length).join('0') + num).slice(-length);
    };

    function Util() {
      this.zero_fill = __bind(this.zero_fill, this);

      this.wrap = __bind(this.wrap, this);

      this.to_rgb = __bind(this.to_rgb, this);

      this.to_hex = __bind(this.to_hex, this);

      this.extend = __bind(this.extend, this);

      this.throttle = __bind(this.throttle, this);

      this.prep_animation = __bind(this.prep_animation, this);

      this.timestamp = __bind(this.timestamp, this);

      this.now = __bind(this.now, this);

      this.block = __bind(this.block, this);

      this.unbind = __bind(this.unbind, this);

      this.bind = __bind(this.bind, this);

      this.is_id = __bind(this.is_id, this);

      this.has_class = __bind(this.has_class, this);

      this.get_offset = __bind(this.get_offset, this);

      this.get = __bind(this.get, this);

      this.to_array = __bind(this.to_array, this);

      this.in_array = __bind(this.in_array, this);

      this.is_empty_object = __bind(this.is_empty_object, this);

      this.is_raw_object = __bind(this.is_raw_object, this);

      this.is_object = __bind(this.is_object, this);

      this.is_function = __bind(this.is_function, this);

      this.is = __bind(this.is, this);
      return this;
    }

    Util._init = function() {};

    return Util;

  }).call(this);

  this.__apptools_preinit.abstract_base_classes.push(Util);

  this.__apptools_preinit.deferred_core_modules.push({
    module: Util
  });

  Util = window.Util = new Util();

  CoreDevAPI = (function(_super) {

    __extends(CoreDevAPI, _super);

    CoreDevAPI.mount = 'dev';

    CoreDevAPI.events = [];

    function CoreDevAPI(apptools, window) {
      var _this = this;
      this.config = {};
      this.environment = {};
      this.performance = {};
      this.debug = {
        logging: true,
        eventlog: true,
        verbose: true,
        serverside: false
      };
      this.setDebug = function(debug) {
        _this.debug = debug;
        return _this._sendLog("[CoreDev] Debug has been set.", _this.debug);
      };
      this._sendLog = function() {
        var args;
        args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
        return console.log.apply(console, args);
      };
      this.log = function() {
        var context, message, module;
        module = arguments[0], message = arguments[1], context = 3 <= arguments.length ? __slice.call(arguments, 2) : [];
        if (!(context != null)) {
          context = '{no context}';
        }
        if (_this.debug.logging === true) {
          _this._sendLog.apply(_this, ["[" + module + "] INFO: " + message].concat(__slice.call(context)));
        }
      };
      this.warning = this.warn = function() {
        var context, message, module;
        module = arguments[0], message = arguments[1], context = 3 <= arguments.length ? __slice.call(arguments, 2) : [];
        if (!(context != null)) {
          context = '{no context}';
        }
        if (_this.debug.logging === true) {
          _this._sendLog.apply(_this, ["[" + module + "] WARNING: " + message].concat(__slice.call(context)));
        }
      };
      this.error = function() {
        var context, message, module;
        module = arguments[0], message = arguments[1], context = 3 <= arguments.length ? __slice.call(arguments, 2) : [];
        if (_this.debug.logging === true) {
          _this._sendLog.apply(_this, ["[" + module + "] ERROR: " + message].concat(__slice.call(context)));
        }
      };
      this.verbose = function() {
        var context, message, module;
        module = arguments[0], message = arguments[1], context = 3 <= arguments.length ? __slice.call(arguments, 2) : [];
        if (_this.debug.verbose === true) {
          _this._sendLog.apply(_this, ["[" + module + "] DEBUG: " + message].concat(__slice.call(context)));
        }
      };
      this.exception = this.critical = function() {
        var context, exception, message, module;
        module = arguments[0], message = arguments[1], exception = arguments[2], context = 4 <= arguments.length ? __slice.call(arguments, 3) : [];
        if (exception == null) {
          exception = window.AppToolsException;
        }
        _this._sendLog("A critical error or unhandled exception occurred.");
        _this._sendLog.apply(_this, ["[" + module + "] CRITICAL: " + message].concat(__slice.call(context)));
        throw new exception(module, message, context);
      };
    }

    return CoreDevAPI;

  })(CoreAPI);

  this.__apptools_preinit.abstract_base_classes.push(CoreDevAPI);

  CoreModelAPI = (function(_super) {

    __extends(CoreModelAPI, _super);

    CoreModelAPI.mount = 'model';

    CoreModelAPI.events = [];

    function CoreModelAPI() {
      var _this = this;
      this.internal = {
        block: function() {
          var async_method, params, results, _done;
          async_method = arguments[0], params = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
          _done = false;
          results = null;
          async_method.apply(null, __slice.call(params).concat([function(r) {
            results = r;
            return _done = true;
          }]));
          while (true) {
            if (_done !== false) {
              break;
            }
          }
          return results;
        },
        validate: function(model, _model) {
          var invalid, item, prop, _i, _len;
          if (_model == null) {
            _model = model.constructor.prototype;
          }
          invalid = [];
          for (prop in model) {
            if (!{}.hasOwnProperty.call(model, prop)) {
              continue;
            }
            if (model[prop].constructor.name === _model[prop].constructor.name) {
              continue;
            }
            invalid.push(prop);
          }
          for (_i = 0, _len = invalid.length; _i < _len; _i++) {
            item = invalid[_i];
            return invalid;
          }
          return true;
        }
      };
      this.put = function(object) {
        return _this.internal.block(_this.put_async, object);
      };
      this.get = function(key, kind) {
        return _this.internal.block(_this.get_async, key, kind);
      };
      this["delete"] = function(key, kind) {
        return _this.internal.block(_this.delete_async, key, kind);
      };
      this.put_async = function(callback) {
        if (callback == null) {
          callback = function(x) {
            return x;
          };
        }
        return apptools.storage.put(_this.constructor.prototype.name, callback);
      };
      this.get_async = function(key, callback) {
        if (callback == null) {
          callback = function(x) {
            return x;
          };
        }
        return apptools.storage.get(_this.key, _this.constructor.prototype.name, callback);
      };
      this.delete_async = function(callback) {
        if (callback == null) {
          callback = function(x) {
            return x;
          };
        }
        return apptools.storage["delete"](_this.key, _this.constructor.prototype.name, callback);
      };
      this.all = function(callback) {
        if (!(callback != null) || !(Util != null ? Util.is_function(callback) : void 0)) {
          if (callback != null) {
            throw 'Provided callback isn\'t a function. Whoops.';
          } else {
            throw 'all() requires a callback.';
          }
        } else {
          throw 'all() currently in active development, sorry.';
        }
      };
      this.register = function() {
        return apptools.dev.verbose('CoreModelAPI', 'register() currently in active development, sorry.');
      };
    }

    CoreModelAPI.init = function() {};

    return CoreModelAPI;

  })(CoreAPI);

  Model = (function() {

    Model.prototype.key = null;

    function Model() {
      this.render = __bind(this.render, this);

      this.all = __bind(this.all, this);

      this.delete_async = __bind(this.delete_async, this);

      this.get_async = __bind(this.get_async, this);

      this.put_async = __bind(this.put_async, this);

      this["delete"] = __bind(this["delete"], this);

      this.get = __bind(this.get, this);

      this.put = __bind(this.put, this);

    }

    Model.prototype.put = function() {
      var args, _ref;
      args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      return (_ref = apptools.model).put.apply(_ref, [this].concat(__slice.call(args)));
    };

    Model.prototype.get = function() {
      var args, _ref;
      args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      return (_ref = apptools.model).get.apply(_ref, [this].concat(__slice.call(args)));
    };

    Model.prototype["delete"] = function() {
      var args, _ref;
      args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      return (_ref = apptools.model)["delete"].apply(_ref, [this].concat(__slice.call(args)));
    };

    Model.prototype.put_async = function() {
      var args, _ref;
      args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      return (_ref = apptools.model).put_async.apply(_ref, [this].concat(__slice.call(args)));
    };

    Model.prototype.get_async = function() {
      var args, _ref;
      args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      return (_ref = apptools.model).get_async.apply(_ref, [this].concat(__slice.call(args)));
    };

    Model.prototype.delete_async = function() {
      var args, _ref;
      args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      return (_ref = apptools.model).delete_async.apply(_ref, [this].concat(__slice.call(args)));
    };

    Model.prototype.all = function() {
      var args, _ref;
      args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      return (_ref = apptools.model).all.apply(_ref, [this].concat(__slice.call(args)));
    };

    Model.prototype.render = function(template) {};

    return Model;

  })();

  this.__apptools_preinit.abstract_base_classes.push(CoreModelAPI);

  this.__apptools_preinit.abstract_base_classes.push(Model);

  CoreEventsAPI = (function(_super) {

    __extends(CoreEventsAPI, _super);

    CoreEventsAPI.mount = 'events';

    CoreEventsAPI.events = [];

    function CoreEventsAPI(apptools, window) {
      var _this = this;
      this.registry = [];
      this.callchain = {};
      this.history = [];
      this.fire = this.trigger = function() {
        var args, bridge, callback_directive, event, event_bridges, hook_error_count, hook_exec_count, result, touched_events, _i, _j, _len, _len1, _ref;
        event = arguments[0], args = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
        apptools.dev.verbose('Events', 'Triggered event:', event, args, _this.callchain[event]);
        if (__indexOf.call(_this.registry, event) >= 0) {
          hook_exec_count = 0;
          hook_error_count = 0;
          event_bridges = [];
          touched_events = [];
          touched_events.push(event);
          _ref = _this.callchain[event].hooks;
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            callback_directive = _ref[_i];
            try {
              if (callback_directive.once === true && callback_directive.has_run === true) {
                continue;
              } else if ((callback_directive.bridge != null) === false) {
                result = callback_directive.fn.apply(callback_directive, args);
                hook_exec_count++;
                _this.history.push({
                  event: event,
                  callback: callback_directive,
                  args: args,
                  result: result
                });
                callback_directive.has_run = true;
              } else if (callback_directive.bridge === true) {
                event_bridges.push({
                  event: callback_directive.event,
                  args: args
                });
              }
            } catch (error) {
              hook_error_count++;
              _this.history.push({
                event: event,
                callback: callback_directive,
                args: args,
                error: error
              });
            }
          }
          for (_j = 0, _len1 = event_bridges.length; _j < _len1; _j++) {
            bridge = event_bridges[_j];
            touched_events.push(bridge.event);
            _this.trigger.apply(_this, [bridge.event].concat(__slice.call(bridge.args)));
          }
          return {
            events: touched_events,
            executed: hook_exec_count,
            errors: hook_error_count
          };
        } else {
          return false;
        }
      };
      this.create = this.register = function(names) {
        var name, _i, _len;
        if (!(names instanceof Array)) {
          names = [names];
        }
        for (_i = 0, _len = names.length; _i < _len; _i++) {
          name = names[_i];
          _this.registry.push.apply(_this.registry, names);
          _this.callchain[name] = {
            hooks: []
          };
        }
        apptools.dev.verbose('Events', 'Registered events:', {
          count: names.length,
          events: names
        });
        return true;
      };
      this.on = this.upon = this.when = this.hook = function(event, callback, once) {
        if (once == null) {
          once = false;
        }
        if (__indexOf.call(_this.registry, event) < 0) {
          apptools.dev.warning('Events', '');
          _this.register(event);
        }
        _this.callchain[event].hooks.push({
          fn: callback,
          once: once,
          has_run: false,
          bridge: false
        });
        apptools.dev.verbose('Events', 'Hook registered on event.', event);
        return true;
      };
      this.delegate = this.bridge = function(from_events, to_events) {
        var source_ev, target_ev, _i, _len, _results;
        if (typeof to_events === 'string') {
          to_events = [to_events];
        }
        if (typeof from_events === 'string') {
          from_events = [from_events];
        }
        _results = [];
        for (_i = 0, _len = from_events.length; _i < _len; _i++) {
          source_ev = from_events[_i];
          _results.push((function() {
            var _j, _len1, _results1;
            _results1 = [];
            for (_j = 0, _len1 = to_events.length; _j < _len1; _j++) {
              target_ev = to_events[_j];
              apptools.dev.verbose('Events', 'Bridging events:', source_ev, '->', target_ev);
              if (!(this.callchain[source_ev] != null)) {
                apptools.dev.warn('Events', 'Bridging from undefined source event:', source_ev);
                this.register(source_ev);
              }
              _results1.push(this.callchain[source_ev].hooks.push({
                event: target_ev,
                bridge: true
              }));
            }
            return _results1;
          }).call(_this));
        }
        return _results;
      };
    }

    return CoreEventsAPI;

  })(CoreAPI);

  this.__apptools_preinit.abstract_base_classes.push(CoreEventsAPI);

  CoreAgentAPI = (function(_super) {

    __extends(CoreAgentAPI, _super);

    CoreAgentAPI.mount = 'agent';

    CoreAgentAPI.events = ['UA_DISCOVER'];

    function CoreAgentAPI(apptools, window) {
      this._data = {};
      this.platform = {};
      this.capabilities = {};
      if (apptools.lib.modernizr != null) {
        this.capabilities = apptools.lib.modernizr;
      }
      this.capabilities.simple = {};
      this._data = {
        browsers: [
          {
            string: navigator.userAgent,
            subString: "Chrome",
            identity: "Chrome"
          }, {
            string: navigator.userAgent,
            subString: "OmniWeb",
            versionSearch: "OmniWeb/",
            identity: "OmniWeb"
          }, {
            string: navigator.vendor,
            subString: "Apple",
            identity: "Safari",
            versionSearch: "Version"
          }, {
            prop: window.opera,
            identity: "Opera"
          }, {
            string: navigator.vendor,
            subString: "iCab",
            identity: "iCab"
          }, {
            string: navigator.vendor,
            subString: "KDE",
            identity: "Konqueror"
          }, {
            string: navigator.userAgent,
            subString: "Firefox",
            identity: "Firefox"
          }, {
            string: navigator.vendor,
            subString: "Camino",
            identity: "Camino"
          }, {
            string: navigator.userAgent,
            subString: "Netscape",
            identity: "Netscape"
          }, {
            string: navigator.userAgent,
            subString: "MSIE",
            identity: "Explorer",
            versionSearch: "MSIE"
          }, {
            string: navigator.userAgent,
            subString: "Gecko",
            identity: "Mozilla",
            versionSearch: "rv"
          }, {
            string: navigator.userAgent,
            subString: "Mozilla",
            identity: "Netscape",
            versionSearch: "Mozilla"
          }
        ],
        os: [
          {
            string: navigator.platform,
            subString: "Win",
            identity: "Windows"
          }, {
            string: navigator.platform,
            subString: "Mac",
            identity: "Mac"
          }, {
            string: navigator.userAgent,
            subString: "iPhone",
            identity: "iPhone/iPod"
          }, {
            string: navigator.platform,
            subString: "Linux",
            identity: "Linux"
          }
        ]
      };
    }

    CoreAgentAPI.prototype._makeMatch = function(data) {
      var prop, string, value, _i, _len;
      for (_i = 0, _len = data.length; _i < _len; _i++) {
        value = data[_i];
        string = value.string;
        prop = value.prop;
        this._data.versionSearchString = value.versionSearch || value.identity;
        if (string !== null) {
          if (value.string.indexOf(value.subString) !== -1) {
            return value.identity;
          }
        } else if (prop) {
          return value.identity;
        }
      }
    };

    CoreAgentAPI.prototype._makeVersion = function(dataString) {
      var index;
      index = dataString.indexOf(this._data.versionSearchString);
      if (index === -1) {

      } else {
        return parseFloat(dataString.substring(index + this._data.versionSearchString.length + 1));
      }
    };

    CoreAgentAPI.prototype.discover = function() {
      var browser, mobile, os, type, version;
      browser = this._makeMatch(this._data.browsers) || "unknown";
      version = this._makeVersion(navigator.userAgent) || this._makeVersion(navigator.appVersion) || "unknown";
      os = this._makeMatch(this._data.os) || "unknown";
      if (browser === 'iPod/iPhone' || browser === 'Android') {
        type = 'mobile';
        mobile = false;
      }
      this.platform = {
        os: os,
        type: type,
        vendor: navigator.vendor,
        product: navigator.product,
        browser: browser,
        version: version,
        flags: {
          online: navigator.onLine || true,
          mobile: mobile,
          webkit: $.browser.webkit,
          msie: $.browser.msie,
          opera: $.browser.opera,
          mozilla: $.browser.mozilla
        }
      };
      this.capabilities.simple.cookies = navigator.cookieEnabled;
      if (window.jQuery != null) {
        return this.capabilities.simple.ajax = $.support.ajax;
      }
    };

    return CoreAgentAPI;

  })(CoreAPI);

  this.__apptools_preinit.abstract_base_classes.push(CoreAgentAPI);

  CoreDispatchAPI = (function(_super) {

    __extends(CoreDispatchAPI, _super);

    CoreDispatchAPI.mount = 'dispatch';

    CoreDispatchAPI.events = [];

    function CoreDispatchAPI(apptools, window) {
      var _this = this;
      this.state = {
        opened: false,
        receiving: false,
        error: false,
        history: {
          errors: [],
          received: []
        },
        pending: {},
        complete: {}
      };
      this.init = function() {
        _this.state.opened = true;
        return apptools.dev.verbose('Dispatch', 'Dispatch startup signal received.');
      };
      this.expect = function(id, request, xhr) {
        _this.state.pending[id] = {
          request: request,
          callbacks: callbacks,
          xhr: xhr
        };
        return apptools.dev.verbose('Dispatch', 'Received EXPECT signal.', id, request, callbacks, xhr);
      };
      this.receive = function(raw_response) {
        var context, response, _base, _base1, _base2;
        try {
          response = JSON.parse(raw_response.data);
        } catch (e) {
          response = raw_response.data;
        }
        apptools.dev.verbose('Dispatch', 'Parsed async message.', response);
        _this.state.history.received.push(raw_response);
        if (response.status === 'ok') {
          apptools.dev.verbose('Dispatch', 'Triggering deferred success callback.');
          _this.state.complete[response.id] = _this.state.pending[response.id];
          _this.state.complete[response.id].response = response;
          delete _this.state.pending[response.id];
          apptools.dev.log('RPC', 'Success', raw_response.data, response.status, _this.state.complete[response.id].xhr);
          apptools.api.rpc.lastResponse = raw_response.data;
          apptools.api.rpc.history[response.id].xhr = _this.state.complete[response.id].xhr;
          apptools.api.rpc.history[response.id].status = response.status;
          apptools.api.rpc.history[response.id].response = raw_response.data;
          context = {
            xhr: _this.state.complete[response.id].xhr,
            status: response.status,
            data: raw_response.data
          };
          apptools.events.trigger('RPC_SUCCESS', context);
          return typeof (_base = _this.state.complete[response.id].callbacks).success === "function" ? _base.success(response.response.content) : void 0;
        } else if (response.status === 'notify') {
          apptools.dev.verbose('Dispatch', 'Received NOTIFY signal.');
          return typeof (_base1 = _this.state.pending[response.id].callbacks).notify === "function" ? _base1.notify(response.response.content) : void 0;
        } else {
          apptools.dev.error('Dispatch', 'Userland deferred task error. Calling error callback.', response);
          return typeof (_base2 = _this.state.pending[response.id].callbacks).error === "function" ? _base2.error(response.content) : void 0;
        }
      };
      this.error = function(error) {
        _this.state.error = true;
        _this.history.errors.push(error);
        return apptools.dev.error('Dispatch', 'Dispatch error state triggered.', error);
      };
      this.close = function() {
        _this.state.opened = false;
        _this.state.receiving = false;
        return apptools.dev.verbose('Dispatch', 'Dispatch shutdown signal received.');
      };
    }

    return CoreDispatchAPI;

  })(CoreAPI);

  this.__apptools_preinit.abstract_base_classes.push(CoreDispatchAPI);

  StorageDriver = (function(_super) {

    __extends(StorageDriver, _super);

    StorageDriver.methods = ['compatible', 'construct'];

    StorageDriver["export"] = "public";

    function StorageDriver() {}

    return StorageDriver;

  })(CoreInterface);

  this.compatible = function() {};

  this.construct = function() {};

  StorageAdapter = (function(_super) {

    __extends(StorageAdapter, _super);

    StorageAdapter.methods = ['get', 'put', 'delete', 'clear', 'get_async', 'put_async', 'delete_async', 'clear_async'];

    StorageAdapter["export"] = "public";

    function StorageAdapter() {
      return;
    }

    return StorageAdapter;

  })(CoreInterface);

  KeyEncoder = (function(_super) {

    __extends(KeyEncoder, _super);

    KeyEncoder.methods = ['build_key', 'encode_key', 'build_cluster', 'encode_cluster'];

    KeyEncoder["export"] = "public";

    function KeyEncoder() {
      return;
    }

    return KeyEncoder;

  })(CoreInterface);

  if (this.__apptools_preinit != null) {
    if (!(this.__apptools_preinit.abstract_base_classes != null)) {
      this.__apptools_preinit.abstract_base_classes = [];
    }
    if (!(this.__apptools_preinit.deferred_core_modules != null)) {
      this.__apptools_preinit.deferred_core_modules = [];
    }
  } else {
    this.__apptools_preinit = {
      abstract_base_classes: [],
      deferred_core_modules: []
    };
  }

  this.__apptools_preinit.detected_storage_engines = [];

  this.__apptools_preinit.abstract_base_classes.push(StorageDriver);

  this.__apptools_preinit.abstract_base_classes.push(StorageAdapter);

  this.__apptools_preinit.abstract_feature_interfaces.push({
    adapter: StorageDriver,
    name: "storage"
  });

  SimpleKeyEncoder = (function(_super) {

    __extends(SimpleKeyEncoder, _super);

    function SimpleKeyEncoder() {
      var _this = this;
      this.build_key = function() {};
      this.encode_key = function() {};
      this.build_cluster = function() {};
      this.encode_cluster = function() {};
    }

    return SimpleKeyEncoder;

  })(KeyEncoder);

  _simple_key_encoder = new SimpleKeyEncoder();

  /* === DOM Storage Engines ===
  */


  LocalStorageEngine = (function(_super) {

    __extends(LocalStorageEngine, _super);

    LocalStorageEngine._state = {
      runtime: {
        count: {
          total_keys: 0,
          by_kind: []
        }
      }
    };

    function LocalStorageEngine(name) {
      var _this = this;
      this.name = name;
      this.get_async = function(key, callback) {
        var object;
        return callback.call(object = _this.get(key));
      };
      this.put_async = function(key, value, callback) {
        _this.put(key, value);
        return callback.call(value);
      };
      this.delete_async = function(key, callback) {
        _this["delete"](key);
        return callback.call(_this);
      };
      this.clear_async = function(callback) {
        _this.clear();
        return callback.call(_this);
      };
      this.get = function(key) {
        return localStorage.getItem(key);
      };
      this.put = function(key, value) {
        if (!(_this.get(key) != null)) {
          _this._state.runtime.count.total_keys++;
        }
        return localStorage.setItem(key, value);
      };
      this["delete"] = function(key) {
        _this._state.runtime.count.total_keys--;
        return localStorage.removeItem(key);
      };
      this.clear = function() {
        _this._state.runtime.count.total_keys = 0;
        return localStorage.clear();
      };
      return;
    }

    return LocalStorageEngine;

  })(StorageAdapter);

  SessionStorageEngine = (function(_super) {

    __extends(SessionStorageEngine, _super);

    SessionStorageEngine._state = {
      runtime: {
        count: {
          total_keys: 0,
          by_kind: []
        }
      }
    };

    function SessionStorageEngine(name) {
      var _this = this;
      this.name = name;
      this.get_async = function(key, callback) {
        var object;
        return callback.call(object = _this.get(key));
      };
      this.put_async = function(key, value, callback) {
        _this.put(key, value);
        return callback.call(value);
      };
      this.delete_async = function(key, callback) {
        _this["delete"](key);
        return callback.call(_this);
      };
      this.clear_async = function(callback) {
        _this.clear();
        return callback.call(_this);
      };
      this.get = function(key) {
        return sessionStorage.getItem(key);
      };
      this.put = function(key, value) {
        if (!(_this.get(key) != null)) {
          _this._state.runtime.count.total_keys++;
        }
        return sessionStorage.setItem(key, value);
      };
      this["delete"] = function(key) {
        _this._state.runtime.count.total_keys--;
        return sessionStorage.removeItem(key);
      };
      this.clear = function() {
        _this._state.runtime.count.total_keys = 0;
        return sessionStorage.clear();
      };
      return;
    }

    return SessionStorageEngine;

  })(StorageAdapter);

  /* === DOM Storage Drivers ===
  */


  LocalStorageDriver = (function(_super) {

    __extends(LocalStorageDriver, _super);

    function LocalStorageDriver() {
      return LocalStorageDriver.__super__.constructor.apply(this, arguments);
    }

    LocalStorageDriver._state = {
      constructor: function() {
        var _this = this;
        this.compatible = function() {
          return !!window.localStorage;
        };
        this.construct = function(name) {
          var new_engine;
          if (name == null) {
            name = 'appstorage';
          }
          if (_this.compatible()) {
            return new_engine = new LocalStorageEngine(name);
          } else {
            return false;
          }
        };
      }
    };

    return LocalStorageDriver;

  })(StorageDriver);

  SessionStorageDriver = (function(_super) {

    __extends(SessionStorageDriver, _super);

    function SessionStorageDriver() {
      return SessionStorageDriver.__super__.constructor.apply(this, arguments);
    }

    SessionStorageDriver._state = {
      constructor: function() {
        var _this = this;
        this.compatible = function() {
          return !!window.sessionStorage;
        };
        this.construct = function(name) {
          var new_engine;
          if (name == null) {
            name = 'appstorage';
          }
          if (_this.compatible()) {
            return new_engine = new SessionStorageEngine(name);
          } else {
            return false;
          }
        };
      }
    };

    return SessionStorageDriver;

  })(StorageDriver);

  this.__apptools_preinit.detected_storage_engines.push({
    name: "LocalStorage",
    adapter: LocalStorageEngine,
    driver: LocalStorageDriver,
    key_encoder: _simple_key_encoder
  });

  this.__apptools_preinit.detected_storage_engines.push({
    name: "SessionStorage",
    adapter: SessionStorageEngine,
    driver: SessionStorageDriver,
    key_encoder: _simple_key_encoder
  });

  IndexedDBEngine = (function(_super) {

    __extends(IndexedDBEngine, _super);

    function IndexedDBEngine() {
      return;
    }

    return IndexedDBEngine;

  })(StorageAdapter);

  IndexedDBDriver = (function(_super) {

    __extends(IndexedDBDriver, _super);

    function IndexedDBDriver() {
      return;
    }

    return IndexedDBDriver;

  })(StorageDriver);

  this.__apptools_preinit.detected_storage_engines.push({
    name: "IndexedDB",
    adapter: IndexedDBEngine,
    driver: IndexedDBDriver
  });

  WebSQLEngine = (function(_super) {

    __extends(WebSQLEngine, _super);

    function WebSQLEngine() {
      return;
    }

    return WebSQLEngine;

  })(StorageAdapter);

  WebSQLDriver = (function(_super) {

    __extends(WebSQLDriver, _super);

    function WebSQLDriver() {
      return;
    }

    return WebSQLDriver;

  })(StorageDriver);

  this.__apptools_preinit.detected_storage_engines.push({
    name: "WebSQL",
    adapter: WebSQLEngine,
    driver: WebSQLDriver
  });

  CoreStorageAPI = (function(_super) {

    __extends(CoreStorageAPI, _super);

    CoreStorageAPI.mount = 'storage';

    CoreStorageAPI.events = ['STORAGE_INIT', 'ENGINE_LOADED', 'STORAGE_READY', 'STORAGE_ERROR', 'STORAGE_ACTIVITY', 'STORAGE_READ', 'STORAGE_WRITE', 'STORAGE_DELETE', 'COLLECTION_SCAN', 'COLLECTION_CREATE', 'COLLECTION_DESTROY', 'COLLECTION_UPDATE', 'COLLECTION_SYNC'];

    function CoreStorageAPI(apptools, window) {
      var _this = this;
      this._state = {
        runtime: {
          index: {
            key_read_tally: {},
            key_write_tally: {},
            local_by_key: {},
            local_by_kind: {}
          },
          count: {
            total_keys: 0,
            by_collection: [],
            by_kind: []
          },
          data: {}
        },
        config: {
          autoload: false,
          autosync: {
            enabled: false,
            interval: 120
          },
          drivers: [],
          engines: {},
          encrypt: false,
          integrity: false,
          obfuscate: false,
          local_only: false,
          callbacks: {
            ready: null,
            sync: null
          }
        },
        supervisor: {},
        cachebridge: {},
        model_kind_map: {},
        collection_kind_map: {}
      };
      this.internal = {
        check_support: function(modernizr) {},
        bootstrap: function(lawnchair) {},
        provision_collection: function(name, adapter, callback) {},
        add_storage_engine: function(name, driver, engine) {
          var d, e;
          try {
            d = new driver(apptools);
            e = new engine(apptools);
          } catch (err) {
            return false;
          }
          if (e.compatible()) {
            _this._state.config.engines[name] = e;
            driver.adapter = _this._state.config.engines[name];
            _this._state.config.drivers.push(driver);
            apptools.sys.drivers.install('storage', name, d, (d.enabled != null) | true, (d.priority != null) | 50, function(driver) {
              return apptools.events.trigger('ENGINE_LOADED', {
                driver: driver,
                engine: driver.adapter
              });
            });
            return true;
          } else {
            apptools.dev.verbose('StorageEngine', 'Detected incompatible storage engine. Skipping.', name, driver, engine);
            return false;
          }
        }
      };
      this.get = function() {};
      this.list = function() {};
      this.count = function() {};
      this.put = function() {};
      this.query = function() {};
      this["delete"] = function() {};
      this.sync = function() {};
      this._init = function() {
        var engine, _i, _len, _ref, _ref1, _ref2;
        apptools.events.trigger('STORAGE_INIT');
        apptools.dev.verbose('Storage', 'Storage support is currently under construction.');
        if (((_ref = apptools.sys) != null ? (_ref1 = _ref.preinit) != null ? _ref1.detected_storage_engines : void 0 : void 0) != null) {
          _ref2 = apptools.sys.preinit.detected_storage_engines;
          for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
            engine = _ref2[_i];
            _this.internal.add_storage_engine(engine.name, engine.driver, engine.adapter);
          }
        }
        return apptools.events.trigger('STORAGE_READY');
      };
      apptools.events.bridge(['STORAGE_READ', 'STORAGE_WRITE', 'STORAGE_DELETE'], 'STORAGE_ACTIVITY');
      apptools.events.bridge(['COLLECTION_CREATE', 'COLLECTION_UPDATE', 'COLLECTION_DESTROY', 'COLLECTION_SYNC', 'COLLECTION_SCAN'], 'STORAGE_ACTIVITY');
    }

    return CoreStorageAPI;

  })(CoreAPI);

  this.__apptools_preinit.abstract_base_classes.push(CoreStorageAPI);

  RPCAPI = (function(_super) {

    __extends(RPCAPI, _super);

    function RPCAPI(name, base_uri, methods, config) {
      var method, _i, _len, _ref;
      this.name = name;
      this.base_uri = base_uri;
      this.methods = methods;
      this.config = config;
      if (this.methods.length > 0) {
        _ref = this.methods;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          method = _ref[_i];
          this[method] = this._buildRPCMethod(method, base_uri, config);
        }
      }
    }

    RPCAPI.prototype._buildRPCMethod = function(method, base_uri, config) {
      var api, rpcMethod,
        _this = this;
      api = this.name;
      rpcMethod = function(params, callbacks, async, push, opts, config) {
        if (params == null) {
          params = {};
        }
        if (callbacks == null) {
          callbacks = null;
        }
        if (async == null) {
          async = false;
        }
        if (push == null) {
          push = false;
        }
        if (opts == null) {
          opts = {};
        }
        if (config == null) {
          config = {};
        }
        return (function(params, callbacks, async, push, opts) {
          var request;
          request = $.apptools.api.rpc.createRPCRequest({
            method: method,
            api: api,
            params: params || {},
            opts: opts || {},
            async: async || false,
            push: push || false
          });
          if (callbacks !== null) {
            return request.fulfill(callbacks, config);
          } else {
            return request;
          }
        })(params, callbacks, async, push, opts);
      };
      $.apptools.api.registerAPIMethod(api, method, base_uri, config);
      return rpcMethod;
    };

    return RPCAPI;

  })(CoreObject);

  RPCRequest = (function(_super) {

    __extends(RPCRequest, _super);

    function RPCRequest(id, opts, agent) {
      this.params = {};
      this.action = null;
      this.method = null;
      this.api = null;
      this.base_uri = null;
      this.envelope = {
        id: null,
        opts: {},
        agent: {}
      };
      this.ajax = {
        accepts: 'application/json',
        async: true,
        cache: true,
        global: true,
        http_method: 'POST',
        crossDomain: false,
        processData: false,
        ifModified: false,
        dataType: 'json',
        push: false,
        contentType: 'application/json; charset=utf-8'
      };
      if (id != null) {
        this.envelope.id = id;
      }
      if (opts != null) {
        this.envelope.opts = opts;
      }
      if (agent != null) {
        this.envelope.agent = agent;
      }
    }

    RPCRequest.prototype.fulfill = function(callbacks, config) {
      var defaultFailureCallback, defaultSuccessCallback,
        _this = this;
      if (callbacks == null) {
        callbacks = {};
      }
      if (!((callbacks != null ? callbacks.success : void 0) != null)) {
        defaultSuccessCallback = function(context, type, data) {
          return $.apptools.dev.log('RPC', 'RPC succeeded but had no success callback.', _this, context, type, data);
        };
        callbacks.success = defaultSuccessCallback;
      }
      if (!((callbacks != null ? callbacks.failure : void 0) != null)) {
        defaultFailureCallback = function(context) {
          return $.apptools.dev.error('RPC', 'RPC failed but had no failure callback.', _this, context);
        };
        callbacks.failure = defaultFailureCallback;
      }
      return $.apptools.api.rpc.fulfillRPCRequest(config, this, callbacks);
    };

    RPCRequest.prototype.setAsync = function(async) {
      var _ref, _ref1;
      if ((_ref = this.ajax) != null) {
        if ((_ref1 = _ref.async) == null) {
          _ref.async = async;
        }
      }
      return this;
    };

    RPCRequest.prototype.setPush = function(push) {
      if (push === true) {
        this.ajax.push = true;
        this.envelope.opts['alt'] = 'socket';
        this.envelope.opts['token'] = $.apptools.push.state.config.token;
      }
      return this;
    };

    RPCRequest.prototype.setOpts = function(opts) {
      var _ref, _ref1;
      if ((_ref = this.envelope) != null) {
        _ref.opts = _.defaults(opts, (_ref1 = this.envelope) != null ? _ref1.opts : void 0);
      }
      return this;
    };

    RPCRequest.prototype.setAgent = function(agent) {
      var _ref, _ref1;
      if ((_ref = this.envelope) != null) {
        if ((_ref1 = _ref.agent) == null) {
          _ref.agent = agent;
        }
      }
      return this;
    };

    RPCRequest.prototype.setAction = function(action) {
      this.action = action;
      return this;
    };

    RPCRequest.prototype.setMethod = function(method) {
      this.method = method;
      return this;
    };

    RPCRequest.prototype.setAPI = function(api) {
      this.api = api;
      return this;
    };

    RPCRequest.prototype.setBaseURI = function(base_uri) {
      this.base_uri = base_uri;
      return this;
    };

    RPCRequest.prototype.setParams = function(params) {
      this.params = params != null ? params : {};
      return this;
    };

    RPCRequest.prototype.payload = function() {
      var _payload;
      _payload = {
        id: this.envelope.id,
        opts: this.envelope.opts,
        agent: this.envelope.agent,
        request: {
          params: this.params,
          method: this.method,
          api: this.api
        }
      };
      return _payload;
    };

    return RPCRequest;

  })(CoreObject);

  RPCResponse = (function(_super) {

    __extends(RPCResponse, _super);

    function RPCResponse() {
      var args;
      args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      $.apptools.dev.verbose('RPC', 'RPCResponse is not yet implemented and is currently stubbed.');
      return;
    }

    return RPCResponse;

  })(CoreObject);

  CoreRPCAPI = (function(_super) {

    __extends(CoreRPCAPI, _super);

    CoreRPCAPI.mount = 'api';

    CoreRPCAPI.events = ['RPC_CREATE', 'RPC_FULFILL', 'RPC_SUCCESS', 'RPC_ERROR', 'RPC_COMPLETE', 'RPC_PROGRESS'];

    function CoreRPCAPI(apptools, window) {
      var original_xhr, _ref, _ref1,
        _this = this;
      this.state = {
        sockets: {
          token: '__NULL__',
          enabled: false,
          status: 'DISCONNECTED',
          "default": null,
          default_host: (((_ref = apptools.config) != null ? (_ref1 = _ref.rpc) != null ? _ref1.socket_host : void 0 : void 0) != null) || null
        }
      };
      this.base_rpc_uri = apptools.config.rpc.base_uri || '/_api/rpc';
      this.socket_host = apptools.config.rpc.socket_host || null;
      if (apptools.sys.libraries.resolve('jQuery') !== false) {
        original_xhr = $.ajaxSettings.xhr;
      } else {
        original_xhr = new XMLHTTPRequest();
      }
      this.internals = {
        transports: {
          xhr: {
            factory: function() {
              var req;
              req = original_xhr();
              if (req) {
                if (typeof req.addEventListener === 'function') {
                  req.addEventListener("progress", function(ev) {
                    return apptools.events.trigger('RPC_PROGRESS', {
                      event: ev
                    });
                  }, false);
                }
              }
              return req;
            }
          },
          websocket: {
            factory: function() {
              var req, socket, _ref2, _ref3, _ref4, _ref5;
              if (apptools.agent.capabilities.websockets != null) {
                if ((((_ref2 = _this.state.sockets) != null ? _ref2.enabled : void 0) != null) === true) {
                  if ((((_ref3 = _this.state.sockets) != null ? _ref3["default"] : void 0) != null) === null && ((_ref4 = _this.state.sockets) != null ? (_ref5 = _ref4.open) != null ? _ref5.length : void 0 : void 0) === 0) {
                    socket = new apptools.push.socket.establish();
                    _this.state.sockets.enabled = true;
                    _this.state.sockets["default"] = socket;
                    _this.state.sockets.status = 'CONNECTED';
                  }
                  req = {};
                  return req;
                }
              } else {
                apptools.dev.error('RPC', 'Socket factory can\'t produce a socket because the client platform does not support WebSockets.');
                throw "SocketsNotSupported: The client platform does not have support for websockets.";
              }
            }
          }
        },
        config: {
          headers: {
            "X-ServiceClient": ["AppToolsJS/", [AppTools.version.major.toString(), AppTools.version.minor.toString(), AppTools.version.micro.toString(), AppTools.version.build.toString()].join('.'), "-", AppTools.version.release.toString()].join(''),
            "X-ServiceTransport": "AppTools/JSONRPC"
          }
        }
      };
      if (apptools.sys.libraries.resolve('jQuery') !== false) {
        $.ajaxSetup({
          global: true,
          xhr: function() {
            return _this.internals.transports.xhr.factory();
          },
          headers: this.internals.config.headers
        });
      }
      this.rpc = {
        lastRequest: null,
        lastFailure: null,
        lastResponse: null,
        history: {},
        action_prefix: null,
        alt_push_response: false,
        used_ids: [],
        factory: function(name, base_uri, methods, config) {
          return apptools.api[name] = new RPCAPI(name, base_uri, methods, config);
        },
        _assembleRPCURL: function(method, api, prefix, base_uri) {
          if (!(api != null) && !(base_uri != null)) {
            throw "[RPC] Error: Must specify either an API or base URI to generate an RPC endpoint.";
          } else {
            if (api != null) {
              if (base_uri != null) {
                base_uri = base_uri + '/' + api;
              } else {
                base_uri = _this.base_rpc_uri + '/' + api;
              }
            } else {
              if (!(base_uri != null)) {
                base_uri = _this.base_rpc_uri;
              }
            }
            if (prefix !== null) {
              return [prefix + base_uri, method].join('.');
            } else {
              return [base_uri, method].join('.');
            }
          }
        },
        provisionRequestID: function() {
          var id;
          if (_this.rpc.used_ids.length > 0) {
            id = Math.max.apply(_this, _this.rpc.used_ids) + 1;
            _this.rpc.used_ids.push(id);
            return id;
          } else {
            _this.rpc.used_ids.push(1);
            return 1;
          }
        },
        decodeRPCResponse: function(data, status, xhr, success, error) {
          return success(data, status);
        },
        createRPCRequest: function(config) {
          var request;
          request = new RPCRequest(_this.rpc.provisionRequestID());
          if (config.api != null) {
            request.setAPI(config.api);
          }
          if (config.method != null) {
            request.setMethod(config.method);
          }
          if (config.agent != null) {
            request.setAgent(config.agent);
          }
          if (config.opts != null) {
            request.setOpts(config.opts);
          }
          if (config.base_uri != null) {
            request.setBaseURI(config.base_uri);
          }
          if (config.params != null) {
            request.setParams(config.params);
          }
          if (config.async != null) {
            request.setAsync(config.async);
          }
          if (config.push != null) {
            request.setPush(config.push);
          } else {
            request.setPush(_this.rpc.alt_push_response);
          }
          apptools.dev.verbose('RPC', 'New Request', request, config);
          request.setAction(_this.rpc._assembleRPCURL(request.method, request.api, _this.rpc.action_prefix, _this.base_rpc_uri));
          return request;
        },
        fulfillRPCRequest: function(config, request, callbacks, transport) {
          var context;
          if (transport == null) {
            transport = 'xhr';
          }
          apptools.dev.verbose('RPC', 'Fulfill', config, request, callbacks);
          _this.rpc.lastRequest = request;
          _this.rpc.history[request.envelope.id] = {
            request: request,
            config: config,
            callbacks: callbacks
          };
          if (request.action === null) {
            if (request.method === null) {
              throw "[RPC] Error: Request must specify at least an action or method.";
            }
            if (request.base_uri === null) {
              if (request.api === null) {
                throw "[RPC] Error: Request must have an API or explicity defined BASE_URI.";
              } else {
                request.action = _this.rpc._assembleRPCURL(request.method, request.api, _this.rpc.action_prefix);
              }
            } else {
              request.action = _this.rpc._assembleRPCURL(request.method, null, _this.rpc.action_prefix, request.base_uri);
            }
          }
          if (request.action === null || request.action === void 0) {
            throw '[RPC] Error: Could not determine RPC action.';
          }
          context = {
            config: config,
            request: request,
            callbacks: callbacks
          };
          apptools.events.trigger('RPC_FULFILL', context);
          (function(apptools, request, callbacks) {
            var driver, xhr, xhr_action, xhr_settings,
              _this = this;
            xhr_settings = {
              resourceId: request.api + '.' + request.method,
              url: request.action,
              data: JSON.stringify(request.payload()),
              async: request.ajax.async,
              global: request.ajax.global,
              type: request.ajax.http_method || 'POST',
              accepts: request.ajax.accepts || 'application/json',
              crossDomain: request.ajax.crossDomain,
              dataType: request.ajax.dataType,
              processData: false,
              ifModified: request.ajax.ifModified,
              contentType: request.ajax.contentType,
              beforeSend: function(xhr, settings) {
                apptools.api.rpc.history[request.envelope.id].xhr = xhr;
                if (callbacks != null) {
                  if (typeof callbacks.status === "function") {
                    callbacks.status('beforeSend');
                  }
                }
                return xhr;
              },
              error: function(xhr, status, error) {
                if (callbacks != null) {
                  if (typeof callbacks.status === "function") {
                    callbacks.status('error');
                  }
                }
                apptools.dev.error('RPC', 'Error: ', {
                  error: error,
                  status: status,
                  xhr: xhr
                });
                apptools.api.rpc.lastFailure = error;
                apptools.api.rpc.history[request.envelope.id].xhr = xhr;
                apptools.api.rpc.history[request.envelope.id].status = status;
                apptools.api.rpc.history[request.envelope.id].failure = error;
                context = {
                  xhr: xhr,
                  status: status,
                  error: error
                };
                apptools.events.trigger('RPC_ERROR', context);
                apptools.events.trigger('RPC_COMPLETE', context);
                return callbacks != null ? typeof callbacks.failure === "function" ? callbacks.failure(error) : void 0 : void 0;
              },
              success: function(data, status, xhr) {
                if (data.status === 'ok') {
                  if (callbacks != null) {
                    if (typeof callbacks.status === "function") {
                      callbacks.status('success');
                    }
                  }
                  apptools.dev.log('RPC', 'Success', data, status, xhr);
                  apptools.api.rpc.lastResponse = data;
                  apptools.api.rpc.history[request.envelope.id].xhr = xhr;
                  apptools.api.rpc.history[request.envelope.id].status = status;
                  apptools.api.rpc.history[request.envelope.id].response = data;
                  context = {
                    xhr: xhr,
                    status: status,
                    data: data
                  };
                  apptools.events.trigger('RPC_SUCCESS', context);
                  apptools.events.trigger('RPC_COMPLETE', context);
                  return callbacks != null ? typeof callbacks.success === "function" ? callbacks.success(data.response.content, data.response.type, data) : void 0 : void 0;
                } else if (data.status === 'wait') {
                  if (callbacks != null) {
                    if (typeof callbacks.status === "function") {
                      callbacks.status('wait');
                    }
                  }
                  apptools.dev.log('RPC', 'PushWait', data, status, xhr);
                  context = {
                    xhr: xhr,
                    status: status,
                    data: data
                  };
                  if (callbacks != null) {
                    if (typeof callbacks.wait === "function") {
                      callbacks.wait(data, status, xhr);
                    }
                  }
                  return apptools.push.internal.expect(request.envelope.id, request, xhr);
                } else if (data.status === 'fail') {
                  if (callbacks != null) {
                    if (typeof callbacks.status === "function") {
                      callbacks.status('error');
                    }
                  }
                  apptools.dev.error('RPC', 'Error: ', {
                    error: data,
                    status: status,
                    xhr: xhr
                  });
                  apptools.api.rpc.lastFailure = data;
                  apptools.api.rpc.history[request.envelope.id].xhr = xhr;
                  apptools.api.rpc.history[request.envelope.id].status = status;
                  apptools.api.rpc.history[request.envelope.id].failure = data;
                  context = {
                    xhr: xhr,
                    status: status,
                    error: data
                  };
                  apptools.events.trigger('RPC_ERROR', context);
                  apptools.events.trigger('RPC_COMPLETE', context);
                  return callbacks != null ? typeof callbacks.failure === "function" ? callbacks.failure(data) : void 0 : void 0;
                } else {
                  return callbacks != null ? typeof callbacks.success === "function" ? callbacks.success(data.response.content, data.response.type, data) : void 0 : void 0;
                }
              },
              statusCode: {
                404: function() {
                  apptools.dev.error('RPC', 'HTTP/404', 'Could not resolve RPC action URI.');
                  return apptools.events.trigger('RPC_ERROR', {
                    message: 'RPC 404: Could not resolve RPC action URI.',
                    code: 404
                  });
                },
                403: function() {
                  apptools.dev.error('RPC', 'HTTP/403', 'Not authorized to access the specified endpoint.');
                  return apptools.events.trigger('RPC_ERROR', {
                    message: 'RPC 403: Not authorized to access the specified endpoint.',
                    code: 403
                  });
                },
                500: function() {
                  apptools.dev.error('RPC', 'HTTP/500', 'Internal server error.');
                  return apptools.events.trigger('RPC_ERROR', {
                    message: 'RPC 500: Woops! Something went wrong. Please try again.',
                    code: 500
                  });
                }
              }
            };
            driver = apptools.sys.drivers.resolve('transport');
            if (driver.name === 'amplify') {
              apptools.dev.verbose('RPC', 'Fulfilling with AmplifyJS transport adapter.');
              xhr_action = driver.driver.request;
              xhr = xhr_action(xhr_settings);
            } else if (driver.name === 'jquery') {
              apptools.dev.verbose('RPC', 'Fulfilling with jQuery AJAX transport adapter.', xhr_settings);
              xhr = jQuery.ajax(xhr_settings.url, xhr_settings);
            } else {
              apptools.dev.error('RPC', 'Native RPC adapter is currently stubbed.');
              throw "[RPC]: No valid AJAX transport adapter found.";
            }
            return apptools.dev.verbose('RPC', 'Resulting XHR: ', xhr);
          })(apptools, request, callbacks);
          return {
            id: request.envelope.id,
            request: request
          };
        }
      };
      this.ext = null;
      this.registerAPIMethod = function(api, name, base_uri, config) {
        var amplify, base_settings, resourceId, _ref2;
        if (apptools != null ? (_ref2 = apptools.sys) != null ? _ref2.drivers : void 0 : void 0) {
          amplify = apptools.sys.drivers.resolve('transport', 'amplify');
          if (amplify !== false) {
            apptools.dev.log('RPCAPI', 'Registering request procedure "' + api + '.' + name + '" with AmplifyJS.');
            resourceId = api + '.' + name;
            base_settings = {
              accepts: 'application/json',
              type: 'POST',
              dataType: 'json',
              contentType: 'application/json',
              url: _this.rpc._assembleRPCURL(name, api, null, base_uri),
              decoder: _this.rpc.decodeRPCResponse
            };
            if (config.caching != null) {
              if (config.caching === true) {
                base_settings.caching = 'persist';
              }
              return amplify.request.define(resourceId, "ajax", base_settings);
            } else {
              return amplify.request.define(resourceId, "ajax", base_settings);
            }
          }
        }
      };
    }

    return CoreRPCAPI;

  })(CoreAPI);

  RPCDriver = (function(_super) {

    __extends(RPCDriver, _super);

    RPCDriver.methods = [];

    RPCDriver["export"] = "private";

    function RPCDriver() {
      return;
    }

    return RPCDriver;

  })(CoreInterface);

  this.__apptools_preinit.abstract_base_classes.push(RPCAPI);

  this.__apptools_preinit.abstract_base_classes.push(RPCDriver);

  this.__apptools_preinit.abstract_base_classes.push(CoreRPCAPI);

  this.__apptools_preinit.abstract_base_classes.push(RPCRequest);

  this.__apptools_preinit.abstract_base_classes.push(RPCResponse);

  this.__apptools_preinit.abstract_feature_interfaces.push({
    adapter: RPCDriver,
    name: "transport"
  });

  CoreUserAPI = (function(_super) {

    __extends(CoreUserAPI, _super);

    CoreUserAPI.mount = 'user';

    CoreUserAPI.events = ['SET_USER_INFO'];

    function CoreUserAPI(apptools, window) {
      this.current_user = null;
    }

    CoreUserAPI.prototype.setUserInfo = function(userinfo) {
      this.current_user = userinfo.current_user || null;
      $.apptools.dev.log('UserAPI', 'Set server-injected userinfo: ', this.current_user);
      return $.apptools.events.trigger('SET_USER_INFO', this.current_user);
    };

    return CoreUserAPI;

  })(CoreAPI);

  this.__apptools_preinit.abstract_base_classes.push(CoreUserAPI);

  CorePushAPI = (function(_super) {

    __extends(CorePushAPI, _super);

    CorePushAPI.mount = 'push';

    CorePushAPI.events = ['PUSH_INIT', 'PUSH_READY', 'PUSH_STATE_CHANGE', 'PUSH_SOCKET_OPEN', 'PUSH_SOCKET_ESTABLISH', 'PUSH_SOCKET_ACTIVITY', 'PUSH_SOCKET_ACTIVITY_FINISH', 'PUSH_SOCKET_ERROR', 'PUSH_SOCKET_CLOSE'];

    function CorePushAPI(apptools, window) {
      var _this = this;
      this.state = {
        ready: false,
        status: 'init',
        transport: {
          sockets: [],
          channel: null
        },
        callbacks: {
          open: null,
          expect: null,
          activity: null,
          error: null,
          close: null
        },
        config: {
          token: null
        }
      };
      apptools.events.bridge(['PUSH_READY', 'PUSH_SOCKET_ESTABLISH', 'PUSH_SOCKET_ERROR', 'PUSH_SOCKET_OPEN', 'PUSH_SOCKET_CLOSE'], 'PUSH_STATE_CHANGE');
      apptools.events.hook('PUSH_SOCKET_OPEN', function() {
        var args;
        args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
        return apptools.api.rpc.alt_push_response = true;
      });
      apptools.events.hook('PUSH_SOCKET_CLOSE', function() {
        var args;
        args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
        return apptools.api.rpc.alt_push_response = false;
      });
      this.events = {
        on_open: function(socket) {
          if (_this.state.transport.sockets.length = 0) {
            _this.state.status = 'ready';
          }
          apptools.events.trigger('PUSH_SOCKET_OPEN', _this.state);
          return apptools.dev.verbose('PushSocket', 'Message transport opened.');
        },
        on_message: function(socket, payload) {
          var _base;
          _this.state.status = 'receiving';
          apptools.dev.verbose('PushSocket', 'Message received.', payload);
          apptools.events.trigger('PUSH_SOCKET_ACTIVITY', _this.state);
          if (typeof (_base = _this.state.callbacks).activity === "function") {
            _base.activity(payload);
          }
          return apptools.events.trigger('PUSH_SOCKET_ACTIVITY_FINISH', _this.state);
        },
        on_error: function(socket, error) {
          _this.state.status = 'error';
          apptools.dev.error('PushSocket', 'Message transport error.', error);
          return apptools.events.trigger('PUSH_SOCKET_ERROR', _this.state);
        },
        on_close: function(socket) {
          _this.state.ready = false;
          _this.state.status = 'close';
          apptools.dev.verbose('PushSocket', 'Message transport closed.');
          return apptools.events.trigger('PUSH_SOCKET_CLOSE', _this.state);
        }
      };
      this.internal = {
        open_channel: function(token) {
          apptools.events.trigger('PUSH_INIT', {
            token: token,
            type: 'channel'
          });
          _this.state.config.token = token;
          _this.state.transport.channel = new goog.appengine.Channel(_this.state.config.token);
          return _this.internal._add_socket(_this.state.transport.channel);
        },
        open_websocket: function(token, server) {
          apptools.events.trigger('PUSH_INIT', {
            token: token,
            server: server,
            type: 'websocket'
          });
          apptools.dev.log('Push', "WARNING: WebSockets support is currently experimental.");
          return _this.internal._add_socket(_this.state.transport.socket);
        },
        _add_socket: function(transport, callbacks) {
          var socket;
          socket = transport.open();
          _this.state.transport.sockets.push(socket);
          apptools.events.trigger('PUSH_SOCKET_ESTABLISH', socket);
          socket.onopen = function() {
            var args, _ref;
            args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
            return (_ref = _this.events).on_open.apply(_ref, [socket].concat(__slice.call(args)));
          };
          socket.onmessage = function() {
            var args, _ref;
            args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
            return (_ref = _this.events).on_message.apply(_ref, [socket].concat(__slice.call(args)));
          };
          socket.onerror = function() {
            var args, _ref;
            args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
            return (_ref = _this.events).on_error.apply(_ref, [socket].concat(__slice.call(args)));
          };
          socket.onclose = function() {
            var args, _ref;
            args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
            return (_ref = _this.events).on_close.apply(_ref, [socket].concat(__slice.call(args)));
          };
          return _this.internal;
        },
        expect: function(id, request, xhr) {
          var _ref, _ref1;
          if ((_ref = _this.state) != null) {
            if ((_ref1 = _ref.callbacks) != null) {
              if (typeof _ref1.expect === "function") {
                _ref1.expect(id, request, xhr);
              }
            }
          }
          return _this.internal;
        }
      };
      this.channel = {
        establish: function(token) {
          return _this.internal.open_channel(token);
        }
      };
      this.socket = {
        establish: function(token, host) {
          if (host == null) {
            host = null;
          }
          return _this.internal.open_websocket(token, host || apptools.config.sockets.host);
        }
      };
      this.listen = function(callbacks) {
        _this.state.callbacks = _.defaults(callbacks, _this.state.callbacks);
        _this.state.ready = true;
        return _this.internal;
      };
    }

    return CorePushAPI;

  })(CoreAPI);

  PushDriver = (function(_super) {

    __extends(PushDriver, _super);

    PushDriver.methods = [];

    PushDriver["export"] = "private";

    function PushDriver() {
      return;
    }

    return PushDriver;

  })(CoreInterface);

  this.__apptools_preinit.abstract_base_classes.push(PushDriver);

  this.__apptools_preinit.abstract_base_classes.push(CorePushAPI);

  this.__apptools_preinit.abstract_feature_interfaces.push({
    adapter: PushDriver,
    name: "transport"
  });

  CoreRenderAPI = (function(_super) {

    __extends(CoreRenderAPI, _super);

    CoreRenderAPI.mount = 'render';

    CoreRenderAPI.events = ['ADD_TEMPLATE', 'RENDER_TEMPLATE'];

    CoreRenderAPI["export"] = 'private';

    function CoreRenderAPI(apptools, window) {
      return;
    }

    CoreRenderAPI.prototype._init = function() {};

    return CoreRenderAPI;

  })(CoreAPI);

  RenderDriver = (function(_super) {

    __extends(RenderDriver, _super);

    RenderDriver["export"] = 'private';

    RenderDriver.methods = ['render', 'register_template'];

    function RenderDriver() {
      return;
    }

    return RenderDriver;

  })(CoreInterface);

  QueryDriver = (function(_super) {

    __extends(QueryDriver, _super);

    QueryDriver["export"] = 'private';

    QueryDriver.methods = ['element_by_id', 'elements_by_class'];

    function QueryDriver() {
      return;
    }

    return QueryDriver;

  })(CoreInterface);

  Template = (function(_super) {

    __extends(Template, _super);

    function Template() {
      this.name = '';
      this.source = '';
      this.cacheable = {
        rendered: false,
        source: false
      };
    }

    return Template;

  })(Model);

  this.__apptools_preinit.abstract_base_classes.push(QueryDriver);

  this.__apptools_preinit.abstract_base_classes.push(RenderDriver);

  this.__apptools_preinit.abstract_base_classes.push(CoreRenderAPI);

  this.__apptools_preinit.abstract_feature_interfaces.push({
    adapter: RenderDriver,
    name: "render"
  });

  CoreWidgetAPI = (function(_super) {

    __extends(CoreWidgetAPI, _super);

    function CoreWidgetAPI() {
      return CoreWidgetAPI.__super__.constructor.apply(this, arguments);
    }

    CoreWidgetAPI.mount = 'widget';

    CoreWidgetAPI.events = [];

    CoreWidgetAPI.prototype._init = function(apptools) {
      apptools.sys.state.add_flag('widgets');
      apptools.dev.verbose('CoreWidget', 'Widget functionality is currently stubbed.');
    };

    return CoreWidgetAPI;

  })(CoreAPI);

  CoreWidget = (function(_super) {

    __extends(CoreWidget, _super);

    function CoreWidget() {
      return CoreWidget.__super__.constructor.apply(this, arguments);
    }

    CoreWidget.prototype.animation = {
      duration: 400,
      easing: null,
      complete: null
    };

    CoreWidget.prototype.prepare_overlay = function(prefix) {
      var id, overlay;
      if (prefix == null) {
        prefix = 'apptools';
      }
      overlay = document.createElement('div');
      overlay.className = 'fixed overlay';
      overlay.setAttribute('id', prefix + '-overlay-' + (id = Math.floor(Math.random() * 1000)));
      overlay.setAttribute('data-overlay-id', id);
      overlay.style.opacity = 0;
      return overlay;
    };

    return CoreWidget;

  })(CoreObject);

  if (this.__apptools_preinit != null) {
    if (!(this.__apptools_preinit.abstract_base_classes != null)) {
      this.__apptools_preinit.abstract_base_classes = [];
    }
    if (!(this.__apptools_preinit.deferred_core_modules != null)) {
      this.__apptools_preinit.deferred_core_modules = [];
    }
  } else {
    this.__apptools_preinit = {
      abstract_base_classes: [],
      deferred_core_modules: []
    };
  }

  this.__apptools_preinit.abstract_base_classes.push(CoreWidget);

  this.__apptools_preinit.abstract_base_classes.push(CoreWidgetAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: CoreWidgetAPI
  });

  ModalAPI = (function(_super) {

    __extends(ModalAPI, _super);

    ModalAPI.mount = 'modal';

    ModalAPI.events = ['MODAL_READY', 'MODAL_API_READY'];

    function ModalAPI(apptools, widget, window) {
      var _this = this;
      this._state = {
        modals: [],
        modals_by_id: {},
        init: false
      };
      this.create = function(target, trigger) {
        var id, modal, options;
        options = target.hasAttribute('data-options') ? JSON.parse(target.getAttribute('data-options')) : {};
        modal = new Modal(target, trigger, options);
        id = modal._state.element_id;
        _this._state.modals_by_id[id] = _this._state.modals.push(modal) - 1;
        return modal._init();
      };
      this.destroy = function(modal) {
        var id;
        id = modal._state.element_id;
        _this._state.modals.splice(_this._state.modals_by_id[id], 1);
        delete _this._state.modals_by_id[id];
        document.body.removeChild(Util.get(id));
        return modal;
      };
      this.enable = function(modal) {
        var trigger;
        trigger = Util.get(modal._state.trigger_id);
        Util.bind(trigger, 'mousedown', modal.open, false);
        return modal;
      };
      this.disable = function(modal) {
        Util.unbind(Util.get(modal._state.trigger_id));
        return modal;
      };
      this.get = function(element_id) {
        return _this._state.modals_by_id[element_id] || false;
      };
      this._init = function() {
        var modal, modals, _i, _len;
        modals = Util.get('pre-modal');
        for (_i = 0, _len = modals.length; _i < _len; _i++) {
          modal = modals[_i];
          _this.enable(_this.create(modal, Util.get('a-' + modal.getAttribute('id'))));
        }
        apptools.events.trigger('MODAL_API_READY', _this);
        return _this._state.init = true;
      };
    }

    return ModalAPI;

  })(CoreWidgetAPI);

  Modal = (function(_super) {

    __extends(Modal, _super);

    function Modal(target, trigger, options) {
      var _this = this;
      this._state = {
        cached_id: target.getAttribute('id'),
        cached_html: null,
        trigger_id: trigger.getAttribute('id'),
        element_id: null,
        overlay: null,
        active: false,
        init: false,
        config: {
          initial: {
            width: '0px',
            height: '0px',
            top: window.innerHeight / 2 + 'px',
            left: window.innerHeight / 2 + 'px'
          },
          ratio: {
            x: 0.4,
            y: 0.4
          },
          template: ['<div id="modal-dialog" style="opacity: 0;" class="fixed dropshadow">', '<div id="modal-fade" style="opacity: 0">', '<div id="modal-content">&nbsp;</div>', '<div id="modal-ui" class="absolute">', '<div id="modal-title" class="absolute"></div>', '<div id="modal-close" class="absolute">X</div>', '</div>', '</div>', '</div>'].join('\n'),
          rounded: true,
          padding: null
        }
      };
      this._state.config = Util.extend(true, this._state.config, options);
      this.internal = {
        calc: function() {
          var css, dH, dW, r, wH, wW;
          css = {};
          r = _this._state.config.ratio;
          wW = window.innerWidth;
          wH = window.innerHeight;
          dW = Math.floor(r.x * wW);
          dH = Math.floor(r.y * wH);
          css.width = dW + 'px';
          css.height = dH + 'px';
          css.left = Math.floor((wW - dW) / 2);
          css.top = Math.floor((wH - dH) / 2);
          return css;
        },
        classify: function(element, method) {
          var ecl;
          if (method === 'close' || !(method != null)) {
            if (Util.in_array('dropshadow', (ecl = element.classList))) {
              ecl.remove('dropshadow');
            }
            if (Util.in_array('rounded', ecl)) {
              ecl.remove('rounded');
            }
            element.style.padding = '0px';
            return element;
          } else if (method === 'open') {
            if (!Util.in_array('dropshadow', (ecl = element.classList))) {
              ecl.add('dropshadow');
            }
            if (!Util.in_array('rounded', ecl) && _this._state.config.rounded) {
              ecl.add('rounded');
            }
            element.style.padding = '10px';
            return element;
          } else if (!(element != null)) {
            return false;
          }
        }
      };
      this.make = function() {
        var close_x, content, d, dialog, doc, fade, id, prop, range, t, template, title, ui, val, _ref;
        template = _this._state.config.template;
        range = document.createRange();
        range.selectNode(doc = document.getElementsByTagName('div').item(0));
        d = range.createContextualFragment(template);
        document.body.appendChild(d);
        dialog = Util.get('modal-dialog');
        title = Util.get('modal-title');
        content = Util.get('modal-content');
        ui = Util.get('modal-ui');
        close_x = Util.get('modal-close');
        fade = Util.get('modal-fade');
        id = _this._state.cached_id;
        dialog.classList.add(dialog.getAttribute('id'));
        dialog.setAttribute('id', id + '-modal-dialog');
        if (_this._state.config.rounded) {
          dialog.classList.add('rounded');
        }
        _ref = _this._state.config.initial;
        for (prop in _ref) {
          val = _ref[prop];
          dialog.style[prop] = val;
        }
        content.classList.add(content.getAttribute('id'));
        content.setAttribute('id', id + '-modal-content');
        content.style.height = _this.internal.calc().height;
        content.innerHTML = (t = Util.get(id)).innerHTML;
        title.classList.add(title.getAttribute('id'));
        title.setAttribute('id', id + '-modal-title');
        title.innerHTML = t.getAttribute('data-title');
        ui.classList.add(ui.getAttribute('id'));
        ui.setAttribute('id', id + '-modal-ui');
        close_x.classList.add(close_x.getAttribute('id'));
        close_x.setAttribute('id', id + '-modal-close');
        fade.classList.add(fade.getAttribute('id'));
        fade.setAttribute('id', id + '-modal-fade');
        _this._state.element_id = dialog.getAttribute('id');
        _this._state.cached_html = t.innerHTML;
        t.innerHTML = '';
        return dialog;
      };
      this.open = function() {
        var close_x, dialog, dialog_animation, fade_animation, final, id, overlay, overlay_animation;
        id = _this._state.cached_id;
        dialog = Util.get(_this._state.element_id);
        close_x = Util.get(id + '-modal-close');
        _this._state.active = true;
        overlay = _this._state.overlay || _this.prepare_overlay('modal');
        _this._state.overlay = overlay;
        if (!(overlay.parentNode != null)) {
          document.body.appendChild(overlay);
        }
        fade_animation = _this.animation;
        dialog_animation = _this.animation;
        overlay_animation = _this.animation;
        dialog_animation.complete = function() {
          _this.internal.classify(dialog, 'open');
          return $('#' + id + '-modal-fade').animate({
            opacity: 1
          }, fade_animation);
        };
        final = _this.internal.calc();
        final.opacity = 1;
        dialog.style.display = 'block';
        overlay.style.display = 'block';
        $(overlay).animate({
          opacity: 0.5
        }, overlay_animation);
        $(dialog).animate(final, dialog_animation);
        Util.bind([close_x, overlay], 'mousedown', _this.close);
        return _this;
      };
      this.close = function() {
        var d_id, dialog, id, midpoint, overlay;
        id = _this._state.cached_id;
        overlay = _this._state.overlay;
        d_id = '#' + _this._state.element_id;
        dialog = Util.get(_this._state.element_id);
        Util.unbind([Util.get(id + '-modal-close'), overlay], 'mousedown');
        midpoint = Util.extend({}, _this._state.config.initial, {
          opacity: 0.5
        });
        Util.get(id + '-modal-content').style.overflow = 'hidden';
        $('#' + id + '-modal-fade').animate({
          opacity: 0
        }, {
          duration: 300,
          complete: function() {
            _this.internal.classify(dialog, 'close');
            return $(d_id).animate(midpoint, {
              duration: 200,
              complete: function() {
                return $(d_id).animate({
                  opacity: 0
                }, {
                  duration: 250,
                  complete: function() {
                    var prop, val, _ref;
                    dialog.style.display = 'none';
                    _ref = _this._state.config.initial;
                    for (prop in _ref) {
                      val = _ref[prop];
                      dialog.style[prop] = val;
                    }
                    return $(_this._state.overlay).animate({
                      opacity: 0
                    }, {
                      duration: 300,
                      complete: function() {
                        _this._state.overlay.style.display = 'none';
                        return _this._state.active = false;
                      }
                    });
                  }
                });
              }
            });
          }
        });
        return _this;
      };
      this._init = function() {
        var dialog;
        dialog = _this.make();
        Util.get(_this._state.trigger_id).removeAttribute('href');
        _this._state.init = true;
        apptools.events.trigger('MODAL_READY', _this);
        return _this;
      };
    }

    return Modal;

  })(CoreWidget);

  this.__apptools_preinit.abstract_base_classes.push(Modal);

  this.__apptools_preinit.abstract_base_classes.push(ModalAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: ModalAPI,
    "package": 'widgets'
  });

  ScrollerAPI = (function(_super) {

    __extends(ScrollerAPI, _super);

    ScrollerAPI.mount = 'scroller';

    ScrollerAPI.events = ['SCROLLER_READY', 'SCROLLER_API_READY'];

    function ScrollerAPI(apptools, widget, window) {
      var _this = this;
      this._state = {
        scrollers: [],
        scrollers_by_id: {},
        init: false
      };
      this.internal = {
        make: function(scroller) {
          scroller = _this.create(scroller);
          console.log('CREATED SCROLLER: ', scroller);
          scroller = _this.enable(scroller);
          console.log('ENABLED SCROLLER: ', scroller);
          return scroller;
        }
      };
      this.create = function(target, options) {
        var id, scroller;
        if (options == null) {
          options = target.hasAttribute('data-options') ? JSON.parse(target.getAttribute('data-options')) : {};
        }
        scroller = new Scroller(target, options);
        id = scroller._state.element_id;
        _this._state.scrollers_by_id[id] = _this._state.scrollers.push(scroller) - 1;
        scroller._init();
        return scroller;
      };
      this.destroy = function(scroller) {
        var id;
        id = scroller._state.element_id;
        _this._state.scrollers.splice(_this._state.scrollers_by_id[id], 1);
        delete _this._state.scrollers_by_id[id];
        document.body.removeChild(Util.get(id));
        return scroller;
      };
      this.enable = function(scroller) {
        var k, v, _fn, _ref;
        _ref = scroller._state.panes;
        _fn = function(k, v) {
          console.log('[Scroller]', 'K: ', k);
          console.log('[Scroller]', 'V: ', v);
          return Util.bind(Util.get(k), 'mousedown', scroller.jump(v));
        };
        for (k in _ref) {
          v = _ref[k];
          _fn(k, v);
        }
        return scroller;
      };
      this.disable = function(scroller) {
        var k, _i, _len, _ref;
        _ref = scroller._state.panes;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          k = _ref[_i];
          Util.unbind(k, 'mousedown');
        }
        return scroller;
      };
      this._init = function() {
        var scroller, scrollers, _i, _len;
        scrollers = Util.get('pre-scroller');
        console.log('SCROLLERS: ', scrollers);
        if (!Util.is_array(scrollers)) {
          _this.internal.make(scrollers);
        } else {
          for (_i = 0, _len = scrollers.length; _i < _len; _i++) {
            scroller = scrollers[_i];
            _this.internal.make(scroller);
          }
        }
        return _this._state.init = true;
      };
    }

    return ScrollerAPI;

  })(CoreWidgetAPI);

  Scroller = (function(_super) {

    __extends(Scroller, _super);

    function Scroller(target, options) {
      var _this = this;
      this._state = {
        frame_id: target.getAttribute('id'),
        panes: {},
        current_pane: null,
        active: false,
        init: false,
        config: {
          axis: 'horizontal'
        }
      };
      this._state.config = Util.extend(true, this._state.config, options);
      this.classify = function() {
        var pane, panes, _i, _len, _results;
        target = Util.get(_this._state.frame_id);
        if (Util.in_array(target.classList, 'pre-scroller')) {
          target.classList.remove('pre-scroller');
        }
        panes = Util.get('scroller-pane', target);
        _results = [];
        for (_i = 0, _len = panes.length; _i < _len; _i++) {
          pane = panes[_i];
          _results.push((function(pane) {
            var trigger_id;
            trigger_id = 'a-' + pane.getAttribute('id');
            _this._state.panes[trigger_id] = pane;
            if (_this._state.config.axis === 'horizontal') {
              pane.classList.remove('left');
              pane.classList.remove('clear');
              pane.classList.add('in-table');
              return target.classList.add('nowrap');
            } else if (_this._state.config.axis === 'vertical') {
              target.classList.remove('nowrap');
              pane.classList.remove('in-table');
              pane.classList.add('left');
              return pane.classList.add('clear');
            }
          })(pane));
        }
        return _results;
      };
      this.jump = function(pane) {
        var animation, diff, frameO, paneO;
        _this._state.active = true;
        animation = _this.animation;
        animation.complete = function() {
          return _this._state.active = false;
        };
        _this._state.current_pane = pane.getAttribute('id');
        frameO = Util.get_offset(target);
        paneO = Util.get_offset(pane);
        if (_this._state.config.axis === 'horizontal') {
          diff = Math.floor(paneO.left - frameO.left);
          return $(target).animate({
            scrollLeft: '+=' + diff
          }, animation);
        } else if (_this._state.config.axis === 'vertical') {
          diff = Math.floor(paneO.top - frameO.left);
          return $(target).animate({
            scrollTop: '+=' + diff
          }, animation);
        }
      };
      this._init = function() {
        _this.classify();
        _this._state.init = true;
        return $.apptools.events.trigger('SCROLLER_READY', _this);
      };
    }

    return Scroller;

  })(CoreWidget);

  this.__apptools_preinit.abstract_base_classes.push(Scroller);

  this.__apptools_preinit.abstract_base_classes.push(ScrollerAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: ScrollerAPI,
    "package": 'widgets'
  });

  TabsAPI = (function(_super) {

    __extends(TabsAPI, _super);

    TabsAPI.mount = 'tabs';

    TabsAPI.events = ['TABS_READY', 'TABS_API_READY'];

    function TabsAPI(apptools, widget, window) {
      var _this = this;
      this._state = {
        tabs: [],
        tabs_by_id: {},
        init: false
      };
      this.create = function(target) {
        var id, options, tabs;
        options = target.hasAttribute('data-options') ? JSON.parse(target.getAttribute('data-options')) : {};
        tabs = new Tabs(target, options);
        id = tabs._state.element_id;
        _this._state.tabs_by_id[id] = _this._state.tabs.push(tabs) - 1;
        return tabs._init();
      };
      this.destroy = function(tabs) {
        var id;
        id = tabs._state.element_id;
        _this._state.tabs.splice(_this._state.tabs_by_id, 1);
        delete _this._state.tabs_by_id[id];
        document.body.removeChild(Util.get(id));
        return tabs;
      };
      this.enable = function(tabs) {
        var trigger;
        for (trigger in tabs._state.tabs) {
          Util.bind(Util.get(trigger), 'click', tabs["switch"], false);
        }
        return tabs;
      };
      this.disable = function(tabs) {
        var trigger;
        for (trigger in tabs._state.tabs) {
          Util.unbind(Util.get(trigger), 'click');
        }
        return tabs;
      };
      this._init = function() {
        var tabs, tabsets, _i, _len;
        tabsets = Util.get('pre-tabs');
        for (_i = 0, _len = tabsets.length; _i < _len; _i++) {
          tabs = tabsets[_i];
          _this.enable(_this.create(tabs));
        }
        apptools.events.trigger('TABS_API_READY', _this);
        return _this._state.init = true;
      };
    }

    return TabsAPI;

  })(CoreAPI);

  Tabs = (function(_super) {

    __extends(Tabs, _super);

    function Tabs(target, options) {
      var _this = this;
      this._state = {
        element_id: target.getAttribute('id'),
        active_tab: null,
        tab_count: 0,
        tabs: {},
        active: false,
        init: false,
        config: {
          rounded: true,
          width: '500px'
        }
      };
      this._state.config = Util.extend(true, this._state.config, options);
      this.internal = {
        classify: function() {
          var cls, tab, tabs, trigger, triggers, _cls, _i, _j, _k, _l, _len, _len1, _len2, _len3, _ref, _ref1;
          target = Util.get(_this._state.element_id);
          triggers = Util.get('a', target);
          tabs = Util.get('div', target);
          target.style.width = _this._state.config.width;
          _ref = ['relative', 'tabset'];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            cls = _ref[_i];
            target.classList.add(cls);
          }
          for (_j = 0, _len1 = triggers.length; _j < _len1; _j++) {
            trigger = triggers[_j];
            if (_this._state.config.rounded) {
              trigger.classList.add('tab-rounded');
            } else {
              trigger.classList.add('tab-link');
            }
          }
          for (_k = 0, _len2 = tabs.length; _k < _len2; _k++) {
            tab = tabs[_k];
            _ref1 = ['absolute', 'tab'];
            for (_l = 0, _len3 = _ref1.length; _l < _len3; _l++) {
              _cls = _ref1[_l];
              tab.classList.add(_cls);
            }
          }
          return _this;
        }
      };
      this.make = function() {
        var trigger, triggers, _fn, _i, _len;
        target = Util.get(_this._state.element_id);
        triggers = Util.get('a', target);
        _fn = function(trigger) {
          var content_div, content_id, trigger_id;
          content_div = Util.get(content_id = trigger.getAttribute('href').slice(1));
          trigger.setAttribute('id', (trigger_id = 'a-' + content_id));
          if (!(content_div != null)) {
            return false;
          } else {
            content_div.style.opacity = 0;
            content_div.classList.remove('pre-tabs');
            trigger.removeAttribute('href');
            _this._state.tabs[trigger_id] = content_id;
            return _this._state.tab_count++;
          }
        };
        for (_i = 0, _len = triggers.length; _i < _len; _i++) {
          trigger = triggers[_i];
          _fn(trigger);
        }
        return _this.internal.classify();
      };
      this["switch"] = function(e) {
        var current, currents, tabset, target_id, trigger, _at;
        console.log('event target: ' + e.target);
        _this._state.active = true;
        tabset = Util.get(_this._state.element_id);
        currents = Util.get('tab-current', tabset);
        current = currents != null ? Util.get('tab-current', tabset)[0] : ((_at = _this._state.active_tab) != null ? Util.get(_at) : false);
        target = Util.get(target_id = (trigger = e.target).getAttribute('id').split('-').splice(1).join('-'));
        console.log('TARGET_ID: ' + target_id + ' AND TARGET: ' + target);
        if (current === target) {
          return _this;
        }
        if (current === false) {
          current = Util.get('div', tabset)[0];
          current.classList.add('tab-current');
        }
        return $(current).animate({
          opacity: 0
        }, {
          duration: 200,
          complete: function() {
            current.classList.remove('tab-current');
            target.classList.add('tab-current');
            _this._state.active_tab = target_id;
            return $(target).animate({
              opacity: 1
            }, {
              duration: 300,
              complete: function() {
                return _this._state.active = false;
              }
            });
          }
        });
      };
      this._init = function() {
        var tabs;
        tabs = _this.make();
        $(Util.get('a', Util.get(_this._state.element_id))[0]).click();
        _this._state.init = true;
        apptools.events.trigger('TABS_READY', _this);
        return _this;
      };
    }

    return Tabs;

  })(CoreWidget);

  this.__apptools_preinit.abstract_base_classes.push(Tabs);

  this.__apptools_preinit.abstract_base_classes.push(TabsAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: TabsAPI,
    "package": 'widgets'
  });

  CoreAdminAPI = (function(_super) {

    __extends(CoreAdminAPI, _super);

    function CoreAdminAPI() {
      this._init = __bind(this._init, this);
      return CoreAdminAPI.__super__.constructor.apply(this, arguments);
    }

    CoreAdminAPI.mount = 'admin';

    CoreAdminAPI.events = [];

    CoreAdminAPI.prototype._init = function(apptools) {
      apptools.sys.state.add_flag('admin');
      apptools.dev.log('AdminAPI', 'NOTICE: Admin APIs are enabled.');
    };

    return CoreAdminAPI;

  })(CoreAPI);

  if (this.__apptools_preinit != null) {
    if (!(this.__apptools_preinit.abstract_base_classes != null)) {
      this.__apptools_preinit.abstract_base_classes = [];
    }
    if (!(this.__apptools_preinit.deferred_core_modules != null)) {
      this.__apptools_preinit.deferred_core_modules = [];
    }
  } else {
    this.__apptools_preinit = {
      abstract_base_classes: [],
      deferred_core_modules: []
    };
  }

  this.__apptools_preinit.abstract_base_classes.push(CoreAdminAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: CoreAdminAPI
  });

  BlogManagerAPI = (function(_super) {

    __extends(BlogManagerAPI, _super);

    BlogManagerAPI.mount = 'blog';

    BlogManagerAPI.events = [];

    function BlogManagerAPI(apptools, admin_api) {
      apptools.dev.verbose('BlogManager', 'AppToolsXMS BlogManager is currently stubbed.');
    }

    return BlogManagerAPI;

  })(CoreAdminAPI);

  this.__apptools_preinit.abstract_base_classes.push(BlogManagerAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: BlogManagerAPI,
    "package": 'admin'
  });

  PageManagerAPI = (function(_super) {

    __extends(PageManagerAPI, _super);

    PageManagerAPI.mount = 'page';

    PageManagerAPI.events = ['PAGE_EDIT', 'PAGE_SAVE', 'PAGE_META_SAVE'];

    function PageManagerAPI(apptools, admin, window) {
      apptools.dev.verbose('PageManager', 'AppToolsXMS PageManager is currently stubbed.');
    }

    return PageManagerAPI;

  })(CoreAdminAPI);

  this.__apptools_preinit.abstract_base_classes.push(PageManagerAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: PageManagerAPI,
    "package": 'admin'
  });

  SiteManagerAPI = (function(_super) {

    __extends(SiteManagerAPI, _super);

    SiteManagerAPI.mount = 'site';

    SiteManagerAPI.events = ['SITE_EDIT', 'SITE_SAVE', 'SITE_META_SAVE'];

    function SiteManagerAPI(apptools, admin, window) {
      apptools.dev.verbose('SiteManager', 'AppToolsXMS SiteManager is currently stubbed.');
    }

    return SiteManagerAPI;

  })(CoreAdminAPI);

  this.__apptools_preinit.abstract_base_classes.push(SiteManagerAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: SiteManagerAPI,
    "package": 'admin'
  });

  ContentManagerAPI = (function(_super) {

    __extends(ContentManagerAPI, _super);

    ContentManagerAPI.mount = 'content';

    ContentManagerAPI.events = [];

    function ContentManagerAPI(apptools, admin, window) {
      var change_count, editing, features, state, style_cache, that,
        _this = this;
      editing = false;
      style_cache = {};
      state = {};
      change_count = 0;
      features = {
        panel: {
          commands: {
            undo: function() {
              return document.execCommand('undo');
            },
            redo: function() {
              return document.execCommand('redo');
            },
            cut: function() {
              return document.execCommand('cut');
            },
            paste: function() {
              return document.execCommand('paste');
            },
            table: function() {
              return document.execCommand('enableInlineTableEditing');
            },
            resize: function() {
              return document.execCommand('enableObjectResizing');
            },
            clip: null,
            b: function() {
              return document.execCommand('bold');
            },
            u: function() {
              return document.execCommand('underline');
            },
            i: function() {
              return document.execCommand('italic');
            },
            clear: function() {
              return document.execCommand('removeFormat');
            },
            h1: function() {
              var t;
              t = document.selection ? document.selection() : window.getSelection();
              return document.execCommand('insertHTML', false, '<h1 class="h1">' + String(t) + '</h1>');
            },
            h2: function() {
              var t;
              t = document.selection ? document.selection() : window.getSelection();
              return document.execCommand('insertHTML', false, '<h2 class="h2">' + String(t) + '</h2>');
            },
            h3: function() {
              var t;
              t = document.selection ? document.selection() : window.getSelection();
              return document.execCommand('insertHTML', false, '<h3 class="h3">' + String(t) + '</h3>');
            },
            fontColor: function() {
              var c, t;
              t = document.selection ? document.selection() : window.getSelection();
              c = prompt('Please enter a hexidecimal color value (i.e. #ffffff)');
              c = c[0] === '#' ? c : '#' + c;
              return document.execCommand('insertHTML', false, '<span style="color:' + c + ';">' + t + '</span>');
            },
            fontSize: function() {
              var s, t;
              t = document.selection ? document.selection() : window.getSelection();
              s = prompt('Please enter desired point size (i.e. 10)');
              return document.execCommand('insertHTML', false, '<span style="font-size:' + s + 'pt;">' + t + '</span>');
            },
            fontFace: null,
            l: function() {
              return document.execCommand('justifyLeft');
            },
            r: function() {
              return document.execCommand('justifyRight');
            },
            c: function() {
              return document.execCommand('justifyCenter');
            },
            "in": function() {
              return document.execCommand('indent');
            },
            out: function() {
              return document.execCommand('outdent');
            },
            bullet: function() {
              return document.execCommand('insertUnorderedList');
            },
            number: function() {
              return document.execCommand('insertOrderedList');
            },
            indentSpecial: null,
            lineSpacing: null,
            link: function() {
              var l, t;
              t = document.selection ? document.selection() : window.getSelection();
              if (!util.is(t)) {
                t = prompt("What link text do you want to display?");
              }
              l = prompt('What URL do you want to link to?');
              return document.execCommand('insertHTML', false, '<a href="' + l + '">' + t + '</a>');
            },
            image: null,
            video: null
          },
          panel_html: ['<div id="CMS_wrap">', '<div id="CMS_panel" class="fixed panel" style="opacity: 0;">', '<div id="CMS_frame" class="nowrap">', '<div class="cms_pane" id="buttons">', '<div class="cms_subpane">', '<h1 class="cms_sp">editing</h1>', '<p>', '<button id="cms_undo" value="undo">undo</button>', '<button id="cms_redo" value="redo">redo</button>', '<button id="cms_cut" value="cut">cut</button>', '<button id="cms_paste" value="paste">paste</button>', '</p>', '</div>', '<hr/>', '<div class="cms_subpane">', '<h1 class="cms_sp">typography</h1>', '<p>', '<select id="cms_headers" class="cms">', '<option id="cms_h1" class="h1">Heading 1</option>', '<option id="cms_h2" class="h2">Heading 2</option>', '<option id="cms_h3" class="h3">Heading 3</option>', '</select>', '<button id="cms_b" value="bold">B</button>', '<button id="cms_u" value="underline">U</button>', '<button id="cms_i" value="italic">I</button>', '<button id="cms_clear" value="clear formatting">clear</button>', '<button id="cms_fontColor" value="font color">font color</button>', '<button id="cms_fontSize" value="font size">font size</button>', '</p>', '</div>', '<hr/>', '<div class="cms_subpane">', '<h1 class="cms_sp">alignment</h1>', '<p style="text-lign:center">', '<button id="cms_l" value="left">left</button>', '<button id="cms_c" value="center">center</button>', '<button id="cms_r" value="right">right</button>', '<br>', '<button id="cms_in" value="indent">&raquo;</button>', '<button id="cms_out" value="outdent">&laquo;</button>', '<br>', '<button id="cms_ul" value="unordered list">&lt;ul&gt;</button>', '<button id="cms_ol" value="ordered list">&lt;ol&gt;</button>', '</p>', '</div>', '<hr/>', '<div class="cms_subpane">', '<h1 class="cms_sp">interactive</h1>', '<p>', '<button id="cms_link" value="link">add link</button>', '</p>', '</div>', '</div>', '<div class="cms_pane" id="styles">', '<div class="cms_subpane">', '<h1 class="cms_sp">styles</h1>', '<p>MIDDLE</p>', '</div>', '</div>', '<div class="cms_pane" id="assets">', '<div class="cms_subpane">', '<h1 class="cms_sp">drop files here</h1>', '<div id="upload_wrap">', '<div id="upload" class="dragdrop">', '<span class="center-text" id="up_content">+</span>', '</div>', '</div>', '</div>', '<hr>', '<div class="cms_subpane">', '<h1 class="cms_sp">uploaded assets</h1>', '<p>', '<button id="pop_assets_button" class="pop" name="assets" value="pop out this pane!">pop me out</button>', '</p>', '</div>', '</div>', '</div>', '<div id="CMS_nav">', '<a class="scroll" href="#buttons">buttons</a>', '<a class="scroll" href="#styles">styles</a>', '<a class="scroll" href="#assets">assets</a>', '</div>', '<div id="CMS_panel_footer">&copy; momentum labs 2012</div>', '</div>', '</div>'].join('\n'),
          status_html: '<div class="fixed panel bigger" id="cms_edit_on" style="vertical-align: middle; left: -305px;top: 50px;width: 300px;text-align: right;padding-right: 10px;opacity: 0;"><span id="cms_span" style="color: #222;cursor: pointer">content editing <span style="color: green;font-weight: bold;">ON</span></span></div>',
          init: false
        },
        scroller: {
          animation: {
            duration: 500,
            easing: 'easeInOutExpo',
            complete: null
          },
          axis: 'horizontal',
          frame: 'CMS_frame',
          init: false
        },
        pop: {
          animation: {
            duration: 500,
            easing: 'easeInOutExpo',
            complete: null
          },
          position: {
            bottom: '60px',
            right: '60px'
          },
          init: false
        },
        modal: {
          animation: {
            duration: 400,
            easing: 'easeInOutExpo',
            complete: null
          },
          initial: {
            width: '0px',
            height: '0px',
            top: window.innerHeight / 2 + 'px',
            left: window.innerWidth / 2 + 'px'
          },
          ratio: {
            x: 0.4,
            y: 0.4
          },
          html: ['<div id="modal_wrap" style="opacity: 0;" class="modal_wrap">', '<div id="modal" style="opacity: 0;" class="fixed modal">', '<div id="modal_status"></div>', '<div id="modal_content">', '*****', '</div>', '<div id="modal_ui"><button id="mod-close">close</button></div>', '</div>', '</div>'].join('\n'),
          content: '<span style="font-size: 25px;margin: 10px auto;color: #5f5f5f;font-weight:bold">hello, lightbox!</span>',
          rounded: true,
          init: false
        },
        overlay: '<div id="m-overlay" class="fixed" style="opacity: 0;"></div>',
        init: false
      };
      this.config = $.extend(true, {}, features);
      this.util = {
        bind: function(obje, eve, fnc) {
          var rObj;
          rObj = {};
          rObj[eve] = fnc;
          return obje.bind(rObj);
        },
        imgPreview: function(eV) {
          var img, res;
          res = eV.target.result;
          img = document.createElement('img');
          img.classList.add('preview');
          img.src = res;
          return document.getElementById('upload').appendChild(img);
        },
        is: function(thing) {
          if ($.inArray(thing, [false, null, NaN, void 0, 0, {}, [], '', 'false', 'False', 'null', 'NaN', 'undefined', '0', 'none', 'None']) === -1) {
            return true;
          } else {
            return false;
          }
        },
        isID: function(str) {
          if (String(str).split('')[0] === '#' || document.getElementById(str) !== null) {
            return true;
          } else {
            return false;
          }
        },
        handleDrag: function(evE) {
          var eT;
          e.preventDefault();
          e.stopPropagation();
          eT = e.target;
          if (e.type === 'dragenter') {
            return $(eT).addClass('hover');
          } else if (e.type !== 'dragover') {
            return $(eT).removeClass('hover');
          }
        },
        makeDragDrop: function(elem) {
          elem.addEventListener('dragenter', _this.util.handleDrag, false);
          elem.addEventListener('dragexit', _this.util.handleDrag, false);
          elem.addEventListener('dragleave', _this.util.handleDrag, false);
          elem.addEventListener('dragover', _this.util.handleDrag, false);
          return elem.addEventListener('drop', _this.uploadAsset, false);
        },
        wrap: function(func) {
          var args;
          args = Array.prototype.slice.call(arguments, 1);
          return function() {
            return func.apply(this, args);
          };
        }
      };
      this.edit = function(o) {
        var $id, $o, offset;
        $o = $(o);
        offset = $o.offset();
        $id = $o.attr('id');
        console.log('Enabling inline editing of #' + $id);
        o.contentEditable = true;
        editing = true;
        style_cache[$id] = $o.attr('style');
        state[$id] = $o.html();
        $o.unbind('click');
        $('body').append(_this.config.overlay);
        $('#m-overlay').animate({
          'opacity': 0.75
        }, {
          duration: 400,
          easing: 'easeInOutExpo'
        });
        $o.css({
          'z-index': function() {
            var z;
            return z = 900 + Math.floor(Math.random() * 81);
          }
        });
        $o.offset(offset);
        if (!_this.util.isID('CMS_panel')) {
          _this.panel.make();
          _this.panel.live();
        }
        return $('#m-overlay').bind({
          click: _this.util.wrap(_this.save, o)
        });
      };
      this.save = function(ob) {
        var $id, $kn, $o, inHTML, that;
        $o = $(ob);
        $id = $o.attr('id');
        inHTML = $o.html();
        $kn = $o.data('snippet-keyname') ? $o.data('snippet-keyname') : 'default-key';
        that = _this;
        ob.contentEditable = false;
        editing = false;
        _this.panel.destroy();
        _this.util.bind($o, 'click', _this.util.wrap(_this.edit, ob));
        if (!_this.util.isID('CMS_sync')) {
          $('body').append('<div class="cms_message warn" id="CMS_sync" style="top: 50px;opacity: 0;"><div id="sync_loader" class="loader">syncing changes...</div></div>');
        }
        return $('#m-overlay').animate({
          'opacity': 0
        }, {
          duration: 500,
          easing: 'easeInOutExpo',
          complete: function() {
            $('#m-overlay').remove();
            if (inHTML !== state[$id]) {
              return $('#CMS_sync').animate({
                'opacity': 1
              }, {
                duration: 700,
                easing: 'easeInOutExpo',
                complete: function() {
                  change_count++;
                  return that.sync({
                    snippet_keyname: $kn,
                    inner_html: inHTML
                  });
                }
              });
            }
          }
        });
      };
      this.sync = function(snippetObj) {
        var that;
        that = _this;
        $.apptools.dev.verbose('CMS', 'Initiating sync operation for snippet.', snippetObj);
        return $.apptools.api.content.save_snippet(snippetObj).fulfill({
          success: function() {
            if (change_count - 1 === 0) {
              $('#CMS_sync').html('changes saved!');
              $('#CMS_sync').removeClass('warn').removeClass('error').addClass('yay');
              setTimeout(function() {
                return $('#CMS_sync').animate({
                  'opacity': 0
                }, {
                  duration: 500,
                  easing: 'easeInOutExpo',
                  complete: function() {
                    return $('#CMS_sync').remove();
                  }
                });
              }, 700);
              return change_count--;
            } else {
              return change_count--;
            }
          },
          failure: function(error) {
            $('#CMS_sync').html('error syncing page.');
            $('#CMS_sync').removeClass('warn').addClass('error');
            return setTimeout(function() {
              $('#CMS_sync').append('<br><a id="sync_retry" style="pointer: cursor;text-decoration: underline;">retry sync</a>');
              return that.util.bind($('#sync_retry'), 'click', that.util.wrap(that.sync, snippetObj));
            }, 1500);
          }
        });
      };
      this.revert = function(obj) {
        var _kn;
        _kn = $(obj).data('snippet-keyname');
        return $.apptools.api.content.revert_snippet({
          snippet_keyname: _kn
        }).fulfill({
          success: function() {
            $(_o).html(response.inner_html);
            $('body').append('div id="CMS_revert" class="cms_message yay" style="opacity: 0;">changes reverted!</div>');
            return $('#CMS_revert').animate({
              'opacity': 1
            }, {
              duration: 400,
              easing: 'easeInOutExpo',
              complete: function() {
                return setTimeout(function() {
                  return $('#CMS_revert').animate({
                    'opacity': 0
                  }, {
                    duration: 500,
                    easing: 'easeInOutExpo',
                    complete: function() {
                      return $('#CMS_revert').remove();
                    }
                  });
                }, 700);
              }
            });
          },
          failure: function(error) {
            $('#CMS_revert').html('error reverting page.');
            return $('#CMS_revert').removeClass('warn').addClass('error');
          }
        });
      };
      this.uploadAsset = function(e) {
        var file, files, readFile, _i, _len, _results;
        e.preventDefault();
        e.stopPropagation();
        $(e.target).removeClass('hover');
        files = e.dataTransfer.files;
        readFile = function(f) {
          var reader;
          if (f.type.match(/image.*/)) {
            reader = new FileReader();
            reader.onloadend = this.util.imgPreview;
            return reader.readAsDataURL(f);
          }
        };
        _results = [];
        for (_i = 0, _len = files.length; _i < _len; _i++) {
          file = files[_i];
          _results.push(readFile(file));
        }
        return _results;
      };
      this.placeAsset = function(ev) {};
      this.panel = {
        make: function() {
          var raw;
          raw = _this.config.panel.panel_html;
          $('body').append(raw);
          $('#CMS_panel').css({
            'bottom': '0px'
          });
          $('#CMS_wrap').css({
            'opacity': 1
          });
          return $('#CMS_panel').animate({
            'bottom': '60px',
            'opacity': 1
          }, {
            'duration': 500,
            'easing': 'easeInOutExpo'
          });
        },
        live: function() {
          var axn, bu, cmds, frame, that, up;
          cmds = _this.config.panel.commands;
          frame = _this.config.scroller.frame;
          up = document.getElementById('upload');
          that = _this;
          $('.scroll').each(function() {
            var $t, rel, t;
            t = this;
            $t = $(t);
            rel = String($t.attr('href')).slice(1);
            $t.attr('id', 'scr' + rel);
            $t.attr('href', 'javascript:void(0);');
            $('#' + frame).data('scroller', {
              axis: 'horizontal'
            });
            that.util.bind($t, 'click', that.util.wrap(that.scroller.jump, rel));
            return that.config.scroller.init = true;
          });
          _this.scroller.classify(frame);
          $('.pop').each(function() {
            var $t, rel, t;
            t = this;
            $t = $(t);
            rel = $t.attr('name');
            $t.removeAttr('name');
            $t.data('pop', {
              target: rel
            });
            that.util.bind($t, 'click', that.util.wrap(that.pop.pop, rel));
            return that.config.pop.init = true;
          });
          _this.util.makeDragDrop(up);
          for (bu in cmds) {
            axn = cmds[bu];
            _this.util.bind($('#cms_' + bu), 'click', axn);
          }
          return _this.config.panel.init = true;
        },
        die: function() {
          var _axn, _bu, _cmds, _results;
          _cmds = _this.config.panel.commands;
          _results = [];
          for (_bu in _cmds) {
            _axn = _cmds[_bu];
            _results.push($('#cms_' + _bu).unbind('click'));
          }
          return _results;
        },
        destroy: function() {
          var deep;
          $('#m-overlay').unbind();
          deep = true;
          if (editing === false) {
            return $('#CMS_panel').animate({
              'opacity': 0,
              'bottom': '0px'
            }, {
              duration: 450,
              easing: 'easeInOutExpo',
              complete: function() {
                if (deep === true) {
                  return $('#CMS_wrap').remove();
                } else {
                  return $('#CMS_wrap').css({
                    'opacity': 1
                  });
                }
              }
            });
          }
        },
        toggle: function() {
          if (_this.util.is($('#CMS_panel'))) {
            _this.panel.destroy;
            return $('#cms_span').html('&gt;');
          } else {
            _this.panel.make();
            _this.panel.live();
            return $('#cms_span').html('x');
          }
        }
      };
      this.scroller = {
        classify: function(ctx) {
          var $c, $d;
          $c = $('#' + ctx);
          $d = $c.data('scroller');
          if (($d.axis === 'horizontal') || !_this.util.is($d.axis)) {
            $('.cms_pane').removeClass('left').removeClass('clear').addClass('in-table');
            return $c.addClass('nowrap');
          } else if ($d.axis === 'vertical') {
            $c.removeClass('nowrap');
            return $('.cms_pane').removeClass('in-table').addClass('left').addClass('clear');
          }
        },
        jump: function(reL, cback, eVent) {
          var $d, $f, anim, diff, f_o, r_o;
          if (_this.util.is(e)) {
            e.preventDefault();
            e.stopPropagation();
          }
          $f = $('#' + _this.config.scroller.frame);
          $d = $f.data('scroller');
          anim = _this.util.is(cback) ? $.extend({}, _this.config.scroller.animation, {
            complete: cback
          }) : _this.config.scroller.animation;
          f_o = $f.offset();
          r_o = $('#' + reL).offset();
          if ($d.axis === 'vertical') {
            diff = Math.floor(r_o.top - f_o.top);
            return $f.animate({
              scrollTop: '+=' + diff
            }, anim);
          } else if ($d.axis === 'horizontal') {
            diff = Math.floor(r_o.left - f_o.left);
            return $f.animate({
              scrollLeft: '+=' + diff
            }, anim);
          }
        }
      };
      this.pop = {
        pop: function(iD) {
          var $t, anim, biD, pHTML, piD, popped, pos, prevSib, that;
          that = _this;
          $t = $('#' + iD);
          piD = 'pop_' + iD;
          biD = piD + '_button';
          pos = _this.config.pop.position;
          pHTML = $t.html();
          prevSib = $t.prev().attr('id');
          $b.unbind('click');
          anim = $.extend({}, _this.config.pop.animation, {
            complete: function() {
              $t.remove();
              $('#' + biD).html('pop back in');
              that.util.bind($('#' + biD), 'click', that.util.wrap(that.pop.reset, iD, 'CMS_frame'));
              return that.util.makeDragDrop(document.getElementById('upload'));
            }
          });
          popped = '<div id="' + piD + '" class="fixed panel" style="opacity:0;">' + pHTML + '</div>';
          $('body').append(popped);
          $('#' + piD).css({
            'bottom': '0px',
            'right': pos.right,
            'z-index': 989
          });
          $('#' + piD).animate({
            'bottom': pos.bottom,
            'opacity': 1
          }, anim);
          return _this.scroller.jump(prevSib);
        },
        reset: function(id, tid) {
          var $tar, anim, bid, pid, that;
          if (tid === false || !_this.util.is(tid)) {
            return $('#pop_' + id).remove();
          } else {
            that = _this;
            pid = 'pop_' + iD;
            $tar = $('#' + tid);
            bid = pid + '_button';
            $(bid).unbind('click');
            return anim = $.extend({}, _this.config.pop.animation, {
              complete: function() {
                $('#' + pid).remove();
                $('#' + bid).html('pop me out');
                that.util.bind($('#' + bid), 'click', that.util.wrap(that.pop.pop, id));
                return that.util.makeDragDrop(document.getElementById('upload'));
              }
            });
          }
        }
      };
      this.modal = {
        show: function(rEL, rELHTML, callBack) {
          var modalCSS, modalHTML, modalHeight, modalWidth, _anim, _html;
          modalCSS = {
            opacity: 1
          };
          _anim = this.util.is(callBack) ? $.extend({}, this.config.modal.animation, {
            complete: callBack
          }) : this.config.modal.animation;
          _html = this.config.modal.html.split('*****');
          modalHTML = _html[0] + rELHTML + _html[1];
          modalWidth = Math.floor(this.config.modal.ratio.x * window.innerWidth);
          modalHeight = Math.floor(this.config.modal.ratio.y * window.innerHeight);
          modalCSS.width = modalWidth + 'px';
          modalCSS.height = modalHeight + 'px';
          modalCSS.top = Math.floor((window.innerHeight - modalHeight) / 2);
          modalCSS.left = Math.floor((window.innerWidth - modalWidth) / 2);
          $('body').append(this.config.overlay);
          $('#m-overlay').animate({
            opacity: 0.5
          }, {
            duration: 400,
            easing: 'easeInOutExpo',
            complete: function() {
              return this.util.bind($('#m-overlay'), 'click', this.modal.hide);
            }
          });
          $('body').append(modalHTML);
          $('#modal-wrap').css({
            opacity: 1
          });
          if (this.config.modal.rounded) {
            $('#modal').addClass('rounded');
          }
          $('#modal').css(this.config.modal.initial);
          $('#modal').animate(modalCSS, _anim);
          return this.util.bind($('#mod-close'), 'click', this.modal.hide);
        },
        hide: function() {
          var $id, _end;
          $id = $('#modal');
          _end = $.extend({}, this.config.modal.initial, {
            left: 0 + 'px',
            width: window.innerWidth,
            right: 0 + 'px',
            opacity: 0.5
          });
          setTimeout(function() {
            $id.removeClass('rounded');
            return $id.css({
              padding: 0
            });
          }, 150);
          return $id.animate(_end, {
            duration: 400,
            easing: 'easeInOutExpo',
            complete: function() {
              $id.animate({
                opacity: 0
              }, {
                duration: 250,
                easing: 'easeInOutExpo'
              });
              return $('#m-overlay').animate({
                opacity: 0
              }, {
                duration: 500,
                easing: 'easeInOutExpo',
                complete: function() {
                  $('#m-overlay').remove();
                  return $('#modal_wrap').remove();
                }
              });
            }
          });
        }
      };
      apptools.dev.verbose('CMS', 'Initializing Momentum extensible management system...');
      that = this;
      $('body').append(this.config.panel.status_html);
      setTimeout(function() {
        $('#cms_span').animate({
          'opacity': 1
        }, {
          duration: 450,
          easing: 'easeInOutExpo'
        });
        return $('#cms_edit_on').animate({
          'opacity': 1,
          'left': '-155px'
        }, {
          duration: 400,
          easing: 'easeInOutExpo',
          complete: function() {
            return setTimeout(function() {
              return $('#cms_edit_on').animate({
                'left': '-290px'
              }, {
                duration: 400,
                easing: 'easeInOutExpo',
                complete: function() {
                  that.util.bind($('#cms_edit_on'), 'click', that.panel.toggle);
                  return that.panel.toggle();
                }
              });
            }, 1750);
          }
        });
      }, 500);
      $('.editable').each(function(){
            var t = this;
            that.util.bind($(t), 'click', that.util.wrap(that.edit, t));
        });;

    }

    return ContentManagerAPI;

  })(CoreAdminAPI);

  this.__apptools_preinit.abstract_base_classes.push(ContentManagerAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: ContentManagerAPI,
    "package": 'admin'
  });

  AppTools = (function() {

    AppTools.version = {
      major: 0,
      minor: 1,
      micro: 4,
      build: 4282012,
      release: "BETA",
      get: function() {
        return [[[this.major.toString(), this.minor.toString(), this.micro.toString()].join('.'), this.build.toString()].join('-'), this.release].join(' ');
      }
    };

    function AppTools(window) {
      var module, _i, _len, _ref, _ref1,
        _this = this;
      this.config = {
        rpc: {
          base_uri: '/_api/rpc',
          host: null,
          enabled: true
        },
        sockets: {
          host: null,
          enabled: false
        }
      };
      this.lib = {};
      this.sys = {
        platform: {},
        version: this.version,
        core_events: ['SYS_MODULE_LOADED', 'SYS_LIB_LOADED', 'SYS_DRIVER_LOADED'],
        state: {
          status: 'NOT_READY',
          flags: ['base'],
          preinit: {},
          modules: {},
          classes: {},
          interfaces: {},
          integrations: [],
          add_flag: function(flagname) {
            return this.sys.flags.push(flagname);
          },
          consider_preinit: function(preinit) {
            var cls, lib, _i, _interface, _j, _k, _len, _len1, _len2, _ref, _ref1, _ref2;
            if (preinit.abstract_base_classes != null) {
              _ref = preinit.abstract_base_classes;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                cls = _ref[_i];
                _this.sys.state.classes[cls.name] = cls;
                if ((cls["package"] != null) && (_this.sys.state.modules[cls["package"]] != null)) {
                  _this.sys.state.modules[cls["package"]].classes[cls.name] = cls;
                }
                if ((cls["export"] != null) && cls["export"] === 'private') {
                  continue;
                } else {
                  window[cls.name] = cls;
                }
              }
            }
            if (preinit.deferred_library_integrations != null) {
              _ref1 = preinit.deferred_library_integrations;
              for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
                lib = _ref1[_j];
                _this.sys.libraries.install(lib.name, lib.library);
              }
            }
            if (preinit.abstract_feature_interfaces != null) {
              _ref2 = preinit.abstract_feature_interfaces;
              for (_k = 0, _len2 = _ref2.length; _k < _len2; _k++) {
                _interface = _ref2[_k];
                _this.sys.interfaces.install(_interface.name, _interface.adapter);
              }
            }
            return preinit;
          }
        },
        modules: {
          install: function(module, mountpoint_or_callback, callback) {
            var module_name, mountpoint, pass_parent, target_mod;
            if (mountpoint_or_callback == null) {
              mountpoint_or_callback = null;
            }
            if (callback == null) {
              callback = null;
            }
            if (mountpoint_or_callback != null) {
              if (typeof mountpoint_or_callback === 'function') {
                callback = mountpoint_or_callback;
                mountpoint = null;
              } else {
                mountpoint = mountpoint_or_callback;
              }
            }
            if (mountpoint != null) {
              if (!(_this[mountpoint] != null)) {
                _this[mountpoint] = {};
              }
              mountpoint = _this[mountpoint];
              pass_parent = true;
            } else {
              mountpoint = _this;
              pass_parent = false;
            }
            if (module.mount != null) {
              module_name = module.mount;
            } else {
              module_name = module.name.toLowerCase();
            }
            if ((module.events != null) && (_this.events != null)) {
              _this.events.register(module.events);
            }
            if (!(mountpoint[module_name] != null)) {
              if (pass_parent) {
                target_mod = mountpoint[module_name] = new module(_this, mountpoint, window);
                _this.sys.state.modules[module_name] = {
                  module: target_mod,
                  classes: {}
                };
              } else {
                target_mod = mountpoint[module_name] = new module(_this, window);
                _this.sys.state.modules[module_name] = {
                  module: target_mod,
                  classes: {}
                };
              }
            }
            if (module._init != null) {
              module._init(_this);
            }
            if ((_this.dev != null) && (_this.dev.verbose != null)) {
              _this.dev.verbose('ModuleLoader', 'Installed module:', target_mod, ' at mountpoint: ', mountpoint, ' under the name: ', module_name);
            }
            if (_this.events != null) {
              _this.events.trigger('SYS_MODULE_LOADED', {
                module: target_mod,
                mountpoint: mountpoint
              });
            }
            if (callback != null) {
              callback(target_mod);
            }
            return target_mod;
          }
        },
        libraries: {
          install: function(name, library, callback) {
            if (callback == null) {
              callback = null;
            }
            _this.lib[name.toLowerCase()] = library;
            _this.sys.state.integrations.push(name.toLowerCase());
            _this.dev.verbose('LibLoader', name + ' detected.');
            _this.events.trigger('SYS_LIB_LOADED', {
              name: name,
              library: library
            });
            if (callback != null) {
              callback(library, name);
            }
            return _this.lib[name.toLowerCase()];
          },
          resolve: function(name) {
            var lib, _i, _len, _ref;
            name = name.toLowerCase();
            _ref = _this.sys.state.integrations;
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              lib = _ref[_i];
              if (lib !== name) {
                continue;
              } else {
                return _this.lib[name.toLowerCase()];
              }
            }
          }
        },
        interfaces: {
          install: function(name, adapter) {
            _this.dev.verbose('InterfaceLoader', 'Installed "' + name + '" interface.');
            _this.events.trigger('SYS_INTERFACE_LOADED', {
              name: name,
              adapter: adapter
            });
            _this.sys.state.interfaces[name] = {
              adapter: adapter,
              methods: adapter.methods
            };
            return _this.sys.state.interfaces[name];
          },
          resolve: function(name) {
            if (_this.sys.state.interfaces[name] != null) {
              return _this.sys.state.interfaces[name];
            } else {
              return false;
            }
          }
        },
        drivers: {
          query: {},
          loader: {},
          transport: {},
          storage: {},
          render: {},
          install: function(type, name, adapter, mountpoint, enabled, priority, callback) {
            if (callback == null) {
              callback = null;
            }
            _this.sys.drivers[type][name] = {
              name: name,
              driver: mountpoint,
              enabled: enabled,
              priority: priority,
              "interface": adapter
            };
            if (callback != null) {
              callback(_this.sys.drivers[type][name].driver);
            }
            _this.events.trigger('SYS_DRIVER_LOADED', _this.sys.drivers[type][name]);
            return _this.sys.drivers[type][name];
          },
          resolve: function(type, name, strict) {
            var driver, priority_state, selected_driver;
            if (name == null) {
              name = null;
            }
            if (strict == null) {
              strict = false;
            }
            if (!(_this.sys.drivers[type] != null)) {
              apptools.dev.critical('CORE', 'Unkown driver type "' + type + '".');
              return;
            } else {
              if (name != null) {
                if (_this.sys.drivers[type][name] != null) {
                  return _this.sys.drivers[type][name].driver;
                } else {
                  if (strict) {
                    apptools.dev.critical('CORE', 'Could not resolve driver ', name, ' of type ', type, '.');
                  }
                }
                return false;
              }
            }
            priority_state = -1;
            selected_driver = false;
            for (driver in _this.sys.drivers[type]) {
              driver = _this.sys.drivers[type][driver];
              if (driver.priority > priority_state) {
                selected_driver = driver;
                break;
              }
            }
            return selected_driver;
          }
        },
        go: function() {
          _this.dev.log('Core', 'All systems go.');
          _this.sys.state.status = 'READY';
          return _this;
        }
      };
      this.sys.modules.install(CoreDevAPI, function(dev) {
        return dev.verbose('CORE', 'CoreDevAPI is up and running.');
      });
      this.sys.modules.install(CoreEventsAPI, function(events) {
        return events.register(_this.sys.core_events);
      });
      if (window.__apptools_preinit != null) {
        this.sys.state.preinit = window.__apptools_preinit;
        this.sys.state.consider_preinit(window.__apptools_preinit);
      }
      if ((window != null ? window.Modernizr : void 0) != null) {
        this.sys.libraries.install('Modernizr', window.Modernizr, function(lib, name) {
          return _this.load = function() {
            var fragments, _ref;
            fragments = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
            return (_ref = _this.lib.modernizr).load.apply(_ref, fragments);
          };
        });
      }
      if ((window != null ? window.jQuery : void 0) != null) {
        this.sys.libraries.install('jQuery', window.jQuery, function(lib, name) {
          _this.sys.drivers.install('query', 'jquery', _this.sys.state.classes.QueryDriver, _this.lib.jquery, true, 100, null);
          return _this.sys.drivers.install('transport', 'jquery', _this.sys.state.classes.RPCDriver, _this.lib.jquery, true, 100, null);
        });
      }
      if ((window != null ? window.Zepto : void 0) != null) {
        this.sys.libraries.install('Zepto', window.Zepto, function(lib, name) {
          _this.sys.drivers.install('query', 'zepto', _this.sys.state.classes.QueryDriver, _this.lib.zepto, true, 500, null);
          return _this.sys.drivers.install('transport', 'zepto', _this.sys.state.classes.RPCDriver, _this.lib.zepto, true, 500, null);
        });
      }
      if ((window != null ? window._ : void 0) != null) {
        this.sys.libraries.install('Underscore', window._, function(lib, name) {
          _this.sys.drivers.install('query', 'underscore', _this.sys.state.classes.QueryDriver, _this.lib.underscore, true, 50, null);
          return _this.sys.drivers.install('render', 'underscore', _this.sys.state.classes.RenderDriver, _this.lib.underscore, true, 50, null);
        });
      }
      if ((window != null ? window.Backbone : void 0) != null) {
        this.sys.libraries.install('Backbone', window.Backbone);
      }
      if ((window != null ? window.Lawnchair : void 0) != null) {
        this.sys.libraries.install('Lawnchair', window.Lawnchair, function(library) {
          return _this.sys.drivers.install('storage', 'lawnchair', _this.sys.state.classes.StorageDriver, _this.lib.lawnchair, true, 500, function(lawnchair) {
            return _this.dev.verbose('Lawnchair', 'Storage is currently stubbed. Come back later.');
          });
        });
      }
      if ((window != null ? window.amplify : void 0) != null) {
        this.sys.libraries.install('Amplify', window.amplify, function(library) {
          _this.sys.drivers.register('transport', 'amplify', _this.sys.state.classes.RPCDriver, _this.lib.amplify, true, 500, null);
          return _this.sys.drivers.register('storage', 'amplify', _this.sys.state.classes.StorageDriver, _this.lib.amplify, true, 100, null);
        });
      }
      if ((window != null ? window.Milk : void 0) != null) {
        this.sys.libraries.install('Milk', window.Milk, function(library) {
          return _this.sys.drivers.install('render', 'milk', _this.sys.state.classes.RenderDriver, _this.lib.milk, true, 100, function(milk) {
            return _this.dev.verbose('Milk', 'Render support is currently stubbed. Come back later.');
          });
        });
      }
      if ((window != null ? window.Mustache : void 0) != null) {
        this.sys.libraries.install('Mustache', window.Mustache, function(library) {
          return _this.sys.drivers.register('render', 'mustache', _this.sys.state.classes.RenderDriver, _this.lib.mustache, true, 500, function(mustache) {
            return _this.dev.verbose('Mustache', 'Render support is currently stubbed. Come back later.');
          });
        });
      }
      this.sys.modules.install(CoreModelAPI);
      this.sys.modules.install(CoreAgentAPI);
      this.sys.modules.install(CoreDispatchAPI);
      this.sys.modules.install(CoreRPCAPI);
      this.sys.modules.install(CorePushAPI);
      this.sys.modules.install(CoreUserAPI);
      this.sys.modules.install(CoreStorageAPI);
      this.sys.modules.install(CoreRenderAPI);
      if (((_ref = window.__apptools_preinit) != null ? _ref.deferred_core_modules : void 0) != null) {
        _ref1 = window.__apptools_preinit.deferred_core_modules;
        for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
          module = _ref1[_i];
          if (module["package"] != null) {
            this.sys.modules.install(module.module, module["package"]);
          } else {
            this.sys.modules.install(module.module);
          }
        }
      }
      return this.sys.go();
    }

    return AppTools;

  })();

  window.AppTools = AppTools;

  window.apptools = new AppTools(window);

  if (window.jQuery != null) {
    $.extend({
      apptools: window.apptools
    });
  } else {
    window.$ = function(id) {
      return document.getElementById(id);
    };
    window.$.apptools = window.apptools;
  }

}).call(this);
