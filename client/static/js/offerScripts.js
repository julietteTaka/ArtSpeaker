$( document ).ready(function() {

    $('#offerStepTwo').submit(function(event){
        event.preventDefault();
        var userId = $("#createOffer").attr("data-userID");
        var offerId = $("#createOffer").attr("data-offerID");

        var text = $("#text").val();
        var begin = $("#begin").val();
        var end = $("#end").val();

        var wantedProfiles = $("#wantedProfiles").val();
        var tags = (($("#tags").val()).split("#")).shift();

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
                    'wantedProfiles' : wantedProfiles,
                    'tags' : tags,
                    'text' : text,
                    'isComplete' : True,
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
        var activity = $("#activity").val();
        var entreprise = $("#entreprise").val();
        var begin = $("#begin").val();
        var end = $("#end").val();
        var phone = $("#phone").val();
        var mail = $("#mail").val();
        var name = $("#name").val();
        var remuneration = $("#remuneration").val();

        var offerDate = {  'begin' : begin,
                            'end' : end,
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
                    'place' : place,
                    'text' : text,
                    'entreprise' : entreprise,
                    'networking' : networking,
                    'offerDate' : offerDate,
                    'name' : name,
                    'phone' : phone,
                    'mail' : mail,
                    'activity' : activity,
                    //'wantedProfiles' : wantedProfiles,
                    'remuneration' : remuneration,
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
        location.href = '/offer/'+ offerId+'/step/2';
    });




    var i = $('#networks div').size() + 1;

    $('.addField').click(function(event){
        i = $('#networks div').size() + 1;
        $('<div><select name="social" size="1"><option value="website" selected="selected">website</option><option value="Facebook">Facebook</option><option value="Twitter">Twitter</option><option value="Other">Custom link</option></select><input style="width:800px; type="text" class="link" placeholder="www.monsite.com" /> <span class="removeField" style="cursor:pointer;"> Remove </span></div>').appendTo("#networks")
        i++;
    });

    /*FIXME

    $(".removeField").click(function(event){
        console.log("remove")
        if( i > 2 ) {
            $(this).parents('div').remove();
            i--;
        }
    });
    */
});