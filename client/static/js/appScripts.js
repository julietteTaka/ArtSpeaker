$( document ).ready(function() {

/* ------------ OFFERS ---------- */
    $('#offerStepTwo').submit(function(event){
        event.preventDefault();
        var userId = $("#createOffer").attr("data-userID");
        var offerId = $("#createOffer").attr("data-offerID");

        var text = $("#text").val();
        var begin = $("#begin").val();
        var end = $("#end").val();

        var offerTitle = $("#offerTitle").val();

        var wantedProfile = $("#wantedProfiles").val();

        var offerDate = {  'begin' : begin,
                            'end' : end,
                        }

        $.ajax({
            type : 'POST',
            url : '/offer/'+offerId+'/step/2',
            contentType: 'application/json; charset=utf-8',
            data : JSON.stringify({
                    'userId' : userId,
                    'offerTitle' : offerTitle,
                    'offerDate' : offerDate,
                    'wantedProfile' : wantedProfile,
                    'text' : text,
                    'isComplete' : "True",
                    }),
            error: function (data, ajaxContext) {
                console.log(ajaxContext.responseText)
            },
        }).done(function(data){
            location.href = "/user/"+userId+"/offers";
        });
    });


    $('#offerStepOne').submit(function(event){
        event.preventDefault();
        var userId = $("#createOffer").attr("data-userID");
        var projectTitle = $("#projectTitle").val();
        var text = $("#text").val();
        var place = $("#place").val();
        var fieldActivity = $("#fieldActivity").val();
        var begin = $("#begin").val();
        var end = $("#end").val();
        var phone = $("#phone").val();
        var mail = $("#mail").val();
        var name = $("#name").val();

        var projectDate = {  'begin' : begin,
                            'end' : end,
                        }

        var contact = { 'name' : name,
                        'phone' : phone,
                        'mail' : mail,
                        }
        var networking = []

        $("#networks div").each(function(){
            networking.push({
                'network' : $(this).find("select option:selected").val(),
                'url' : $(this).find("input").val(),
            })
        })

        $.ajax({
            type : 'POST',
            url : '/offer',
            contentType: 'application/json; charset=utf-8',
            data : JSON.stringify({
                    'userId' : userId,
                    'projectTitle' : projectTitle,
                    'fieldActivity' : fieldActivity,
                    'place' : place,
                    'networking' : networking,
                    'projectDate' : projectDate,
                    'contact' : contact,
                    }),
            error: function (data, ajaxContext) {
                console.log(ajaxContext.responseText)
            },
        }).done(function(data){
            location.href = "/offer/"+data.offerId+"/step/2";
        });
    });


    $('button#deleteOffer').click(function(event){
        event.preventDefault();
        var offerId = $(this).attr("data-offerId")
        $.ajax({
            type : 'DELETE',
            url : '/offer/'+ offerId,
            success: function(){
                location.reload();
            }
        });
    })

    $('button#completeOffer').click(function(event){
        event.preventDefault();
        var offerId = $(this).attr("data-offerId")
        location.href = '/offer/'+ offerId+'/step/1';
    });

/* ------------ PORTFOLIO ---------- */
$('#portfolioCreation').submit(function(event){
        event.preventDefault();
        var userId = $("#createPortfolio").attr("data-userID");
        var pseudo = $("#pseudo").val();
        var place = $("#place").val();
        var fieldActivity = $("#fieldActivity").val();
        var begin = $("#begin").val();
        var end = $("#end").val();
        var phone = $("#phone").val();
        var mail = $("#mail").val();
        var name = $("#name").val();

        var availability = {  'begin' : begin,
                            'end' : end,
                        }

        var contact = { 'name' : name,
                        'phone' : phone,
                        'mail' : mail,
                        }
        var networking = []

        $("#networks div").each(function(){
            networking.push({
                'network' : $(this).find("select option:selected").val(),
                'url' : $(this).find("input").val(),
            })
        })

        $.ajax({
            type : 'POST',
            url : '/portfolio',
            contentType: 'application/json; charset=utf-8',
            data : JSON.stringify({
                    'userId' : userId,
                    'pseudo' : pseudo,
                    'fieldActivity' : fieldActivity,
                    'place' : place,
                    'networking' : networking,
                    'availability' : availability,
                    'contact' : contact,
                    }),
            error: function (data, ajaxContext) {
                console.log(ajaxContext.responseText)
            },
        }).done(function(data){
            location.href = "/user/"+userId+"/portfolio";
        });
    });

    $('button#deletePortfolio').click(function(event){
        event.preventDefault();
        if (confirm('Are you sure you want to delete your beautiful portfolio ?')) {
            var portfolioId = $(this).attr("data-portfolioId")
            $.ajax({
                type : 'DELETE',
                url : '/portfolio/'+ portfolioId,
                success: function(){
                    location.href = "/user/"+userId+"/portfolio"
                }
            });
        }
    })

/* ------------ FORMS ---------- */

    var i = $('#networks div').size();

    $('.addField').click(function(event)
    {
        $('<div><select name="social" size="1"><option value="website" selected="selected">website</option><option value="Facebook">Facebook</option><option value="Twitter">Twitter</option><option value="Other">Custom link</option></select><input type="text" class="link" placeholder="www.monsite.com" /><span class="removeField" onclick=""> Remove </span></div>').appendTo("#networks");
        i++;
    });

    
    $('#networks').on('click', '.removeField', function () {
        if( i > 1 ) {
            $(this).parent('div').remove();
            i--;
        }
    });

    $('#checkbox_always').change(function() {
        if(this.checked) {
            $('#availability #end').attr('readonly', true);
            $('#availability #end').addClass('input-disabled');
            $('#availability #begin').attr('readonly', true);
            $('#availability #begin').addClass('input-disabled');
        }else
        {
            $('#availability #end').attr('readonly', false);
            $('#availability #end').addClass('input-enabled');
            $('#availability #begin').attr('readonly', false);
            $('#availability #begin').addClass('input-enabled');
        }
    });

    /* ---------------UPLOAD --------------*/

//Cover picture

        $("#uploadtrigger").click(function(event){
            event.preventDefault();

            var form_data = new FormData($('#addCoverPictureForm')[0]);

            var portfolioId = $("#addCoverPicture").attr("attr-portfolioId");
            var userId = $("#addCoverPicture").attr("attr-userId");

            url = "/user/"+userId+"/portfolio/"+portfolioId+"/cover";
            $.ajax({
                    type : 'POST',
                    url : url,
                    data:form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function(data){
                        $("#cover").attr('class', 'customCover');
                        location.reload();
                    },
                    error:function(data){
                        console.log(data);
                    }
                }).done(function(){
                    $("#addCoverPictureModal").hide();
                    $('.modal-backdrop').remove();
                })
        });

});




/* ------------ PAGINATION ---------- */
function pagination(){
    console.log( $('#pagination').attr("data-page"));
    var perPage = $('#pagination').attr("data-perPage");
    var currentPage = $('#pagination').attr("data-page");
    var totalPage = $('#pagination').attr("data-totalPages");
    var content = "";

    //all pages displayed :
    for (i=1; i<totalPage; i++){
        if(i == currentPage)
            content+="<a href='/offers/number/"+perPage+"/page/"+i+"'> <strong> "+i+" </strong></a>"
        else
            content+="<a href='/offers/number/"+perPage+"/page/"+i+"'> "+i+" </a>"
    }

    //TODO : skip middle pages

    //display pagination
    $("#pagination").append(content);
}