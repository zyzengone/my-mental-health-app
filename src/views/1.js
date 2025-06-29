!function() {
    $(document).ready(function() {
        function t() {
            var t, e = document.title.split("_")[0];
            return location.pathname.search(/\/s\//) >= 0 ? e = e.split("(")[0] : (e = $("h1").html(),
                t = location.href.split("?")[1],
            void 0 === t && (t = ""),
            void 0 === e && (e = document.title.split("_")[0])),
            "pagePath=" + location.pathname + "&pathName=" + encodeURIComponent(e) + "&pathParam=" + t
        }
        if (location.pathname.indexOf("stockdata") > 0 || location.pathname.indexOf("shareholder") > 0 || location.pathname.indexOf("article") > 0 || location.pathname.indexOf("/s/") >= 0) {
            var e = !1;
            $(window).scroll(function() {
                setTimeout(function() {
                    if ($(document).scrollTop() > $(document).height() / 5) {
                        for (var n = window.navigator.userAgent, a = ["Android", "iPhone", "SymbianOS", "Windows Phone", "iPod", "iPad"], o = !0, i = 0, s = a.length; i < s; i++)
                            if (n.indexOf(a[i]) > 0) {
                                o = !1;
                                break
                            }
                        e || ($.ajax({
                            type: "POST",
                            url: "/rewards/add-point?" + t() + "&isPC=" + o,
                            data: {},
                            headers: {
                                Accept: "application/json; charset=utf-8",
                                "X-CSRF-Token": document.getElementsByName("_csrf")[0].content
                            },
                            complete: function(t) {
                                201 === t.status && ($("body").append("<div id='reward' style='font-weight:bold; line-height: 32px;position: fixed; bottom: 50%; left: 50%;'><img style='margin-right: 10px' src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADPUlEQVRYR81XTWwNURT+vjstfdPSCJZVLCTogp1ItfOEhU0FqQrRPWIpkZC0TYiNXZPaI9L6S7CRIG/aklgpCyQW/rpUGtVO0Tdz5E7fNG+mfZ3beg139ebdc77z3XPOvfe7hOGQp1jh5zN7SNUGkU0A1oBYHboLvgIYAflOJOizKiYfsxE/TKCZZiT9NZsDCU4DOAJgVZp9YX4UQK+i6mbz+Nv5fOYl4OfsC1A4DcFKw8BxM2IMAbqtrHe+lH9JAnm3eoCQXYsKnHAScLDCmWiaC2tOAr5rfwlrXN4xYjne2iTkLAK+a38AsL68sWfQPlqOt6EYO0bAd+2bAFqXKHgEe8tyvMPRxwyBsOGIc0scfBpecDFqzJBAuNUQPJ+v2wlxi8kJ6MRTGZ8HuU4EG+dcEDGmoHboLRoS8F27B8CJlNW/tBxve2STd+1BAo3Rtwq4jbsnXunvfC7TRrI3Be+K5XgnKY9W1QaVvz4BqE1LvxLuY3bi4XTWMm2BzASJdXjQX+2KSHMK3nc1tbyeebf6OCFX04LreQIPlOO1RLa+a0uhpl1W1uvUv6eeZHYqi89M8ARsZz5n3yZxyMRB26gK1cDG8deF0oW7Rim1lU3jbwrpv07ymAmeCO7Qd+0XAGZqa+DYYzneqTCYm2lVYIdyvIZCWeoC4WcDjMhkSBPQDnULcIKqqqrljm9jYcpzdmdlIf1+LnMJ5NkFYA3T77cnILBTnSiXrebJM0k7GajZEqU/mtOkFNGRjgnPnADkmuVMtqeCFrJiTmARJdAkAgmyldmf4eE0latyFFXOhFzCZti4CQNBVzJAVHud8uI5i9KcPClLkBui31/dC5G2NPaaQBQw1dbN5IwIkH3Mu5kDBO+mgULQFSCI3QfFJYhngB0mBARykFpsBnlbH8Wmei+MVZwR466Pr3JUVXj1C7mMYu5lIDB9GU2fYOnXcbJEyaY02nYRSPI61v//U0ESESunEi7V1EmFPJcoXQpFHPGZpYxLyfKlUMazFLFmVfJhUmaFHFPCxeX5f59mEcuix+lRE91Y8PsO4MZfP06LU6XFq1/5uwUi+8lQbs96novgPch71tSy+9w7qkmkjj/r2mPsdOQWZgAAAABJRU5ErkJggg=='></img>积分 +1</div>"),
                                    setTimeout(function() {
                                        $("#reward").fadeOut(1e3)
                                    }, 3e3))
                            },
                            dataType: "application/json"
                        }),
                            e = !0)
                    }
                }, 3e3)
            });
            var n = document.title.split("_")[0];
            location.pathname.search(/s/) && (n = n.split("(")[0])
        }
    })
}(),
    function(t) {
        function e(t) {
            var e = location.href.split("/");
            return e[e.length - 1] = t,
                e.join("/")
        }
        function n(t) {
            var e = location.href.split("=");
            return e[e.length - 1] = t,
                e.join("=")
        }
        function a(t) {
            var e = location.href.split("=");
            return e[e.length - 1] = t,
                e.join("=")
        }
        function o(t) {
            var e = location.href.split("=");
            return e[e.length - 2] = t + "&tag",
                e.join("=")
        }
        t(document).ready(function() {
            t(".a-li-content").each(function() {
                var e = t(this).height()
                    , n = t(this).find("p");
                for (n.text(n.text().replace(new RegExp(String.fromCharCode(160),"g"), "").replace(/\s/g, "")); n.outerHeight() > e; )
                    n.text(n.text().replace(/(\s)*([a-zA-Z0-9]+|\W)(\.\.\.)?$/, "..."))
            }),
                t("#goto_page").click(function() {
                    location.href = e(t("#page_num").val())
                }),
                t("#goto_history_page").click(function() {
                    location.href = n(t("#page_num").val())
                }),
                t("#search_goto_page").click(function() {
                    location.href = a(t("#page_num").val())
                }),
                t("#book_goto_page").click(function() {
                    location.href = o(t("#page_num").val())
                }),
                t("#page_num").keypress(function(n) {
                    if (13 == n.which) {
                        var i = t("#page_num").val();
                        t("#search_goto_page").length > 0 && (location.href = a(i)),
                        t("#goto_page").length > 0 && (location.href = e(i)),
                        t("#book_goto_page").length > 0 && (location.href = o(i))
                    }
                })
        })
    }(jQuery),
    function(t) {
        function e() {
            var e = t('meta[name="_csrf"]').attr("content")
                , o = t('meta[name="_csrf_header"]').attr("content")
                , i = Cookies.getJSON("thumbsUp") || {
                ids: []
            }
                , s = n()
                , r = t(".article-thumbs-up-button");
            i.ids.indexOf(s) !== -1 ? r.addClass("article-thumbs-up-button-voted") : r.click(function(n) {
                n.preventDefault(),
                    t.ajax({
                        url: a() + "stock/article/thumbs-up/" + s,
                        type: "PUT",
                        beforeSend: function(t) {
                            t.setRequestHeader(o, e)
                        },
                        success: function() {
                            i.ids.push(s),
                                Cookies.set("thumbsUp", i);
                            var t = r.find(".article-thumbs-up-times");
                            t.text(Number(t.text()) + 1),
                                r.addClass("article-thumbs-up-button-voted"),
                                r.off("click")
                        }
                    })
            })
        }
        function n() {
            var t = window.location.pathname.split("/");
            return t[t.length - 1]
        }
        function a() {
            return location.pathname.replace(/stock.*/g, "")
        }
        function o() {
            return location.pathname.replace(/books.*/g, "")
        }
        t(document).ready(function() {
            t(".article-tag").on("click", function(t) {
                location.href.match(/\/books\/.*/g) ? window.open(o() + "books/" + t.target.textContent + "/1", "_blank") : location.href.match(/\/stock\/.*/g) && window.open(a() + "search?text=" + t.target.textContent + "&page=1", "_blank")
            }),
                t('.recommend-list-title[href="#"]').on("click", function(e) {
                    t(e.target).parent().find(".news-summary").toggle()
                }),
            t(".article-body").length > 0 && e()
        })
    }(jQuery),
    function(t) {
        function e() {
            var e = (t(".article-head h1").text() + t(".article-content-body").text()).replace(/[^\u4e00-\u9fa5_a-zA-Z_0-9]/g, ",");
            u = n(e, 500),
                m = 0,
                o(u[m]),
                m++,
                d = setInterval(a, 50)
        }
        function n(t, e) {
            var n, a = t.length / e, o = [];
            for (n = 0; n < a - 1; n++)
                o[n] = t.substring(n * e, (n + 1) * e);
            return o[n] = t.substring(n * e, t.length - 1),
                o
        }
        function a() {
            t("#baiduaudio")[0].ended && (m < u.length ? (o(u[m]),
                m++) : clearInterval(d))
        }
        function o(e) {
            var n, a;
            f ? (n = "http://tts.baidu.com/text2audio?tex=",
                a = "&lan=zh&cuid=" + g + "&ctp=1&tok=" + f + "&" + p + "&" + h + "&vol=5&pit=5") : (n = "http://tts.baidu.com/text2audio?idx=1&tex=",
                a = "&cuid=baidu_speech_demo&cod=2&lan=zh&ctp=1&pdt=1&" + p + "&" + h + "&vol=5&pit=5");
            var o = encodeURIComponent(encodeURIComponent(e))
                , i = n + o + a
                , s = t("#baiduaudio").attr("src", i);
            s.get(0).play()
        }
        function i() {
            return location.pathname.replace(/stock.*/g, "")
        }
        function s() {
            f || (f = l("luguleguToken"),
            f || t.ajax({
                url: i() + "baidutts/token",
                type: "get",
                dataType: "json",
                success: function(t) {
                    f = t.access_token,
                        c("luguleguToken", f, 336)
                },
                error: function() {
                    f = null
                }
            })),
            g || (g = l("luguleguMac"),
            g || t.ajax({
                url: i() + "baidutts/mac",
                type: "get",
                dataType: "text",
                success: function(t) {
                    g = t,
                        c("luguleguMac", g, 336)
                },
                error: function() {
                    g = "baidu_speech_demo"
                }
            })),
                h = l("guShi321SoundType"),
            h || (h = "per=0"),
                p = l("guShi321SoundSpd"),
            p || (p = "spd=5")
        }
        function r() {
            switch (h = l("guShi321SoundType")) {
                case "per=0":
                    t("#femaleSound").button("toggle");
                    break;
                case "per=2":
                    t("#maleSound").button("toggle");
                    break;
                case "per=3":
                    t("#maleSoundHigh2").button("toggle")
            }
            switch (p = l("guShi321SoundSpd")) {
                case "spd=3":
                    t("#slowSpd").button("toggle");
                    break;
                case "spd=5":
                    t("#normalSpd").button("toggle");
                    break;
                case "spd=7":
                    t("#fastSpd").button("toggle")
            }
        }
        function c(t, e, n) {
            var a = t + "=" + escape(e);
            if (n > 0) {
                var o = new Date
                    , i = 3600 * n * 1e3;
                o.setTime(o.getTime() + i),
                    a += "; expires=" + o.toGMTString()
            }
            document.cookie = a
        }
        function l(t) {
            var e = document.cookie.match(new RegExp("(^| )" + t + "=([^;]*)(;|$)"));
            return e ? unescape(e[2]) : null
        }
        var u, d, h = "per=0", p = "spd=5", f = null, g = null, m = 0;
        r(),
            t("#femaleSound").click(function() {
                h = "per=0",
                    c("guShi321SoundType", h, 336),
                    y()
            }),
            t("#maleSound").click(function() {
                h = "per=2",
                    c("guShi321SoundType", h, 336),
                    y()
            }),
            t("#maleSoundHigh").click(function() {
                h = "per=1",
                    c("guShi321SoundType", h, 336),
                    y()
            }),
            t("#maleSoundHigh2").click(function() {
                h = "per=3",
                    c("guShi321SoundType", h, 336),
                    y()
            }),
            t("#slowSpd").click(function() {
                p = "spd=3",
                    c("guShi321SoundSpd", p, 336),
                    y()
            }),
            t("#normalSpd").click(function() {
                p = "spd=5",
                    c("guShi321SoundSpd", p, 336),
                    y()
            }),
            t("#fastSpd").click(function() {
                p = "spd=7",
                    c("guShi321SoundSpd", p, 336),
                    y()
            });
        var y = function() {
            "pause" != t("#playButton").attr("data-action") && "play" != t("#playButton").attr("data-action") || (m && o(u[m - 1]),
                t("playButton").attr("data-action", "play"),
                t("#player-icon").attr("class", "fa fa-pause fa-lg"))
        };
        t("#playButton").click(function() {
            "stop" == t("#playButton").attr("data-action") ? (s(),
                e(),
                t("#playButton").attr("data-action", "play"),
                t("#player-icon").attr("class", "fa fa-pause fa-lg")) : "play" == t("#playButton").attr("data-action") ? (t("#baiduaudio").get(0).pause(),
                t("#playButton").attr("data-action", "pause"),
                t("#player-icon").attr("class", "fa fa-play fa-lg")) : "pause" == t("#playButton").attr("data-action") && (t("#baiduaudio").get(0).play(),
                t("#playButton").attr("data-action", "play"),
                t("#player-icon").attr("class", "fa fa-pause fa-lg"))
        })
    }(jQuery),
    function(t) {
        function e() {
            var e = t("#tag");
            "金融学" == e.text() ? t(".book-type.col-xs-12 ul li a:nth(1)").addClass("active") : "理财技巧" == e.text() ? t(".book-type.col-xs-12 ul li a:nth(2)").addClass("active") : "证券分析" == e.text() ? t(".book-type.col-xs-12 ul li a:nth(3)").addClass("active") : "价值投资" == e.text() ? t(".book-type.col-xs-12 ul li a:nth(4)").addClass("active") : t(".book-type.col-xs-12 ul li a:first").addClass("active")
        }
        t(document).ready(function() {
            e()
        })
    }(jQuery),
    function(t, e, n) {
        var a = t();
        t.fn.dropdownHover = function(n) {
            return "ontouchstart"in document ? this : (a = a.add(this.parent()),
                this.each(function() {
                    function o(t) {
                        r.parents(".navbar").find(".navbar-toggle").is(":visible") || (e.clearTimeout(i),
                            e.clearTimeout(s),
                            s = e.setTimeout(function() {
                                a.find(":focus").blur(),
                                p.instantlyCloseOthers === !0 && a.removeClass("open"),
                                    e.clearTimeout(s),
                                    r.attr("aria-expanded", "true"),
                                    c.addClass("open"),
                                    r.trigger(d)
                            }, p.hoverDelay))
                    }
                    var i, s, r = t(this), c = r.parent(), l = {
                        delay: 500,
                        hoverDelay: 0,
                        instantlyCloseOthers: !0
                    }, u = {
                        delay: t(this).data("delay"),
                        hoverDelay: t(this).data("hover-delay"),
                        instantlyCloseOthers: t(this).data("close-others")
                    }, d = "show.bs.dropdown", h = "hide.bs.dropdown", p = t.extend(!0, {}, l, n, u);
                    c.hover(function(t) {
                        return !c.hasClass("open") && !r.is(t.target) || void o(t)
                    }, function() {
                        e.clearTimeout(s),
                            i = e.setTimeout(function() {
                                r.attr("aria-expanded", "false"),
                                    c.removeClass("open"),
                                    r.trigger(h)
                            }, p.delay)
                    }),
                        r.hover(function(t) {
                            return !c.hasClass("open") && !c.is(t.target) || void o(t)
                        }),
                        c.find(".dropdown-submenu").each(function() {
                            var n, a = t(this);
                            a.hover(function() {
                                e.clearTimeout(n),
                                    a.children(".dropdown-menu").show(),
                                    a.siblings().children(".dropdown-menu").hide()
                            }, function() {
                                var t = a.children(".dropdown-menu");
                                n = e.setTimeout(function() {
                                    t.hide()
                                }, p.delay)
                            })
                        })
                }))
        }
            ,
            t(document).ready(function() {
                t('[data-hover="dropdown"]').dropdownHover()
            })
    }(jQuery, window),
    function() {
        function t() {
            var t = -1;
            if ("Microsoft Internet Explorer" == navigator.appName) {
                var e = navigator.userAgent;
                /'MSIE([0-9]{1,}[\.0-9]{0,})'/.test(e) && (t = parseFloat(RegExp.$1))
            }
            return t
        }
        function e() {
            var e = t();
            e > -1 && e < 9 && alert("为了获得更好的体验,请将IE浏览器升级到IE9以上,或者使用更先进Chrome浏览器或者360安全浏览器")
        }
        e()
    }(),
    function(t) {
        t(document).ready(function() {
            console.log("乐咕乐股网 欢迎你"),
                t('[data-toggle="tooltip"]').tooltip(),
                t('[data-toggle="popover"]').popover()
        })
    }(jQuery),
    function(t) {
        function e(t) {
            var e = new Date(t)
                , n = "" + (e.getMonth() + 1)
                , a = "" + e.getDate()
                , o = e.getFullYear();
            return n.length < 2 && (n = "0" + n),
            a.length < 2 && (a = "0" + a),
                [o, n, a].join("-")
        }
        t(document).ready(function() {
            function n() {
                var t;
                return t = "legulegu.com" === location.hostname || "www.legulegu.com" === location.hostname ? "https://" + location.hostname : "http://localhost:8080"
            }
            location.href.indexOf("/settings/donate") > 0 && (t("#leave-message-form").keydown(function(t) {
                if (13 === t.keyCode)
                    return t.preventDefault(),
                        !1
            }),
                t.ajax({
                    url: n() + "/geetest/api1",
                    type: "get",
                    dataType: "json",
                    success: function(n) {
                        initGeetest({
                            gt: n.gt,
                            challenge: n.challenge,
                            offline: !n.success,
                            https: !0,
                            new_captcha: !0,
                            width: "100%",
                            product: "popup"
                        }, function(n) {
                            n.appendTo("#popup-captcha"),
                                t("#leave-message-form").submit(function(a) {
                                    a.preventDefault();
                                    var o = n.getValidate();
                                    if (o) {
                                        var i = {
                                            purchaseOrderId: t("#purchaseOrderId").val(),
                                            money: t("#money").val(),
                                            message: t("#message").val()
                                        }
                                            , s = new Hashes.MD5
                                            , r = s.hex(e(new Date));
                                        t.ajax({
                                            url: t(this).attr("action") + "?token=" + r,
                                            type: "POST",
                                            data: JSON.stringify(i),
                                            contentType: "application/json; charset=utf-8",
                                            dataType: "json",
                                            headers: {
                                                Accept: "application/json; charset=utf-8",
                                                "X-CSRF-Token": document.getElementsByName("_csrf")[0].content
                                            },
                                            success: function(t) {
                                                alert("提交成功！"),
                                                    location.reload()
                                            },
                                            error: function() {
                                                alert("提交请求失败，请稍后再试。")
                                            }
                                        })
                                    } else
                                        alert("请点击按钮完成验证！")
                                }),
                                n.onReady(function() {}).onSuccess(function() {}).onError(function() {})
                        })
                    }
                }),
                setInterval(function() {
                    t.ajax({
                        url: "/settings/notifications/latest",
                        type: "GET",
                        contentType: "application/json; charset=utf-8",
                        dataType: "json",
                        headers: {
                            Accept: "application/json; charset=utf-8",
                            "X-CSRF-Token": document.getElementsByName("_csrf")[0].content
                        },
                        success: function(e) {
                            e && 0 === t("#notification-close").length && location.reload()
                        },
                        error: function() {}
                    })
                }, 3e3)),
                t("#money").on("blur", function() {
                    var e = t(this).val()
                        , n = e.replace(/[^0-9.]/g, "");
                    t(this).val(n);
                    var a = /^[-+]?[0-9]*\.?[0-9]+$/;
                    a.test(e) || (alert("请输入正确的浮点数"),
                        t(this).val(""))
                })
        })
    }(jQuery),
    function(t) {
        t(document).ready(function() {
            var e = t(".echarts-element");
            if (e) {
                e.append('<button class=\'btn btn-default full-screen-button\'><span class="glyphicon glyphicon-resize-full" aria-hidden="true"></span> 放大</button>');
                var n = t(".full-screen-button");
                n.click(function() {
                    e.hasClass("full-screen") ? (e.removeClass("full-screen"),
                        e.css("height", "100%"),
                        n.html('<span class="glyphicon glyphicon-resize-full" aria-hidden="true"></span> 放大')) : (e.addClass("full-screen"),
                        e.css("height", "100%"),
                        n.html('<span class="glyphicon glyphicon-resize-small" aria-hidden="true"></span> 还原'))
                })
            }
        })
    }(jQuery),
    function(t) {
        t(document).ready(function() {
            var e = t(".your-favorite-data-body .data-list-item");
            t(".your-favorite-data-head .search-wrapper .form-group .search").on("input", function(n) {
                e.each(function() {
                    t(this).text().toLowerCase().indexOf(n.target.value.toLowerCase()) === -1 ? t(this).addClass("hidden") : t(this).removeClass("hidden"),
                    n.target.value || t(this).removeClass("hidden")
                })
            })
        })
    }(jQuery),
    function(t, e, n, a) {
        function o(e, n) {
            this.element = t(e),
                this.settings = t.extend({}, x, n),
                this._defaults = x,
                this._name = h,
                this.init()
        }
        function i(e) {
            k && (e.element.addClass("navbar-hidden").animate({
                top: -1 * parseInt(e.element.css("height"), 10)
            }, {
                queue: !1,
                duration: e.settings.animationDuration
            }),
                t(".dropdown.open .dropdown-toggle", e.element).dropdown("toggle"),
                k = !1)
        }
        function s(t) {
            k || (t.element.removeClass("navbar-hidden").animate({
                top: 0
            }, {
                queue: !1,
                duration: t.settings.animationDuration
            }),
                k = !0)
        }
        function r(t) {
            var e = p.scrollTop()
                , n = e - b;
            if (b = e,
            n < 0) {
                if (k)
                    return;
                (t.settings.showOnUpscroll || e <= d) && s(t)
            } else if (n > 0) {
                if (!k)
                    return void (t.settings.showOnBottom && e + w === f.height() && s(t));
                e >= d && i(t)
            }
        }
        function c(t) {
            t.settings.disableAutohide || (v = (new Date).getTime(),
                r(t))
        }
        function l(t) {
            f.on("scroll." + h, function() {
                (new Date).getTime() - v > y ? c(t) : (clearTimeout(g),
                    g = setTimeout(function() {
                        c(t)
                    }, y))
            }),
                p.on("resize." + h, function() {
                    clearTimeout(m),
                        m = setTimeout(function() {
                            w = p.height()
                        }, y)
                })
        }
        function u() {
            f.off("." + h),
                p.off("." + h)
        }
        var d, h = "autoHidingNavbar", p = t(e), f = t(n), g = null, m = null, y = 70, v = 0, b = null, w = p.height(), k = !0, x = {
            disableAutohide: !1,
            showOnUpscroll: !0,
            showOnBottom: !0,
            hideOffset: "auto",
            animationDuration: 200
        };
        o.prototype = {
            init: function() {
                return this.elements = {
                    navbar: this.element
                },
                    this.setDisableAutohide(this.settings.disableAutohide),
                    this.setShowOnUpscroll(this.settings.showOnUpscroll),
                    this.setShowOnBottom(this.settings.showOnBottom),
                    this.setHideOffset(this.settings.hideOffset),
                    this.setAnimationDuration(this.settings.animationDuration),
                    d = "auto" === this.settings.hideOffset ? parseInt(this.element.css("height"), 10) : this.settings.hideOffset,
                    l(this),
                    this.element
            },
            setDisableAutohide: function(t) {
                return this.settings.disableAutohide = t,
                    this.element
            },
            setShowOnUpscroll: function(t) {
                return this.settings.showOnUpscroll = t,
                    this.element
            },
            setShowOnBottom: function(t) {
                return this.settings.showOnBottom = t,
                    this.element
            },
            setHideOffset: function(t) {
                return this.settings.hideOffset = t,
                    this.element
            },
            setAnimationDuration: function(t) {
                return this.settings.animationDuration = t,
                    this.element
            },
            show: function() {
                return s(this),
                    this.element
            },
            hide: function() {
                return i(this),
                    this.element
            },
            destroy: function() {
                return u(this),
                    s(this),
                    t.data(this, "plugin_" + h, null),
                    this.element
            }
        },
            t.fn[h] = function(e) {
                var n = arguments;
                if (e === a || "object" == typeof e)
                    return this.each(function() {
                        t.data(this, "plugin_" + h) || t.data(this, "plugin_" + h, new o(this,e))
                    });
                if ("string" == typeof e && "_" !== e[0] && "init" !== e) {
                    var i;
                    return this.each(function() {
                        var a = t.data(this, "plugin_" + h);
                        a instanceof o && "function" == typeof a[e] && (i = a[e].apply(a, Array.prototype.slice.call(n, 1)))
                    }),
                        i !== a ? i : this
                }
            }
            ,
            t(".navbar-fixed-top").autoHidingNavbar({})
    }(jQuery, window, document),
    function(t) {
        function e(t, e, n) {
            if ("show" == e)
                switch (n) {
                    case "fade":
                        t.fadeIn();
                        break;
                    case "slide":
                        t.slideDown();
                        break;
                    default:
                        t.fadeIn()
                }
            else
                switch (n) {
                    case "fade":
                        t.fadeOut();
                        break;
                    case "slide":
                        t.slideUp();
                        break;
                    default:
                        t.fadeOut()
                }
        }
        t.goup = function(n) {
            var a = t.extend({
                location: "right",
                locationOffset: 20,
                bottomOffset: 10,
                containerRadius: 0,
                containerClass: "goup-container",
                arrowClass: "goup-arrow",
                alwaysVisible: !1,
                trigger: 500,
                entryAnimation: "fade",
                goupSpeed: "slow",
                hideUnderWidth: 300,
                containerColor: "#D9534F",
                arrowColor: "#fff",
                title: "",
                titleAsText: !1,
                titleAsTextClass: "goup-text"
            }, n);
            t("body").append('<div style="display:none" class="' + a.containerClass + '"></div>');
            var o = t("." + a.containerClass);
            t(o).html('<div class="' + a.arrowClass + '"></div>');
            var i = t("." + a.arrowClass)
                , s = a.location;
            "right" != s && "left" != s && (s = "right");
            var r = a.locationOffset;
            r < 0 && (r = 0);
            var c = a.bottomOffset;
            c < 0 && (c = 0);
            var l = a.containerRadius;
            l < 0 && (l = 0);
            var u = a.trigger;
            u < 0 && (u = 0);
            var d = a.hideUnderWidth;
            d < 0 && (d = 0);
            var h, p = /(^#[0-9A-F]{6}$)|(^#[0-9A-F]{3}$)/i;
            h = p.test(a.containerColor) ? a.containerColor : "#000";
            var f;
            f = p.test(a.arrowColor) ? a.arrowColor : "#fff",
            "" === a.title && (a.titleAsText = !1);
            var g = {};
            g = {
                position: "fixed",
                width: 40,
                height: 40,
                background: h,
                cursor: "pointer"
            },
                g.bottom = c,
                g[s] = r,
                g["border-radius"] = l;
            var m;
            if (t(o).css(g),
                a.titleAsText) {
                t("body").append('<div class="' + a.titleAsTextClass + '">' + a.title + "</div>"),
                    m = t("." + a.titleAsTextClass),
                    t(m).attr("style", t(o).attr("style")),
                    t(m).css("background", "transparent").css("width", 80).css("height", "auto").css("text-align", "center").css(s, r - 20);
                var y = t(m).height() + 10;
                t(o).css("bottom", "+=" + y + "px")
            } else
                t(o).attr("title", a.title);
            var v = {};
            v = {
                width: 0,
                height: 0,
                margin: "0 auto",
                "padding-top": 13,
                "border-style": "solid",
                "border-width": "0 10px 10px 10px",
                "border-color": "transparent transparent " + f + " transparent"
            },
                t(i).css(v);
            var b = !1;
            t(window).resize(function() {
                t(window).outerWidth() <= d ? (b = !0,
                    e(t(o), "hide", a.entryAnimation),
                m && e(t(m), "hide", a.entryAnimation)) : (b = !1,
                    t(window).trigger("scroll"))
            }),
            t(window).outerWidth() <= d && (b = !0,
                t(o).hide(),
            m && t(m).hide()),
                a.alwaysVisible ? (e(t(o), "show", a.entryAnimation),
                m && e(t(m), "show", a.entryAnimation)) : t(window).scroll(function() {
                    t(window).scrollTop() >= u && !b && (e(t(o), "show", a.entryAnimation),
                    m && e(t(m), "show", a.entryAnimation)),
                    t(window).scrollTop() < u && !b && (e(t(o), "hide", a.entryAnimation),
                    m && e(t(m), "hide", a.entryAnimation))
                }),
            t(window).scrollTop() >= u && !b && (e(t(o), "show", a.entryAnimation),
            m && e(t(m), "show", a.entryAnimation)),
                t(o).on("click", function() {
                    return t("html,body").animate({
                        scrollTop: 0
                    }, a.goupSpeed),
                        !1
                }),
                t(m).on("click", function() {
                    return t("html,body").animate({
                        scrollTop: 0
                    }, a.goupSpeed),
                        !1
                })
        }
        ;
        var n = 160
            , a = 60
            , o = "";
        t(window).outerWidth() <= 768 && (n = 80,
            a = 16,
            o = ""),
            t.goup({
                trigger: 100,
                bottomOffset: n,
                locationOffset: a,
                title: o,
                titleAsText: !0
            })
    }(jQuery),
    function(t) {
        t(document).ready(function() {
            var e = "/login";
            location.search && location.search.length > 0 && (e += "?redirect_url=" + location.pathname + location.search),
            (!location.search || location.search.length <= 0) && (e += "?redirect_url=" + location.pathname),
            location.pathname.includes("login") && (e = "/login"),
            location.pathname.includes("register") && (e = "/login"),
            location.pathname.includes("request-reset-password") && (e = "/login"),
                t(".login-link").attr("href", e)
        })
    }(jQuery),
    function(t) {
        t(document).ready(function() {
            t(".lg-my-star-pages-side-bar").click(function() {
                var e = Cookies.getJSON("mobileToken") || "";
                t.ajax({
                    type: "GET",
                    url: "/user/api/star-pages?mobileToken=" + e,
                    headers: {
                        Accept: "application/json; charset=utf-8",
                        "X-CSRF-Token": document.getElementsByName("_csrf")[0].content
                    },
                    success: function(e) {
                        var n = "";
                        e.filter(function(t) {
                            return 3 === t.type
                        }).forEach(function(t) {
                            n += "<div class='lg-my-star-modal-item col-md-6 col-xs-12'><a class='lg-my-star-modal-link' target='_blank' href='" + t.pagePath + "'>" + t.pathName + "</a></div>"
                        }),
                            t("#my-star-chart-data").html("<div class='lg-my-star-modal-tab-content row'>" + (n.length > 0 ? n : "目前没有收藏") + "</div>");
                        var a = "";
                        e.filter(function(t) {
                            return 1 === t.type
                        }).forEach(function(t) {
                            a += "<a class='lg-my-star-modal-link' style='padding-top: 5px' target='_blank' href='" + t.pagePath + "'>" + t.pathName + "</a>"
                        }),
                            t("#my-star-stock-data").html("<div class='lg-my-star-modal-tab-content'>" + (a.length > 0 ? a : "目前没有收藏") + "</div>")
                    },
                    dataType: "json"
                }),
                    t.ajax({
                        type: "GET",
                        url: "/stockdata/user-aggregation-charts",
                        headers: {
                            Accept: "application/json; charset=utf-8",
                            "X-CSRF-Token": document.getElementsByName("_csrf")[0].content
                        },
                        success: function(e) {
                            var n = "";
                            e.forEach(function(t) {
                                n += "<div class='lg-my-star-modal-item col-md-6 col-xs-12'><a class='lg-my-star-modal-link' target='_blank' href='/stockdata/chart-builder?id=" + t.id + "'>" + t.chartName + "</a></div>"
                            }),
                                t("#my-charts").html("<div class='lg-my-star-modal-tab-content row'>" + (n.length > 0 ? n : "目前没有自定图表") + "</div>")
                        },
                        dataType: "json"
                    })
            })
        })
    }(jQuery),
    function(t) {
        t(document).ready(function() {
            t(document).on("click", function() {
                t(t(".navbar-toggle").get()).hasClass("collapsed") || t("#navbar-collapse").collapse("hide")
            })
        })
    }(jQuery),
    function() {
        function t() {
            const t = {
                lookup: function(t, e) {
                    t ? $.ajax({
                        type: "GET",
                        url: window.location.origin + "/s/auto-complete?query=" + t,
                        headers: {
                            Accept: "application/json; charset=utf-8",
                            "X-CSRF-Token": document.getElementsByName("_csrf")[0].content
                        },
                        success: function(n) {
                            const a = o.suggestions.filter(function(e) {
                                return e.value.indexOf(t) > -1
                            });
                            if (a && a.suggestions && a.suggestions.length > 0) {
                                const i = a.suggestions.concat(n.suggestions || []);
                                e({
                                    suggestions: i
                                })
                            } else
                                e(n)
                        },
                        dataType: "json"
                    }) : e(o)
                },
                beforeRender: function(t, e) {
                    var n = $(this).data("autocomplete").suggestions.length - 1;
                    "删除搜索历史" === $(this).data("autocomplete").suggestions[n].value && t.find(".autocomplete-suggestion").eq(n).css("color", "#9e9e9e").append($('<span style="line-height: 36px;display: inline-block; height: 36px; vertical-align: middle;" class="pull-right glyphicon glyphicon-trash">'))
                },
                deferRequestBy: 200,
                appendTo: "#search-form",
                minChars: 0,
                onSelect: function(t) {
                    if ("删除搜索历史" === t.value)
                        localStorage.removeItem("searchHistory"),
                            o.suggestions = [],
                            $("#autocomplete").val("");
                    else {
                        var e = t.data.match(/\d+/g);
                        null !== e && 9 === t.data.length && (window.location.href = window.location.origin + "/s/" + t.data),
                        null !== t.url && 0 === t.data.length && (window.location.href = window.location.origin + t.url),
                        t.value === t.data && t.data.length > 0 && (window.location.href = window.location.origin + "/search?text=" + t.data + "&page=1")
                    }
                }
            };
            $("#autocomplete").autocomplete(t).on("focus", function() {
                $(this).autocomplete().getSuggestions()
            }),
                $("#mobile-autocomplete").autocomplete(t).on("focus", function() {
                    $(this).autocomplete().getSuggestions()
                })
        }
        function e(t) {
            var e = new Date(t)
                , n = "" + (e.getMonth() + 1)
                , a = "" + e.getDate()
                , o = e.getFullYear();
            return n.length < 2 && (n = "0" + n),
            a.length < 2 && (a = "0" + a),
                [o, n, a].join("-")
        }
        const n = localStorage.getItem("searchHistory")
            , a = JSON.parse(n)
            , o = {
            suggestions: a && a.map(function(t) {
                return {
                    value: t,
                    data: t
                }
            }) || []
        };
        o && o.suggestions && o.suggestions.length > 0 && o.suggestions.push({
            value: "删除搜索历史",
            data: ""
        }),
            $(document).ready(function() {
                t();
                var n = 0;
                $(".top-nav-search-icon").on("click", function() {
                    if ($("#mobile-search-form").addClass("lg-mobile-search"),
                    0 === n) {
                        var t = new Hashes.MD5
                            , a = t.hex(e(new Date));
                        $.ajax("/api/stockdata/latest-top-10-fund-sw-industry-holding-industry-name?token=" + a, {
                            headers: {
                                Accept: "application/json",
                                "Content-Type": "application/json",
                                "X-CSRF-Token": document.getElementsByName("_csrf")[0].content
                            },
                            method: "GET",
                            success: function(t) {
                                t.forEach(function(t) {
                                    const e = "/search?text=" + t + "&page=1";
                                    $("#recent-search").append('<a href="' + e + '">' + t + "</a>")
                                }),
                                    n++
                            },
                            error: function(t) {
                                console.log(t)
                            }
                        })
                    }
                }),
                    $(".mobile-search-close-icon").on("click", function() {
                        $("#mobile-search-form").removeClass("lg-mobile-search")
                    }),
                    $(".lg-nav-search-icon").on("click", function() {
                        if ($(".lg-nav-search-panel").toggle(),
                        0 === n) {
                            var t = new Hashes.MD5
                                , a = t.hex(e(new Date));
                            $.ajax("/api/stockdata/latest-top-10-fund-sw-industry-holding-industry-name?token=" + a, {
                                headers: {
                                    Accept: "application/json",
                                    "Content-Type": "application/json",
                                    "X-CSRF-Token": document.getElementsByName("_csrf")[0].content
                                },
                                method: "GET",
                                success: function(t) {
                                    t.forEach(function(t) {
                                        const e = "/search?text=" + t + "&page=1";
                                        $("#hot-searches").append('<a href="' + e + '">' + t + "</a>")
                                    }),
                                        n++
                                },
                                error: function(t) {
                                    console.log(t)
                                }
                            })
                        }
                    }),
                    $(".lg-nav-search-panel").on("mouseleave", function() {
                        $(".lg-nav-search-panel").hide()
                    }),
                    $("#search-icon").on("click", function() {
                        var t = $("#autocomplete").val();
                        location.href = "/search?text=" + t + "&page=1"
                    })
            })
    }(),
    function(t) {
        t(document).ready(function() {
            function e() {
                var e, n = document.title.split("_")[0];
                return location.pathname.search(/\/s\//) >= 0 ? n = n.split("(")[0] : (n = t("h1").html(),
                    e = location.href.split("?")[1],
                void 0 === e && (e = "")),
                "pagePath=" + location.pathname + "&pathName=" + encodeURIComponent(n) + "&pathParam=" + e
            }
            function n() {
                t.ajax({
                    type: "POST",
                    url: "/user/toggle-star-of-page?mobileToken=" + a + "&" + e(),
                    data: {},
                    headers: {
                        Accept: "application/json; charset=utf-8",
                        "X-CSRF-Token": document.getElementsByName("_csrf")[0].content
                    },
                    success: function(e) {
                        e ? (t("#star-btn").html('<button id="user-star-btn" class="star-fix"><i class="fa fa-star" aria-hidden="true"></i><span class="star-text">已收藏</span></button>'),
                            t("#user-star-btn").click(n)) : (t("#star-btn").html('<button id="user-star-btn" class="star-fix"><i class="fa fa-star-o" aria-hidden="true"></i><span class="star-text">收藏</span></button>'),
                            t("#user-star-btn").click(n))
                    },
                    error: function() {
                        location = "/login?redirect_url=" + location.href
                    },
                    dataType: "json"
                })
            }
            var a = Cookies.getJSON("mobileToken") || "";
            void 0 != t("#star-btn").html() && t.ajax({
                type: "POST",
                url: "/user/is-this-page-star?mobileToken=" + a + "&" + e(),
                data: {},
                headers: {
                    Accept: "application/json; charset=utf-8",
                    "X-CSRF-Token": document.getElementsByName("_csrf")[0].content
                },
                success: function(e) {
                    e ? (t("#star-btn").html('<button id="user-star-btn" class="star-fix"><i class="fa fa-star" aria-hidden="true"></i><span class="star-text">已收藏</span></button>'),
                        t("#user-star-btn").click(n)) : (t("#star-btn").html('<button id="user-star-btn" class="star-fix"><i class="fa fa-star-o" aria-hidden="true"></i><span class="star-text">收藏</span></button>'),
                        t("#user-star-btn").click(n))
                },
                error: function() {
                    t("#star-btn").html('<button id="user-star-btn" class="star-fix"><i class="fa fa-star-o" aria-hidden="true"></i><span class="star-text">收藏</span></button>'),
                        t("#user-star-btn").click(n)
                },
                dataType: "json"
            })
        })
    }(jQuery),
    function(t) {
        t(document).ready(function() {
            var e = t(".lg-updates .updates-items");
            e.length > 0 && t(".lg-updates .updates-items").mCustomScrollbar({
                theme: "minimal-dark"
            })
        })
    }(jQuery);
