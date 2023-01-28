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