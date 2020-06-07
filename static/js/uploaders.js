(function($){
    var SELECTOR = {
        CSRF_TOKEN : "input[name='csrfmiddlewaretoken']",
        PICTURE : "input[type='file'][name='picture']",
        PATH : "input[name='picture_path']"
    };

    var DEFAULTS = {
        labels: {
            "Select": "select file"
        }
    };
    function Uploaders(form, uploadUrl,options){
        if(form && uploadUrl){
            this.form = form;
            this.url = uploadUrl;
            this.processOptions(options);
            this.gatherFormElement();
            this.wrapFileField();
            this.setupFileUpload();
        }
    }

    Uploaders.prototype.mergeObjects = function(source, target){
        var self = this;
        Object.keys(source).forEach(function(key){
            var sourceVal = source[key];
            var targetVal = target[key];
            if (!target.hasOwnProperty(key)){
                target[key] = sourceVal;
            } else if (typeof sourceVal === "object" && typeof targetVal === "object"){
                self.mergeObjects(sourceVal, targetVal);
            }
        });
    };

    Uploaders.prototype.processOptions = function(options){
        options = options || {};
        this.mergeObjects(DEFAULTS, options);
        this.options = options;
    };

    Uploaders.prototype.gatherFormElement = function(){
        this.csrf = this.form.querySelector(SELECTOR.CSRF_TOKEN);
        this.picture = this.form.querySelector(SELECTOR.PICTURE);
        this.path = this.form.querySelector(SELECTOR.PATH);

        this.createButton();
        this.createContainer();
    };

    Uploaders.prototype.createButton = function(){
        var label = this.options.labels["Select Picture"];
        this.button = document.createElement("button");
        this.button.appendChild(document.createTextNode(label));
        this.button.setAttribute("type", "button");
        this.button.classList.add(
            "btn", "btn-primary", "fileinput-button"
        );
    };

    Uploaders.prototype.createContainer = function(){
        this.container = document.createElement("table");
        this.container.setAttribute("role", "presentation");
        this.container.classList.add("table", "table-striped");
        this.list = document.createElement("tbody");
        this.list.classList.add("files");
        this.container.appendChild(this.list);
    }

    Uploaders.prototype.wrapFileField = function(){
        this.picture.parentNode.insertBefore(
            this.button, this.picture);
        this.button.appendChild(this.picture);
        this.button.parentNode.insertBefore(
            this.container,this.button
        );
    };

    Uploaders.prototype.setupFileUpload = function(){
        var self = this;
        var safeMethodsRE = /^(GET|HEAD|OPTIONS|TRACE)$/;
        $.ajaxSettings.beforeSend = (function(existing) {
            var csrftoken = document.cookie.replace(
                /^(?:.*)?csrftoken=(.*?)(?:;.*)?$/, "$1"
            )
            return function(xhr, settings){
                if(!safeMethodsRE.test(settings.type)&& !this.crossDomail){
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }
            $(this.form).fileupload({
                url: this.url,
                dataType: 'json',
                acceptFileType: /^image\/(gif|p?jpeg|jpg|png)$/,
                autoUpload: false,
                replaceFileInput: true,
                messages: self.options.labels,
                maxNumberOffFiles: 1
            }).on("fileuploaddone", function(e, data){
                self.path.value = data.result.files[0].path;
            }).on("fileuploaddestroy", function(e, data){
                self.path.value = "";
            });
        });
    }
    window.Uploaders = Uploaders;

}(JQuery));