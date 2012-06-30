// Generated by CoffeeScript 1.3.3
(function() {
  var ActivityItem, AddUserRole, AuthController, Back, Comment, CreateProposal, Follow, GoalReached, Key, Login, MediaUpdate, Openfire, OpenfireController, OpenfireException, OpenfireObject, Project, ProjectCard, ProjectClosed, ProjectController, ProjectOpened, Proposal, ProposalController, ProposalDenied, ProposalPromoted, ProposalReturned, Session, Signup, ThresholdReached, Update, User, UserController,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

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
      return OpenfireObject.__super__.constructor.apply(this, arguments);
    }

    return OpenfireObject;

  })(CoreObject);

  OpenfireController = (function() {

    function OpenfireController() {}

    return OpenfireController;

  })();

  OpenfireException = (function(_super) {

    __extends(OpenfireException, _super);

    function OpenfireException(controller, message, context) {
      this.controller = controller;
      this.message = message;
      this.context = context;
    }

    OpenfireException.prototype.toString = function() {
      return '[' + this.controller + '] OpenfireException: ' + this.message;
    };

    return OpenfireException;

  })(Error);

  this.__openfire_preinit.abstract_base_objects.push(OpenfireObject);

  this.__openfire_preinit.abstract_base_controllers.push(OpenfireController);

  this.__openfire_preinit.abstract_base_classes.push(OpenfireException);

  Key = (function(_super) {

    __extends(Key, _super);

    function Key() {}

    return Key;

  })(Model);

  ProjectCard = (function(_super) {

    __extends(ProjectCard, _super);

    function ProjectCard() {
      return ProjectCard.__super__.constructor.apply(this, arguments);
    }

    ProjectCard.prototype.name = String();

    ProjectCard.prototype.project = Key();

    ProjectCard.prototype.progress = String();

    ProjectCard.prototype.backer_count = Number();

    ProjectCard.prototype.met = Boolean();

    return ProjectCard;

  })(Model);

  ActivityItem = (function(_super) {

    __extends(ActivityItem, _super);

    function ActivityItem() {
      return ActivityItem.__super__.constructor.apply(this, arguments);
    }

    ActivityItem.prototype.timestamp = Date();

    ActivityItem.prototype.project = Key();

    return ActivityItem;

  })(Model);

  Follow = (function(_super) {

    __extends(Follow, _super);

    function Follow() {
      return Follow.__super__.constructor.apply(this, arguments);
    }

    Follow.prototype.username = String();

    Follow.prototype.project = Key();

    Follow.prototype.timestamp = Date();

    return Follow;

  })(ActivityItem);

  Back = (function(_super) {

    __extends(Back, _super);

    function Back() {
      return Back.__super__.constructor.apply(this, arguments);
    }

    Back.prototype.username = String();

    Back.prototype.project = Key();

    Back.prototype.timestamp = Date();

    return Back;

  })(ActivityItem);

  Update = (function(_super) {

    __extends(Update, _super);

    function Update() {
      return Update.__super__.constructor.apply(this, arguments);
    }

    Update.prototype.username = String();

    Update.prototype.text = String();

    Update.prototype.timestamp = Date();

    Update.prototype.project = Key();

    return Update;

  })(ActivityItem);

  MediaUpdate = (function(_super) {

    __extends(MediaUpdate, _super);

    function MediaUpdate() {
      return MediaUpdate.__super__.constructor.apply(this, arguments);
    }

    return MediaUpdate;

  })(Update);

  GoalReached = (function(_super) {

    __extends(GoalReached, _super);

    function GoalReached() {
      return GoalReached.__super__.constructor.apply(this, arguments);
    }

    return GoalReached;

  })(Update);

  ThresholdReached = (function(_super) {

    __extends(ThresholdReached, _super);

    function ThresholdReached() {
      return ThresholdReached.__super__.constructor.apply(this, arguments);
    }

    return ThresholdReached;

  })(Update);

  ProjectOpened = (function(_super) {

    __extends(ProjectOpened, _super);

    function ProjectOpened() {
      return ProjectOpened.__super__.constructor.apply(this, arguments);
    }

    return ProjectOpened;

  })(Update);

  ProjectClosed = (function(_super) {

    __extends(ProjectClosed, _super);

    function ProjectClosed() {
      return ProjectClosed.__super__.constructor.apply(this, arguments);
    }

    return ProjectClosed;

  })(Update);

  CreateProposal = (function(_super) {

    __extends(CreateProposal, _super);

    function CreateProposal() {
      return CreateProposal.__super__.constructor.apply(this, arguments);
    }

    return CreateProposal;

  })(ActivityItem);

  ProposalPromoted = (function(_super) {

    __extends(ProposalPromoted, _super);

    function ProposalPromoted() {
      return ProposalPromoted.__super__.constructor.apply(this, arguments);
    }

    return ProposalPromoted;

  })(Update);

  ProposalDenied = (function(_super) {

    __extends(ProposalDenied, _super);

    function ProposalDenied() {
      return ProposalDenied.__super__.constructor.apply(this, arguments);
    }

    return ProposalDenied;

  })(Update);

  ProposalReturned = (function(_super) {

    __extends(ProposalReturned, _super);

    function ProposalReturned() {
      return ProposalReturned.__super__.constructor.apply(this, arguments);
    }

    return ProposalReturned;

  })(Update);

  AddUserRole = (function(_super) {

    __extends(AddUserRole, _super);

    function AddUserRole() {
      return AddUserRole.__super__.constructor.apply(this, arguments);
    }

    return AddUserRole;

  })(ActivityItem);

  Comment = (function(_super) {

    __extends(Comment, _super);

    function Comment() {
      return Comment.__super__.constructor.apply(this, arguments);
    }

    Comment.prototype.username = String();

    Comment.prototype.text = String();

    return Comment;

  })(ActivityItem);

  Login = (function(_super) {

    __extends(Login, _super);

    function Login() {
      return Login.__super__.constructor.apply(this, arguments);
    }

    return Login;

  })(Model);

  Signup = (function(_super) {

    __extends(Signup, _super);

    function Signup() {
      return Signup.__super__.constructor.apply(this, arguments);
    }

    return Signup;

  })(Model);

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

  Project = (function(_super) {

    __extends(Project, _super);

    function Project() {
      return Project.__super__.constructor.apply(this, arguments);
    }

    return Project;

  })(OpenfireObject);

  Proposal = (function(_super) {

    __extends(Proposal, _super);

    function Proposal() {
      return Proposal.__super__.constructor.apply(this, arguments);
    }

    return Proposal;

  })(OpenfireObject);

  ProjectController = (function(_super) {

    __extends(ProjectController, _super);

    ProjectController.key = null;

    ProjectController.events = [];

    function ProjectController(openfire, window) {
      var _this = this;
      this._init = function() {};
    }

    ProjectController.prototype.follow = function() {
      var _this = this;
      return $.apptools.api.project.follow().fulfill({
        success: function() {
          return alert('Success.');
        },
        failure: function() {
          return alert('Failure.');
        }
      });
    };

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
    this.__openfire_preinit.abstract_base_objects.push(Project);
    this.__openfire_preinit.abstract_base_objects.push(Proposal);
    this.__openfire_preinit.abstract_base_controllers.push(ProjectController);
    this.__openfire_preinit.abstract_base_controllers.push(ProposalController);
  }

  Openfire = (function() {

    function Openfire(window) {
      var session,
        _this = this;
      this.sys = {
        core_events: ['OPENFIRE_READY'],
        config: {
          session: {
            cookie: "ofsession",
            header: "X-AppFactory-Session",
            timeout: 86400
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
            established: false,
            authenticated: false,
            csrf: {
              next: null,
              history: []
            }
          },
          consider_preinit: function(preinit) {
            var cls, ctrlr, obj, _i, _j, _k, _len, _len1, _len2, _ref, _ref1, _ref2;
            if (preinit.abstract_base_objects != null) {
              _ref = preinit.abstract_base_objects != null;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                obj = _ref[_i];
                _this.sys.install.object(obj);
              }
            }
            if (preinit.abstract_base_classes != null) {
              _ref1 = preinit.abstract_base_classes;
              for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
                cls = _ref1[_j];
                _this.sys.install["class"](cls);
              }
            }
            if (preinit.abstract_base_controllers != null) {
              _ref2 = preinit.abstract_base_controllers;
              for (_k = 0, _len2 = _ref2.length; _k < _len2; _k++) {
                ctrlr = _ref2[_k];
                _this.sys.install.controller(ctrlr);
              }
            }
            return preinit;
          }
        },
        sniff_headers: function(document) {
          var cookie, i, session, _ref;
          session = null;
          _ref = document.cookie.split(";");
          for (i in _ref) {
            cookie = _ref[i];
            cookie = cookie.split("=");
            if (cookie[0] === _this.sys.config.session.cookie) {
              session = cookie[1].split("|");
              if (session.length > 2) {
                if ((_this.sys.config.session.timeout * 1000) > +new Date()) {
                  session = cookie[2];
                }
              }
              break;
            }
            continue;
          }
          if (session !== null && session !== false) {
            return _this.sys.state.session.established = true;
          }
        },
        install: {
          object: function(obj) {
            var event, o, _i, _len, _ref, _ref1, _ref2;
            _this.sys.state.objects[(o = obj.constructor.name)] = obj;
            if (obj.events != null) {
              _ref = obj.events;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                event = _ref[_i];
                if ((_ref1 = window.apptools) != null) {
                  if ((_ref2 = _ref1.events) != null) {
                    _ref2.register(event);
                  }
                }
              }
            }
            if ((obj["export"] != null) !== 'private') {
              (obj = new obj(_this)) && (window[o] = obj);
            } else {
              obj = new obj();
            }
            if (typeof obj._init === "function") {
              obj._init();
            }
            return obj;
          },
          "class": function(cls) {
            var cl, event, _i, _len, _ref, _ref1, _ref2;
            _this.sys.state.classes[(cl = cls.constructor.name)] = cls;
            if (cls.events != null) {
              _ref = cls.events;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                event = _ref[_i];
                if ((_ref1 = window.apptools) != null) {
                  if ((_ref2 = _ref1.events) != null) {
                    _ref2.register(event);
                  }
                }
              }
            }
            if ((cls["export"] != null) !== 'private') {
              (cls = new cls(_this)) && (window[cl] = cls);
            } else {
              cls = new cls();
            }
            if (typeof cls._init === "function") {
              cls._init();
            }
            return cls;
          },
          controller: function(ctrlr) {
            var c, event, _i, _len, _ref, _ref1, _ref2;
            _this.sys.state.controllers[(c = ctrlr.constructor.name)] = ctrlr;
            if (ctrlr.events != null) {
              _ref = ctrlr.events;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                event = _ref[_i];
                if ((_ref1 = window.apptools) != null) {
                  if ((_ref2 = _ref1.events) != null) {
                    _ref2.register(event);
                  }
                }
              }
            }
            if ((ctrlr["export"] != null) !== 'private') {
              (ctrlr = new ctrlr(_this, window)) && (window[c] = ctrlr);
            } else {
              ctrlr = new ctrlr(window);
            }
            if (typeof ctrlr._init === "function") {
              ctrlr._init();
            }
            return ctrlr;
          }
        },
        go: function() {
          var _ref, _ref1;
          if ((_ref = window.apptools) != null) {
            if ((_ref1 = _ref.dev) != null) {
              _ref1.verbose('Openfire', 'Openfire systems go.');
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
      session = this.sys.sniff_headers(document);
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
