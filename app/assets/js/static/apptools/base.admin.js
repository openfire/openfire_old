(function() {
  var Accordion, AccordionAPI, AppException, AppTools, AppToolsCollection, AppToolsException, AppToolsModel, AppToolsRouter, AppToolsView, ArrayBufferUploader, BinaryUploader, BlogManagerAPI, ContentManagerAPI, CoreAPI, CoreAdminAPI, CoreAgentAPI, CoreDevAPI, CoreDispatchAPI, CoreEventsAPI, CoreException, CoreInterface, CoreModelAPI, CoreObject, CorePushAPI, CoreRPCAPI, CoreRenderAPI, CoreStorageAPI, CoreUserAPI, CoreWidget, CoreWidgetAPI, DataURLUploader, Editor, EditorAPI, Expand, Find, IndexedDBDriver, IndexedDBEngine, KeyEncoder, LocalStorageDriver, LocalStorageEngine, Milk, Modal, ModalAPI, Model, PageManagerAPI, Parse, PushDriver, QueryDriver, RPCAPI, RPCDriver, RPCRequest, RPCResponse, RenderDriver, Scroller, ScrollerAPI, SessionStorageDriver, SessionStorageEngine, SimpleKeyEncoder, SiteManagerAPI, Sticky, StickyAPI, StorageAdapter, StorageDriver, Tabs, TabsAPI, Template, TemplateCache, Uploader, UploaderAPI, Util, WebSQLDriver, WebSQLEngine, _simple_key_encoder,
    __slice = Array.prototype.slice,
    __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; },
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __indexOf = Array.prototype.indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; },
    _this = this;

  this.__apptools_preinit = {};

  TemplateCache = {};

  Find = function(name, stack, value) {
    var ctx, i, part, parts, _i, _len, _ref, _ref2;
    if (value == null) value = null;
    if (name === '.') return stack[stack.length - 1];
    _ref = name.split(/\./), name = _ref[0], parts = 2 <= _ref.length ? __slice.call(_ref, 1) : [];
    for (i = _ref2 = stack.length - 1; _ref2 <= -1 ? i < -1 : i > -1; _ref2 <= -1 ? i++ : i--) {
      if (stack[i] == null) continue;
      if (!(typeof stack[i] === 'object' && name in (ctx = stack[i]))) continue;
      value = ctx[name];
      break;
    }
    for (_i = 0, _len = parts.length; _i < _len; _i++) {
      part = parts[_i];
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
    var BuildRegex, buffer, buildInterpolationTag, buildInvertedSectionTag, buildPartialTag, buildSectionTag, cache, content, contentEnd, d, error, escape, isStandalone, match, name, parseError, pos, sectionInfo, tag, tagPattern, tmpl, type, whitespace, _name, _ref, _ref2, _ref3;
    if (delimiters == null) delimiters = ['{{', '}}'];
    if (section == null) section = null;
    cache = (TemplateCache[_name = delimiters.join(' ')] || (TemplateCache[_name] = {}));
    if (template in cache) return cache[template];
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
      isStandalone = (contentEnd === -1 || template.charAt(contentEnd) === '\n') && ((_ref2 = template.charAt(pos)) === (void 0) || _ref2 === '' || _ref2 === '\r' || _ref2 === '\n');
      if (content) {
        buffer.push((function(content) {
          return function() {
            return content;
          };
        })(content));
      }
      if (isStandalone && (type !== '' && type !== '&' && type !== '{')) {
        if (template.charAt(pos) === '\r') pos += 1;
        if (template.charAt(pos) === '\n') pos += 1;
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
              var value, _ref3;
              if ((value = (_ref3 = Find(name, context)) != null ? _ref3 : '') instanceof Function) {
                value = Expand.apply(null, [this, Parse("" + (value()))].concat(__slice.call(arguments)));
              }
              if (!is_unescaped) value = this.escape("" + value);
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
              if (indentation) partial = partial.replace(/^(?=.)/gm, indentation);
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
          _ref3 = Parse(template, delimiters, sectionInfo), tmpl = _ref3[0], pos = _ref3[1];
          sectionInfo['#'] = buildSectionTag = function(name, delims, raw) {
            return function(context) {
              var parsed, result, v, value;
              value = Find(name, context) || [];
              tmpl = value instanceof Function ? value(raw) : raw;
              if (!(value instanceof Array)) value = [value];
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
              if (!(value instanceof Array)) value = [1];
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
          if (error) throw parseError(tagPattern.lastIndex, error);
          template = template.slice(section.start, contentEnd + 1 || 9e9);
          cache[template] = buffer;
          return [template, pos];
        case '=':
          if ((delimiters = tag.split(/\s+/)).length !== 2) {
            error = "Set Delimiters tags should have two and only two values!";
          }
          if (error) throw parseError(tagPattern.lastIndex, error);
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
    if (section != null) throw section.error;
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
      if (partials == null) partials = null;
      if (!((partials || (partials = this.partials || {})) instanceof Function)) {
        partials = (function(partials) {
          return function(name) {
            if (!(name in partials)) throw "Unknown partial '" + name + "'!";
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
      AppException.__super__.constructor.apply(this, arguments);
    }

    AppException.prototype.toString = function() {
      return '[' + this.module + '] AppException: ' + this.message;
    };

    return AppException;

  })(CoreException);

  AppToolsException = (function(_super) {

    __extends(AppToolsException, _super);

    function AppToolsException() {
      AppToolsException.__super__.constructor.apply(this, arguments);
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
        AppToolsView.__super__.constructor.apply(this, arguments);
      }

      return AppToolsView;

    })(Backbone.View);
    AppToolsModel = (function(_super) {

      __extends(AppToolsModel, _super);

      function AppToolsModel() {
        AppToolsModel.__super__.constructor.apply(this, arguments);
      }

      return AppToolsModel;

    })(Backbone.Model);
    AppToolsRouter = (function(_super) {

      __extends(AppToolsRouter, _super);

      function AppToolsRouter() {
        AppToolsRouter.__super__.constructor.apply(this, arguments);
      }

      return AppToolsRouter;

    })(Backbone.Router);
    AppToolsCollection = (function(_super) {

      __extends(AppToolsCollection, _super);

      function AppToolsCollection() {
        AppToolsCollection.__super__.constructor.apply(this, arguments);
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

    Util.prototype.is_body = function(object) {
      return this.is_object(object) && (Object.prototype.toString.call(object) === '[object HTMLBodyElement]' || object.constructor.name === 'HTMLBodyElement');
    };

    Util.prototype.is_array = Array.isArray || function(object) {
      return typeof object === 'array' || Object.prototype.toString.call(object) === '[object Array]' || object.constructor.name === 'Array';
    };

    Util.prototype.in_array = function(item, array) {
      var it, matches, _fn, _i, _len,
        _this = this;
      if (array.indexOf != null) return !!~array.indexOf(item);
      matches = [];
      _fn = function(it) {
        if (it === item) return matches.push(it);
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
      return array;
    };

    Util.prototype.filter = function(array, condition) {
      var item, new_array, _i, _len;
      new_array = [];
      for (_i = 0, _len = array.length; _i < _len; _i++) {
        item = array[_i];
        if (condition(item)) new_array.push(item);
      }
      return new_array;
    };

    Util.prototype.sort = null;

    Util.prototype.create_element_string = function(tag, attrs, separator, ext) {
      var el_str, k, no_close, v;
      if (separator == null) separator = '*';
      no_close = ['area', 'base', 'basefont', 'br', 'col', 'frame', 'hr', 'img', 'input', 'link'];
      tag = tag.toLowerCase();
      el_str = '<' + tag;
      for (k in attrs) {
        v = attrs[k];
        el_str += ' ' + k + '="' + v + '"';
      }
      if (ext != null) el_str += ' ' + ext;
      el_str += '>';
      if (!this.in_array(tag, no_close)) el_str += separator + '</' + tag + '>';
      return el_str;
    };

    Util.prototype.create_doc_frag = function(html_string) {
      var frag, range;
      range = document.createRange();
      range.selectNode(document.getElementsByTagName('div').item(0));
      frag = range.createContextualFragment(html_string);
      return frag;
    };

    Util.prototype.add = function(element_type, attrs, parent_node) {
      var node_id, q_name,
        _this = this;
      if (!(element_type != null) || !this.is_object(attrs)) return false;
      q_name = this.is_body(parent_node) || !(parent_node != null) || !(node_id = parent_node.getAttribute('id')) ? 'dom' : node_id;
      if (!(this._state.queues[q_name] != null)) this.internal.queues.add(q_name);
      this._state.queues[q_name].push([element_type, attrs]);
      return this.internal.queues.go(q_name, function(response) {
        var args, dfrag, html, parent, q, _i, _len;
        q = response.queue;
        parent = response.name === 'dom' ? document.body : _this.get(response.name);
        html = [];
        for (_i = 0, _len = q.length; _i < _len; _i++) {
          args = q[_i];
          html.push(_this.create_element_string.apply(_this, args));
        }
        dfrag = _this.create_doc_frag(html.join(''));
        return parent.appendChild(dfrag);
      });
    };

    Util.prototype.remove = function(node) {
      return node.parentNode.removeChild(node);
    };

    Util.prototype.get = function(query, node) {
      var cls, id, tg;
      if (node == null) node = document;
      if (!(query != null)) return null;
      if (query.nodeType) return query;
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
        if (!(elem = elem.offsetParent)) break;
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
      if (str.charAt(0) === '#') return true;
      if (document.getElementById(str) !== null) return true;
      return false;
    };

    Util.prototype.bind = function(element, event, fn, prop) {
      var el, ev, evt, func, _i, _j, _len, _len2, _results, _results2, _results3;
      if (prop == null) prop = false;
      if (!(element != null)) return false;
      if (this.is_array(element)) {
        _results = [];
        for (_i = 0, _len = element.length; _i < _len; _i++) {
          el = element[_i];
          _results.push(this.bind(el, event, fn, prop));
        }
        return _results;
      } else if (this.is_array(event)) {
        _results2 = [];
        for (_j = 0, _len2 = event.length; _j < _len2; _j++) {
          evt = event[_j];
          _results2.push(this.bind(element, evt, fn, prop));
        }
        return _results2;
      } else if (this.is_raw_object(event)) {
        _results3 = [];
        for (ev in event) {
          func = event[ev];
          _results3.push(this.bind(element, ev, func, prop));
        }
        return _results3;
      } else {
        return element.addEventListener(event, fn, prop);
      }
    };

    Util.prototype.unbind = function(element, event) {
      var el, ev, _i, _j, _len, _len2, _results, _results2, _results3;
      if (!(element != null)) return false;
      if (this.is_array(element)) {
        _results = [];
        for (_i = 0, _len = element.length; _i < _len; _i++) {
          el = element[_i];
          _results.push(this.unbind(el, event));
        }
        return _results;
      } else if (this.is_array(event)) {
        _results2 = [];
        for (_j = 0, _len2 = event.length; _j < _len2; _j++) {
          ev = event[_j];
          _results2.push(this.unbind(element, ev));
        }
        return _results2;
      } else if (this.is_raw_object(element)) {
        _results3 = [];
        for (el in element) {
          ev = element[el];
          _results3.push(this.unbind(el, ev));
        }
        return _results3;
      } else if (element.constructor.name === 'NodeList') {
        return this.unbind(this.to_array(element), event);
      } else {
        return element.removeEventListener(event);
      }
    };

    Util.prototype.block = function(async_method, object) {
      var result, _done;
      if (object == null) object = {};
      console.log('[Util] Enforcing blocking at user request... :(');
      _done = false;
      result = null;
      async_method(object, function(x) {
        result = x;
        return _done = true;
      });
      while (true) {
        if (_done !== false) break;
      }
      return result;
    };

    Util.prototype.now = function() {
      return +new Date();
    };

    Util.prototype.timestamp = function(d) {
      if (d == null) d = new Date();
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
      var last, timer_id,
        _this = this;
      timer_id = null;
      last = 0;
      return function() {
        var args, clear, elapsed, go;
        args = arguments;
        elapsed = _this.now() - last;
        clear = function() {
          go();
          return timer_id = null;
        };
        go = function() {
          last = _this.now();
          return fn.apply(_this, args);
        };
        if (prefire && !timer_id) go();
        if (!!timer_id) clearTimeout(timer_id);
        if (!(prefire != null) && elapsed >= buffer) {
          return go();
        } else {
          return timer_id = setTimeout((prefire ? clear : go), !(prefire != null) ? buffer - elapsed : buffer);
        }
      };
    };

    Util.prototype.debounce = function(fn, buffer, prefire) {
      if (buffer == null) buffer = 200;
      if (prefire == null) prefire = false;
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
      if (!this.is_object(target) && !this.is_function(target)) target = {};
      args = Array.prototype.slice.call(arguments, i);
      _fn = function(arg) {
        var a, clone, copied_src, o, option, options, src, value, _results;
        options = arg;
        _results = [];
        for (option in options) {
          if (!__hasProp.call(options, option)) continue;
          value = options[option];
          if (target === value) continue;
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
      this.remove = __bind(this.remove, this);
      this.add = __bind(this.add, this);
      this.create_doc_frag = __bind(this.create_doc_frag, this);
      this.create_element_string = __bind(this.create_element_string, this);
      this.filter = __bind(this.filter, this);
      this.to_array = __bind(this.to_array, this);
      this.in_array = __bind(this.in_array, this);
      this.is_body = __bind(this.is_body, this);
      this.is_empty_object = __bind(this.is_empty_object, this);
      this.is_raw_object = __bind(this.is_raw_object, this);
      this.is_object = __bind(this.is_object, this);
      this.is_function = __bind(this.is_function, this);
      this.is = __bind(this.is, this);
      var _this = this;
      this._state = {
        active: null,
        queues: {
          fx: [],
          dom: [],
          handlers: {}
        }
      };
      this.internal = {
        queues: {
          add: function(name, callback) {
            _this._state.queues[name] = [];
            return _this._state.queues.handlers[name] = _this.debounce(function(n, c) {
              return _this.internal.queues.process(n, c);
            }, _this.prep_animation().duration, true);
          },
          remove: function(name, callback) {
            var handler, q;
            handler = _this._state.queues.handlers[name];
            delete _this._state.queues.handlers[name];
            q = _this._state.queues[name];
            delete _this._state.queues[name];
            if (q.length > 0) {
              return {
                queue: q,
                handler: handler
              };
            } else {
              return true;
            }
          },
          go: function(name, callback) {
            return _this._state.queues.handlers[name](name, callback);
          },
          process: function(name, callback) {
            var q;
            q = _this._state.queues[name];
            _this._state.queues[name] = [];
            return callback != null ? callback.call(_this, {
              queue: q,
              name: name
            }) : void 0;
          }
        }
      };
      this._init = function(apptools) {};
    }

    return Util;

  }).call(this);

  this.__apptools_preinit.abstract_base_classes.push(Util);

  this.__apptools_preinit.deferred_core_modules.push({
    module: Util
  });

  window.Util = Util = new Util();

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
        if (!(context != null)) context = '{no context}';
        if (_this.debug.logging === true) {
          _this._sendLog.apply(_this, ["[" + module + "] INFO: " + message].concat(__slice.call(context)));
        }
      };
      this.warning = this.warn = function() {
        var context, message, module;
        module = arguments[0], message = arguments[1], context = 3 <= arguments.length ? __slice.call(arguments, 2) : [];
        if (!(context != null)) context = '{no context}';
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
        if (exception == null) exception = window.AppToolsException;
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
            if (_done !== false) break;
          }
          return results;
        },
        validate: function(model, _model) {
          var invalid, item, prop, _i, _len;
          if (_model == null) _model = model.constructor.prototype;
          invalid = [];
          for (prop in model) {
            if (!{}.hasOwnProperty.call(model, prop)) continue;
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
        var args, bridge, callback_directive, event, event_bridges, hook_error_count, hook_exec_count, result, touched_events, _i, _j, _len, _len2, _ref;
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
          for (_j = 0, _len2 = event_bridges.length; _j < _len2; _j++) {
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
        if (!(names instanceof Array)) names = [names];
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
        if (once == null) once = false;
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
        if (typeof to_events === 'string') to_events = [to_events];
        if (typeof from_events === 'string') from_events = [from_events];
        _results = [];
        for (_i = 0, _len = from_events.length; _i < _len; _i++) {
          source_ev = from_events[_i];
          _results.push((function() {
            var _j, _len2, _results2;
            _results2 = [];
            for (_j = 0, _len2 = to_events.length; _j < _len2; _j++) {
              target_ev = to_events[_j];
              apptools.dev.verbose('Events', 'Bridging events:', source_ev, '->', target_ev);
              if (!(this.callchain[source_ev] != null)) {
                apptools.dev.warn('Events', 'Bridging from undefined source event:', source_ev);
                this.register(source_ev);
              }
              _results2.push(this.callchain[source_ev].hooks.push({
                event: target_ev,
                bridge: true
              }));
            }
            return _results2;
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
          if (value.string.indexOf(value.subString) !== -1) return value.identity;
        } else if (prop) {
          return value.identity;
        }
      }
    };

    CoreAgentAPI.prototype._makeVersion = function(dataString) {
      var index;
      index = dataString.indexOf(this._data.versionSearchString);
      if (index === -1) {} else {
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
        var context, response, _base, _base2, _base3;
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
          return typeof (_base2 = _this.state.pending[response.id].callbacks).notify === "function" ? _base2.notify(response.response.content) : void 0;
        } else {
          apptools.dev.error('Dispatch', 'Userland deferred task error. Calling error callback.', response);
          return typeof (_base3 = _this.state.pending[response.id].callbacks).error === "function" ? _base3.error(response.content) : void 0;
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
        if (!(_this.get(key) != null)) _this._state.runtime.count.total_keys++;
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
        if (!(_this.get(key) != null)) _this._state.runtime.count.total_keys++;
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
      LocalStorageDriver.__super__.constructor.apply(this, arguments);
    }

    LocalStorageDriver._state = {
      constructor: function() {
        var _this = this;
        this.compatible = function() {
          return !!window.localStorage;
        };
        this.construct = function(name) {
          var new_engine;
          if (name == null) name = 'appstorage';
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
      SessionStorageDriver.__super__.constructor.apply(this, arguments);
    }

    SessionStorageDriver._state = {
      constructor: function() {
        var _this = this;
        this.compatible = function() {
          return !!window.sessionStorage;
        };
        this.construct = function(name) {
          var new_engine;
          if (name == null) name = 'appstorage';
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
        var engine, _i, _len, _ref, _ref2, _ref3;
        apptools.events.trigger('STORAGE_INIT');
        apptools.dev.verbose('Storage', 'Storage support is currently under construction.');
        if (((_ref = apptools.sys) != null ? (_ref2 = _ref.preinit) != null ? _ref2.detected_storage_engines : void 0 : void 0) != null) {
          _ref3 = apptools.sys.preinit.detected_storage_engines;
          for (_i = 0, _len = _ref3.length; _i < _len; _i++) {
            engine = _ref3[_i];
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
        if (params == null) params = {};
        if (callbacks == null) callbacks = null;
        if (async == null) async = false;
        if (push == null) push = false;
        if (opts == null) opts = {};
        if (config == null) config = {};
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
        accept: 'application/json',
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
      if (id != null) this.envelope.id = id;
      if (opts != null) this.envelope.opts = opts;
      if (agent != null) this.envelope.agent = agent;
    }

    RPCRequest.prototype.fulfill = function(callbacks, config) {
      var defaultFailureCallback, defaultSuccessCallback,
        _this = this;
      if (callbacks == null) callbacks = {};
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
      var _ref;
      if ((_ref = this.ajax) != null) if (_ref.async == null) _ref.async = async;
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
      var _ref, _ref2;
      if ((_ref = this.envelope) != null) {
        _ref.opts = _.defaults(opts, (_ref2 = this.envelope) != null ? _ref2.opts : void 0);
      }
      return this;
    };

    RPCRequest.prototype.setAgent = function(agent) {
      var _ref;
      if ((_ref = this.envelope) != null) {
        if (_ref.agent == null) _ref.agent = agent;
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
      var original_xhr, _ref, _ref2,
        _this = this;
      this.state = {
        sockets: {
          token: '__NULL__',
          enabled: false,
          status: 'DISCONNECTED',
          "default": null,
          default_host: (((_ref = apptools.config) != null ? (_ref2 = _ref.rpc) != null ? _ref2.socket_host : void 0 : void 0) != null) || null
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
              var req, socket, _ref3, _ref4, _ref5, _ref6;
              if (apptools.agent.capabilities.websockets != null) {
                if ((((_ref3 = _this.state.sockets) != null ? _ref3.enabled : void 0) != null) === true) {
                  if ((((_ref4 = _this.state.sockets) != null ? _ref4["default"] : void 0) != null) === null && ((_ref5 = _this.state.sockets) != null ? (_ref6 = _ref5.open) != null ? _ref6.length : void 0 : void 0) === 0) {
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
              if (!(base_uri != null)) base_uri = _this.base_rpc_uri;
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
          if (config.api != null) request.setAPI(config.api);
          if (config.method != null) request.setMethod(config.method);
          if (config.agent != null) request.setAgent(config.agent);
          if (config.opts != null) request.setOpts(config.opts);
          if (config.base_uri != null) request.setBaseURI(config.base_uri);
          if (config.params != null) request.setParams(config.params);
          if (config.async != null) request.setAsync(config.async);
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
          if (transport == null) transport = 'xhr';
          apptools.dev.verbose('RPC', 'Fulfill', config, request, callbacks);
          if (apptools.sys.libraries.resolve('jQuery') !== false) {
            $.ajaxSetup({
              type: 'POST',
              accepts: 'application/json',
              contentType: 'application/json',
              global: true,
              xhr: function() {
                return _this.internals.transports.xhr.factory();
              },
              headers: _this.internals.config.headers
            });
          }
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
        var amplify, base_settings, resourceId, _ref3;
        if (apptools != null ? (_ref3 = apptools.sys) != null ? _ref3.drivers : void 0 : void 0) {
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
              if (config.caching === true) base_settings.caching = 'persist';
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
          var _ref, _ref2;
          if ((_ref = _this.state) != null) {
            if ((_ref2 = _ref.callbacks) != null) {
              if (typeof _ref2.expect === "function") {
                _ref2.expect(id, request, xhr);
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
          if (host == null) host = null;
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
      CoreWidgetAPI.__super__.constructor.apply(this, arguments);
    }

    return CoreWidgetAPI;

  })(CoreAPI);

  CoreWidget = (function(_super) {

    __extends(CoreWidget, _super);

    function CoreWidget() {
      var _this = this;
      this._init = function() {};
    }

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
      this.create = function(target, trigger, callback, options) {
        var id, modal;
        if (options == null) {
          options = target.hasAttribute('data-options') ? JSON.parse(target.getAttribute('data-options')) : {};
        }
        modal = new Modal(target, trigger, options);
        id = modal._state.cached_id;
        _this._state.modals_by_id[id] = _this._state.modals.push(modal) - 1;
        if (callback != null) {
          return typeof callback === "function" ? callback(modal._init()) : void 0;
        } else {
          return modal._init();
        }
      };
      this.destroy = function(modal) {
        var cached_el, cached_id, el, id;
        modal = _this.disable(modal);
        id = modal._state.element_id;
        cached_id = modal_state.cached_id;
        _this._state.modals.splice(_this._state.modals_by_id[id], 1);
        delete _this._state.modals_by_id[id];
        (el = Util.get(id)).parentNode.removeChild(el);
        (cached_el = Util.get(id)).parentNode.removeChild(cached_el);
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
        var index;
        if ((index = _this._state.modals_by_id[element_id]) != null) {
          return _this._state.modals[index];
        } else {
          return false;
        }
      };
      this._init = function() {
        var modal, modals, _i, _len, _m, _t;
        modals = Util.get('pre-modal');
        if (modals != null) {
          for (_i = 0, _len = modals.length; _i < _len; _i++) {
            modal = modals[_i];
            _m = _this.create(modal, (_t = Util.get('a-' + modal.getAttribute('id'))));
            _this.enable(_m);
          }
        }
        _this._state.init = true;
        return _this;
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
          calc: null,
          padding: null
        }
      };
      this._state.config = Util.extend(this._state.config, options);
      this.internal = {
        calc: function() {
          var css, dH, dW, r, wH, wW;
          if (_this._state.config.calc != null) {
            return _this._state.config.calc();
          } else {
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
          }
        },
        classify: function(element, method) {
          var ecl;
          if (method === 'close' || !(method != null)) {
            if (Util.in_array('dropshadow', (ecl = element.classList))) {
              ecl.remove('dropshadow');
            }
            if (Util.in_array('rounded', ecl)) ecl.remove('rounded');
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
        var close_x, content, d, dialog, fade, id, pre, prop, range, t, template, title, ui, val, _ref, _ref2;
        template = _this._state.config.template;
        range = document.createRange();
        range.selectNode(document.getElementsByTagName('div').item(0));
        d = range.createContextualFragment(template);
        document.body.appendChild(d);
        dialog = Util.get('modal-dialog');
        title = Util.get('modal-title');
        content = Util.get('modal-content');
        ui = Util.get('modal-ui');
        close_x = Util.get('modal-close');
        fade = Util.get('modal-fade');
        id = _this._state.cached_id;
        pre = Util.get(id);
        dialog.classList.add(dialog.getAttribute('id'));
        dialog.setAttribute('id', id + '-modal-dialog');
        if (_this._state.config.rounded) dialog.classList.add('rounded');
        _ref = _this._state.config.initial;
        for (prop in _ref) {
          val = _ref[prop];
          dialog.style[prop] = val;
        }
        content.classList.add(content.getAttribute('id'));
        content.setAttribute('id', id + '-modal-content');
        _ref2 = pre.style;
        for (prop in _ref2) {
          val = _ref2[prop];
          content.style[prop] = val;
        }
        content.style.opacity = 1;
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
        var close_x, dialog, dialog_animation, fade_animation, final, id;
        id = _this._state.cached_id;
        dialog = Util.get(_this._state.element_id);
        close_x = Util.get(id + '-modal-close');
        _this._state.active = true;
        fade_animation = Util.prep_animation();
        dialog_animation = Util.prep_animation();
        dialog_animation.complete = function() {
          _this.internal.classify(dialog, 'open');
          return $('#' + id + '-modal-fade').animate({
            opacity: 1
          }, fade_animation);
        };
        final = _this.internal.calc();
        final.opacity = 1;
        dialog.style.display = 'block';
        $(dialog).animate(final, dialog_animation);
        Util.bind(close_x, 'mousedown', _this.close);
        return _this;
      };
      this.close = function(callback) {
        var dialog, id, midpoint;
        id = _this._state.cached_id;
        dialog = Util.get(_this._state.element_id);
        Util.unbind(Util.get(id + '-modal-close'), 'mousedown');
        midpoint = Util.extend({}, _this._state.config.initial, {
          opacity: 0.5
        });
        Util.get(id + '-modal-content').style.overflow = 'hidden';
        return $('#' + id + '-modal-fade').animate({
          opacity: 0
        }, {
          duration: 300,
          complete: function() {
            _this.internal.classify(dialog, 'close');
            return $(dialog).animate(midpoint, {
              duration: 200,
              complete: function() {
                return $(dialog).animate({
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
                    _this._state.active = false;
                    if (callback != null) {
                      return typeof callback === "function" ? callback(_this) : void 0;
                    } else {
                      return _this;
                    }
                  }
                });
              }
            });
          }
        });
      };
      this._init = function() {
        var dialog;
        dialog = _this.make();
        Util.get(_this._state.trigger_id).removeAttribute('href');
        _this._state.init = true;
        return _this;
      };
    }

    return Modal;

  })(CoreWidget);

  this.__apptools_preinit.abstract_base_classes.push(Modal);

  this.__apptools_preinit.abstract_base_classes.push(ModalAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: ModalAPI,
    package: 'widgets'
  });

  AccordionAPI = (function(_super) {

    __extends(AccordionAPI, _super);

    AccordionAPI.mount = 'accordion';

    AccordionAPI.events = ['ACCORDION_READY', 'ACCORDION_API_READY'];

    function AccordionAPI(apptools, widget, window) {
      var _this = this;
      this._state = {
        accordions: [],
        accordions_by_id: {},
        init: false
      };
      this.create = function(target) {
        var accordion, id, options;
        options = target.hasAttribute('data-options') ? JSON.parse(target.getAttribute('data-options')) : {};
        accordion = new Accordion(target, options);
        id = accordion._state.element_id;
        _this._state.accordions_by_id[id] = _this._state.accordions.push(accordion) - 1;
        return accordion._init();
      };
      this.destroy = function(accordion) {
        var id;
        id = accordion._state.element_id;
        _this._state.accordions.splice(_this._state.accordions_by_id[id], 1);
        delete _this._state.accordions_by_id[id];
        return accordion;
      };
      this.enable = function(accordion) {
        var f, trigger, _i, _len, _ref;
        _ref = accordion._state.folds;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          f = _ref[_i];
          if (((trigger = Util.get('a-' + f)) != null) && trigger.nodeType) {
            trigger.addEventListener('click', accordion.fold, false);
          }
        }
        return accordion;
      };
      this.disable = function(accordion) {
        var fold, trigger, _i, _len, _ref;
        _ref = accordion._state.folds;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          fold = _ref[_i];
          if (((trigger = Util.get('a-' + fold)) != null) && trigger.nodeType) {
            trigger.removeEventListener('click');
          }
        }
        return accordion;
      };
      this.get = function(element_id) {
        var u;
        if ((u = _this._state.accordions_by_id[element_id]) != null) {
          return _this._state.accordions[u];
        } else {
          return false;
        }
      };
      this._init = function() {
        var accordion, accordions, _i, _len;
        accordions = Util.get('pre-accordion');
        if (accordions != null) {
          for (_i = 0, _len = accordions.length; _i < _len; _i++) {
            accordion = accordions[_i];
            _this.enable(_this.create(accordion));
          }
        }
        apptools.events.trigger('ACCORDION_API_READY', _this);
        _this._state.init = true;
        return _this;
      };
    }

    return AccordionAPI;

  })(CoreWidgetAPI);

  Accordion = (function(_super) {

    __extends(Accordion, _super);

    function Accordion(target, options) {
      var _this = this;
      this._state = {
        element_id: target.getAttribute('id'),
        folds: [],
        current_fold: null,
        active: false,
        init: false,
        config: {
          axis: 'vertical',
          vertical: {
            closed: {
              height: '0px',
              opacity: 0
            },
            opened: {
              height: '150px',
              opacity: 1
            }
          },
          horizontal: {
            closed: {
              width: '0px',
              opacity: 0
            },
            opened: {
              width: '300px',
              opacity: 1
            }
          }
        }
      };
      this._state.config = Util.extend(true, this._state.config, options);
      this.internal = {
        register_fold: function(anchor) {
          var anchor_id, f, fold, fold_id;
          fold_id = (f = anchor.getAttribute('href')).charAt(0) !== '#' ? f : f.slice(1);
          fold = Util.get(fold_id);
          anchor_id = 'a-' + fold_id;
          fold.classList.add('accordion-fold');
          fold.classList.add('none');
          anchor.removeAttribute('href');
          anchor.setAttribute('id', anchor_id);
          anchor.classList.add('accordion-link');
          return _this._state.folds.push(fold_id);
        }
      };
      this.fold = function(e) {
        var accordion, axis, block_folds, close_anim, closed, curr_folds, current, current_fold, folds, open_anim, open_tab, opened, prop, same, tab, target_div, target_id, trigger, unique_folds, _i, _j, _k, _len, _len2, _len3, _ref, _ref2;
        if (e.preventDefault) {
          e.preventDefault();
          e.stopPropagation();
        }
        trigger = e.target;
        target_div = Util.get(target_id = trigger.getAttribute('id').split('-').splice(1).join('-'));
        current_fold = Util.get(_this._state.current_fold) || false;
        current = false;
        same = target_div === current_fold;
        accordion = Util.get(_this._state.element_id);
        _ref = [Util.get('current-fold', accordion), Util.get('block', accordion)], curr_folds = _ref[0], block_folds = _ref[1];
        _ref2 = [curr_folds, block_folds];
        for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
          folds = _ref2[_i];
          if (folds != null) {
            folds = Util.filter(folds, function(el) {
              return el.parentNode === accordion;
            });
          }
        }
        unique_folds = curr_folds;
        if (block_folds) {
          for (_j = 0, _len2 = block_folds.length; _j < _len2; _j++) {
            tab = block_folds[_j];
            if (!Util.in_array(tab, unique_folds)) unique_folds.push(tab);
          }
        }
        if (unique_folds != null) current = true;
        _this._state.active = true;
        opened = _this._state.config[axis = _this._state.config.axis].opened;
        closed = _this._state.config[axis].closed;
        open_anim = (close_anim = Util.prep_animation());
        if (unique_folds != null) {
          for (_k = 0, _len3 = unique_folds.length; _k < _len3; _k++) {
            open_tab = unique_folds[_k];
            $(open_tab).animate(closed, {
              duration: 400,
              complete: function() {
                var cls, _l, _len4, _ref3;
                _ref3 = ['current-fold', 'block'];
                for (_l = 0, _len4 = _ref3.length; _l < _len4; _l++) {
                  cls = _ref3[_l];
                  open_tab.classList.remove(cls);
                }
                return open_tab.classList.add('none');
              }
            });
          }
        }
        open_anim.complete = function() {
          target_div.classList.add('current-fold');
          _this._state.active = false;
          return _this;
        };
        for (prop in closed) {
          target_div.style[prop];
        }
        if (Util.has_class(target_div, 'none')) {
          target_div.classList.remove('none');
          target_div.classList.add('block');
        }
        if (!same) $(target_div).animate(opened, open_anim);
        _this._state.current_fold = target_id;
        return _this;
      };
      this._init = function() {
        var accordion, e, link, links, _i, _len;
        accordion = Util.get(_this._state.element_id);
        links = Util.filter(Util.get('a', accordion), function(el) {
          return el.parentNode === accordion;
        });
        if (links != null) {
          for (_i = 0, _len = links.length; _i < _len; _i++) {
            link = links[_i];
            _this.internal.register_fold(link);
          }
        }
        if (typeof current_fold !== "undefined" && current_fold !== null) {
          e = {};
          e.target = links[0];
          _this.fold(e);
        }
        _this._state.init = true;
        return _this;
      };
    }

    return Accordion;

  })(CoreWidget);

  this.__apptools_preinit.abstract_base_classes.push(Accordion);

  this.__apptools_preinit.abstract_base_classes.push(AccordionAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: AccordionAPI,
    package: 'widgets'
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
        return scroller._init();
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
        scrollers = Util.get('pre-scroller') || [];
        for (_i = 0, _len = scrollers.length; _i < _len; _i++) {
          scroller = scrollers[_i];
          _this.create(_this.enable(scroller));
        }
        _this._state.init = true;
        return _this;
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
        return _this;
      };
    }

    return Scroller;

  })(CoreWidget);

  this.__apptools_preinit.abstract_base_classes.push(Scroller);

  this.__apptools_preinit.abstract_base_classes.push(ScrollerAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: ScrollerAPI,
    package: 'widgets'
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
          Util.bind(Util.get(trigger), 'mousedown', tabs["switch"], false);
        }
        return tabs;
      };
      this.disable = function(tabs) {
        var trigger;
        for (trigger in tabs._state.tabs) {
          Util.unbind(Util.get(trigger), 'mousedown');
        }
        return tabs;
      };
      this._init = function() {
        var tabs, tabsets, _i, _len;
        tabsets = Util.get('pre-tabs');
        if (tabsets != null) {
          for (_i = 0, _len = tabsets.length; _i < _len; _i++) {
            tabs = tabsets[_i];
            _this.enable(_this.create(tabs));
          }
        }
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
        current_tab: null,
        tab_count: 0,
        tabs: {},
        active: false,
        init: false,
        config: {
          rounded: true,
          width: '500px',
          div_string: 'div'
        }
      };
      this._state.config = Util.extend(true, this._state.config, options);
      this.internal = {
        classify: function() {
          var cls, div_string, tab, tabs, test, trigger, triggers, _cls, _i, _j, _k, _l, _len, _len2, _len3, _len4, _ref, _ref2;
          div_string = _this._state.config.div_string;
          target = Util.get(_this._state.element_id);
          tabs = Util.filter(Util.get(div_string, target), (test = function(el) {
            return el.parentNode === target;
          }));
          triggers = Util.filter(Util.get('a', target), test);
          target.style.width = _this._state.config.width;
          _ref = ['relative', 'tabset'];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            cls = _ref[_i];
            target.classList.add(cls);
          }
          for (_j = 0, _len2 = triggers.length; _j < _len2; _j++) {
            trigger = triggers[_j];
            if (_this._state.config.rounded) {
              trigger.classList.add('tab-rounded');
            } else {
              trigger.classList.add('tab-link');
            }
          }
          for (_k = 0, _len3 = tabs.length; _k < _len3; _k++) {
            tab = tabs[_k];
            _ref2 = ['absolute', 'tab'];
            for (_l = 0, _len4 = _ref2.length; _l < _len4; _l++) {
              _cls = _ref2[_l];
              tab.classList.add(_cls);
            }
          }
          return _this;
        }
      };
      this.make = function() {
        var trigger, triggers, _fn, _i, _len;
        target = Util.get(_this._state.element_id);
        triggers = Util.filter(Util.get('a', target), function(x) {
          return x.parentNode === target;
        });
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
        var c, current, current_a, current_tab, div_string, tabset, target_id, target_tab, trigger;
        tabset = Util.get(_this._state.element_id);
        div_string = _this._state.config.div_string;
        current_tab = Util.get(_this._state.current_tab) || ((c = Util.get('current-tab', tabset)) != null ? Util.filter(c, function(x) {
          return x.parentNode === tabset && x.tagName.toLowerCase() === div_string;
        })[0] : null) || null;
        current = false;
        if (e != null) {
          if (e.preventDefault) {
            e.preventDefault();
            e.stopPropagation();
            target_tab = Util.get(target_id = (trigger = e.target).getAttribute('id').split('-').splice(1).join('-'));
          } else if ((e != null) && e.nodeType) {
            target_tab = e;
            trigger = Util.get('a-' + (target_id = e.getAttribute('id')));
          } else {
            target_tab = Util.get(e);
            trigger = Util.get('a-' + (target_id = e));
          }
        } else {
          target_tab = Util.get(target_id = (trigger = Util.get('a', tabset)[0]).getAttribute('id').split('-').splice(1).join('-'));
        }
        if (current_tab != null) {
          current_a = Util.get('a-' + current_tab.getAttribute('id')) || Util.get('a-' + _this._state.current_tab);
          current = true;
        }
        if (current_tab === target_tab) return _this;
        _this._state.active = true;
        console.log('Switching to tab: ' + target_id);
        if (!current) {
          target_tab.classList.remove('none');
          target_tab.classList.add('current-tab');
          target_tab.classList.add('block');
          trigger.classList.add('current-tab');
          _this._state.current_tab = target_tab.getAttribute('id');
          $(target_tab).animate({
            opacity: 1
          }, {
            duration: 300,
            complete: function() {
              return _this._state.active = false;
            }
          });
        } else {
          $(current_tab).animate({
            opacity: 0
          }, {
            duration: 200,
            complete: function() {
              current_a.classList.remove('current-tab');
              current_tab.classList.remove('current-tab');
              current_tab.classList.remove('block');
              target_tab.classList.remove('none');
              current_tab.classList.add('none');
              target_tab.classList.add('block');
              target_tab.classList.add('current-tab');
              trigger.classList.add('current-tab');
              _this._state.current_tab = target_tab.getAttribute('id');
              return $(target_tab).animate({
                opacity: 1
              }, {
                duration: 300,
                complete: function() {
                  return _this._state.active = false;
                }
              });
            }
          });
        }
        return _this;
      };
      this._init = function() {
        var tabs;
        tabs = _this.make();
        _this["switch"]();
        _this._state.init = true;
        return _this;
      };
    }

    return Tabs;

  })(CoreWidget);

  this.__apptools_preinit.abstract_base_classes.push(Tabs);

  this.__apptools_preinit.abstract_base_classes.push(TabsAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: TabsAPI,
    package: 'widgets'
  });

  EditorAPI = (function(_super) {

    __extends(EditorAPI, _super);

    EditorAPI.mount = 'editor';

    EditorAPI.events = ['EDITOR_READY', 'EDITOR_API_READY'];

    function EditorAPI(apptools, widget, window) {
      var _this = this;
      this._state = {
        editors: [],
        editors_by_id: {},
        init: false
      };
      this.create = function(target) {
        var editor, id, options;
        options = target.hasAttribute('data-options') ? JSON.parse(target.getAttribute('data-options')) : {};
        editor = new Editor(target, options);
        id = editor._state.element_id;
        _this._state.editors_by_id[id] = _this._state.editors.push(editor) - 1;
        return editor._init();
      };
      this.destroy = function(editor) {
        var id;
        id = editor._state.element_id;
        _this._state.editors.splice(_this._state.editors_by_id[id], 1);
        delete _this._state.editors_by_id[id];
        return editor;
      };
      this.enable = function(editor) {
        var target;
        target = Util.get(editor._state.element_id);
        Util.bind(target, 'dblclick', editor.edit, false);
        return editor;
      };
      this.disable = function(editor) {
        Util.unbind(Util.get(editor._state.element_id), 'dblclick');
        return editor;
      };
      this._init = function() {
        var editor, editors, _i, _len;
        editors = Util.get('mini-editable');
        if (editors != null) {
          for (_i = 0, _len = editors.length; _i < _len; _i++) {
            editor = editors[_i];
            _this.enable(_this.create(editor));
          }
        }
        return _this;
      };
    }

    return EditorAPI;

  })(CoreWidgetAPI);

  Editor = (function(_super) {

    __extends(Editor, _super);

    function Editor(target, options) {
      var _this = this;
      this._state = {
        element_id: target.getAttribute('id'),
        snippet_keyname: target.getAttribute('data-snippet-keyname') || null,
        pane_id: null,
        active: false,
        init: false,
        config: {
          bundles: {
            plain: {
              save: {
                char: '&#xf0053;',
                command: function() {
                  return _this.save();
                }
              }
            },
            basic: {
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
              }
            },
            rich: {
              h1: function() {
                return document.execCommand('heading', false, 'h1');
              },
              h2: function() {
                return document.execCommand('heading', false, 'h2');
              },
              h3: function() {
                return document.execCommand('heading', false, 'h3');
              },
              fontColor: function() {
                var c, sel;
                c = Util.toHex(prompt('Please enter hex (#000000) or RGB (rgb(0,0,0)) values.'));
                sel = document.selection() || window.getSelection();
                return document.execCommand('insertHTML', false, '<span style="color: ' + c + ';">' + sel + '</span>');
              },
              fontSize: function() {
                var s, sel;
                s = prompt('Please enter desired numerical pt size (i.e. 10)');
                sel = document.selection() || window.getSelection();
                return document.execCommand('insertHTML', false, '<span style="font-size: ' + s + ';">' + sel + '</span>');
              },
              left: function() {
                return document.execCommand('justifyLeft');
              },
              right: function() {
                return document.execCommand('justifyRight');
              },
              center: function() {
                return document.execCommand('justifyCenter');
              },
              indent: function() {
                return document.execCommand('indent');
              },
              outdent: function() {
                return document.execCommand('outdent');
              },
              link: function() {
                var l, t, _t;
                t = document.selection() || window.getSelection();
                if ((t != null) && t.match(/^http|www/)) {
                  _t = t;
                  t = prompt('What link text do you want to display?');
                } else if (!(t != null)) {
                  t = prompt('What link text do you want to display?');
                }
                l = _t || prompt('What URL do you want to link to? (http://www...)');
                return document.execCommand('insertHTML', false, '<a href="' + Util.strip_script(l + '">' + t + '</a>'));
              }
            }
          },
          bundle: 'plain',
          width: 'auto'
        }
      };
      this._state.config = Util.extend(true, this._state.config, options);
      this.make = function() {
        var command, feature, features, k, pane, pane_id, t, t_id, v, width, _button, _off, _ref, _w;
        t = Util.get(t_id = _this._state.element_id);
        width = _this._state.config.width;
        pane = document.createElement('div');
        pane.setAttribute('id', (pane_id = 'editor-pane-' + t_id));
        pane.classList.add('absolute');
        pane.style.padding = 10 + 'px';
        pane.style.width = width + 'px';
        pane.style.zIndex = 1;
        pane.style.opacity = 0;
        features = _this._state.config.bundles.plain;
        if (_this._state.config.bundle === 'rich') {
          _ref = _this._state.config.bundles.rich;
          for (k in _ref) {
            v = _ref[k];
            features[k] = v;
          }
        }
        _button = function(f, c) {
          var button;
          button = document.createElement('button');
          button.innerHTML = command.char;
          button.className = 'editorbutton';
          Util.bind(button, 'mousedown', command.command);
          return pane.appendChild(button);
        };
        for (feature in features) {
          command = features[feature];
          _button(feature, command);
        }
        _off = Util.get_offset(t);
        _w = pane.offsetWidth;
        document.body.appendChild(pane);
        pane.style.left = _off.left - 50 + 'px';
        pane.style.top = _off.top + 'px';
        _this._state.pane_id = pane_id;
        return pane;
      };
      this.show = function() {
        var p;
        (p = Util.get(_this._state.pane_id)).style.zIndex = 9990;
        $(p).animate({
          opacity: 1
        }, Util.prep_animation());
        return _this;
      };
      this.hide = function() {
        var p;
        (p = Util.get(_this._state.pane_id)).style.zIndex = 1;
        $(p).animate({
          opacity: 0
        }, Util.prep_animation());
        return _this;
      };
      this.edit = function(e) {
        var el;
        if (e.preventDefault) {
          e.preventDefault();
          e.stopPropagation();
        }
        _this.show();
        (el = Util.get(_this._state.element_id)).contentEditable = true;
        _this._state.active = true;
        Util.bind(document.body, 'dblclick', _this.save);
        el.focus();
        return _this;
      };
      this.save = function(e) {
        var clicked, html;
        if ((e != null) && (e.preventDefault != null)) {
          e.preventDefault;
          e.stopPropagation;
          clicked = e.target;
        }
        console.log('Saving snippet...');
        html = Util.get(_this._state.element_id).innerHTML;
        $.apptools.api.content.save_snippet({
          snippet_keyname: _this._state.snippet_keyname,
          inner_html: html
        }).fulfill({
          success: function(response) {
            var el;
            _this.hide();
            (el = Util.get(_this._state.element_id)).contentEditable = false;
            _this._state.active = false;
            Util.unbind(document.body, 'dblclick');
            if (clicked != null) clicked.classList.add('success');
            return alert('save_snippet() via editor success');
          },
          failure: function(error) {
            clicked.classList.add('success');
            alert('save_snippet() via editor failure');
            return console.log(error);
          }
        });
        return _this;
      };
      this._init = function() {
        var pane;
        pane = this.make();
        document.body.appendChild(pane);
        this._state.init = true;
        return this;
      };
    }

    return Editor;

  })(CoreWidget);

  this.__apptools_preinit.abstract_base_classes.push(Editor);

  this.__apptools_preinit.abstract_base_classes.push(EditorAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: EditorAPI,
    package: 'widgets'
  });

  UploaderAPI = (function(_super) {

    __extends(UploaderAPI, _super);

    UploaderAPI.mount = 'uploader';

    UploaderAPI.events = ['UPLOADER_READY', 'UPLOADER_API_READY'];

    function UploaderAPI(apptools, widget, window) {
      var _this = this;
      this._state = {
        uploaders: [],
        uploaders_by_id: {},
        init: false
      };
      this.create = function(kind, options) {
        var bound, id, uploader;
        if (Util.is_raw_object(kind)) {
          options = kind;
          kind = null;
        }
        if (!(options != null)) options = {};
        uploader = !(kind != null) ? new DataURLUploader(options) : kind === 'data' ? new DataURLUploader(options) : kind === 'array' ? new ArrayBufferUploader(options) : kind === 'binary' ? new BinaryUploader(options) : new Uploader(options);
        if ((options != null ? options.id : void 0) != null) {
          id = options.id;
          if (Util.is_id(id)) uploader = _this.enable(uploader);
        } else {
          (bound = uploader._state.boundary).match(/^-+(\w+)-+$/);
          uploader._state.config.id = (id = RegExp.$1);
        }
        _this._state.uploaders_by_id[id] = _this._state.uploaders.push(uploader) - 1;
        return uploader._init();
      };
      this.destroy = function(uploader) {
        var id;
        id = uploader._state.config.id;
        _this._state.uploaders.splice(_this._state.uploaders_by_id[id], 1);
        delete _this._state.uploaders_by_id[id];
        return uploader;
      };
      this.enable = function(uploader) {
        var id, target;
        target = Util.get(id = uploader._state.config.id);
        console.log('[UPLOADER:INIT]', 'Enabling drop zone on #' + id);
        if (target != null) {
          target.addEventListener('drop', uploader.upload, false);
        }
        return uploader;
      };
      this.disable = function(uploader) {
        var target;
        target = Util.get(uploader._state.config.id);
        if (target != null) Util.unbind(target, 'drop');
        return uploader;
      };
      this.get = function(element_id) {
        var u;
        if ((u = _this._state.uploaders_by_id[element_id]) != null) {
          return _this._state.uploaders[u];
        } else {
          return false;
        }
      };
      this._init = function() {
        var uploader, uploaders, _i, _j, _len;
        uploaders = Util.get('pre-uploader');
        _i = function(_u) {
          var options;
          options = Util.extend(true, (_u.hasAttribute('data-options') ? JSON.parse(_u.getAttribute('data-options')) : {}), {
            id: _u.getAttribute('id')
          });
          _u.classList.remove('pre-uploader');
          _u.classList.add('uploader');
          return _u = _this.create(options);
        };
        if (uploaders != null) {
          for (_j = 0, _len = uploaders.length; _j < _len; _j++) {
            uploader = uploaders[_j];
            _i(uploader);
          }
        }
        apptools.events.trigger('UPLOADER_API_READY', _this);
        _this._state.init = true;
        return _this;
      };
    }

    return UploaderAPI;

  })(CoreAPI);

  Uploader = (function(_super) {

    __extends(Uploader, _super);

    function Uploader(options) {
      var _this = this;
      this._state = {
        boundary: null,
        active: false,
        init: false,
        queued: 0,
        session: null,
        config: {
          boundary_base: 'd4v1dR3K0W',
          banned_types: ['application/exe'],
          banned_extensions: ['.exe'],
          max_cache: 15,
          endpoints: [],
          finish: null
        },
        cache: {
          uploads_by_type: {},
          uploaded: []
        }
      };
      this._state.config = Util.extend(this._state.config, options);
      this.internal = {
        allow: function(file) {
          var extension, type;
          extension = file.name.split('.').pop();
          type = file.type;
          if (Util.in_array(extension, _this._state.config.banned_extensions)) {
            return false;
          }
          if (Util.in_array(type, _this._state.config.banned_types)) return false;
          return true;
        },
        finish: function(response) {
          if (_this._state.config.finish != null) {
            return _this._state.config.finish.call(_this, response);
          } else {
            return response;
          }
        },
        prep_body: function(file, data) {
          var body, boundary, crlf;
          if (!_this.internal.allow(file)) return false;
          boundary = _this._state.boundary;
          crlf = '\r\n';
          body = '--' + boundary + crlf;
          body += 'Content-Disposition: form-data; name="filename"; filename="' + file.name + '"' + crlf;
          body += 'Content-type: ' + file.type + crlf + crlf;
          body += data + crlf + crlf + '--' + boundary + '--';
          return body;
        },
        preview: function(e) {},
        progress: function(file, xhr) {
          return xhr.upload.onprogress = function(ev) {
            var percent, _f;
            _f = file.name.split('.')[0];
            if (ev.lengthComputable) {
              percent = Math.floor((ev.loaded / ev.total) * 100);
              return console.log(percent);
            }
          };
        },
        provision_boundary: function() {
          var base, char, rand, _b, _i, _len, _ref;
          _b = ['-----'];
          base = _this._state.config.boundary_base;
          rand = Math.floor(Math.pow(Math.random() * 10000, 3));
          _ref = rand.toString().split('');
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            char = _ref[_i];
            _b.push(base[char]);
          }
          _b.push('-----');
          return _b.join('');
        },
        read: function(file, callback) {
          var reader;
          reader = new FileReader();
          reader.file = file;
          reader.onloadend = callback;
          return reader.readAsBinaryString(file);
        },
        ready: function(file, xhr) {
          return xhr.onreadystatechange = function() {
            var response;
            if (xhr.readyState === 4 && xhr.status === 200) {
              response = xhr.responseText;
              _this.internal.update_cache(file, xhr);
              return _this.internal.finish(JSON.parse(response));
            } else if (xhr.readyState === 4) {
              return 'XHR send finished with status ' + xhr.status;
            } else {
              return 'XHR send failed at readyState ' + xhr.readyState;
            }
          };
        },
        send: function(file, data, url) {
          var body, xhr;
          xhr = new XMLHttpRequest();
          body = _this.internal.prep_body(file, data);
          _this.internal.progress(file, xhr);
          xhr.open('POST', url, true);
          xhr.setRequestHeader('Content-type', 'multipart/form-data; boundary=' + _this._state.boundary);
          _this.internal.ready(file, xhr);
          apptools.dev.verbose('UPLOADER', 'About to upload file: ' + file.name);
          if (!!body) {
            return xhr.send(body);
          } else {
            return false;
          }
        },
        update_cache: function(file, xhr) {
          var l, mx, name, remaining, t, type, u;
          remaining = _this._state.queued--;
          if (remaining === 0) _this._state.config.endpoints = [];
          if ((t = _this._state.cache.uploads_by_type)[type = file.type] != null) {
            t[type]++;
          } else {
            t[type] = (name = file.name);
          }
          (u = _this._state.cache.uploaded).push(name);
          if ((l = u.length) > (mx = _this._state.config.max_cache)) {
            return u = u.splice(l - mx);
          }
        }
      };
      this._state.boundary = this.internal.provision_boundary();
      this.add_endpoint = function(endpoint) {
        var endpt, _i, _len;
        if (Util.is_array(endpoint)) {
          for (_i = 0, _len = endpoint.length; _i < _len; _i++) {
            endpt = endpoint[_i];
            _this.add_endpoint(endpt);
          }
        } else {
          _this._state.config.endpoints.push(endpoint);
        }
        return _this;
      };
      this.add_callback = function(callback) {
        if (Util.is_function(callback)) _this._state.config.finish = callback;
        return _this;
      };
      this.handle = function(e) {
        var target;
        if (e.preventDefault) {
          e.preventDefault();
          e.stopPropagation();
        }
        target = e.target;
        switch (e.type) {
          case 'dragenter':
          case 'dragover':
            target.style.border = '2px dashed green';
            break;
          case 'dragexit':
          case 'dragleave':
            target.style.border = '2px solid transparent';
            break;
          default:
            console.log('[Uploader]', 'Not sure how to handle a ' + e.type + ' event...:(');
        }
        return _this;
      };
      this.upload = function(e) {
        var diff, file, files, i, process_upload, _len;
        if (e.preventDefault) {
          e.preventDefault();
          e.stopPropagation();
          files = e.dataTransfer.files;
        } else if (Util.is_array(e)) {
          files = e;
        } else if (e.size) {
          files = [e];
        } else {
          files = [];
        }
        process_upload = function(f, url) {
          _this._state.active = true;
          return _this.internal.read(f, function(ev) {
            var data, _f;
            ev.preventDefault();
            ev.stopPropagation();
            _f = ev.target.file;
            data = ev.target.result;
            return _this.internal.send(_f, data, url);
          });
        };
        if (!((e = _this._state.config.endpoints) != null) || e.length < files.length) {
          if (!(e != null)) _this._state.config.endpoints = [];
          diff = files.length - _this._state.config.endpoints.length;
          $.apptools.api.media.generate_endpoint({
            backend: 'blobstore',
            file_count: diff
          }).fulfill({
            success: function(response) {
              var endpt, _i, _len, _ref, _results;
              _ref = response.endpoints;
              _results = [];
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                endpt = _ref[_i];
                _results.push(_this._state.config.endpoints.push(endpt));
              }
              return _results;
            },
            failure: function(error) {
              return alert('Uploader endpoint generation failed.');
            }
          });
        }
        _this._state.queued = files.length;
        for (i = 0, _len = files.length; i < _len; i++) {
          file = files[i];
          process_upload(file, _this._state.config.endpoints[i]);
        }
        return _this;
      };
      this._init = function() {
        _this._state.init = true;
        return _this;
      };
    }

    return Uploader;

  })(CoreWidget);

  BinaryUploader = (function(_super) {

    __extends(BinaryUploader, _super);

    function BinaryUploader() {
      BinaryUploader.__super__.constructor.apply(this, arguments);
    }

    return BinaryUploader;

  })(Uploader);

  DataURLUploader = (function(_super) {

    __extends(DataURLUploader, _super);

    function DataURLUploader(options) {
      var _this = this;
      DataURLUploader.__super__.constructor.call(this, options);
      this.internal.read = function(file, callback) {
        var reader;
        reader = new FileReader();
        reader.file = file;
        reader.onloadend = callback;
        return reader.readAsDataURL(file);
      };
    }

    return DataURLUploader;

  })(Uploader);

  ArrayBufferUploader = (function(_super) {

    __extends(ArrayBufferUploader, _super);

    function ArrayBufferUploader(options) {
      var _this = this;
      ArrayBufferUploader.__super__.constructor.call(this, options);
      this.internal.send = function(file, data, url) {
        var fd, to_blob, xhr;
        if (!(typeof ArrayBuffer !== "undefined" && ArrayBuffer !== null)) {
          return false;
        }
        xhr = new XMLHttpRequest();
        _this.internal.progress(file, xhr);
        to_blob = function(dataURL) {
          var abuff, abuff_view, blobb, bytes, char, d, i, l, mime, _len;
          bytes = atob((d = dataURL.split(','))[1]);
          mime = d[0].split(':')[1].split(';')[0];
          abuff = new ArrayBuffer(l = bytes.length);
          abuff_view = new Uint8Array(abuff);
          for (i = 0, _len = bytes.length; i < _len; i++) {
            char = bytes[i];
            abuff_view[i] = bytes.charCodeAt(i);
          }
          blobb = window.BlobBuilder ? new BlobBuilder() : window.WebKitBlobBuilder ? new WebKitBlobBuilder() : window.MozBlobBuilder ? new MozBlobBuilder() : null;
          if (blobb != null) {
            blobb.append(abuff);
            return blobb.getBlob(mime);
          } else {
            return null;
          }
        };
        fd = new FormData();
        fd.append('file', to_blob(data));
        xhr.open('POST', url, true);
        _this.internal.ready(file, xhr);
        return xhr.send(fd);
      };
    }

    return ArrayBufferUploader;

  })(DataURLUploader);

  this.__apptools_preinit.abstract_base_classes.push(Uploader);

  this.__apptools_preinit.abstract_base_classes.push(UploaderAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: UploaderAPI,
    package: 'widgets'
  });

  StickyAPI = (function(_super) {

    __extends(StickyAPI, _super);

    StickyAPI.mount = 'sticky';

    StickyAPI.events = ['STICKY_READY', 'STICKY_API_READY'];

    function StickyAPI(apptools, widget, window) {
      var _this = this;
      this._state = {
        stickies: [],
        stickies_by_id: {},
        init: false
      };
      this.create = function(target) {
        var id, options, sticky;
        options = target.hasAttribute('data-options') ? JSON.parse(target.getAttribute('data-options')) : {};
        sticky = new Sticky(target, options);
        id = sticky._state.element_id;
        _this._state.stickies_by_id[id] = _this._state.stickies.push(sticky) - 1;
        return sticky._init();
      };
      this.destroy = function(sticky) {};
      this.enable = function(sticky) {
        Util.bind(window, 'scroll', Util.debounce(sticky.refresh, 15, false));
        return sticky;
      };
      this.disable = function(sticky) {
        Util.unbind(window, 'scroll');
        return sticky;
      };
      this.get = function(element_id) {
        var index;
        index = _this.stickies_by_id[element_id];
        return _this.stickies[index];
      };
      this._init = function() {
        var stickies, sticky, _i, _len;
        stickies = Util.get('pre-sticky');
        if (stickies != null) {
          for (_i = 0, _len = stickies.length; _i < _len; _i++) {
            sticky = stickies[_i];
            _this.enable(_this.create(sticky));
          }
        }
        apptools.events.trigger('STICKY_API_READY', _this);
        _this._state.init = true;
        return _this;
      };
    }

    return StickyAPI;

  })(CoreAPI);

  Sticky = (function(_super) {

    __extends(Sticky, _super);

    function Sticky(target, options) {
      var _this = this;
      this._state = {
        element_id: target.getAttribute('id'),
        active: false,
        init: false,
        config: {
          side: 'top'
        },
        cache: {
          original_offset: null,
          past_offset: null,
          classes: null,
          style: {}
        }
      };
      this._state.config = Util.extend(true, this._state.config, options);
      this.refresh = function() {
        var achieved, distance, el, offset_side, past_offset, scroll, window_offset;
        el = document.getElementById(_this._state.element_id);
        console.log('[STICKY]', 'REFRESH METHOD HIT!');
        offset_side = _this._state.config.side;
        window_offset = offset_side === 'top' ? window.scrollY : window.scrollX;
        past_offset = _this._state.cache.past_offset || 0;
        _this._state.cache.past_offset = window_offset;
        distance = _this._state.cache.original_offset[offset_side] - 8;
        achieved = window_offset - distance;
        scroll = window_offset - past_offset;
        if (scroll > 0) {
          if (_this._state.active || achieved < 0) {
            return false;
          } else if (achieved > 0) {
            return _this.stick();
          }
        } else if (scroll < 0) {
          if (!_this._state.active || achieved > 0) {
            return false;
          } else if (achieved < 0) {
            return _this.unstick();
          }
        } else {
          return false;
        }
      };
      this.stick = function() {
        var el, prop, val, _ref;
        _this._state.active = true;
        el = document.getElementById(_this._state.element_id);
        _this._state.cache.classes = el.className;
        _ref = el.style;
        for (prop in _ref) {
          val = _ref[prop];
          _this._state.cache.style[prop] = val;
        }
        el.classList.add('fixed');
        el.style.top = -8 + 'px';
        el.style.left = _this._state.cache.original_offset.left + 'px';
        return _this;
      };
      this.unstick = function() {
        var el;
        el = document.getElementById(_this._state.element_id);
        el.classList.remove('fixed');
        el.style.left = '';
        el.style.top = '-170px';
        el.style.right = '5%';
        _this._state.active = false;
        return _this;
      };
      this._init = function() {
        _this._state.cache.original_offset = Util.get_offset(Util.get(_this._state.element_id));
        _this._state.init = true;
        return _this;
      };
    }

    return Sticky;

  })(CoreWidget);

  this.__apptools_preinit.abstract_base_classes.push(Sticky);

  this.__apptools_preinit.abstract_base_classes.push(StickyAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: StickyAPI,
    package: 'widgets'
  });

  CoreAdminAPI = (function(_super) {

    __extends(CoreAdminAPI, _super);

    function CoreAdminAPI() {
      this._init = __bind(this._init, this);
      CoreAdminAPI.__super__.constructor.apply(this, arguments);
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
    package: 'admin'
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
    package: 'admin'
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
    package: 'admin'
  });

  ContentManagerAPI = (function(_super) {

    __extends(ContentManagerAPI, _super);

    function ContentManagerAPI(apptools) {
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
              return _this.config.panel.commands.html('b');
            },
            u: function() {
              return _this.config.panel.commands.html('u');
            },
            i: function() {
              return _this.config.panel.commands.html('i');
            },
            clear: function() {
              return document.execCommand('removeFormat');
            },
            h1: function() {
              return _this.config.panel.commands.html('h1', 'class="h1"');
            },
            h2: function() {
              return _this.config.panel.commands.html('h2', 'class="h2"');
            },
            h3: function() {
              return _this.config.panel.commands.html('h3', 'class="h3"');
            },
            fontColor: function() {
              var c;
              c = prompt('Please enter a hexidecimal color value (i.e. #ffffff)');
              c = c[0] === '#' ? c : '#' + c;
              return _this.config.panel.commands.html('span', 'style="color:' + String(c + ';"'));
            },
            fontSize: function() {
              var s;
              s = prompt('Please enter desired point size (i.e. 10)');
              return _this.config.panel.commands.html('span', 'style="font-size:' + String(s + 'pt;"'));
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
              if (!_this.util.is(t)) {
                t = prompt("What link text do you want to display?");
              }
              l = prompt('What URL do you want to link to?');
              return _this.config.panel.commands.html('a', 'href="' + l + '"');
            },
            image: null,
            video: null,
            html: function(tag, params) {
              var sel;
              sel = document.selection ? document.selection() : window.getSelection();
              if (_this.util.is(params)) {
                return document.execCommand('insertHTML', false, '<' + tag + ' ' + params + '>' + sel + '</' + tag + '>');
              } else {
                return document.execCommand('insertHTML', false, '<' + tag + '>' + sel + '</' + tag + '>');
              }
            }
          },
          panel_html: ['<div id="CMS_wrap">', '<div id="CMS_panel" class="fixed panel">', '<div id="CMS_frame" class="nowrap">', '<div class="cms_pane" id="editing">', '<div class="cms_subpane">', '<h1 class="cms_sp">editing</h1>', '<p>', '<button id="cms_undo" value="undo">undo</button>', '<button id="cms_redo" value="redo">redo</button>', '<button id="cms_cut" value="cut">cut</button>', '<button id="cms_paste" value="paste">paste</button>', '<br>', '<button id="cms_clear" value="clear formatting">clear formatting</button>', '</p>', '</div>', '<hr/>', '<div class="cms_subpane">', '<h1 class="cms_sp">typography</h1>', '<p>', '<select id="cms_headers" class="cms">', '<option id="cms_h1" class="h1">Heading 1</option>', '<option id="cms_h2" class="h2">Heading 2</option>', '<option id="cms_h3" class="h3">Heading 3</option>', '</select>', '<button id="cms_b" value="bold">B</button>', '<button id="cms_u" value="underline">U</button>', '<button id="cms_i" value="italic">I</button>', '<br>', '<button id="cms_fontColor" value="font color">font color</button>', '<button id="cms_fontSize" value="font size">font size</button>', '</p>', '</div>', '<hr/>', '<div class="cms_subpane">', '<h1 class="cms_sp">alignment</h1>', '<p>', '<button id="cms_l" value="left">left</button>', '<button id="cms_c" value="center">center</button>', '<button id="cms_r" value="right">right</button>', '<button id="cms_in" value="indent">&raquo;</button>', '<button id="cms_out" value="outdent">&laquo;</button>', '</p>', '</div>', '<hr>', '<div class="cms_subpane">', '<h1 class="cms_sp">lists</h1>', '<p>', '<button id="cms_bullet" value="unordered list">bulleted</button>', '<button id="cms_number" value="ordered list">numbered</button>', '<button class="cms_disabled" id="cms_outline" value="outline">outline</button>', '</p>', '</div>', '<hr/>', '<div class="cms_subpane">', '<h1 class="cms_sp">interactive</h1>', '<p>', '<button id="cms_link" value="link">add link</button>', '</p>', '</div>', '</div>', '<div class="cms_pane" id="content">', '<div class="cms_subpane">', '<h1 class="cms_sp">pages</h1>', '<div id="acco-page-manager-pane" class="acco-wrap">', '<div id="acco-page-manager" class="accordion">', '<a class="acco" href="#page-1">main page</a>', '<div id="#acco-pages-page-1" class="acco-btf block">', '<a class="pop" href="javascript:void(0)">subpage 1</a><br>', '<a class="pop" href="javascript:void(0)">subpage 2</a>', '</div>', '<a class="acco" href="#page-2">second page</a>', '<div id="#acco-pages-page-2" class="acco-btf block">', '<a class="pop" href="javascript:void(0)">another subpage 1</a><br>', '<a class="pop" href="javascript:void(0)">another subpage 2</a>', '</div>', '<a class="acco" href="#page-3">third page</a>', '<div id="#acco-pages-page-3" class="acco-btf block">', '<a class="pop" href="javascript:void(0)">yep, subpage 1</a><br>', '<a class="pop" href="javascript:void(0)">yep, subpage 2</a>', '</div>', '</div>', '</div>', '</div>', '</div>', '<div class="cms_pane" id="assets">', '<div class="cms_subpane">', '<h1 class="cms_sp">drop files here</h1>', '<div id="upload_wrap">', '<div id="upload" class="dragdrop">', '<span class="center-text" id="up_content">+</span>', '</div>', '</div>', '</div>', '<hr>', '<div class="cms_subpane">', '<h1 class="cms_sp">uploaded assets</h1>', '<div id="upload-files-pane">', '</div>', '</div>', '</div>', '</div>', '<div id="CMS_nav">', '<a class="scroll" href="#editing">editing</a>', '<a class="scroll" href="#content">content</a>', '<a class="scroll" href="#assets">assets</a>', '</div>', '<div id="CMS_panel_footer">&copy; momentum labs 2012</div>', '</div>', '</div>'].join('\n'),
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
        accordion: {
          animation: {
            duration: 400,
            easing: 'easeInOutExpo',
            complete: null
          },
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
        calcModal: function() {
          var mH, mW, r, rObj, wH, wW;
          rObj = {};
          r = _this.config.modal.ratio;
          wW = window.innerWidth;
          wH = window.innerHeight;
          mW = Math.floor(r.x * wW);
          mH = Math.floor(r.y * wH);
          rObj.width = mW + 'px';
          rObj.height = mH + 'px';
          rObj.top = Math.floor((wH - mH) / 2);
          rObj.left = Math.floor((wW - mW) / 2);
          return rObj;
        },
        imagePreview: function(_file) {
          var appendImg, _reader;
          appendImg = function(_event) {
            var fN, src;
            src = _event.target.result;
            fN = _event.target.file.name.split('.')[0];
            return $('#landing-' + fN).append('<img id="' + fN + '" src="' + src + '">');
          };
          _reader = new FileReader();
          _reader.file = _file;
          _reader.addEventListener('loadend', appendImg, false);
          return _reader.readAsDataURL(_file);
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
          evE.preventDefault();
          evE.stopPropagation();
          eT = evE.target;
          if (evE.type === 'dragenter') {
            return $(eT).addClass('hover');
          } else if (evE.type !== 'dragover') {
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
        makeProgressBar: function() {
          return false;
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
        var doUpload, file, files, _i, _len, _results;
        e.preventDefault();
        e.stopPropagation();
        $(e.target).removeClass('hover');
        files = e.dataTransfer.files;
        doUpload = function(f) {
          var divID, liID, spanID, _fN;
          _fN = f.name.split('.')[0];
          liID = 'li-' + _fN;
          spanID = 'upload-percentage-' + _fN;
          divID = 'upload-progress-' + _fN;
          if (!_this.util.isID('upload-files-list')) {
            $('#upload-files-pane').append('<ul id="upload-files-list"></ul>');
          }
          $('#upload-files-list').append('<li id="' + liID + '"></li>');
          $('#' + liID).append('<div class="upload-preview-landing" id="landing-' + _fN + '"></div>').append('<span class="upload-percentage" id="' + spanID + '">1%</span>').append('<div class="upload-progress" id="' + divID + '">&nbsp;</div>');
          _this.util.imagePreview(f);
          return $.apptools.api.assets.generate_upload_url().fulfill({
            success: function(response) {
              var reader, sendFile;
              sendFile = function(_e) {
                var body, boundary, crlf, data, xhr, _f;
                boundary = '-------m0m3n+umUPL04D3R-------';
                crlf = '\r\n';
                xhr = new XMLHttpRequest();
                body = '--' + boundary + crlf;
                data = _e.target.result;
                _f = _e.target.file;
                body += 'Content-Disposition: form-data; filename="' + _f.name + '"' + crlf;
                body += 'Content-type: ' + _f.type + crlf + crlf;
                body += data + crlf + boundary + '--';
                xhr.upload.addEventListener('progress', function(eVT) {
                  var percentDone, proW, _fname;
                  _fname = _f.name.split('.')[0];
                  if (eVT.lengthComputable) {
                    percentDone = Math.floor((eVT.loaded / eVT.total) * 100);
                    proW = Math.floor((eVT.loaded / eVT.total) * 128);
                    $('#upload-percentage-' + _fname).html(percentDone + '%');
                    return $('#upload-progress-' + _fname).css({
                      width: proW
                    });
                  }
                }, false);
                xhr.open('POST', response.url, true);
                xhr.setRequestHeader('Content-type', 'multipart/form-data; boundary=' + boundary);
                xhr.onreadystatechange = function() {
                  var _fname;
                  if (xhr.readyState === 4) {
                    _fname = _f.name.split('.')[0];
                    $.apptools.dev.verbose('UPLOAD', 'file name: ' + _fname);
                    $('#upload-progress-' + _fname).addClass('upload-done').removeClass('upload-progress');
                    if (xhr.status === 200) {
                      return $.apptools.dev.verbose('UPLOAD', 'Upload succeeded!');
                    } else {
                      return $.apptools.dev.verbose('UPLOAD', 'Upload completed but returned status ' + xhr.status);
                    }
                  }
                };
                $.apptools.dev.verbose('UPLOAD', 'Uploading ' + _f.name + '...');
                return xhr.send(body);
              };
              reader = new FileReader();
              reader.file = f;
              reader.addEventListener('loadend', sendFile, false);
              return reader.readAsBinaryString(f);
            },
            failure: function(error) {
              return $.apptools.dev.error('UPLOAD', 'UPLOAD FAILED WITH ERROR: ' + error);
            }
          });
        };
        _results = [];
        for (_i = 0, _len = files.length; _i < _len; _i++) {
          file = files[_i];
          _results.push(doUpload(file));
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
          $('.acco').each(function() {
            var $t, rel, t;
            t = this;
            $t = $(t);
            rel = String($t.attr('href')).slice(1);
            $t.attr('href', 'javascript:void(0);');
            $t.attr('id', 'a-' + rel);
            return that.util.bind($t, 'click', that.util.wrap(that.accordion.fold, rel));
          });
          _this.accordion.fold('page-1');
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
          if (_this.util.is(eVent)) {
            eVent.preventDefault();
            eVent.stopPropagation();
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
          if (this.config.modal.rounded) $('#modal').addClass('rounded');
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
      this.accordion = {
        fold: function(rEl) {
          var curr, nD;
          rEl = rEl !== null && typeof rEl !== 'undefined' ? rEl : _this.config.accordion.home;
          nD = '#acco-pages-' + rEl;
          if ($(nD).hasClass('none')) {
            $(nD).css({
              'height': '0px'
            });
            curr = $('.current-fold').attr('id') ? $('.current-fold').attr('id').slice(2) : false;
            if (curr !== false) {
              $('.current-fold').removeClass('current-fold');
              $('#' + curr).animate({
                'height': '0px',
                'opacity': 0
              }, {
                duration: 400,
                easing: 'easeInOutExpo',
                complete: function() {
                  if ('#' + curr !== nD) {
                    return $('#' + curr).removeClass('block').addClass('none');
                  }
                }
              });
              $(nD).removeClass('none').addClass('block');
              $('#a-' + rEl).addClass('current-fold');
              return $(nD).animate({
                'height': '350px',
                'opacity': 1
              }, {
                duration: 400,
                easing: 'easeInOutExpo'
              });
            } else if ($(nD).hasClass('block')) {
              $('#a-' + rEl).removeClass('current-fold');
              return $(nD).animate({
                'height': '0px',
                'opacity': 0
              }, {
                duration: 400,
                easing: 'easeInOutExpo',
                complete: function() {
                  return $(nD).removeClass('block').addClass('none');
                }
              });
            }
          }
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

  })(CoreAPI);

  this.__apptools_preinit.abstract_base_classes.push(ContentManagerAPI);

  this.__apptools_preinit.deferred_core_modules.push({
    module: ContentManagerAPI,
    package: 'admin'
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
      var module, _i, _len, _ref, _ref2,
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
            return _this.sys.state.flags.push(flagname);
          },
          consider_preinit: function(preinit) {
            var cls, lib, _i, _interface, _j, _k, _len, _len2, _len3, _ref, _ref2, _ref3;
            if (preinit.abstract_base_classes != null) {
              _ref = preinit.abstract_base_classes;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                cls = _ref[_i];
                _this.sys.state.classes[cls.name] = cls;
                if ((cls.package != null) && (_this.sys.state.modules[cls.package] != null)) {
                  _this.sys.state.modules[cls.package].classes[cls.name] = cls;
                }
                if ((cls["export"] != null) && cls["export"] === 'private') {
                  continue;
                } else {
                  window[cls.name] = cls;
                }
              }
            }
            if (preinit.deferred_library_integrations != null) {
              _ref2 = preinit.deferred_library_integrations;
              for (_j = 0, _len2 = _ref2.length; _j < _len2; _j++) {
                lib = _ref2[_j];
                _this.sys.libraries.install(lib.name, lib.library);
              }
            }
            if (preinit.abstract_feature_interfaces != null) {
              _ref3 = preinit.abstract_feature_interfaces;
              for (_k = 0, _len3 = _ref3.length; _k < _len3; _k++) {
                _interface = _ref3[_k];
                _this.sys.interfaces.install(_interface.name, _interface.adapter);
              }
            }
            return preinit;
          }
        },
        modules: {
          install: function(module, mountpoint_or_callback, callback) {
            var module_name, mountpoint, pass_parent, target_mod, _base;
            if (mountpoint_or_callback == null) mountpoint_or_callback = null;
            if (callback == null) callback = null;
            if (mountpoint_or_callback != null) {
              if (typeof mountpoint_or_callback === 'function') {
                callback = mountpoint_or_callback;
                mountpoint = null;
              } else {
                mountpoint = mountpoint_or_callback;
              }
            }
            if (mountpoint != null) {
              if (!(_this[mountpoint] != null)) _this[mountpoint] = {};
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
                target_mod = new module(_this, mountpoint, window);
                mountpoint[module_name] = target_mod;
                _this.sys.state.modules[module_name] = {
                  module: target_mod,
                  classes: {}
                };
              } else {
                target_mod = new module(_this, window);
                mountpoint[module_name] = target_mod;
                _this.sys.state.modules[module_name] = {
                  module: target_mod,
                  classes: {}
                };
              }
            }
            if (typeof (_base = mountpoint[module_name])._init === "function") {
              _base._init(_this);
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
            if (callback != null) callback(target_mod);
            return target_mod;
          }
        },
        libraries: {
          install: function(name, library, callback) {
            if (callback == null) callback = null;
            _this.lib[name.toLowerCase()] = library;
            _this.sys.state.integrations.push(name.toLowerCase());
            _this.dev.verbose('LibLoader', name + ' detected.');
            _this.events.trigger('SYS_LIB_LOADED', {
              name: name,
              library: library
            });
            if (callback != null) callback(library, name);
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
            if (callback == null) callback = null;
            _this.sys.drivers[type][name] = {
              name: name,
              driver: mountpoint,
              enabled: enabled,
              priority: priority,
              interface: adapter
            };
            if (callback != null) callback(_this.sys.drivers[type][name].driver);
            _this.events.trigger('SYS_DRIVER_LOADED', _this.sys.drivers[type][name]);
            return _this.sys.drivers[type][name];
          },
          resolve: function(type, name, strict) {
            var driver, priority_state, selected_driver;
            if (name == null) name = null;
            if (strict == null) strict = false;
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
        _ref2 = window.__apptools_preinit.deferred_core_modules;
        for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
          module = _ref2[_i];
          if (module.package != null) {
            this.sys.modules.install(module.module, module.package);
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
