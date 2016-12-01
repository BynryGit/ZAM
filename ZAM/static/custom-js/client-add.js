/**
 * Created by hduser on 12/17/15.
 */


 $(function () {
      $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            $('a[data-toggle="tab"]').removeClass('btn-primary');
            $('a[data-toggle="tab"]').addClass('btn-default');
            $(this).removeClass('btn-default');
            $(this).addClass('btn-primary');
        })

        $('.next').click(function () {
            var nextId = $(this).parents('.tab-pane').next().attr("id");
            $('[href=#' + nextId + ']').tab('show');
        })

        $('.prev').click(function () {
            var prevId = $(this).parents('.tab-pane').prev().attr("id");
            $('[href=#' + prevId + ']').tab('show');
        })

        $(".js-source-states").select2();
        $(".js-source-states-2").select2();

        $('.submitWizard').click(function () {

            var approve = $(".approveCheck").is(':checked');
            if (approve) {
                // Got to step 1
                $('[href=#step1]').tab('show');

                // Serialize data to post method
                var datastring = $("#simpleForm").serialize();

                // Show notification
                swal({
                    title: "Thank you!",
                    text: "You approved our example form!",
                    type: "success"
                });
            } else {
                // Show notification
                swal({
                    title: "Error!",
                    text: "You have to approve form checkbox.",
                    type: "error"
                });
            }
        })
 })


 function client_validation(){
            var contact = $('#txt_firm_contact_no').val();
            var n = contact.length;
            var email = $('#txt_firm_email_add').val();
            var pin_number = $('#txt_pin_code').val();


            var state_name = $('#select_state').val();
            var city_name = $('#select_city').val();
            var reg = /[-!$%^&*#()_+|~=`{}\[\]:";'<>?,.\/]/;

            var check_contact_no=false;
            var check_email=false;


            if ($('#txt_firm_name').val() === "") {
                $('#lbl_name').css("color", "red");
            } else {
                $('#lbl_name').css("color", "#6A6C6F");
            }


            if ($('#select_firm_type option:selected').val() === "") {
                $('#lbl_type').css("color", "red");
            } else {
                $('#lbl_type').css("color", "#6A6C6F");
            }
            
            if ($('#txt_firm_contact_no').val() != "" && $('#txt_firm_contact_no').val()!=null && $('#txt_firm_contact_no').val()) {
               if($('#txt_firm_contact_no').val().length<10) { 
               $('#lbl_contact_no').html('&nbsp Minimum length should be 10');
               $('#lbl_contact_no').css("color", "red");
               return false;
            }else{
     						return true;       	
            	}
            }

            if ($('#txt_firm_email_add').val() === "") {
                 $('#lbl_email').css("color", "red");
                $('#lbl_emailc').css("color", "white");
                
                check_email=false;
            }  else {
                var atpos = email.indexOf("@");
                var dotpos = email.lastIndexOf(".");
                var len = email.length
                if (atpos < 1 || ( dotpos - atpos < 2 ) || ( len - dotpos < 3 )) {
                     $('#lbl_email').css("color", "#6A6C6F");
                    $('#lbl_emailc').html('&nbsp Please enter valid Email Id');
                    $('#lbl_emailc').css("color", "red");
                    check_email=false;
                }else{
                    $('#lbl_emailc').css("color", "white");
                    $('#lbl_email').css("color", "#6A6C6F");
                    check_email=true;
                }
            }

            if ($('#txt_address_line1').val() === "") {
                $('#lbl_add').css("color", "red");
            } else {
                $('#lbl_add').css("color", "#6A6C6F");
            }

            if ($('#client_country option:selected').val() === "") {
                $('#lbl_country').css("color", "red");
            } else {
                $('#lbl_country').css("color", "#6A6C6F");
            }

            if ($('#client_priority').val() === ""|| $('#client_priority').val() === null) {
                $('#lbl_pri').css("color", "red");
            } else {
                $('#lbl_pri').css("color", "#6A6C6F");
            }

            if ($('#txt_firm_name').val() === "" || $('#select_firm_type').val() === "" ||
                     $('#txt_firm_email_add').val() === "" || $('#txt_firm_email_add').val() === null ||
                    $('#txt_address_line1').val() === "" || $('#client_country').val() === "" ||
                   $('#client_priority').val() === ""|| $('#client_priority').val() === null||check_email==false
            ) {
                return false;
            }
            
            

            if (($.isNumeric(state_name) && state_name != "" && state_name != null) || (reg.test(state_name))) {
                alert("Please enter valid State Name");
                return false;
            }

            if ($.isNumeric(city_name) && city_name != "" && city_name != null || (reg.test(city_name))) {
                alert("Please enter valid City Name");
                return false;
            }
            if ($('#txt_pin_code').val().length != 6 && $('#txt_pin_code').val() != "" && $('#txt_pin_code').val() != null) {
                alert("Please enter valid Pincode");
                return false;
            }
     return true;
        }