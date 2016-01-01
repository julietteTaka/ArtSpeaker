$( document ).ready(function() {

    $('#offerStepOne').submit(function(event, offerStepOne){
        event.preventDefault();
        var userId = $("#createOffer").attr("data-userID");
        var projectTitle = $("#projectTitle").val();
        var text = $("#text").val();
        var entreprise = $("#entreprise").val();
        var networking = $("#networking").val();
        var begin = $("#begin").val();
        var end = $("#end").val();
        var phone = $("#phone").val();
        var mail = $("#mail").val();
        var profileType = $("#profileType").val();
        var remuneration = $("#remuneration").val();

        $.ajax({
            type : 'POST',
            url : '/offer',
            data : {'userId' : userId,
                    'projectTitle' : projectTitle,
                    'text' : text,
                    'entreprise' : entreprise,
                    'networking' : networking,
                    'begin' : begin,
                    'end' : end,
                    'phone' : phone,
                    'mail' : mail,
                    'profileType' : profileType,
                    'remuneration' : remuneration,
                    },
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