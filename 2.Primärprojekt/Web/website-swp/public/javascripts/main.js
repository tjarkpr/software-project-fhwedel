$(document).ready(function () {
    // add filename to label when imgae is uploaded
    $(function () {
        $("#inputImg").change(function (event) {
            var x = event.target.files[0].name
            $("#inputImgLabel").text(x)
        });
    })

    $(function () {
        $("#referenceImg").change(function (event) {
            var x = event.target.files[0].name
            $("#referenceImgLabel").text(x)
        });
    })

    // make at least 1 checkebox required
    $(function () {
        var requiredCheckboxes = $('.methods[required]');
        requiredCheckboxes.change(function () {
            if (requiredCheckboxes.is(':checked')) {
                requiredCheckboxes.removeAttr('required');
            } else {
                requiredCheckboxes.attr('required', 'required');
            }
        });
    });

    $(function () {
        var requiredCheckboxes = $('.dataset[required]');
        requiredCheckboxes.change(function () {
            if (requiredCheckboxes.is(':checked')) {
                requiredCheckboxes.removeAttr('required');
            } else {
                requiredCheckboxes.attr('required', 'required');
            }
        });
    });

    // stop images from being too small on small screen width
    $(window).resize(function () {
        if ($(window).width() < 768) {
            $('.outputImg').each(function () {
                $(this).removeClass("img-fluid");
                $(this).addClass("img-small");
            });
        } else {
            $('.outputImg').each(function () {
                $(this).addClass("img-fluid");
                $(this).removeClass("img-small");
            });
        }
    })

    $('#overlay').addClass('hidden');
});

$(window).on("pagehide",function(){
     $('#overlay').addClass('hidden');
})

function addOverlay() {
    $('#overlay').removeClass('hidden');
    $('#inputImgLabel').html('');
    $('#referenceImgLabel').html('');
}

function selectAll(s,bool) {
    $(s).each(function() {
        $(this).prop('checked', bool);
    });
}
