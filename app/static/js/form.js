
(function ($) {

    "use strict";

    var SUBMIT_BUTTON_SELECTOR = "input[type='submit']," +
        "button[type='submit']," +
        "button[data-type='submit']," +
        "input[data-type='submit']";

    function safeCall() {
        var array = $(arguments).toArray(),
            fn = array.shift();

        typeof fn === 'function' && fn.apply(this, array);
    }

    function getFormParameters($inputs) {
        var result = {};

        $inputs.each(function (i, ele) {
            var name = ele.getAttribute("name");

            result[name] = ele.value;
        });

        return result;
    }

    function verifyForm(data, formValidator, cb, eb) {
        var validatorResult,
            validArr,
            field,
            fn,
            i;

        data.form.extend(formAjax);

        for (field in formValidator) {

            if (!formValidator.hasOwnProperty(field) || !(field in data.fields)) continue;

            validArr = formValidator[field];

            if (typeof validArr === "function") {
                validArr = [validArr];
            }

            if (!Array.isArray(validArr)) {
                console.error(field + "验证器缺失:", validArr);
                continue;
            }

            for (i=0;i<validArr.length;i++) {
                fn = validArr[i];

                if (typeof fn !== "function") {
                    console.warn("invalid validator. Field: "+field);
                    console.warn(fn);
                    continue;
                }

                validatorResult = fn.call(data.form, data.fields[field], data.data[field], data);

                if (validatorResult !== true && typeof validatorResult !== "undefined") {

                    safeCall.call(data.form, eb, data.fields[field], data.data[field], validatorResult);

                    return;
                }

            }
        }

        safeCall.call(data.form, cb, data);
    }

    var formApp = {

        parseForm: function ($form) {
            var inputDoms = $form.find("input,select"),
                result = {},
                inputs = {},
                name,
                each,
                i;

            result.form = $form;
            result.url = $form.attr("action");
            result.method = $form.attr("method");
            result.data = getFormParameters(inputDoms);

            for (i=0;i<inputDoms.length;i++) {
                each = inputDoms[i];
                name = each.getAttribute('name');

                if (each.type.toUpperCase() === 'checkbox') {

                    if (each.checked)
                        inputs[name] = each.value
                } else {
                    inputs[each.getAttribute("name")] = each;
                }
            }

            result.fields = inputs;

            return result;
        },

        handle: function (options) {

            var $submitBtn,
                callback = options.success,
                errback = options.error,
                formValidator = options.validators || {},
                $forms = this;

            if (typeof formValidator !== 'object') {
                throw new Error("invalid validators map: ", formValidator);
            }

            $submitBtn = $forms.find(SUBMIT_BUTTON_SELECTOR);
            $submitBtn.click(function (e) {
                var $btn = $(e.target);
                var $form = $btn.parent("form");

                if ($btn.attr("type").toUpperCase() === "SUBMIT") {
                    e.preventDefault();
                }

                var formData = formApp.parseForm($form);

                verifyForm(formData, formValidator, callback, errback);
            });

            $forms.bind('submit', function (event) {
                event.preventDefault();
            });
        }
    };

    function sendAjax(form, options) {
        var $form = $(form),
            dataset = $form.data(),
            key;

        options.cache = false;

        for (key in dataset) {
            if (!(key in options)) {
                options[key] = dataset[key]
            }
        }

        if (!('method' in options)) {
            options.method = $form.attr('method');
        }

        if (!('url' in options)) {
            options.url = $form.attr('action');
        }

        $.ajax(options);
    }

    var formAjax = {
        ajax: function (options) {

            var each,
                i;

            for (i=0;i<this.length;i++) {
                each = this[i];

                if (each.tagName !== "FORM") {
                    console.error(each);
                    continue;
                }

                sendAjax(each, options);
            }
        }
    };

    $.fn.extend({

        form: function () {
            var forms = this.filter("form");
            if (forms.length) {

                return forms
                    .extend(formApp);
            } else {
                return forms;
            }
        }
    });

    var validators = {

        validators: {
            required: function (message) {
                return function (dom, v) {
                    if (!v) return message;
                }
            },

            regexp: function (re, message) {
                return function (dom, v) {
                    if (!re.test(v)) return message;
                }
            },

            email: function (message) {
                return validators.validators.regexp(/^\w+@\w+(\\.\w+)?$/i, message);
            },

            length: function (options) {
                var min = options.min || 0,
                    max = options.max || Infinity,
                    message = options.message;

                return function (dom, v) {

                    if (v.length > max || v.length < min) {
                        return message;
                    }
                };
            }
        }
    };

    $.extend(validators);
})(jQuery);
