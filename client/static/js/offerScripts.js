$( document ).ready(function() {

    $('#offerStepOne').submit(function(event, offerStepOne){
        event.preventDefault();
        var userId = $("#createOffer").attr("data-userID");
        var projectTitle = $("#projectTitle").val();
        var text = $("#text").val();
        var place = $("#place").val();
        var entreprise = $("#entreprise").val();
        var networking = $("#networking").val();
        var begin = $("#begin").val();
        var end = $("#end").val();
        var phone = $("#phone").val();
        var mail = $("#mail").val();
        var name = $("#name").val();
        var wantedProfiles = ($("#wantedProfiles").val()).split(",");
        var remuneration = $("#remuneration").val();

        var offerDate = {  'begin' : begin,
                            'end' : end,
                        }

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
                    'wantedProfiles' : wantedProfiles,
                    'remuneration' : remuneration,
                    }),
            error: function (data, ajaxContext) {
                console.log(ajaxContext.responseText)
            }
        }).done(function(data, offerStepOne){
            console.log("done !" + data);
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
});