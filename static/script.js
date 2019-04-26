

$(async function(){

baseUrl = 'http://localhost:5000'


$(".like_form").on("submit", async function(evt){
    evt.preventDefault()
    let messageId = $(evt.target).attr('id')

    var response = await $.ajax({
        method: "POST",
        url: `${baseUrl}/messages/${messageId}/like`,
        contentType: "application/json",
    })
    
    if (response.likes === 'true'){
        $(`#${messageId}`).children().children().toggleClass('fas far')
    }
    else{
        $(`#${messageId}`).children().children().toggleClass('fas far')
    }

})
})