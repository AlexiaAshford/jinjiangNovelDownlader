function getLocTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日/g, " ");
}


function pwdEncryption(str) {
    var k;
    $.ajax({
        url: '//my.jjwxc.net/login.php?action=setPwdKey&r=' + Math.random(),
        async: false,
        success: function (data) {
            k = data;
        }
    });
    var s = "", b, b1, b2, b3, pwdtype = "";
    if (k) {
        pwdtype = "encryption";
        var strLen = k.length;
        var a = k.split("");
        for (var i = 0; i < str.length; i++) {
            b = str.charCodeAt(i);
            b1 = b % strLen;
            b = (b - b1) / strLen;
            b2 = b % strLen;
            b = (b - b2) / strLen;
            b3 = b % strLen;
            s += a[b3] + a[b2] + a[b1];
        }
    } else {
        s = str;
    }
    return {"pwdtype": pwdtype, "pwd": s};
}

$(function () {
    var captchaType;
    var now = new Date();
    var time = Math.round(now.getTime() / 1000);
    var phptime = 1674919318;
    if (Math.abs(phptime - time) >= 43200) {
        $.blockUI('<div align="center"><div style="float:right"><img src="//static.jjwxc.net/images/close.gif" width="12" height="12" style="cursor:pointer" onClick="$.unblockUI()"/></div><b>您的电脑日期时间 ' + now.getFullYear() + '-' + (now.getMonth() + 1) + '-' + now.getDate() + ' ' + now.getHours() + ':' + now.getMinutes() + ' 与实际不符，可能导致网站功能异常，请校正</b><br/><br/><br/><br/><input type="button" value="确 定" onClick="$.unblockUI()"/></div>', {
            width: '330px',
            height: '100px',
            cursor: 'default'
        });
    }
    checkneedauthnum()
    $('#loginname').focus();
    if (jjCookie.get('login_need_authnum')) {
        needauth = true;
        showauthnum();
    }
    (function () {
        var loginname = $('#loginname').val();
        $('#loginname').keyup(function () {
            var newloginname = $(this).val();
            if (loginname == newloginname) {
                $('#devicecode_div').show();
            } else {
                $('#devicecode_div').hide();
            }
        })
    })()

})

function checkfill(self, loginname, loginpassword) {
    //判断是否
    var loginForm = $(self).parents("form:eq(0)");
    loginForm.hide();
    var pwdObj = pwdEncryption(loginpassword);
    $("#loginpassword").remove();
    loginForm.append("<input type='text' value='" + pwdObj.pwd + " ' name='loginpassword'/>");
    $("#pwdtype").val(pwdObj.pwdtype);
    return true;
}

window.onload = function () {
    $.ajax({
        url: "//my.jjwxc.net/lib/ajax.php?action=getCaptchaType",
        dataType: 'jsonp',
        type: "get",
        async: false,
        jsonp: 'callback',
        //jsonpCallback: 'callbackGetCaptchaType',
        success: function (res) {
            captchaType = res.captchaType;
            if (needauth) {
                if (captchaType == 'jjwxc') {
                    $('#captcha_wrapper').html('<input type="text" id="auth_num" name="auth_num" size="20" maxlength="32" tabindex="3" style="width:85px"/> <img src=""><span class="input_after" title="点击重新获取验证码" id="getauthnum" onclick="getauthnum()" style="padding-left:1em;">换一个</span>');
                } else if (captchaType == 'shumei') {
                    var shumei_deviceId = $('#shumeideviceId').val() ? $('#shumeideviceId').val() : '';
                    $.ajax({
                        url: "//my.jjwxc.net/lib/ajax.php?action=shumeiCodePreRequest&deviceId=" + shumei_deviceId + '&appId=pc_login',
                        dataType: 'jsonp',
                        type: "get",
                        jsonp: 'callback',
                        jsonpCallback: 'jsonpCallback20210407',
                        success: function (res) {
                            $('#shumei_transcation').val(res.transactionKey);
                            initSMCaptcha({
                                organization: res.organization ? res.organization : 'E9kUZWhov0uih0OKfOb6',
                                appId: res.appId ? res.appId : 'jj_pc_login',
                                width: 300,
                                //https: false,
                                mode: res.mode ? res.mode : "select",
                                product: res.product ? res.product : "embed",
                                appendTo: '#captcha_wrapper'
                            }, smCaptchaCallback);//

                            function smCaptchaCallback(SMCaptcha) {
                                SMCaptcha.onSuccess(function (data) {
                                    //成功的时候提交表单
                                    if (data.pass === true) {
                                        //验证提交表单
                                        $("input[name='shumei_captcha_rid']").val(data.rid);
                                    }
                                })
                                //资源加载异常,建议开发时进行监听,便于查询错误
                                SMCaptcha.onError(function (errType, errMsg) {
                                    console.log('onError', errType, errMsg);
                                });

                            }
                        }
                    });
                }
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest, textStatus, errorThrown);
        }
    });
}

//统一登入界面
function show_login(username, password) {
    checkneedauthnum();
    var url = window.location.href;
    jjCookie.set('returnUrl', url, false, '.jjwxc.net');
//删除原有的页面
    $('#login_info_remove').remove();
    $('#login_info_for_jj_remove').remove();
    if ($('#mylogin').length > 0) {
        $('#mylogin').val('no');
    }
    username = undefined == username ? '' : username;
    password = undefined == password ? '' : password;
    var checked = '';
    if (username && password) {
        checked = 'checked';
    }
    let widthEnough = parseInt($('body').width()) > 850;
    let loginWidth = widthEnough ? '810px' : '100%';
    let blockWidth = widthEnough ? '850px' : '94%';
    let blockMargin = widthEnough ? '-430px' : '-47.5%';
    let u = navigator.userAgent;
    if (!!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/) || !widthEnough) {
        loginWidth = '750px';
        blockWidth = '762px'
        blockMargin = '-385px';
    }
    let htmlStr = '<script type="text/javascript" src="//static.jjwxc.net/scripts/shumeiDeviceIdSdk.js?var=20230114"></script><style>#login_info_remove *{font-family: \'微软雅黑\',Arial, Helvetica, sans-serif;}#login_info_remove ul{padding-left:0}#login_info_remove li{list-style:none;}#login_form_ajax{margin: 0 auto; font-weight:bold;}#login_form_ajax .hint{font-family:\'宋体\';font-size:12px;color:#A7A7A7;margin-left:60px;margin-top:3px;font-weight:normal} #login_form_ajax label{display:inline-block;text-align:right; font-size:16px; }#login_form_ajax input{vertical-align:middle;height: 28px;width: 275px;margin-left:5px;color:black}#login_form_ajax .input_after{color:#009900;font-size:13px;}#login_form_ajax .alert{color:red}#logincaptchaimg *{display:inline-block;vertical-align:middle} </style>';

    $.ajax({
        url: httpProtocol + "://my.jjwxc.net/lib/ajax.php?action=getCaptchaType",
        dataType: 'jsonp',
        type: "get",
        async: false,
        jsonp: 'callback',
        //jsonpCallback: 'callbackGetCaptchaType',
        success: function (res) {
            captchaType = res.captchaType;
            needauth = res.needAuth;
            if (captchaType == 'jjwxc') {
                if (needauth) {
                    var html = '<div id="login_auth_num" style="display:none"><p style="margin-top:10px;"><label>图案验证码</label> <input tabindex="3" name="auth_num" type="input" id="auth_num"  maxlength="32"/></p>';
                    html += '<p style="margin-top:10px;"><label></label> <img src=""><span class="input_after" title="点击重新获取验证码" id="getauthnum" onclick="getauthnum()" style="padding-left:1em;">换一个</span></p><p><label></label><span class="alert"></span></p></div>';
                    $('.login_blockui_captcha').html(html);
                    getauthnum();
                }
            } else if (captchaType == 'shumei') {
                if (!needauth) {
                    $('.login_blockui_captcha').html('');
                    return false;
                }
                $('.login_blockui_captcha').html('<div id="captcha_wrapper_blockui">验证码加载中...</div>');
                var shumei_deviceid_retry = 0;
                var timer = setInterval(function () {
                    var shumei_deviceId = ($('#shumeideviceId').length > 0 && $('#shumeideviceId').val().length > 0) ? $('#shumeideviceId').val() : '';
                    if (shumei_deviceId !== '') {
                        clearInterval(timer);
                    } else if (shumei_deviceid_retry++ >= 10) {
                        shumei_deviceId = 'get_deviceid_timeout';
                        clearInterval(timer);
                    } else {
                        return true;
                    }
                    $.ajax({
                        url: httpProtocol + "://my.jjwxc.net/lib/ajax.php?action=shumeiCodePreRequest&deviceId=" + shumei_deviceId + '&appId=pc_login',
                        dataType: 'jsonp',
                        type: "get",
                        async: false,
                        jsonp: 'callback',
                        //jsonpCallback: 'jsonpHandler',
                        success: function (res) {
                            $('#login_form > .shumei_transcation').val(res.transactionKey);
                            param = {
                                organization: res.organization ? res.organization : 'E9kUZWhov0uih0OKfOb6',
                                appId: res.appId ? res.appId : 'jj_pc_login',
                                mode: res.mode ? res.mode : "select",
                                product: res.product ? res.product : "embed",
                            }
                            //某些活动页面没有引用sdk需要手动加载
                            if (typeof initSMCaptcha == 'undefined') {
                                loadScriptUtf8('https://castatic.fengkongcloud.cn/pr/v1.0.3/smcp.min.js', initShumeiCaptcha, param);
                            } else {
                                initShumeiCaptcha(param);
                            }
                        },
                        error: function (XMLHttpRequest, textStatus, errorThrown) {
                            console.log(XMLHttpRequest, textStatus, errorThrown);
                        }
                    });
                }, 300);

            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest, textStatus, errorThrown);
        }
    });
    return false;
}

//初始化验证码
function initShumeiCaptcha() {
    initSMCaptcha({
        organization: param.organization ? param.organization : 'E9kUZWhov0uih0OKfOb6',
        appId: param.appId ? param.appId : 'jj_pc_login',
        //https: false,
        width: '314',
        mode: param.mode ? param.mode : "select",
        product: param.product ? param.product : "embed",
        appendTo: 'captcha_wrapper_blockui'
    }, smCaptchaCallback);//

    function smCaptchaCallback(SMCaptcha) {
        //验证码校验情况回调
        SMCaptcha.onSuccess(function (data) {
            //成功的时候提交表单
            if (data.pass === true) {
                //验证提交表单
                $('#login_form > .shumei_captcha_rid').val(data.rid);
            }
        })
    }
}

// $('#login_form > .shumei_transcation').val(res.transactionKey);
// param = {