var btn = $('#update')
btn.on('click', function () {
    if(($('#Cid').val() != '') && ($('#Ssnid').val() == '')){
        axios.post('/api/customer', { 'cid': $('#Cid').val() }).then(function (response){
            $('#fieldset').prop('disabled', false);
            $('#ssnid').val(response.data['ssnid']);
            $('#cid').val(response.data['cid']);
            $('#address').val(response.data['address']);
            $('#Age').val(response.data['age']);
            $('#Name').val(response.data['name']);
            if(response.data['Error']){
                $("#error").html(response.data['Error']);
                $('#fieldset').prop('disabled', true);
            }
            else{
                $("#error").html("");
            }
            $("#done").html("")
            $('#Cid').val("");
            $('#Ssnid').val("");
        }, function (error) {
            console.log(error)
        });
    }
    else if ($('#Ssnid').val() != ''){
        axios.post('/api/customer', { 'ssnid': $('#Ssnid').val() }).then(function (response){
            $('#fieldset').prop('disabled', false);
            $('#ssnid').val(response.data['ssnid']);
            $('#cid').val(response.data['cid']);
            $('#address').val(response.data['address']);
            $('#Age').val(response.data['age']);
            $('#Name').val(response.data['name']);
            if(response.data['Error']){
                $("#error").html(response.data['Error']);
                $('#fieldset').prop('disabled', true);
            }
            else{
                $("#error").html("");
            }
            $('#Cid').val("");
            $("#done").html("");
            $('#Ssnid').val("");
        }, function (error) {
            console.log(error)
        });
    }
});
$("#submit").click(function (){
    axios.post('/update/customer',
    {
        'cid': $('#cid').val(),
        'name': $('#Name').val(),
        'age': $("#Age").val(),
        'addr': $("#address").val(),
        'ssnid': $("#ssnid").val()
    }
).then(function (response){
    $("#done").html("Submitted successfully");
}).catch(function (error){
    $("#error").html("Could not resolve your request at this time, please try again later");
});
});
$("#delete-customer").click(function (){
    axios.post('/api/delete', {'cid': $('#cid').val()}).then(function (response){
        $("#suc1").html("Succesfully deleted the Customer");
        $('#cid').val("");
    }).catch(function (error){
    });
});
$("#delete-account").click(function (){
    axios.post('/api/delete', {'cid': $('#cid1').val(), 'aid': $("#aid").val()}).then(function (response){
        $("#suc2").html("Succesfully deleted the Account");
        $('#cid1').val("");
        $('#aid').val("");
    }).catch(function (error){
    });
});

$("#search-acc").click(function(){
    if($("#Ssnid").val() != "" && $("#Aid").val() == "")
    {
        axios.post('/api/get/accounts', {'id': $("#Ssnid").val()}).then(function (response){
            var options = response.data['data'];
            for(var val in options){
                var option = ('<option value="' + options[val] + '">' + options[val] + '</option>');
                $("#Aid1").append(option);
            }
        });
    }
    else if ($("#Aid").val() != ""){
        axios.post('/api/info/account', {'id': $("#Aid").val()}).then(function (response){
            $("#Cid").val(response.data['cid']);
            $("#aid").val(response.data['aid']);
            $("#atype").val(response.data['atype']);
            $("#bal").val(response.data['bal']);
        })
    }
});
$("#Aid1").click(function (){
    if($("#Aid1").val() != null){
        axios.post('/api/info/account', {'id': $("#Aid1").val()}).then(function (response){
            $("#Cid").val(response.data['cid']);
            $("#aid").val(response.data['aid']);
            $("#atype").val(response.data['atype']);
            $("#bal").val(response.data['bal']);
        });
    }
});

$("#self-transac").click(function () {
    if ($("#Aid").val() == "" && $("#amount").val() == ""){
        $("#e").html("Please enter valid account information")
    }
    else{
        axios.post('/api/deposit/account', {"id": $("#Aid").val(), "amt": $("#amount").val()}).then(function (response){
            if ('error' in response.data){
                $("#error").html(response.data['error']);
                $("#e").html("");
            }
            else{
                $("#e").html("");
                $("#Aid").val("");
                $("#amount").val("");
                $("#done").html("Account Retrieval and Updation Successful")
                $("#Cid").val(response.data['cid']);
                $("#aid").val(response.data['aid']);
                $("#pbal").val(response.data['pb']);
                $("#cbal").val(response.data['cb']);
            }
        });
    }
});
$("#get-bal").click(function (){
    if ($("#Aid").val() == ""){
        $("#e").html("Please enter valid account information");
        $("#acc-bal-disp").html("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;");
    }
    else{
        axios.post('/api/withdraw/account', {"id": $("#Aid").val(), "withdraw": false}).then(function (response){
            if ('error' in response.data){
                $("#error").html(response.data['error']);
                $("#e").html("");
                $("#acc-bal-disp").html("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;");
            }
            else{
                $("#e").html("");
                $("#error").html("");
                $("#acc-bal-disp").html(response.data['balance']);
            }
        });
    }
});
$("#wdraw").click(function (){
    if ($("#Aid").val() == "" || $("#amount").val() == ""){
        $("#e").html("Please enter data in all fields");
        $("#acc-bal-disp").html("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;");
        $("#done").html("");
        $("#error").html("Please enter valid amount and account information");
        $("#aid").val("");
        $("#pbal").val("");
        $("#cbal").val("");
    }
    else if (parseInt($("#amount").val()) == $("#amount").val()){
        axios.post('/api/withdraw/account', {"id": $("#Aid").val(), "withdraw": true, 'amount': $('#amount').val()}).then(function (response){
            if ('error' in response.data){
                $("#error").html(response.data['error']);
                $("#e").html("");
            }
            else{
                $("#e").html("");
                $("#error").html("");
                $("#done").html("Retrieval and Withdrawl Successful");
                $('#amount').val("");
                $("#acc-bal-disp").html(response.data['cbal']);
                $("#aid").val(response.data['aid']);
                $("#pbal").val(response.data['pb']);
                $("#cbal").val(response.data['cbal']);
            }
        });
    }
    else{
        $("#e").html("Please enter a valid amount");
        $("#acc-bal-disp").html("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;");
        $("#done").html("");
        $("#error").html("Please enter valid amount and account information");
        $("#aid").val("");
        $("#pbal").val("");
        $("#cbal").val("");
    }
});

$("#get-trans-bal").click(function (){
    if ($("#Aid").val() == ""){
        $("#acc-bal-disp").html("Please enter valid information");
    }
    else{
        axios.post('/api/withdraw/account', {"id": $("#Aid").val(), "withdraw": false}).then(function (response){
            if ('error' in response.data){
                $("#error").html(response.data['error']);
                $("#acc-bal-disp").html("");
            }
            else{
                $("#error").html("");
                $("#acc-bal-disp").html(response.data['balance']);
            }
        });
    }
});
var dacc = 0;
$("#transfer").click(function(){
    if ($("#Aid").val() == "" || $("#amt").val() == "" || $("#daid").val() == ""){
        $("#error").html("Please enter data in all fields");
        // $("#Aid").val("");
        // $("#daid").val("");
        // $("#amt").val("");
    }
    else{
        axios.post('/api/withdraw/account', {"id": $("#Aid").val(), "withdraw": false}).then(function (response){
            dacc = response.data["balance"]
        });
        axios.post('/api/transfer/account', {
            'baid': $("#Aid").val(),
            'daid': $("#daid").val(),
            'amount': $("#amt").val()
        }).then(function (response){
            if(!('error' in response.data))
            {
                $('#aid1').val($("#Aid").val());
                $('#aid2').val($("#daid").val());
                $('#pbal1').val(response.data['pb1']);
                $('#pbal2').val(response.data['pb2']);
                $('#cbal1').val(response.data['cb1']);
                $('#cbal2').val(response.data['cb2']);
                $("#Aid").val("");
                $("#daid").val("");
                $("#amt").val("");
            }
            else{
                $("#error").html(response.data['error']);
                $("#acc-bal-disp").html("");
                $("#amt").addClass("is-invalid");
                $("#amt").focus();
            }
        });
    }
});

$("#self-state").click(function (){
    if($('#Aid').val()==''|| $('#exampleFormControlSelect1').val()==""){
        $('#error').html("Invalid Account Number");
    }
    else{
        $("#statement").html("");
        axios.post('/api/statement/account', {"id": $("#Aid").val(), "transaction": $("#exampleFormControlSelect1").val(), 'bydate': false}).then(function (response){
            if ('error' in response.data){
                $("#error").html(response.data['error']);
            }
            else{
                $("#error").html("");
                var options = response.data;
                for(var val in options){
                    var option = ('<tr>' + '<td>'+options[val][0]+'</td>' + '<td>'+options[val][1]+'</td>' +
                                        '<td>'+options[val][2]+'</td>' + '<td>'+options[val][3]+'</td></tr>');
                    $("#statement").append(option);
                }
            }
        });
    }
})
$("#self-state-date").click(function (){
    if($('#to').val()==''|| $('#from').val()==""){
        $('#error').html("Please select the to and from dates");
    }
    else{
        $("#statement").html("");
        axios.post('/api/statement/account', {"id": $("#Aid").val(), "from": $("#from").val(), "to": $("#to").val(), 'bydate': true}).then(function (response){
            if ('error' in response.data){
                $("#error").html(response.data['error']);
            }
            else{
                $("#error").html("");
                var options = response.data;
                for(var val in options){
                    var option = ('<tr>' + '<td>'+options[val][0]+'</td>' + '<td>'+options[val][1]+'</td>' +
                                        '<td>'+options[val][2]+'</td>' + '<td>'+options[val][3]+'</td></tr>');
                    $("#statement").append(option);
                }
            }
        });
    }
})
