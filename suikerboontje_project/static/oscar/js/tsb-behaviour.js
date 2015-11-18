// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.
function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
};

// Quick access to CSS transform functionality.
jQuery.fn.extend({
    trans: function(x, y) {
        return this.each(function() {
            $(this).css('transform', 'translate(' + x + 'px, ' + y + 'px)');
        });
    }
});

$(function() { 
    
    var resetButtons = function() {
        $('.tsb-btn--select').removeClass('tsb-btn--select');
        $('.tsb-nav-grp--show').removeClass('tsb-nav-grp--show');
    }
    
    $('#tsb-nav-btn').click(function () {
        if ($('#tsb-nav-btn-grp').hasClass('tsb-nav-grp--show')) {
            resetButtons();
        } else {
            resetButtons();
            $('#tsb-nav-btn').addClass('tsb-btn--select');
            $('#tsb-nav-btn-grp').addClass('tsb-nav-grp--show').fadeIn();
        }
    });
    
    $('#tsb-nav-srch').click(function () {
        if ($('#tsb-nav-srch-grp').hasClass('tsb-nav-grp--show')) {
            resetButtons();
        } else {
            resetButtons();
            $('#tsb-nav-srch').addClass('tsb-btn--select');
            $('#tsb-nav-srch-grp').addClass('tsb-nav-grp--show');
        }
    });
    
    $('#tsb-nav-cart').click(function () {
        if ($('#tsb-nav-cart-grp').hasClass('tsb-nav-grp--show')) {
            resetButtons();
        } else {
            resetButtons();
            $('#tsb-nav-cart').addClass('tsb-btn--select');
            $('#tsb-nav-cart-grp .tsb-cart-list').css('max-height', $(window).height() - 220 + 'px');
            $('#tsb-nav-cart-grp').addClass('tsb-nav-grp--show');
        }
    });
    
    $('#tsb-content, #tsb-ftr').click(function () {
        resetButtons();
    });
             
    // This section should only be executed when CSS transformations are available.
    Modernizr.addTest('csstransforms', function() {

        var paralax = (function() {
            var active = false;
            var turnOn = function () {
                if (!active) {
                    $('#tsb-airplane-layer, #tsb-sun-layer, #tsb-clouds-layer').css('position', 'fixed').trans(0, 0);
                    $('#tsb-ground-top-layer, #tsb-ground-middle-layer, #tsb-rainbow-layer, #tsb-bird-layer, #tsb-ground-sky-layer').css({
                        'position': 'fixed',
                        'bottom': '0'
                    }).trans(0, 600);
                    active = true;
                }
            }
            var turnOff = function() {
                if (active) {
                    $('#tsb-airplane-layer, #tsb-sun-layer, #tsb-clouds-layer').css('position', 'absolute').trans(0, 0);
                    $('#tsb-ground-top-layer, #tsb-ground-middle-layer, #tsb-rainbow-layer, #tsb-bird-layer, #tsb-ground-sky-layer').css({
                        'position': 'absolute',
                        'bottom': 'auto'
                    }).trans(0, 0);
                    active = false;
                }
            }
            return {
                check: function() {
                    paralax.do();
                    if (jQuery(window).width() >= 800) {
                        turnOn();
                        paralax.do();
                    } else {
                        turnOff();
                    }
                },
                do: function() {
                    if (active) {
                        var topDistance = $(this).scrollTop() > 0 ? $(this).scrollTop() : 0;
                        var bottomDistance = (topDistance + $(window).height() - $('body').height() - 300 <= 0 ? topDistance + $(window).height() - $('body').height() - 300 : 0);
                        $('#tsb-clouds-layer').trans(0, -topDistance/3);
                        $('#tsb-airplane-layer').trans(0, -topDistance/5);
                        $('#tsb-sun-layer').trans(0, -topDistance/6);
                        bottomDistance < 700 ? $('#tsb-ground-top-layer').trans(0, 600 - ( (700 + bottomDistance) / 7 * 6 )) : false;                        
                        bottomDistance < 800 ? $('#tsb-ground-middle-layer').trans(0, 600 - ( (800 + bottomDistance) / 8 * 6 )) : false;                        
                        bottomDistance < 900 ? $('#tsb-rainbow-layer').trans(0, 600 - ( (900 + bottomDistance ) / 9 * 6 ) ) : false; 
                        bottomDistance < 850 ? $('#tsb-bird-layer').trans(0, 600 - ( (850 + bottomDistance ) / 8.5 * 6 ) ) : false; 
                        bottomDistance < 950 ? $('#tsb-ground-sky-layer').trans(0, 600 - ( (950 + bottomDistance ) / 9.5 * 6) ) : false; 
                    }
                }
            };
        })();
        
        paralax.check();

        $(window)
            .resize(debounce(paralax.check, 1, true))
            .scroll(debounce(paralax.do, 1, true));
    });
});