function select_car_search_field() {
            var text = $(this).html();
            $(this).parent().parent().parent().parent().find('dt a span').html(text);
            $(this).parent().parent().parent().find('ul').hide();
        }


$(function () {

    function navbar_affix() {
        var screen_width = $(window).width();
        var navbar_selector = $('.navbar-custom');
        if (screen_width >= 768) {
            navbar_selector.affix({
                offset: {
                    top: $('header').height()
                }
            });
            navbar_selector.children().addClass('navbar-collapse');
            navbar_selector.removeClass('sb-slidebar sb-left');
        } else {
            $(window).off('.affix');
            navbar_selector.removeData('bs.affix').removeClass('affix affix-top affix-bottom');
            navbar_selector.children().removeClass('navbar-collapse');
            navbar_selector.addClass('sb-slidebar sb-left');
        }
    }

    function move_search() {
        var screen_width = $(window).width();
        var search_form = $('#search-form');
        var search_placeholder_xs = $('#block-search-form-xs');
        var search_placeholder_sm = $('#block-search-form-sm');
        if (screen_width >= 768) {
            search_placeholder_xs.hide();
            search_placeholder_sm.show();
            search_form.appendTo(search_placeholder_sm);
        } else {
            search_placeholder_sm.hide();
            search_placeholder_xs.show();
            search_form.appendTo(search_placeholder_xs);
        }
    }

    function toggle_benefits_tooltip() {
      var screen_width = $(window).width();
      var benefit_selector = $('.benefit');

      if (screen_width >= 992) {
        benefit_selector.tooltip('disable');
      } else {
        benefit_selector.tooltip('enable');
      }

    }

    $('#select_vehicle, #select_brand, #select_model, #select_type').on('change', function() {
        
        var select_data = {
            'vehicle': $('#select_vehicle option:selected').val(),
            'brand': $('#select_brand option:selected').val(),
            'model': $('#select_model option:selected').val(),
            'type': $('#select_type option:selected').val()
        };
    
        $.ajax({
            url: '/',
            type: 'POST',
            data: select_data,
            dataType: 'json',
            success: function(json) {
    
                $('#select_vehicle').empty();
                $('#vehicle-title').text('Select Vehicle');
                $('#select_vehicle').append($("<option value=''>Select Vehicle</option>"));
                $.each(json['vehicles'], function(key, value) {
                    var $item = $("<option value='" + value + "'>" + value + "</option>");
                    $('#select_vehicle').append($item);
                    if (value == select_data['vehicle']) {
                        $('#select_vehicle').val(value);
                        $('#vehicle-title').text(value);
                    }
                });
    
                $('#select_brand').empty();
                $('#brand-title').text('Select Brand');
                $('#select_brand').append($("<option value=''>Select Brand</option>"));
                $.each(json['brands'], function(key, value) {
                    var $item = $("<option value='" + value + "'>" + value + "</option>");
                    $('#select_brand').append($item);
                    if (value == select_data['brand']) {
                        $('#select_brand').val(value);
                        $('#brand-title').text(value);
                    }
                });
    
                $('#select_model').empty();
                $('#model-title').text('Select Model');
                $('#select_model').append($("<option value=''>Select Model</option>"));
                $.each(json['models'], function(key, value) {
                    var $item = $("<option value='" + value + "'>" + value + "</option>");
                    $('#select_model').append($item);
                    if (value == select_data['model']) {
                        $('#select_model').val(value);
                        $('#model-title').text(value);
                    }
                });
    
                $('#select_type').empty();
                $('#type-title').text('Select Type');
                $('#select_type').append($("<option value=''>Select Type</option>"));
                $.each(json['type_data'], function(key, value) {
                    var $item = $("<option value='" + value[0] + "'>" + value[1] + "</option>");
                    $('#select_type').append($item);
                    if (value[0] == select_data['type']) {
                        $('#select_type').val(value[0]);
                        $('#type-title').text(value[1]);
                    }
                });
            }
        });
    });

    $(document).ready(function () {
        navbar_affix();


        var tooltip_selector = $('*[data-toggle="tooltip"]');
        tooltip_selector.tooltip();
        tooltip_selector.on('shown.bs.tooltip', function () {
            var tooltip_id = jQuery(this).attr('aria-describedby');
            var tooltip_color = jQuery(this).data('tooltip-color');
            $('#' + tooltip_id + '> .tooltip-inner').addClass(tooltip_color);
        });
		
/*        $('.block-container-selects').backstretch([
            "static/images/slider-first.png",
            "static/images/slider-second.jpg"
        ], {duration: 10000, fade: 750});
*/	
	/*=== update// : "static/images/slider-first.png" to "../../static/images/slider-first-2.png"  === */
        $('.block-container-selects').backstretch([
            "../../static/images/slider-first.jpg",
            "../../static/images/slider-second.jpg"
        ], {duration: 5000, fade: 750});
		/** // update **/


        var swipebars = new $.slidebars({
            disableOver: 767,
            hideControlClasses: true,
            siteClose: false
        });

        var html_selector = $('html');

        // Left Swipe
        $(document).on('swipeleft', function (event) {
            if (html_selector.hasClass('sb-active-left')) {
                // The left Slidebar is open, close it.
                swipebars.slidebars.close();
            } else if (html_selector.hasClass('sb-active-right')) {
                // The right Slidebar is open, do nothing.
            } else {
                // No Slidebar is open, open the right.
                swipebars.slidebars.open('right');
            }
        });

        // Right Swipe
        $(document).on('swiperight', function (event) {
            if (html_selector.hasClass('sb-active-left')) {
                // The left Slidebar is open, do nothing.
            } else if (html_selector.hasClass('sb-active-right')) {
                // The right Slidebar is open, close it.
                swipebars.slidebars.close();
            } else {
                // No Slidebar is open, open the right.
                swipebars.slidebars.open('left');
            }
        });

        var closeSlidebars = function (event) {
            if (html_selector.hasClass('sb-active-left') || html_selector.hasClass('sb-active-right')) {
                event.preventDefault();
                event.stopPropagation();
                swipebars.slidebars.close();
            }
        };

        // Click or Tap to Close
        $('.sb-slide').on('click tap', closeSlidebars);

        var benefit_selector = $('.benefit');
        benefit_selector.tooltip({
          placement: 'bottom',
          title: function(){
            return $(this).children('span').text()
          }
        });
        toggle_benefits_tooltip();

    });

    $(window).on('resize', function () {
        navbar_affix();
        toggle_benefits_tooltip();
    });

    // Add (+/-) Button Number Incrementers for product page
    $(".button-change").on("click", function() {

      var $span = $(this);
      var oldValue = $span.parent().find("input").val();

      if ($span.text() == "+") {
          var newVal = parseFloat(oldValue) + 1;
        } else {
       // Don't allow decrementing below one
        if (oldValue > 1) {
          var newVal = parseFloat(oldValue) - 1;
        } else {
          newVal = 1;
        }
      }

      $span.parent().find("input").val(newVal);

    });// End of add (+/-) Button Number Incrementers for product page

    // Add image galary for product in product page
    $.fn.simplegallery = function(options) {

        var defaults = {
            'galltime': 300,
            'gallcontent': '.content',
            'gallthumbnail': '.thumbnail',
            'gallthumb': '.thumb'
        };

        var settings = $.extend({}, defaults, options);

        return this.each(function() {

            $(settings.gallthumb).click(function() {

                $(settings.gallcontent).find('img').stop(true,true).fadeOut(settings.galltime).hide();

                var img_attr = $(this).find('img').attr("id"),
                    image_id = img_attr.replace('thumb_', '');

                $('.image_' + image_id + '').stop(true,true).fadeIn(settings.galltime);
                return false;

            });

        });

    };
    $('#gallery').simplegallery({
        galltime : 400,
        gallcontent: '.gall-content',
        gallthumbnail: '.gall-thumbnail',
        gallthumb: '.thumb'
    });

    $('a.goback').click(function(){
        window.history.back();
        return false;
    });// End Add image galary for product in product page
	
});

// Fix select styles for safari and chrome on MacOs 
var ua = navigator.userAgent.toLowerCase(); 
  if (navigator.appVersion.indexOf("Mac")!=-1) {
    if (ua.indexOf('chrome') > -1) {
        $('.form__select_custom').each(function(){ 
        $(this).find('select').css({
        top: 1,
        left: 10
        });
    });
    } else if (ua.indexOf('safari') != -1) {
      $('.form__select_custom').each(function(){ 
        $(this).find('select').css({
        top: -2,
        left: 10
        });
    });
    } else {
        
    }
  }

// Disable auto zoom on iphone or ipad when tap on select
var iOS = ( navigator.userAgent.match(/(iPad|iPhone|iPod)/g) ? true : false );
    if(iOS) { $('.form__select_custom select').css('font-size', '50px'); }


//$("#id_score").replaceWith('<input type="number" name="score" id="id_score" class="rating" min=0 max=5 step=1 data-size="xs"/>');