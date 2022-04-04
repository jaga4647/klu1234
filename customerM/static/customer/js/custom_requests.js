// Edit Delete requests for Blueprint
// Common funtion
// $.delete = function (url, data, callback, type) {
//     if ($.isFunction(data)) {
//         type = type || callback,
//             callback = data,
//             data = {}
//     }
//     return $.ajax({
//         url: url,
//         type: 'DELETE',
//         success: callback,
//         data: data,
//         contentType: type
//     });
// }

// function extract_form_data_handler(event){
//     eventData={};
//     var inputs = event.originalEvent.srcElement.getElementsByTagName("Input");
//     for (var index=0; index<inputs.length-1; index++){
//         if (inputs[index].name==="csrfmiddlewaretoken"){
//             eventData["csrfmiddlewaretoken"]=inputs[index].value;
//         }else{
//             eventData[inputs[index].name]=inputs[index].value;
//         }
//     }
//     return eventData;
// }
// function extract_action_url_handler(event){
//     return event.originalEvent.srcElement.getAttribute('action');
// }
// function send_delete_request(event){
//     event.preventDefault();
//     data=extract_form_data_handler(event);
//     url=extract_action_url_handler(event);
//     $.delete(url=url, data=data, callback=null, type="DELETE");
// }

// // Page specific 
// $(document).ready(function() {
//     $('#blueprint_delete_button').click(function(event) {
//         $('#blueprint_delete').submit(send_delete_request);
//     });

//     // $('#blueprint_edit_button').click(function(event) {
//     //     $('#blueprint_edit').submit(extract_action_url_handler);
//     // });
// });

function success(data){
    var selectTag = document.getElementById("dealer");
    var d = JSON.parse(data)
    if (d.length>1){
        selectTag.innerHTML="";
        for (var dealer in d.slice(1)){
            var pk = d[parseInt(dealer)+1][0];
            var name = d[parseInt(dealer)+1][1];
            var optTag = "<option value='"+pk+"'>"+name+"</option>";
            selectTag.innerHTML += optTag;

        }
    }
}
function retrieveDealers(carElement){
    if (carElement.value!==""){
        var req = $.get("/customer/getDealers/", {'carId': carElement.value});
        req.done(success);
    }
}
