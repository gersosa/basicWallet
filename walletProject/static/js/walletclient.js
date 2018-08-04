var localhost = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
var authorization = localhost+'/api/api-token-auth/'
var users = localhost+'/api/users/'
var wallets = localhost+'/api/wallets/'
var coins = localhost+'/api/coins/'
var operations = localhost+'/api/operations/'
var token = ''
var userid = ''

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
      console.log(data)
      $('#card_name').show()
      $('#name').append(data[0]['user']['username'])
      data.forEach(function(e) {
        $('#wallets').append('<div class="card bg-light">'+e['coin']['name']+': '+e['cant']+'</div>')
        $('#balance_select').append($('<option>', {
            value: e['id'],
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
           console.log('error')
           //callbackErr(error,self)
       }

    });
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
  var coin_name = $( "#coins_select option:selected" ).text()
  var amount = $('#new_coin').val()
  console.log(user, coin_name, amount)
  $.ajax({
    url: wallets,
    type: 'POST',
    dataType: 'json',
    data: {
      id:id
    },
    success: function(data, status) {
      console.log(data)
      $('#card_name').show()
      $('#name').append(data[0]['user']['username'])
      data.forEach(function(e) {
        $('#wallets').append('<div class="card bg-light">'+e['coin']['name']+': '+e['cant']+'</div>')
        $('#balance_select').append($('<option>', {
            value: e['id'],
            text: e['coin']['name']
          }));
      });

    },
    beforeSend: function(xhr, settings) { xhr.setRequestHeader('Authorization','JWT ' + token); } 
  });
}