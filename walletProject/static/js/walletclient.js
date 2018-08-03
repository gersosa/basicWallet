var localhost = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');


$( "#login" ).submit(function() {
  console.log('entraaaa')
  $.ajax({
       type: 'POST',
       data: {
        username:$('#inputUsername').val(),
        password:$('#inputPassword').val(),
       },
       url: localhost+'/api-token-auth',
       success: function(res){
               console.log(res)
               $.ajaxSetup({
                  headers: {
                    "token": res.token
                  }
               });
       },
       error: function(error) {
           callbackErr(error,self)
       }
   })
});