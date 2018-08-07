var localhost = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
var authorization = localhost+'/api/api-token-auth/'
var users = localhost+'/api/users/'
var wallets = localhost+'/api/wallets/'
var coins = localhost+'/api/coins/'
var operations = localhost+'/api/operations/'
var token = ''
var userid = ''
var name = ''
alertify.set('notifier','position', 'top-right');


function get_other_users() {
  var coin = $( "#wallet_origin option:selected" ).text().split('->')[0]
  $.ajax({
    url: wallets+'havent_user/',
    type: 'GET',
    dataType: 'json',
    data: {
      user: name
    },
    success: function(data, status) {
      $('#wallet_to').children('option:not(:first)').remove();
      data.forEach(function(e) {
        if (coin == e['coin']['name']) {
          $('#wallet_to').append($('<option>', {
            value: e['id'],
            text: e['coin']['name']+'->'+e['cant']+'-'+e['user']['username']
          }));
        }
      });
    },
    beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','JWT ' + token); } 
  });
}

$(document).on("change","#wallet_origin",function() {
  get_other_users()
});


function get_coins_selects() {
  $.ajax({
    url: coins,
    type: 'GET',
    dataType: 'json',
    data: {},
    success: function(data, status) {
      data.forEach(function(element) {
          $('#coins_select').append($('<option>', {
            value: element['id'],
            text: element['name']
          }));
      });
    },
    beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','JWT ' + token); } 
  });
}

function get_wallet(id) {
  $.ajax({
    url: wallets+id+'/get_wallet_of_user/',
    type: 'POST',
    dataType: 'json',
    data: {
      id:id
    },
    success: function(data, status) {
      $('#card_name').show()
      name = data[0]['user']['username']
      $('#name').append(name)
      data.forEach(function(e) {
        $('#wallets').append('<div class="card bg-light">'+e['coin']['name']+': '+e['cant']+'</div>')
        $('#wallet_origin').append($('<option>', {
            value: e['id'],
            text: e['coin']['name']+'->'+e['cant']
          }));
        $('#balance_select').append($('<option>', {
            value: e['coin']['id'],
            text: e['coin']['name']
          }));
      });

    },
    beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','JWT ' + token); } 
  });
  get_coins_selects()
}

function get_data(user) {
  $.ajax({
    url: users,
    type: 'GET',
    dataType: 'json',
    data: {},
    success: function(data, status) {
      data.forEach(function(element) {
        if (element['username']==user) {
          userid = element['id']
          get_wallet(userid)
        }else{
          $('#users_select').append($('<option>', {
              value: element['id'],
              text: element['username']
          }));
        }
      });
    },
    beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','JWT ' + token); } 
  });
}

$(document).on("click",".login-button", function(){
  var user = $('#inputUsername').val()
  var pass = $('#inputPassword').val()
  if (user) {
    if (pass) {
      $.ajax({
        url: authorization,
        type: 'POST',
        data: {
          username: user,
          password: pass
         },
        dataType: 'json', 
          success: function(result){
            token = result['token']
            $('#login').hide()
            get_data(user)
            $('#wallet').show()
        },
        error: function(error) {
              alertify.error('Los datos son incorrectos!')
             //callbackErr(error,self)
         }
      });
    }else{
      alertify.error('Debe ingresar su password')
    }
  }else{
    alertify.error('Debe ingresar su usuario')
  }
});

$(document).on("click","#send",function(){
    $("#form_send").toggle();
});

$(document).on("click","#create",function(){
    $("#coin_create").toggle();
});

$(document).on("click","#balance",function(){
    $("#card_balance").toggle();
});


//operation functions

function create() {
  var user = $('#name').text()
  var coin_name = $( "#coins_select option:selected" ).val()
  var amount = $('#new_coin').val()
  if (coin_name) {
    if (amount) {
      $.ajax({
        url: wallets,
        type: 'POST',
        dataType: 'json',
        data: {
          user: user,
          cant: amount,
          coin: coin_name
        },
        success: function(data, status) {
          alertify.success('Se creo correctamente')
          $('#wallets').append('<div class="card bg-light">'+data['coin']['name']+': '+data['cant']+'</div>')


        },
        beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','JWT ' + token); } 
      });
    }else{
      alertify.error('Debe ingresar un monto')
    }
  }else{
    alertify.error('Debe seleccionar una moneda')
  }
}

function send() {
  var wallet_origin = $("#wallet_origin option:selected").val()
  var wallet_to = $("#wallet_to option:selected").val()
  var amount = $("#amount").val()
  if (wallet_origin) {
    if (wallet_to) {
      if (amount) {
        $.ajax({
          url: operations,
          type: 'POST',
          dataType: 'json',
          data: {
            wallet_from: wallet_origin,
            wallet_to: wallet_to,
            amount:amount
          },
          success: function(data, status) {
            alertify.success('El envió se realizo correctamente')
          },
          beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','JWT ' + token); } 
        });
      }else{
        alertify.error('Debe ingresar un monto')
      }
    }else{
      alertify.error('Debe seleccionar el destino')
    }
  }else{
    alertify.error('Debe seleccionar el origen')
  }
}

function balance(){
  var coin = $("#balance_select option:selected").text()
  if (coin!='--Seleccione un moneda--') {
    $.ajax({
      url: wallets+'calculator/',
      type: 'GET',
      dataType: 'json',
      data: {
        user: name,
        coin: coin
      },
      success: function(data, status) {
        alertify.alert('Usted cuenta con:', data['balance']+' '+coin);
        $('#wallets').empty()
        get_wallet(userid)
      },
      beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','JWT ' + token); } 
    });
  }else{
    alertify.error('Debe seleccionar una moneda')
  }  
}