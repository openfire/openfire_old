(function() {
  var ActivityGraph, ActivityItem, Asset, AuthController, Back, Follow, Goal, Key, MediaError, Openfire, OpenfireController, OpenfireException, OpenfireObject, Project, ProjectAvatar, ProjectCard, ProjectController, ProjectEditError, ProjectImage, ProjectVideo, Proposal, ProposalController, Session, Tier, Update, User, UserController, UserPermissionsError, Util,
    __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  ActivityGraph = (function() {

    function ActivityGraph(graphId, graphType) {
      this.graphId = graphId;
      this.graphType = graphType;
      this.setup_bar();
      this.setup_bubble();
      this.setup_line();
    }

    ActivityGraph.prototype.setup_bar = function() {
      var chart, data, x, y;
      data = [1, 2, 4, 8, 9, 10, 14, 17];
      x = d3.scale.linear().domain([0, d3.max(data)]).range([0, 420]);
      y = d3.scale.ordinal().domain(data).rangeBands([0, 120]);
      chart = d3.select("#spark-graph").append("svg").attr("class", "chart").attr("width", 250).attr("height", 140).append("g").attr("transform", "translate(10,15)");
      chart.selectAll("rect").data(data).enter().append("rect").attr("y", y).attr("width", x).attr("height", y.rangeBand());
      chart.selectAll("line").data(x.ticks(10)).enter().append("line").attr("x1", x).attr("x2", x).attr("y1", 0).attr("y2", 120).style("stroke", "#ccc");
      chart.selectAll("text").data(data).enter().append("text").attr("x", x).attr("y", function(d) {
        return y(d) + y.rangeBand() / 2;
      }).attr("dx", -3).attr("dy", ".35em").attr("text-anchor", "end").text(String).style("fill", "#fff");
      chart.selectAll(".rule").data(x.ticks(10)).enter().append("text").attr("class", "rule").attr("x", x).attr("y", 0).attr("dy", -3).attr("text-anchor", "middle").text(String).style("fill", "#000");
      return chart.append("line").attr("y1", 0).attr("y2", 120).style("stroke", "#000");
    };

    ActivityGraph.prototype.setup_bubble = function() {
      var chart, d, x, y, _results;
      chart = d3.select("#category-graph").append("svg").attr("class", "bubble").attr("width", 250).attr("height", 140);
      _results = [];
      for (d = 0; d < 10; d++) {
        x = Math.floor(Math.random() * 200);
        y = Math.floor(Math.random() * 140);
        chart.append("circle").attr("r", Math.floor(Math.random() * 30)).attr("cx", x).attr("cy", y).attr("fill", "SteelBlue");
        _results.push(chart.append("text").attr("dx", x).attr("dy", y).text(Math.floor(Math.random() * 100)));
      }
      return _results;
    };

    ActivityGraph.prototype.setup_line = function() {
      var data, g, graph, h, i, line, margin, w, x, y;
      data = (function() {
        var _results;
        _results = [];
        for (i = 0; i < 10; i++) {
          _results.push(Math.floor(Math.random() * 50));
        }
        return _results;
      })();
      w = 250;
      h = 140;
      margin = 20;
      y = d3.scale.linear().domain([0, d3.max(data)]).range([0 + margin, h - margin]);
      x = d3.scale.linear().domain([0, data.length]).range([0 + margin, w - margin]);
      graph = d3.select("#backers-graph").append("svg:svg").attr("width", w).attr("height", h);
      g = graph.append("svg:g").attr("transform", "translate(0, 140)");
      line = d3.svg.line().x(function(d, i) {
        return x(i);
      }).y(function(d) {
        return -1 * y(d);
      });
      g.append("svg:path").attr("d", line(data));
      g.append("svg:line").attr("x1", x(0)).attr("y1", -1 * y(0)).attr("x2", x(w)).attr("y2", -1 * y(0));
      g.append("svg:line").attr("x1", x(0)).attr("y1", -1 * y(0)).attr("x2", x(0)).attr("y2", -1 * y(d3.max(data)));
      g.selectAll(".xLabel").data(x.ticks(5)).enter().append("svg:text").attr("class", "xLabel").text(String).attr("x", function(d) {
        return x(d);
      }).attr("y", 0).attr("text-anchor", "middle");
      g.selectAll(".yLabel").data(y.ticks(4)).enter().append("svg:text").attr("class", "yLabel").text(String).attr("x", 0).attr("text-anchor", "right").attr("dy", 4..attr("y", function(d) {
        return -1 * y(d);
      }));
      g.selectAll(".xTicks").data(x.ticks(5)).enter().append("svg:line").attr("class", "xTicks").attr("x1", function(d) {
        return x(d);
      }).attr("y1", -1 * y(0)).attr("x2", function(d) {
        return x(d);
      }).attr("y2", -1 * y(-0.3));
      return g.selectAll(".yTicks").data(y.ticks(4)).enter().append("svg:line").attr("class", "yTicks").attr("y1", function(d) {
        return -1 * y(d);
      }).attr("x1", x(-0.3)).attr("y2", function(d) {
        return -1 * y(d);
      }).attr("x2", x(0));
    };

    return ActivityGraph;

  })();

  window.ActivityGraph = ActivityGraph;

  if (this.__openfire_preinit != null) {
    this.__openfire_preinit.abstract_base_objects = [];
    this.__openfire_preinit.abstract_base_classes = [];
    this.__openfire_preinit.abstract_base_controllers = [];
  } else {
    this.__openfire_preinit = {
      abstract_base_objects: [],
      abstract_base_classes: [],
      abstract_base_controllers: []
    };
  }

  OpenfireObject = (function(_super) {

    __extends(OpenfireObject, _super);

    function OpenfireObject() {
      OpenfireObject.__super__.constructor.apply(this, arguments);
    }

    return OpenfireObject;

  })(CoreObject);

  OpenfireController = (function() {

    function OpenfireController() {}

    return OpenfireController;

  })();

  OpenfireException = (function(_super) {

    __extends(OpenfireException, _super);

    function OpenfireException(controller, message) {
      this.controller = controller;
      this.message = message;
    }

    OpenfireException.prototype.toString = function() {
      return '[' + this.controller + '] OpenfireException: ' + this.message;
    };

    return OpenfireException;

  })(Error);

  MediaError = (function(_super) {

    __extends(MediaError, _super);

    function MediaError() {
      MediaError.__super__.constructor.apply(this, arguments);
    }

    return MediaError;

  })(OpenfireException);

  UserPermissionsError = (function(_super) {

    __extends(UserPermissionsError, _super);

    function UserPermissionsError() {
      UserPermissionsError.__super__.constructor.apply(this, arguments);
    }

    return UserPermissionsError;

  })(OpenfireException);

  ProjectEditError = (function(_super) {

    __extends(ProjectEditError, _super);

    function ProjectEditError() {
      ProjectEditError.__super__.constructor.apply(this, arguments);
    }

    return ProjectEditError;

  })(OpenfireException);

  Util = new window.Util();

  this.__openfire_preinit.abstract_base_objects.push(OpenfireObject);

  this.__openfire_preinit.abstract_base_controllers.push(OpenfireController);

  this.__openfire_preinit.abstract_base_classes.push(OpenfireException);

  this.__openfire_preinit.abstract_base_classes.push(MediaError);

  this.__openfire_preinit.abstract_base_classes.push(UserPermissionsError);

  Key = (function() {

    function Key(key) {
      this.key = key;
      return this;
    }

    return Key;

  })();

  ProjectCard = (function() {

    function ProjectCard() {}

    ProjectCard.prototype.name = String();

    ProjectCard.prototype.project = Key();

    ProjectCard.prototype.progress = String();

    ProjectCard.prototype.backer_count = Number();

    ProjectCard.prototype.met = Boolean();

    return ProjectCard;

  })();

  ActivityItem = (function() {

    function ActivityItem() {}

    ActivityItem.prototype.timestamp = Date();

    ActivityItem.prototype.project = Key();

    return ActivityItem;

  })();

  Follow = (function(_super) {

    __extends(Follow, _super);

    function Follow() {
      Follow.__super__.constructor.apply(this, arguments);
    }

    Follow.prototype.username = String();

    Follow.prototype.project = Key();

    Follow.prototype.timestamp = Date();

    return Follow;

  })(ActivityItem);

  Back = (function(_super) {

    __extends(Back, _super);

    function Back() {
      Back.__super__.constructor.apply(this, arguments);
    }

    Back.prototype.username = String();

    Back.prototype.project = Key();

    Back.prototype.timestamp = Date();

    return Back;

  })(ActivityItem);

  Update = (function(_super) {

    __extends(Update, _super);

    function Update() {
      Update.__super__.constructor.apply(this, arguments);
    }

    Update.prototype.username = String();

    Update.prototype.text = String();

    Update.prototype.timestamp = Date();

    Update.prototype.project = Key();

    return Update;

  })(ActivityItem);

  Asset = (function() {

    function Asset(hash) {
      var prop, val;
      if ((hash != null) && Util.is_object(hash)) {
        for (prop in hash) {
          val = hash[prop];
          this[prop] = val;
        }
      }
      return this;
    }

    return Asset;

  })();

  Session = (function(_super) {

    __extends(Session, _super);

    Session["export"] = 'private';

    Session.events = ['SESSION_START', 'SESSION_ENDED'];

    function Session(openfire) {
      var _this = this;
      this._state = {
        status: null,
        init: false
      };
      this.internal = {
        resolve_storage_driver: function() {
          return storage;
        },
        provision_token: function() {
          return token;
        }
      };
      this.start = function() {
        return session;
      };
      this.end = function() {};
    }

    return Session;

  })(OpenfireObject);

  User = (function(_super) {

    __extends(User, _super);

    User["export"] = 'private';

    User.events = [];

    function User(openfire) {
      return;
    }

    return User;

  })(OpenfireObject);

  AuthController = (function(_super) {

    __extends(AuthController, _super);

    AuthController.events = [];

    function AuthController(openfire, window) {
      var _this = this;
      this._state = {
        init: false
      };
      this.internal = {
        session: {
          open: function() {
            var s;
            return (s = new Session()).start();
          },
          close: function(session) {
            return session.end();
          }
        }
      };
      this.login = function() {};
      this.create_user = function() {};
      this._init = function() {};
    }

    return AuthController;

  })(OpenfireController);

  if (this.__openfire_preinit != null) {
    this.__openfire_preinit.abstract_base_objects.push(Session);
    this.__openfire_preinit.abstract_base_classes.push(User);
    this.__openfire_preinit.abstract_base_controllers.push(AuthController);
  }

  UserController = (function(_super) {

    __extends(UserController, _super);

    UserController.events = [];

    function UserController(openfire, window) {
      var _this = this;
      this._init = function() {};
      return;
    }

    return UserController;

  })(OpenfireController);

  if (this.__openfire_preinit != null) {
    this.__openfire_preinit.abstract_base_controllers.push(UserController);
  }

  ProjectImage = (function(_super) {

    __extends(ProjectImage, _super);

    function ProjectImage() {
      ProjectImage.__super__.constructor.apply(this, arguments);
    }

    return ProjectImage;

  })(Asset);

  ProjectVideo = (function(_super) {

    __extends(ProjectVideo, _super);

    function ProjectVideo() {
      ProjectVideo.__super__.constructor.apply(this, arguments);
    }

    return ProjectVideo;

  })(Asset);

  ProjectAvatar = (function(_super) {

    __extends(ProjectAvatar, _super);

    function ProjectAvatar() {
      ProjectAvatar.__super__.constructor.apply(this, arguments);
    }

    return ProjectAvatar;

  })(Asset);

  Goal = (function() {

    function Goal() {
      var _this = this;
      this.from_message = function(message) {
        return Util.extend(true, _this, message);
      };
      this.to_message = function() {
        var message, prop, val;
        message = {};
        for (prop in _this) {
          if (!__hasProp.call(_this, prop)) continue;
          val = _this[prop];
          message[prop] = val;
        }
        return message;
      };
    }

    return Goal;

  })();

  Tier = (function() {

    function Tier() {
      var _this = this;
      this.from_message = function(message) {
        return Util.extend(true, _this, message);
      };
      this.to_message = function() {
        var message, prop, val;
        message = {};
        for (prop in _this) {
          if (!__hasProp.call(_this, prop)) continue;
          val = _this[prop];
          message[prop] = val;
        }
        return message;
      };
    }

    return Tier;

  })();

  Project = (function() {

    Project.prototype.model = {
      name: String(),
      status: String(),
      category: String(),
      summary: String(),
      pitch: String(),
      tech: String(),
      keywords: Array(),
      creator: String(),
      owners: Array(),
      goals: Array(),
      tiers: Array()
    };

    function Project(key) {
      var _this = this;
      this.key = key;
      this.assets = {
        store: [],
        index: {}
      };
      this.goals = {
        store: [],
        index: {}
      };
      this.tiers = {
        store: [],
        index: {}
      };
      this.attach = function(kind, obj) {
        var idx, item, new_store, old_store, _i, _len, _ns;
        if ((obj != null) && (kind != null)) {
          if (_this[kind] != null) {
            key = obj.key;
            if (_this[kind].index[key] != null) {
              idx = _this[kind].index[key];
              old_store = _this[kind].store;
              new_store = old_store.slice(0, idx);
              (_ns = old_store.slice(idx + 1)).unshift(obj);
              for (_i = 0, _len = _ns.length; _i < _len; _i++) {
                item = _ns[_i];
                new_store.push(item);
              }
              _this[kind].store = new_store;
              return obj;
            } else {
              return _this[kind].index[key] = _this[kind].store.push(obj) - 1;
            }
          } else {
            throw 'Invalid project store specified for attach()ment';
          }
        } else {
          throw 'Too few arguments passed to attach(): function(store_name, object_to_store){}';
        }
      };
      this.from_message = function(message) {
        var key, model, validate, value;
        model = _this.prototype.model;
        validate = function(k, v) {
          if ((k != null) && (v != null)) {
            if (!(k in model)) return false;
            if (v.constructor.name !== model[k].constructor.name) return false;
            return true;
          } else {
            throw 'Too few arguments passed to validate(): function(key, value){}';
          }
        };
        for (key in message) {
          if (!__hasProp.call(message, key)) continue;
          value = message[key];
          if (validate(key, value)) _this[key] = value;
        }
        return _this;
      };
      this.to_message = function() {
        var message, prop, val;
        message = {};
        for (prop in _this) {
          if (!__hasProp.call(_this, prop)) continue;
          val = _this[prop];
          message[prop] = val;
        }
        return message;
      };
      this.get = function(callback) {
        return $.apptools.api.project.get({
          key: _this.key
        }).fulfill({
          success: function(response) {
            if (callback != null) {
              return typeof callback === "function" ? callback(_this.from_message(response)) : void 0;
            } else {
              return _this.from_message(response);
            }
          },
          failure: function(error) {
            return alert('project get() failure');
          }
        });
      };
      this.get_attached = function(kind, key, index_only) {
        var idx, _i;
        if (index_only == null) index_only = false;
        if ((key != null) && (_this[kind] != null)) {
          if ((_i = parseInt(key, 10)) > 0 || _i < 0 || _i === 0) {
            return _this[kind].store[_i] || false;
          }
          if ((idx = _this[kind].index[key]) != null) {
            if (index_only) {
              return idx;
            } else {
              return _this[kind].store[idx];
            }
          } else {
            return false;
          }
        } else {
          throw 'Too few arguments passed to get_attached(): function(store_name, index){}';
        }
      };
    }

    return Project;

  })();

  Proposal = (function() {

    Proposal.prototype.model = null;

    function Proposal(key) {
      this.key = key;
      return this;
    }

    return Proposal;

  })();

  ProjectController = (function(_super) {

    __extends(ProjectController, _super);

    ProjectController.mount = 'project';

    ProjectController.events = ['PROJECT_CONTROLLER_READY', 'PROJECT_CONTROLLER_INIT', 'PROJECT_MEDIA_ADDED', 'PROJECT_AVATAR_ADDED', 'PROJECT_BACKED', 'PROJECT_EDITED', 'PROJECT_FOLLOWED', 'PROJECT_READY', 'PROJECT_SHARED', 'PROJECT_UPDATED'];

    function ProjectController(openfire) {
      var _this = this;
      this._state = Util.extend(true, {}, window._cp);
      this.project = new Project(this._state.ke);
      this.project_key = this.project.key;
      this.add_media = function(file_or_url, kind) {
        var choice, e, fi, file, files, filetype, reader, url, _i, _len;
        if (_this._state.o) {
          if (file_or_url.preventDefault) {
            file_or_url.preventDefault();
            file_or_url.stopPropagation();
            e = file_or_url;
            files = e.dataTransfer.files;
            if (files != null) {
              for (_i = 0, _len = files.length; _i < _len; _i++) {
                fi = files[_i];
                return _this.add_media(fi, 'image');
              }
            }
          }
          if (file_or_url.size && file_or_url.type) {
            file = file_or_url;
            filetype = file.type;
            console.log('Received dropped ', filetype);
            reader = new FileReader();
            reader.file = file;
            reader.onloadend = function(e) {
              e.preventDefault();
              e.stopPropagation();
              return Util.get('project-image-drop-preview').setAttribute('src', e.target.result);
            };
            choice = $.apptools.widgets.modal.create((function() {
              var docfrag;
              docfrag = Util.create_doc_frag((function() {
                return Util.create_element_string('div', {
                  id: 'project-image-drop-choice',
                  style: 'width: 100%;margin: 0 auto;opacity: 0;text-align: center;background-color: #eee;font-size: 9pt;',
                  "class": 'pre-modal',
                  "data-title": 'Hey, you dropped your photo!'
                }).split('*').join([
                  '', Util.create_element_string('img', {
                    id: 'project-image-drop-preview',
                    style: 'max-width: 140px;',
                    "class": 'dropshadow'
                  }), '', '', '<span style="font-size: 14px; font-weight: bolder;">My, that looks nice.</span>', '', '', '', 'Would you like to attach "' + file.name + '" to your project?', '', '', [
                    Util.create_element_string('button', {
                      id: 'project-image-drop-avatar',
                      "class": 'rounded',
                      value: 'avatar'
                    }).split('*').join('yes!<br>(as an avatar)'), Util.create_element_string('button', {
                      id: 'project-image-drop-image',
                      "class": 'rounded',
                      value: 'image'
                    }).split('*').join('yes!<br>(as an image)'), Util.create_element_string('button', {
                      id: 'project-image-drop-no',
                      "class": 'rounded',
                      value: 'no'
                    }).split('*').join('oops!<br>(no thanks)')
                  ].join('')
                ].join('<br>'));
              })());
              document.body.appendChild(docfrag);
              return document.getElementById('project-image-drop-choice');
            })(), (function() {
              var docfrag;
              docfrag = Util.create_doc_frag((function() {
                return Util.create_element_string('a', {
                  id: 'a-project-image-drop-choice',
                  href: '#project-image-drop-choice',
                  style: 'display: none;'
                });
              })());
              document.body.appendChild(docfrag);
              return document.getElementById('a-project-image-drop-choice');
            })(), function(m) {
              return m.open();
            }, {
              initial: {
                width: '0px',
                height: '0px',
                bottom: '60px',
                right: '60px'
              },
              ratio: {
                x: 0.3,
                y: 0.5
              },
              calc: function() {
                var css, mH, mW, r, wH, wW;
                css = {};
                r = this.ratio;
                wW = window.innerWidth;
                wH = window.innerHeight;
                mW = Math.floor(r.x * wW);
                mH = Math.floor(r.y * wH);
                css.width = mW + 'px';
                css.height = mH + 'px';
                css.bottom = this.initial.bottom;
                css.right = this.initial.right;
                return css;
              }
            });
            if (/^image\/(png|jpeg|gif)$/gi.test(filetype)) {
              reader.readAsDataURL(file);
              Util.get('project-image-drop-image').addEventListener('click', function(e) {
                var btn, callback;
                if (e.preventDefault) {
                  e.preventDefault();
                  e.stopPropagation();
                }
                (btn = e.target).innerHTML = 'Great!<br>Uploading...';
                callback = function(res) {
                  console.log('attach_image() callback reached!');
                  console.log('callback response: ', res);
                  _this.project.attach(new ProjectImage(res));
                  $.apptools.events.trigger('PROJECT_MEDIA_ADDED', _this);
                  btn.style.backgroundColor = '#bada55';
                  btn.innerHTML = 'Awesome!<br>Good to go.';
                  return _this;
                };
                return $.apptools.api.media.attach_image({
                  target: _this.project_key,
                  size: file.size,
                  name: file.name
                }).fulfill({
                  success: function(response) {
                    var uploader;
                    if (!(_this.uploader != null)) {
                      uploader = $.apptools.widgets.uploader.create('data', {
                        id: 'body',
                        endpoints: [response.endpoint],
                        finish: callback
                      });
                      _this.uploader = uploader;
                    } else {
                      uploader = _this.uploader.add_endpoint(response.endpoint);
                      uploader = uploader.add_callback(callback);
                    }
                    return uploader.upload(file);
                  },
                  failure: function(error) {
                    btn.style.backgroundColor = '#ee9099';
                    btn.innerHTML = 'Bummer!<br> :(';
                    return alert('uploaded attach_image() failure');
                  }
                });
              }, false);
              Util.get('project-image-drop-avatar').addEventListener('click', function(e) {
                var btn, callback;
                if (e.preventDefault) {
                  e.preventDefault();
                  e.stopPropagation();
                }
                (btn = e.target).innerHTML = 'Great!<br>Uploading...';
                callback = function(res) {
                  console.log('attach_image() callback reached!');
                  console.log('callback response: ', res);
                  _this.project.attach(new ProjectAvatar(res));
                  $.apptools.events.trigger('PROJECT_AVATAR_ADDED', _this);
                  btn.style.backgroundColor = '#bada55';
                  return btn.innerHTML = 'Awesome!<br>Good to go.';
                };
                return $.apptools.api.media.attach_avatar({
                  target: _this.project_key,
                  size: file.size,
                  name: file.name
                }).fulfill({
                  success: function(response) {
                    var uploader;
                    if (!(_this.uploader != null)) {
                      uploader = $.apptools.widgets.uploader.create('data', {
                        id: 'body',
                        endpoints: [response.endpoint],
                        finish: callback
                      });
                      _this.uploader = uploader;
                    } else {
                      uploader = _this.uploader.add_endpoint(response.endpoint);
                      uploader = uploader.add_callback(callback);
                    }
                    return uploader.upload(file);
                  },
                  failure: function(error) {
                    btn.style.backgroundColor = '#ee9099';
                    btn.innerHTML = 'Bummer!<br> :(';
                    return alert('uploaded attach_avatar() failure');
                  }
                });
              }, false);
              Util.get('project-image-drop-no').addEventListener('click', function(e) {
                if (e.preventDefault) {
                  e.preventDefault();
                  e.stopPropagation();
                }
                return $.apptools.widgets.modal.get('project-image-drop-choice').close();
              }, false);
            } else {
              throw new MediaError(_this.constructor.name, 'Tried to upload unsupported filetype. Images must be .jpg, .png, or .gif.');
            }
          } else {
            url = file_or_url;
            console.log('received url to attach: ', url);
            if (kind === 'image') {
              return $.apptools.api.media.attach_image({
                intake: 'url',
                target: _this.project_key
              }).fulfill({
                success: function(response) {
                  _this.project.attach(new Image(response.media_key, response.serve_url));
                  return $.apptools.events.trigger('PROJECT_MEDIA_ADDED', _this);
                },
                failure: function(error) {
                  return alert('url-linked attach_image() failure');
                }
              });
            } else if (kind === 'video') {
              return $.apptools.api.media.attach_video({
                reference: url,
                target: _this.project_key
              }).fulfill({
                success: function(response) {
                  _this.project.attach(new Video(response.media_key, response.serve_url));
                  return $.apptools.events.trigger('PROJECT_MEDIA_ADDED', _this);
                },
                failure: function(error) {
                  return alert('attach_video() failure');
                }
              });
            } else {
              throw new MediaError(_this.constructor.name, 'Unrecognized media kind linked.');
            }
          }
        } else {
          throw new UserPermissionsError(_this.constructor.name, 'Current user is not a project owner.');
        }
      };
      this.back = function() {
        return $.apptools.api.project.back({
          target: _this.project_key
        }).fulfill({
          success: function(response) {
            return $('#back-text').animate({
              opacity: 0
            }, {
              duration: 250,
              complete: function() {
                document.getElementById('back-text').innerHTML = 'you rock.';
                document.getElementById('back').classList.add('backed');
                return $('#back-text').animate({
                  opacity: 1
                }, {
                  duration: 250,
                  complete: function() {
                    return alert('back() success');
                  }
                });
              }
            });
          },
          failure: function(error) {
            return alert('back() failure');
          }
        });
      };
      this.edit = function() {};
      this.edit_tier = function() {
        return _this.tiers.edit.apply(_this, arguments);
      };
      this.edit_goal = function() {
        return _this.tiers.edit.apply(_this, arguments);
      };
      this.follow = function() {
        return $.apptools.api.project.follow({
          target: _this.project_key
        }).fulfill({
          success: function(response) {
            document.getElementById('follow').classList.add('following');
            return alert('follow() success');
          },
          failure: function(error) {
            return alert('follow() failure');
          }
        });
      };
      this.get = function(refresh, callback) {
        if (!(refresh != null)) {
          refresh = false;
        } else if (typeof refresh !== 'boolean') {
          if (callback == null) callback = refresh;
          refresh = false;
        }
        if (typeof callback !== 'function') callback = null;
        if (refresh) {
          return _this.project.get(callback);
        } else if (callback != null) {
          return typeof callback.call === "function" ? callback.call(_this, _this.project) : void 0;
        } else {
          return _this.project;
        }
      };
      this.get_backers = function() {
        return $.apptools.api.project.backers({
          target: _this.project_key
        }).fulfill({
          success: function(response) {
            return alert('get_backers() success');
          },
          failure: function(error) {
            return alert('get_backers() failure');
          }
        });
      };
      this.get_followers = function() {
        return $.apptools.api.project.followers({
          target: _this.project_key
        }).fulfill({
          success: function(response) {
            return alert('get_followers() success');
          },
          failure: function(error) {
            return alert('get_followers() failure');
          }
        });
      };
      this.get_updates = function() {
        return $.apptools.api.project.posts({
          target: _this.project_key
        }).fulfill({
          success: function(response) {
            return alert('get_updates() success');
          },
          failure: function(error) {
            return alert('get_updates() failure');
          }
        });
      };
      this.goals = {
        get: function(goal_key, callback) {
          var idx;
          if (goal_key === false) {
            goal_key = callback;
            idx = _this.project.goals_by_key[goal_key];
            if (idx) {
              return _this.project.goals[idx];
            } else {
              return null;
            }
          } else {
            return $.apptools.api.project.get_goal({
              key: goal_key
            }).fulfill({
              success: function(response) {
                var goal;
                goal = _this.project.attach('goal', new Goal().from_message(response.goal));
                if (callback != null) {
                  return callback.call(_this, goal);
                } else {
                  return goal;
                }
              },
              failure: function(error) {
                return alert('goals.get() failure');
              }
            });
          }
        },
        list: function(callback) {
          return $.apptools.api.project.list_goals({
            project: _this.project_key
          }).fulfill({
            success: function(response) {
              var goal, goals, _at, _i, _len, _ref;
              goals = [];
              _at = function(_g) {
                var _goal;
                _goal = new Goal();
                _goal = _goal.from_message(_g);
                _this.project.attach('goals', _goal);
                return _goal;
              };
              _ref = response.goals;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                goal = _ref[_i];
                goals.push(_at(goal));
              }
              if (callback != null) {
                return callback.call(_this, goals);
              } else {
                return goals;
              }
            },
            failure: function(error) {
              alert('goals.list() failure');
              return console.log('Error listing goals: ' + error);
            }
          });
        },
        put: function(goal, callback) {
          return $.apptools.api.project.put_goal(goal.to_message()).fulfill({
            success: function(response) {
              alert('goals.put() success');
              if (callback != null) {
                return callback.call(_this, response);
              } else {
                return response.key;
              }
            },
            failure: function(error) {
              return alert('goals.put() failure');
            }
          });
        },
        "delete": function(goal_key, callback) {
          return $.apptools.api.project.delete_goal({
            key: goal_key
          }).fulfill({
            success: function(response) {
              alert('goals.delete() success');
              if (callback != null) {
                return callback.call(_this, response);
              } else {
                return response.key;
              }
            },
            failure: function(error) {
              return alert('goals.delete() failure');
            }
          });
        },
        edit: function(goal_or_key) {
          var base_el, base_id;
          base_id = 'project-goal-editor';
          base_el = null;
          return _this.goals.list(function(goals) {
            var _idx, _key, _pk;
            _pk = _this.project_key;
            _idx = null;
            _key = null;
            $.apptools.widgets.modal.create((function() {
              document.body.appendChild(Util.create_doc_frag(Util.create_element_string('div', {
                id: base_id,
                "class": 'pre-modal',
                style: 'opacity: 0;',
                'data-title': 'editing project goals...'
              }, (function(goal_div) {
                var g, _i, _len;
                if (goal_div == null) goal_div = '';
                for (_i = 0, _len = goals.length; _i < _len; _i++) {
                  g = goals[_i];
                  goal_div += Util.create_element_string('div', {
                    id: 'goal-editing-' + (function() {
                      var go;
                      go = _this.project.attach('goals', g);
                      _idx = _this.project.get_attached('goals', go.key, true);
                      return _idx;
                    })(),
                    "class": 'mini-editable goal'
                  }, (function(parts) {
                    if (parts == null) parts = '';
                    parts += Util.create_element_string('h3', {
                      "class": 'goal-field amount',
                      id: 'goal-amount-' + _idx,
                      contenteditable: true
                    }, g.amount);
                    parts += Util.create_element_string('p', {
                      "class": 'rounded goal-field description',
                      id: 'goal-description-' + _idx,
                      contenteditable: true
                    }, (g.description != null ? g.description : '<span class="shh">default description</span>'));
                    parts += Util.create_element_string('button', {
                      id: 'goal-save-' + _idx,
                      "class": 'goal-button save'
                    }, 'save goal');
                    parts += Util.create_element_string('button', {
                      id: 'goal-get-' + _idx,
                      "class": 'goal-button get'
                    }, 'refresh goal');
                    parts += Util.create_element_string('button', {
                      id: 'goal-delete-' + _idx,
                      "class": 'goal-button delete'
                    }, 'delete goal');
                    return parts;
                  })());
                }
                return goal_div;
              })())));
              return document.getElementById(base_id);
            })(), (function() {
              document.body.appendChild(Util.create_doc_frag(Util.create_element_string('a', {
                id: 'a-' + base_id,
                href: '#' + base_id,
                style: 'display: none'
              }, '')));
              return document.getElementById('a-' + base_id);
            })(), function(m) {
              var editors, fields, goal_field, populate, _i, _len;
              editors = [];
              populate = function(gfield) {
                var close_x, editor, _el, _id;
                editor = $.apptools.widgets.editor.create(gfield);
                $.apptools.widgets.editor.enable(editor);
                _el = Util.get((_id = editor._state.element_id));
                _idx = _id.split('-').pop();
                document.getElementById('goal-save-' + _idx).addEventListener('click', function(e) {
                  var clicked, goal;
                  if ((e != null) && e.preventDefault) {
                    e.preventDefault();
                    e.stopPropagation();
                    clicked = e.target;
                    _idx = clicked != null ? clicked.getAttribute('id').split('-').pop() : void 0;
                    goal = _this.project.get_attached('goals', _idx);
                    _key = goal.key;
                  }
                  goal.target = _this.project_key;
                  goal.amount = parseInt(document.getElementById('goal-amount-' + _idx).innerHTML);
                  goal.description = document.getElementById('goal-description-' + _idx).innerHTML;
                  if (!(goal.amount != null) || !(goal.description != null)) {
                    return false;
                  }
                  return $.apptools.api.project.put_goal(goal).fulfill({
                    success: function(response) {
                      _el.style.backgroundColor = '#bada55';
                      if (clicked != null) clicked.classList.add('success');
                      setTimeout(function() {
                        return $(_el).animate({
                          'background-color': 'transparent'
                        }, {
                          duration: 300,
                          complete: function() {
                            return editor.hide();
                          }
                        });
                      }, 200);
                      return _this.project.attach('goals', goal.from_message(response));
                    },
                    failure: function(error) {
                      _el.style.backgroundColor = 'red';
                      clicked.classList.add('failure');
                      return alert('goal put() failure');
                    }
                  });
                }, false);
                (close_x = document.getElementById(base_id + '-modal-close')).removeEventListener('mousedown');
                close_x.addEventListener('click', function() {
                  return m.close(function(_m) {
                    return $.apptools.widgets.modal.destroy(_m);
                  });
                }, false);
                document.getElementById('goal-get-' + _idx).addEventListener('click', function(e) {
                  var clicked, goal;
                  if (e != null ? e.preventDefault : void 0) {
                    e.preventDefault();
                    e.stopPropagation();
                    clicked = e.target;
                    _idx = clicked != null ? clicked.getAttribute('id').split('-').pop() : void 0;
                    goal = _this.project.get_attached('goals', _idx);
                    _key = goal.key;
                  }
                  return _this.goals.get(_key, function(gol) {
                    document.getElementById('goal-amount-' + _idx).innerHTML = gol.amount;
                    document.getElementById('goal-description-' + _idx).innerHTML = gol.description;
                    return _this.project.attach('goals', gol);
                  });
                }, false);
                document.getElementById('goal-delete-' + _idx).addEventListener('click', function(e) {
                  var clicked, goal;
                  if (e != null ? e.preventDefault : void 0) {
                    e.preventDefault();
                    e.stopPropagation();
                    clicked = e.target;
                    _idx = clicked != null ? clicked.getAttribute('id').split('-').pop() : void 0;
                    goal = _this.project.get_attached('goals', _idx);
                    _key = goal.key;
                  }
                  return _this.goals["delete"](_key);
                }, false);
                return editor;
              };
              if ((fields = Util.get('goal', document.getElementById(base_id + '-modal-content'))) != null) {
                for (_i = 0, _len = fields.length; _i < _len; _i++) {
                  goal_field = fields[_i];
                  editors.push(populate(goal_field));
                }
              }
              return m.open();
            }, {
              initial: {
                width: '0px',
                height: '0px',
                bottom: '60px',
                right: '60px'
              },
              ratio: {
                x: 0.3,
                y: 0.5
              },
              calc: function() {
                var css, mH, mW, r, wH, wW;
                css = {};
                r = this.ratio;
                wW = window.innerWidth;
                wH = window.innerHeight;
                mW = Math.floor(r.x * wW);
                mH = Math.floor(r.y * wH);
                css.width = mW + 'px';
                css.height = mH + 'px';
                css.bottom = this.initial.bottom;
                css.right = this.initial.right;
                return css;
              }
            });
            return _this;
          });
          /* end current edit functionality - below code is future-planned, thanks to bugs :(
          
          # extract goal & key from params
          if goal_or_key.key.key
              # we got a goal
              goal = goal_or_key
              goal_key = goal.key
              goals = [goal]
          
          else if goal_or_key.key and goal_or_key.constructor.name is 'Key'
          
              goal_key = goal_or_key
              goal = @goals.get(goal_key)
              goals = [goal]
          
          
          goal_editor.steps = []
          goal_editor._state.current = 0
          goal_editor.step = (incr, callback) ->
              if not incr?
                  incr = 1
          
              current_idx = @_state.current
              current_step = @steps[current_idx]
              next_step = @steps[current_idx + incr]
          
              $(current_step).animate opacity: 0
                  duration: 250
                  complete: () =>
                      $(next_step).animate opacity: 1
                          duration: 200
                          complete: () =>
                              @_state.current += incr
                              return if callback? then callback?(next_step) else @
          */
        }
      };
      this.share = function(sm_service) {
        return alert('Testing social sharing!');
      };
      this.tiers = {
        get: function(tier_key, callback) {
          var idx;
          if (tier_key === false) {
            tier_key = callback;
            idx = _this.project.tiers_by_key[tier_key];
            if (idx) {
              return _this.project.tiers[idx];
            } else {
              return null;
            }
          } else {
            return $.apptools.api.project.get_tier({
              key: tier_key
            }).fulfill({
              success: function(response) {
                var tier;
                tier = _this.project.attach('tier', new Tier().from_message(response.tier));
                if (callback != null) {
                  return callback.call(_this, tier);
                } else {
                  return tier;
                }
              },
              failure: function(error) {
                return alert('tiers.get() failure');
              }
            });
          }
        },
        list: function(callback) {
          return $.apptools.api.project.list_tiers({
            project: _this.project_key
          }).fulfill({
            success: function(response) {
              var tier, tiers, _at, _i, _len, _ref;
              tiers = [];
              _at = function(_t) {
                var _tier;
                _tier = new Tier();
                _tier = _tier.from_message(_t);
                _this.project.attach('tiers', _tier);
                return _tier;
              };
              _ref = response.tiers;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                tier = _ref[_i];
                tiers.push(_at(tier));
              }
              if (callback != null) {
                return callback.call(_this, tiers);
              } else {
                return tiers;
              }
            },
            failure: function(error) {
              alert('tiers.list() failure');
              return console.log('Error listing tiers: ' + error);
            }
          });
        },
        put: function(tier, callback) {
          return $.apptools.api.project.put_tier(tier.to_message()).fulfill({
            success: function(response) {
              alert('tiers.put() success');
              if (callback != null) {
                return callback.call(_this, response);
              } else {
                return response.key;
              }
            },
            failure: function(error) {
              return alert('tiers.put() failure');
            }
          });
        },
        "delete": function(tier_key, callback) {
          return $.apptools.api.project.delete_tier({
            key: tier_key
          }).fulfill({
            success: function(response) {
              alert('tiers.delete() success');
              if (callback != null) {
                return callback.call(_this, response);
              } else {
                return response.key;
              }
            },
            failure: function(error) {
              return alert('tiers.delete() failure');
            }
          });
        },
        edit: function(tier_or_key) {
          var base_el, base_id;
          base_id = 'project-tier-editor';
          base_el = null;
          return _this.tiers.list(function(tiers) {
            var _idx, _key, _pk;
            _pk = _this.project_key;
            _idx = null;
            _key = null;
            $.apptools.widgets.modal.create((function() {
              document.body.appendChild(Util.create_doc_frag(Util.create_element_string('div', {
                id: base_id,
                "class": 'pre-modal',
                style: 'opacity: 0;',
                'data-title': 'editing project tiers...'
              }, (function(tier_div) {
                var t, _i, _len;
                if (tier_div == null) tier_div = '';
                for (_i = 0, _len = tiers.length; _i < _len; _i++) {
                  t = tiers[_i];
                  tier_div += Util.create_element_string('div', {
                    id: 'tier-editing-' + (function() {
                      var ti;
                      ti = _this.project.attach('tiers', t);
                      _idx = _this.project.get_attached('tiers', ti.key, true);
                      return _idx;
                    })(),
                    "class": 'mini-editable tier'
                  }, (function(parts) {
                    if (parts == null) parts = '';
                    parts += Util.create_element_string('h3', {
                      "class": 'tier-field amount',
                      id: 'tier-amount-' + _idx,
                      contenteditable: true
                    }, t.amount);
                    parts += Util.create_element_string('p', {
                      "class": 'rounded tier-field description',
                      id: 'tier-description-' + _idx,
                      contenteditable: true
                    }, (t.description != null ? t.description : '<span class="shh">default description</span>'));
                    parts += Util.create_element_string('button', {
                      id: 'tier-save-' + _idx,
                      "class": 'tier-button save'
                    }, 'save tier');
                    parts += Util.create_element_string('button', {
                      id: 'tier-get-' + _idx,
                      "class": 'tier-button get'
                    }, 'refresh tier');
                    parts += Util.create_element_string('button', {
                      id: 'tier-delete-' + _idx,
                      "class": 'tier-button delete'
                    }, 'delete tier');
                    return parts;
                  })());
                }
                return tier_div;
              })())));
              return document.getElementById(base_id);
            })(), (function() {
              document.body.appendChild(Util.create_doc_frag(Util.create_element_string('a', {
                id: 'a-' + base_id,
                href: '#' + base_id,
                style: 'display: none'
              }, '')));
              return document.getElementById('a-' + base_id);
            })(), function(m) {
              var editors, fields, populate, tier_field, _i, _len;
              editors = [];
              populate = function(tfield) {
                var editor, _el, _id;
                editor = $.apptools.widgets.editor.create(tfield);
                $.apptools.widgets.editor.enable(editor);
                _el = Util.get((_id = editor._state.element_id));
                _idx = _id.split('-').pop();
                document.getElementById('tier-save-' + _idx).addEventListener('click', function(e) {
                  var clicked, tier;
                  if ((e != null) && e.preventDefault) {
                    e.preventDefault();
                    e.stopPropagation();
                    clicked = e.target;
                    _idx = clicked != null ? clicked.getAttribute('id').split('-').pop() : void 0;
                    tier = _this.project.get_attached('tiers', _idx);
                    _key = tier.key;
                  }
                  tier.target = _this.project_key;
                  tier.amount = parseInt(document.getElementById('tier-amount-' + _idx).innerHTML);
                  tier.description = document.getElementById('tier-description-' + _idx).innerHTML;
                  if (!(tier.amount != null) || !(tier.description != null)) {
                    return false;
                  }
                  return $.apptools.api.project.put_tier(tier).fulfill({
                    success: function(response) {
                      _el.style.backgroundColor = '#bada55';
                      if (clicked != null) clicked.classList.add('success');
                      setTimeout(function() {
                        return $(_el).animate({
                          'background-color': 'transparent'
                        }, {
                          duration: 300,
                          complete: function() {
                            return editor.hide();
                          }
                        });
                      }, 200);
                      return _this.project.attach('tiers', new tier.from_message(response));
                    },
                    failure: function(error) {
                      _el.style.backgroundColor = 'red';
                      clicked.classList.add('failure');
                      return alert('tier put() failure');
                    }
                  });
                }, false);
                document.getElementById('tier-get-' + _idx).addEventListener('click', function(e) {
                  var clicked, tier;
                  if (e != null ? e.preventDefault : void 0) {
                    e.preventDefault();
                    e.stopPropagation();
                    clicked = e.target;
                    _idx = clicked != null ? clicked.getAttribute('id').split('-').pop() : void 0;
                    tier = _this.project.get_attached('tiers', _idx);
                    _key = tier.key;
                  }
                  return _this.tiers.get(_key, function(teer) {
                    document.getElementById('tier-amount-' + _idx).innerHTML = teer.amount;
                    document.getElementById('tier-description-' + _idx).innerHTML = teer.description;
                    return _this.project.attach('tiers', teer);
                  });
                }, false);
                document.getElementById('tier-delete-' + _idx).addEventListener('click', function(e) {
                  var clicked, tier;
                  if (e != null ? e.preventDefault : void 0) {
                    e.preventDefault();
                    e.stopPropagation();
                    clicked = e.target;
                    _idx = clicked != null ? clicked.getAttribute('id').split('-').pop() : void 0;
                    tier = _this.project.get_attached('tiers', _idx);
                    _key = tier.key;
                  }
                  return _this.tiers["delete"](_key);
                }, false);
                return editor;
              };
              if ((fields = Util.get('tier', document.getElementById(base_id + '-modal-content'))) != null) {
                for (_i = 0, _len = fields.length; _i < _len; _i++) {
                  tier_field = fields[_i];
                  editors.push(populate(tier_field));
                }
              }
              return m.open();
            }, {
              initial: {
                width: '0px',
                height: '0px',
                bottom: '60px',
                right: '60px'
              },
              ratio: {
                x: 0.3,
                y: 0.5
              },
              calc: function() {
                var css, mH, mW, r, wH, wW;
                css = {};
                r = this.ratio;
                wW = window.innerWidth;
                wH = window.innerHeight;
                mW = Math.floor(r.x * wW);
                mH = Math.floor(r.y * wH);
                css.width = mW + 'px';
                css.height = mH + 'px';
                css.bottom = this.initial.bottom;
                css.right = this.initial.right;
                return css;
              }
            });
            return _this;
          });
        }
      };
      this.update = function() {
        if (_this._state.o) {
          return $.apptools.api.project.post({
            target: _this.project_key
          }).fulfill({
            success: function() {
              return alert('update() success');
            },
            failure: function(error) {
              return alert('update() failure');
            }
          });
        } else {
          throw new UserPermissionsError(_this.constructor.name, 'Current user is not a project owner.');
        }
      };
      this._init = function() {
        var d_off, d_on;
        if (window._cp) {
          document.getElementById('follow').addEventListener('click', _this.follow, false);
          document.getElementById('share').addEventListener('click', _this.share, false);
          document.getElementById('back').addEventListener('click', _this.back, false);
          if (_this._state.o) {
            document.body.addEventListener('drop', _this.add_media, false);
            document.getElementById('promote-goals').addEventListener('click', _this.goals.edit, false);
            document.getElementById('promote-tiers').addEventListener('click', _this.tiers.edit, false);
            document.getElementById('promote-dropzone').addEventListener('dragenter', (d_on = function(ev) {
              if (ev != null ? ev.preventDefault : void 0) {
                ev.preventDefault();
                ev.stopPropagation();
              }
              return ev.target.classList.add('hover');
            }), false);
            document.getElementById('promote-dropzone').addEventListener('dragover', d_on, false);
            document.getElementById('promote-dropzone').addEventListener('dragleave', (d_off = function(ev) {
              if (ev != null ? ev.preventDefault : void 0) {
                ev.preventDefault();
                ev.stopPropagation();
              }
              return ev.target.className = 'dropzone';
            }), false);
            document.getElementById('promote-dropzone').addEventListener('dragexit', d_off, false);
            document.getElementById('promote-dropzone').addEventListener('drop', (function(ev) {
              d_off(ev);
              return _this.add_media(ev);
            }));
          }
        }
        return _this.get();
      };
    }

    return ProjectController;

  })(OpenfireController);

  ProposalController = (function(_super) {

    __extends(ProposalController, _super);

    ProposalController.events = [];

    function ProposalController(openfire, window) {
      var _this = this;
      this._init = function() {};
    }

    return ProposalController;

  })(OpenfireController);

  if (this.__openfire_preinit != null) {
    this.__openfire_preinit.abstract_base_objects.push(Asset);
    this.__openfire_preinit.abstract_base_objects.push(ProjectImage);
    this.__openfire_preinit.abstract_base_objects.push(ProjectVideo);
    this.__openfire_preinit.abstract_base_objects.push(ProjectVideo);
    this.__openfire_preinit.abstract_base_classes.push(Project);
    this.__openfire_preinit.abstract_base_classes.push(Proposal);
    this.__openfire_preinit.abstract_base_controllers.push(ProjectController);
    this.__openfire_preinit.abstract_base_controllers.push(ProposalController);
  }

  Openfire = (function() {

    function Openfire(window) {
      var _base,
        _this = this;
      this.sys = {
        core_events: ['OPENFIRE_READY'],
        config: {
          session: {
            cookie: "ofsession",
            header: "X-AppFactory-Session",
            timeout: 86400,
            cookieless: false
          },
          csrf: {
            cookie: "ofcsrf",
            header: "X-AppFactory-CSRF"
          }
        },
        state: {
          status: 'NOT_READY',
          flags: [],
          preinit: {},
          controllers: {},
          classes: {},
          objects: {},
          session: {
            data: null,
            verified: false,
            timestamp: null,
            signature: null,
            established: false,
            authenticated: false,
            csrf: {
              next: null,
              history: []
            }
          },
          consider_preinit: function(preinit) {
            var cls, ctrlr, obj, _i, _j, _k, _len, _len2, _len3, _ref, _ref2, _ref3;
            if (preinit.abstract_base_objects != null) {
              _ref = preinit.abstract_base_objects;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                obj = _ref[_i];
                _this.sys.install.object(obj);
              }
            }
            if (preinit.abstract_base_classes != null) {
              _ref2 = preinit.abstract_base_classes;
              for (_j = 0, _len2 = _ref2.length; _j < _len2; _j++) {
                cls = _ref2[_j];
                _this.sys.install["class"](cls);
              }
            }
            if (preinit.abstract_base_controllers != null) {
              _ref3 = preinit.abstract_base_controllers;
              for (_k = 0, _len3 = _ref3.length; _k < _len3; _k++) {
                ctrlr = _ref3[_k];
                _this.sys.install.controller(ctrlr);
              }
            }
            return preinit;
          },
          sniff_headers: function(document) {
            var cookie, data, i, key, session, signature, timestamp, _ref, _ref2, _ref3;
            $.apptools.dev.verbose('openfire', 'Sniffing response cookies.');
            try {
              session = null;
              _ref = document.cookie.split(";");
              for (i in _ref) {
                cookie = _ref[i];
                $.apptools.dev.verbose('openfire:sessions', 'Found a cookie.', i, cookie, cookie.replace('"', '').replace('"', '').split("="));
                _ref2 = cookie.split("="), key = _ref2[0], cookie = _ref2[1];
                if (key === _this.sys.config.session.cookie) {
                  _ref3 = session = cookie.split("|"), data = _ref3[0], timestamp = _ref3[1], signature = _ref3[2];
                  $.apptools.dev.verbose('openfire:sessions', 'Possibly valid session cookie found!', _this.sys.config.session.cookie, data, timestamp, signature);
                  if (session.length > 2) {
                    $.apptools.dev.verbose('openfire:sessions', 'Checking session timeout with TTL of ', _this.sys.config.session.timeout, 'and session creation time of', session[1]);
                    if (((+new Date(+timestamp * 1000)) + (_this.sys.config.session.timeout * 1000)) > +new Date()) {
                      session = {
                        data: data,
                        timestamp: timestamp,
                        signature: signature
                      };
                      $.apptools.dev.log('openfire:sessions', 'Valid session found and loaded.', session);
                    }
                  }
                  break;
                }
                continue;
              }
              if (session !== null && session !== false) {
                _this.sys.state.session.data = session.data;
                _this.sys.state.session.timestamp = session.timestamp;
                _this.sys.state.session.signature = signature.replace('"', '');
                _this.sys.state.session.established = true;
              }
            } catch (err) {
              $.apptools.dev.error('openfire:sessions', 'An unknown exception was encountered when attempting to load the user\'s session.', err);
              _this.sys.state.session.error = true;
            }
            return _this.sys.state.session.established;
          }
        },
        install: {
          object: function(obj) {
            var event, o, _i, _len, _ref, _ref2, _ref3;
            _this.sys.state.objects[(o = obj.constructor.name)] = obj;
            if (obj.events != null) {
              _ref = obj.events;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                event = _ref[_i];
                if ((_ref2 = window.apptools) != null) {
                  if ((_ref3 = _ref2.events) != null) _ref3.register(event);
                }
              }
            }
            if ((obj["export"] != null) !== 'private') {
              (obj = new obj(_this)) && (window[o] = obj);
            } else {
              obj = new obj();
            }
            if (typeof obj._init === "function") obj._init();
            return obj;
          },
          "class": function(cls) {
            var cl, event, _i, _len, _ref, _ref2, _ref3;
            _this.sys.state.classes[(cl = cls.constructor.name)] = cls;
            if (cls.events != null) {
              _ref = cls.events;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                event = _ref[_i];
                if ((_ref2 = window.apptools) != null) {
                  if ((_ref3 = _ref2.events) != null) _ref3.register(event);
                }
              }
            }
            if ((cls["export"] != null) !== 'private') {
              (cls = new cls(_this)) && (window[cl] = cls);
            } else {
              cls = new cls();
            }
            if (typeof cls._init === "function") cls._init();
            return cls;
          },
          controller: function(ctrlr) {
            var event, mount_point, _i, _len, _ref, _ref2, _ref3;
            _this.sys.state.controllers[ctrlr.mount] = ctrlr;
            if (ctrlr.events != null) {
              _ref = ctrlr.events;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                event = _ref[_i];
                if ((_ref2 = window.apptools) != null) {
                  if ((_ref3 = _ref2.events) != null) _ref3.register(event);
                }
              }
            }
            if (ctrlr.mount != null) mount_point = ctrlr.mount;
            if ((ctrlr["export"] != null) !== 'private') {
              (ctrlr = new ctrlr(_this, window)) && (window[ctrlr.constructor.name] = ctrlr);
            } else {
              ctrlr = new ctrlr(window);
            }
            _this[mount_point] = ctrlr;
            if (typeof ctrlr._init === "function") ctrlr._init();
            return ctrlr;
          }
        },
        go: function() {
          var _ref, _ref2;
          if ((_ref = window.apptools) != null) {
            if ((_ref2 = _ref.dev) != null) {
              _ref2.verbose('Openfire', 'Openfire systems go.');
            }
          }
          _this.sys.state.status = 'READY';
          return _this;
        }
      };
      if (window.__openfire_preinit != null) {
        this.sys.state.preinit = window.__openfire_preinit;
        this.sys.state.consider_preinit(window.__openfire_preinit);
      }
      if (typeof (_base = this.sys.state).sniff_headers === "function" ? _base.sniff_headers(document) : void 0) {
        if (this.sys.config.session.cookieless) {
          $.apptools.api.internals.config.headers[this.sys.config.csrf.header] = this.sys.state.session.signature;
          $.apptools.api.internals.config.headers[this.sys.config.session.header] = document.cookie;
        }
      }
      return this.sys.go();
    }

    return Openfire;

  })();

  window.Openfire = Openfire;

  window.openfire = new Openfire(window);

  if (typeof $ !== "undefined" && $ !== null) {
    $.extend({
      openfire: window.openfire
    });
  } else {
    window.$ = function(id) {
      if (window.Util != null) {
        return window.Util.get(id);
      } else {
        return document.getElementById(id);
      }
    };
    window.$.openfire = window.openfire;
  }

}).call(this);
