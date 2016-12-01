/**
 * Created by hduser on 2/26/16.
 */

        /*-------------BANK ACCOUNT------------*/ 
        
        			$('.cancel_div').click(function () {
        				$("#add_bank").hide();
                $("#other_saving_product").hide();
           $("#direct_equity").hide();
            $("#gold").hide();
             $("#property").hide();
              $("#provident_fund").hide();
               $("#equity_funds").hide();
        			});
		
               $("#ab").click(function () {
               $("#add_bank").show();
                $("#other_saving_product").hide();
           $("#direct_equity").hide();
            $("#gold").hide();
             $("#property").hide();
              $("#provident_fund").hide();
               $("#equity_funds").hide();
               
               $('#lbl_bn').css("color", "#6A6C6F");
               $('#lbl_at').css("color", "#6A6C6F");
               $('#lbl_bb').css("color", "#6A6C6F");
                $('#lbl_bd').css("color", "#6A6C6F");
                $('#lbl_bpr').css("color", "#6A6C6F");
                $('#lbl_bpo').css("color", "#6A6C6F");
                $('#lbl_bl').css("color", "#6A6C6F");
               });
               
               $("#cd").click(function () {
               $("#add_bank").hide();
                $("#other_saving_product").show();
           $("#direct_equity").hide();
            $("#gold").hide();
             $("#property").hide();
              $("#provident_fund").hide();
               $("#equity_funds").hide();
               
               	$('#lbl_os').css("color", "#6A6C6F");
						 $('#lbl_ob').css("color", "#6A6C6F");
						$('#lbl_od').css("color", "#6A6C6F");
						$('#lbl_opr').css("color", "#6A6C6F");
						$('#lbl_opo').css("color", "#6A6C6F");
						 $('#lbl_ol').css("color", "#6A6C6F");
               });   
               
               
               $("#ef").click(function () {
               $("#add_bank").hide();
                $("#other_saving_product").hide();
           $("#direct_equity").show();
            $("#gold").hide();
             $("#property").hide();
              $("#provident_fund").hide();
               $("#equity_funds").hide();
               
               $('#lbl_dn').css("color", "#6A6C6F");
					$('#lbl_db').css("color", "#6A6C6F");
					$('#lbl_dd').css("color", "#6A6C6F");
					$('#lbl_dpr').css("color", "#6A6C6F");
					$('#lbl_dpo').css("color", "#6A6C6F");
					$('#lbl_dl').css("color", "#6A6C6F");
               
               });
               
               $("#gh").click(function () {
               $("#add_bank").hide();
                $("#other_saving_product").hide();
           $("#direct_equity").hide();
            $("#gold").hide();
             $("#property").hide();
              $("#provident_fund").hide();
               $("#equity_funds").show();
               
                $('#lbl_ef').css("color", "#6A6C6F");
						$('#lbl_eb').css("color", "#6A6C6F");
						$('#lbl_ed').css("color", "#6A6C6F");
						$('#lbl_ep').css("color", "#6A6C6F");
						$('#lbl_epo').css("color", "#6A6C6F");
						 $('#lbl_el').css("color", "#6A6C6F");
               
               });
               
                $("#ij").click(function () {
               $("#add_bank").hide();
                $("#other_saving_product").hide();
           $("#direct_equity").hide();
            $("#gold").hide();
             $("#property").hide();
              $("#provident_fund").show();
               $("#equity_funds").hide();
               
               $('#lbl_pn').css("color", "#6A6C6F");
					$('#lbl_prob').css("color", "#6A6C6F");
					 $('#lbl_prod').css("color", "#6A6C6F");
					$('#lbl_pr_pre').css("color", "#6A6C6F");
					$('#lbl_pr_po').css("color", "#6A6C6F");
					$('#lbl_pr_liq').css("color", "#6A6C6F");
               
               });
               
                 $("#kl").click(function () {
               	$("#add_bank").hide();
                $("#other_saving_product").hide();
          		 $("#direct_equity").hide();
            	$("#gold").hide();
             	$("#property").show();
              	$("#provident_fund").hide();
               $("#equity_funds").hide();
               
               $('#lbl_prop').css("color", "#6A6C6F");
					 $('#lbl_prop_bal').css("color", "#6A6C6F");
					$('#lbl_pro_dur').css("color", "#6A6C6F");
					$('#lbl_pro_t').css("color", "#6A6C6F");
					$('#lbl_pro_p').css("color", "#6A6C6F");
					$('#lbl_pro_l').css("color", "#6A6C6F");

               
               
               
               });
               
                $("#mn").click(function () {
                $("#add_bank").hide();
                $("#other_saving_product").hide();
           		 $("#direct_equity").hide();
                $("#gold").show();
                $("#property").hide();
               $("#provident_fund").hide();
               $("#equity_funds").hide();
               
               $('#lbl_gol').css("color", "#6A6C6F");
					$('#lbl_gol_b').css("color", "#6A6C6F");
					 $('#lbl_gol_d').css("color", "#6A6C6F");
					$('#lbl_gol_pre').css("color", "#6A6C6F");
					$('#lbl_gol_po').css("color", "#6A6C6F");
					$('#lbl_gol_liq').css("color", "#6A6C6F");
               
               });                
                      
               
   $("#bank_account").click(function () {
   	

    if ($('#bank_name').val() == "" || $('#bank_name').val() == null) {
        $('#lbl_bn').css("color", "red");
    } else {
        $('#lbl_bn').css("color", "#6A6C6F");
    }

    if ($('#account_type option:selected').val() == "" || $('#account_type option:selected').val() == null) {
        $('#lbl_at').css("color", "red");
    } else {
        $('#lbl_at').css("color", "#6A6C6F");
    }
    
    if ($('#bank_balance').val() == "" || $('#bank_balance').val() == null) {
        $('#lbl_bb').css("color", "red");
    } else {
        $('#lbl_bb').css("color", "#6A6C6F");
    }

    if ($('#bank_dur').val() == "" || $('#bank_dur').val() == null) {
        $('#lbl_bd').css("color", "red");
    } else {
        $('#lbl_bd').css("color", "#6A6C6F");
    }
    
    if ($('#bank_pre').val() == "" || $('#bank_pre').val() == null) {
        $('#lbl_bpr').css("color", "red");
    } else {
        $('#lbl_bpr').css("color", "#6A6C6F");
    }
    
     if($('#bank_pre').val()>100){
     $('#lbl_BPRE').html('&nbsp % Less than 100');
     $('#lbl_BPRE').css("color", "red");
     return false;
	}else{
		$("#lbl_BPRE").html("");
      $('#lbl_BPRE').css("color", "#6A6C6F");
		
		}
    
    if ($('#bank_pos').val() == "" || $('#bank_pos').val() == null) {
        $('#lbl_bpo').css("color", "red");
    } else {
        $('#lbl_bpo').css("color", "#6A6C6F");
    }
    
     if($('#bank_pos').val()>100){
     $('#lbl_BPOS').html('&nbsp % Less than 100');
     $('#lbl_BPOS').css("color", "red");
     return false;
	}else{
		$("#lbl_BPOS").html("");
      $('#lbl_BPOS').css("color", "#6A6C6F");		
		}
    
    if ($('#bank_liq').val() == "" || $('#bank_liq').val() == null) {
        $('#lbl_bl').css("color", "red");
    } else {
        $('#lbl_bl').css("color", "#6A6C6F");
    }


    if ($('#bank_name').val() == "" || $('#account_type option:selected').val() == "" || $('#account_type option:selected').val() == null ||
        $('#bank_balance').val() == "" ||  $('#bank_dur').val() == "" || $('#bank_pre').val() == "" ||  $('#bank_pos').val() == "" ||$('#bank_liq').val() == "" 
        ) {
        return false;
    }
    
   
	
    $.ajax({
        type: 'POST',
        url: '/save-full-asset-tool/',
        data: $('#bank_account_form').serialize(),
        success: function (response) {
            console.log(response);
            if (response.success == "true") {
            	toastr.success('Bank Account is added sucessfully.');
                load_asset_data();
                  $('#bank_name').val("");
                $('#bank_balance').val("");
                $('#bank_dur').val("");
                $('#bank_pre').val("");
                $('#bank_pos').val("");
                $('#bank_liq').val("");
            }

        },
        error: function (response) {
            console.log(response);
        },
        beforeSend: function () {
            $("#load").show();
        },
        error: function (response) {
            console.log(response);
            alert('error');
            $("#load").hide();
        },
        complete: function () {
            $("#load").hide();
        }
    })
});
                /*-------------------END-----------------*/
                
                
                /*-------------OTHER SAVING PRODUCT------------*/               
               
   $("#other_saving").click(function () {

    if ($('#othr_sav').val() == "" || $('#othr_sav').val() == null) {
        $('#lbl_os').css("color", "red");
    } else {
        $('#lbl_os').css("color", "#6A6C6F");
    }
    
    if ($('#othr_bal').val() == "" || $('#othr_bal').val() == null) {
        $('#lbl_ob').css("color", "red");
    } else {
        $('#lbl_ob').css("color", "#6A6C6F");
    }

    if ($('#othr_dur').val() == "" || $('#othr_dur').val() == null) {
        $('#lbl_od').css("color", "red");
    } else {
        $('#lbl_od').css("color", "#6A6C6F");
    }
    
    if ($('#othr_pre').val() == "" || $('#othr_pre').val() == null) {
        $('#lbl_opr').css("color", "red");
    } else {
        $('#lbl_opr').css("color", "#6A6C6F");
    }
    
     if($('#othr_pre').val()>100){
     $('#lbl_OPPRE').html('&nbsp % Less than 100');
     $('#lbl_OPPRE').css("color", "red");
     return false;
	}else{
		$("#lbl_OPPRE").html("");
      $('#lbl_OPPRE').css("color", "#6A6C6F");	
		}
    
    if ($('#othr_po').val() == "" || $('#othr_po').val() == null) {
        $('#lbl_opo').css("color", "red");
    } else {
        $('#lbl_opo').css("color", "#6A6C6F");
    }
    
     if($('#othr_po').val()>100){
     $('#lbl_OPPOS').html('&nbsp % Less than 100');
     $('#lbl_OPPOS').css("color", "red");
     return false;
	}else{
		$("#lbl_OPPOS").html("");
      $('#lbl_OPPOS').css("color", "#6A6C6F");	
		}
    
    if ($('#othr_li').val() == "" || $('#othr_li').val() == null) {
        $('#lbl_ol').css("color", "red");
    } else {
        $('#lbl_ol').css("color", "#6A6C6F");
    }

    if ($('#othr_sav').val() == "" || $('#othr_bal').val() == "" ||  $('#othr_dur').val() == "" ||
         $('#othr_pre').val() == "" ||  $('#othr_po').val() == "" ||$('#othr_li').val() == "" 
        ) {
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/save-full-asset-tool/',
        data: $('#other_saving_product_form').serialize(),
        success: function (response) {
            console.log(response);
            if (response.success == "true") {
            	toastr.success('Other Saving Product is added sucessfully.');
                load_asset_data();
                $('#othr_sav').val("");
                $('#othr_bal').val("");
                $('#othr_dur').val("");
                $('#othr_pre').val("");
                $('#othr_po').val("");
                $('#othr_li').val("");
            }

        },
        error: function (response) {
            console.log(response);
        },
        beforeSend: function () {
            $("#load").show();
        },
        error: function (response) {
            console.log(response);
            alert('error');
            $("#load").hide();
        },
        complete: function () {
            $("#load").hide();
        }
    })
});
                /*-------------------END-----------------*/
                
                  /*-------------DIRECT EQUITY------------*/               
               
   $("#direct_equity_product").click(function () {

    if ($('#dir_eq').val() == "" || $('#dir_eq').val() == null) {
        $('#lbl_dn').css("color", "red");
    } else {
        $('#lbl_dn').css("color", "#6A6C6F");
    }
    
    if ($('#dir_bal').val() == "" || $('#dir_bal').val() == null) {
        $('#lbl_db').css("color", "red");
    } else {
        $('#lbl_db').css("color", "#6A6C6F");
    }

    if ($('#dir_dur').val() == "" || $('#dir_dur').val() == null) {
        $('#lbl_dd').css("color", "red");
    } else {
        $('#lbl_dd').css("color", "#6A6C6F");
    }
    
    if ($('#dir_pre').val() == "" || $('#dir_pre').val() == null) {
        $('#lbl_dpr').css("color", "red");
    } else {
        $('#lbl_dpr').css("color", "#6A6C6F");
    }
    
     if($('#dir_pre').val()>100){
     $('#lbl_DEPRE').html('&nbsp % Less than 100');
     $('#lbl_DEPRE').css("color", "red");
     return false;
	}else{
		$("#lbl_DEPRE").html("");
      $('#lbl_DEPRE').css("color", "#6A6C6F");	
		}
    
    if ($('#dir_pro').val() == "" || $('#dir_pro').val() == null) {
        $('#lbl_dpo').css("color", "red");
    } else {
        $('#lbl_dpo').css("color", "#6A6C6F");
    }
    
    if($('#dir_pro').val()>100){
     $('#lbl_DEPOS').html('&nbsp % Less than 100');
     $('#lbl_DEPOS').css("color", "red");
     return false;
	}else{
		$("#lbl_DEPOS").html("");
      $('#lbl_DEPOS').css("color", "#6A6C6F");	
		}
    
    if ($('#dir_liq').val() == "" || $('#dir_liq').val() == null) {
        $('#lbl_dl').css("color", "red");
    } else {
        $('#lbl_dl').css("color", "#6A6C6F");
    }

    if ($('#dir_eq').val() == "" || $('#dir_bal').val() == "" ||  $('#dir_dur').val() == "" ||
         $('#dir_pre').val() == "" ||  $('#dir_pro').val() == "" ||$('#dir_liq').val() == "" 
        ) {
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/save-full-asset-tool/',
        data: $('#direct_equity_form').serialize(),
        success: function (response) {
            console.log(response);
            if (response.success == "true") {
            	toastr.success('Direct Equity is added sucessfully.');
                load_asset_data();
                 $('#dir_eq').val("");
                $('#dir_bal').val("");
                $('#dir_dur').val("");
                $('#dir_pre').val("");
                $('#dir_pro').val("");
                $('#dir_liq').val("");
            }

        },
        error: function (response) {
            console.log(response);
        },
        beforeSend: function () {
            $("#load").show();
        },
        error: function (response) {
            console.log(response);
            alert('error');
            $("#load").hide();
        },
        complete: function () {
            $("#load").hide();
        }
    })
});
                /*-------------------END-----------------*/
                
                
                 /*------------- EQUITY  FUNDS------------*/               
               
   $("#equity_fund").click(function () {

    if ($('#eq_fu').val() == "" || $('#eq_fu').val() == null) {
        $('#lbl_ef').css("color", "red");
    } else {
        $('#lbl_ef').css("color", "#6A6C6F");
    }
    
    if ($('#eq_ba').val() == "" || $('#eq_ba').val() == null) {
        $('#lbl_eb').css("color", "red");
    } else {
        $('#lbl_eb').css("color", "#6A6C6F");
    }

    if ($('#eq_dur').val() == "" || $('#eq_dur').val() == null) {
        $('#lbl_ed').css("color", "red");
    } else {
        $('#lbl_ed').css("color", "#6A6C6F");
    }
    
    if ($('#eq_pre').val() == "" || $('#eq_pre').val() == null) {
        $('#lbl_ep').css("color", "red");
    } else {
        $('#lbl_ep').css("color", "#6A6C6F");
    }
    
    if($('#eq_pre').val()>100){
     $('#lbl_EFPRE').html('&nbsp % Less than 100');
     $('#lbl_EFPRE').css("color", "red");
     return false;
		}else{
		$("#lbl_EFPRE").html("");
      $('#lbl_EFPRE').css("color", "#6A6C6F");	
		}
    
    if ($('#eq_po').val() == "" || $('#eq_po').val() == null) {
        $('#lbl_epo').css("color", "red");
    } else {
        $('#lbl_epo').css("color", "#6A6C6F");
    }
    
     if($('#eq_po').val()>100){
     $('#lbl_EFPOS').html('&nbsp % Less than 100');
     $('#lbl_EFPOS').css("color", "red");
     return false;
	}else{
		$("#lbl_EFPOS").html("");
      $('#lbl_EFPOS').css("color", "#6A6C6F");	
		}
    
    if ($('#eq_liq').val() == "" || $('#eq_liq').val() == null) {
        $('#lbl_el').css("color", "red");
    } else {
        $('#lbl_el').css("color", "#6A6C6F");
    }

    if ($('#eq_fu').val() == "" || $('#eq_ba').val() == "" ||  $('#eq_dur').val() == "" ||
         $('#eq_pre').val() == "" ||  $('#eq_po').val() == "" ||$('#eq_liq').val() == "" 
        ) {
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/save-full-asset-tool/',
        data: $('#equity_fund_form').serialize(),
        success: function (response) {
            console.log(response);
            if (response.success == "true") {
            	toastr.success('Equity Fund is added sucessfully.');
                load_asset_data();
                $('#eq_fu').val("");
                $('#eq_ba').val("");
                $('#eq_dur').val("");
                $('#eq_pre').val("");
                $('#eq_po').val("");
                $('#eq_liq').val("");
            }

        },
        error: function (response) {
            console.log(response);
        },
        beforeSend: function () {
            $("#load").show();
        },
        error: function (response) {
            console.log(response);
            alert('error');
            $("#load").hide();
        },
        complete: function () {
            $("#load").hide();
        }
    })
});
                /*-------------------END-----------------*/
                
                                 /*------------- PROVIDENT  FUNDS------------*/               
               
   $("#provident_fund_product").click(function () {

    if ($('#pro_fu').val() == "" || $('#pro_fu').val() == null) {
        $('#lbl_pn').css("color", "red");
    } else {
        $('#lbl_pn').css("color", "#6A6C6F");
    }
    
    if ($('#pro_bal').val() == "" || $('#pro_bal').val() == null) {
        $('#lbl_prob').css("color", "red");
    } else {
        $('#lbl_prob').css("color", "#6A6C6F");
    }

    if ($('#pro_dur').val() == "" || $('#pro_dur').val() == null) {
        $('#lbl_prod').css("color", "red");
    } else {
        $('#lbl_prod').css("color", "#6A6C6F");
    }
    
    if ($('#pro_pr').val() == "" || $('#pro_pr').val() == null) {
        $('#lbl_pr_pre').css("color", "red");
    } else {
        $('#lbl_pr_pre').css("color", "#6A6C6F");
    }
    
     if($('#pro_pr').val()>100){
     $('#lbl_PFPRE').html('&nbsp % Less than 100');
     $('#lbl_PFPRE').css("color", "red");
     return false;
		}else{
		$("#lbl_PFPRE").html("");
      $('#lbl_PFPRE').css("color", "#6A6C6F");	
		}
    
    if ($('#pro_po').val() == "" || $('#pro_po').val() == null) {
        $('#lbl_pr_po').css("color", "red");
    } else {
        $('#lbl_pr_po').css("color", "#6A6C6F");
    }
    
    if($('#pro_po').val()>100){
     $('#lbl_PFPOS').html('&nbsp % Less than 100');
     $('#lbl_PFPOS').css("color", "red");
     return false;
		}else{
		$("#lbl_PFPOS").html("");
      $('#lbl_PFPOS').css("color", "#6A6C6F");	
		}
    
    if ($('#pro_li').val() == "" || $('#pro_li').val() == null) {
        $('#lbl_pr_liq').css("color", "red");
    } else {
        $('#lbl_pr_liq').css("color", "#6A6C6F");
    }

    if ($('#pro_fu').val() == "" || $('#pro_bal').val() == "" ||  $('#pro_dur').val() == "" ||
         $('#pro_pr').val() == "" ||  $('#pro_po').val() == "" ||$('#pro_li').val() == "" 
        ) {
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/save-full-asset-tool/',
        data: $('#provident_fund_form').serialize(),
        success: function (response) {
            console.log(response);
            if (response.success == "true") {
            	toastr.success('Provident Fund is added sucessfully.');
                load_asset_data();
                $('#pro_fu').val("");
                $('#pro_bal').val("");
                $('#pro_dur').val("");
                $('#pro_pr').val("");
                $('#pro_po').val("");
                $('#pro_li').val("");
            }

        },
        error: function (response) {
            console.log(response);
        },
        beforeSend: function () {
            $("#load").show();
        },
        error: function (response) {
            console.log(response);
            alert('error');
            $("#load").hide();
        },
        complete: function () {
            $("#load").hide();
        }
    })
});
                /*-------------------END-----------------*/
                
                                                /*------------- PROPERTY------------*/               
               
   $("#property_product").click(function () {

    if ($('#property_name').val() == "" || $('#property_name').val() == null) {
        $('#lbl_prop').css("color", "red");
    } else {
        $('#lbl_prop').css("color", "#6A6C6F");
    }
    
    if ($('#property_bal').val() == "" || $('#property_bal').val() == null) {
        $('#lbl_prop_bal').css("color", "red");
    } else {
        $('#lbl_prop_bal').css("color", "#6A6C6F");
    }

    if ($('#property_dur').val() == "" || $('#property_dur').val() == null) {
        $('#lbl_pro_dur').css("color", "red");
    } else {
        $('#lbl_pro_dur').css("color", "#6A6C6F");
    }
    
    if ($('#pro_tax').val() == "" || $('#pro_tax').val() == null) {
        $('#lbl_pro_t').css("color", "red");
    } else {
        $('#lbl_pro_t').css("color", "#6A6C6F");
    }
    
      if($('#pro_tax').val()>100){
     $('#lbl_PPRE').html('&nbsp % Less than 100');
     $('#lbl_PPRE').css("color", "red");
     return false;
		}else{
		$("#lbl_PPRE").html("");
      $('#lbl_PPRE').css("color", "#6A6C6F");	
		}
    
    if ($('#pro_pos').val() == "" || $('#pro_pos').val() == null) {
        $('#lbl_pro_p').css("color", "red");
    } else {
        $('#lbl_pro_p').css("color", "#6A6C6F");
    }
    
     if($('#pro_pos').val()>100){
     $('#lbl_PPOS').html('&nbsp % Less than 100');
     $('#lbl_PPOS').css("color", "red");
     return false;
		}else{
		$("#lbl_PPOS").html("");
      $('#lbl_PPOS').css("color", "#6A6C6F");	
		}
    
    if ($('#pro_liq').val() == "" || $('#pro_liq').val() == null) {
        $('#lbl_pro_l').css("color", "red");
    } else {
        $('#lbl_pro_l').css("color", "#6A6C6F");
    }

    if ($('#property_name').val() == "" || $('#property_bal').val() == "" ||  $('#property_dur').val() == "" ||
         $('#pro_tax').val() == "" ||  $('#pro_pos').val() == "" ||$('#pro_liq').val() == "" 
        ) {
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/save-full-asset-tool/',
        data: $('#property_form').serialize(),
        success: function (response) {
            console.log(response);
            if (response.success == "true") {
            	toastr.success('Property is added sucessfully.');
                load_asset_data();
                $('#property_name').val("");
                $('#property_bal').val("");
                $('#property_dur').val("");
                $('#pro_tax').val("");
                $('#pro_pos').val("");
                $('#pro_liq').val("");
            }

        },
        error: function (response) {
            console.log(response);
        },
        beforeSend: function () {
            $("#load").show();
        },
        error: function (response) {
            console.log(response);
            alert('error');
            $("#load").hide();
        },
        complete: function () {
            $("#load").hide();
        }
    })
});
                /*-------------------END-----------------*/
                
                 /*------------- GOLD------------*/               
               
   $("#gold_product").click(function () {
   	

    if ($('#gol_na').val() == "" || $('#gol_na').val() == null) {
        $('#lbl_gol').css("color", "red");
    } else {
        $('#lbl_gol').css("color", "#6A6C6F");
    }
    
    if ($('#gol_ba').val() == "" || $('#gol_ba').val() == null) {
        $('#lbl_gol_b').css("color", "red");
    } else {
        $('#lbl_gol_b').css("color", "#6A6C6F");
    }

    if ($('#gol_dur').val() == "" || $('#gol_dur').val() == null) {
        $('#lbl_gol_d').css("color", "red");
    } else {
        $('#lbl_gol_d').css("color", "#6A6C6F");
    }
    
    if ($('#gol_pre').val() == "" || $('#gol_pre').val() == null) {
        $('#lbl_gol_pre').css("color", "red");
    } else {
        $('#lbl_gol_pre').css("color", "#6A6C6F");
    }
    
     if($('#gol_pre').val()>100){
     $('#lbl_GPRE').html('&nbsp % Less than 100');
     $('#lbl_GPRE').css("color", "red");
     return false;
		}else{
		$("#lbl_GPRE").html("");
      $('#lbl_GPRE').css("color", "#6A6C6F");	
		}
    
    if ($('#gol_pos').val() == "" ) {
        $('#lbl_gol_po').css("color", "red");
    } else {
        $('#lbl_gol_po').css("color", "#6A6C6F");
    }
    
    if($('#gol_pos').val() > 100){
     $('#lbl_GPOS').html('&nbsp % Less than 100');
     $('#lbl_GPOS').css("color", "red");
     return false;
		}else{
		$("#lbl_GPOS").html("");
      $('#lbl_GPOS').css("color", "#6A6C6F");	
		}
    
    if ($('#gol_liq').val() == "" ) {
    	    
        $('#lbl_gol_liq').css("color", "red");
    } else {
        $('#lbl_gol_liq').css("color", "#6A6C6F");
    }

    if ($('#gol_na').val() == "" || $('#gol_ba').val() == "" ||  $('#gol_dur').val() == "" ||
         $('#gol_pre').val() == "" ||  $('#gol_pos').val() == "" ||$('#gol_liq').val() == "" 
        ) {
        return false;
    }
    


    $.ajax({
        type: 'POST',
        url: '/save-full-asset-tool/',
        data: $('#gold_form').serialize(),
        success: function (response) {
            console.log(response);
            if (response.success == "true") {
            	toastr.success('Gold is added sucessfully.');
                load_asset_data();
                $('#gol_na').val("");
                $('#gol_ba').val("");
                $('#gol_dur').val("");
                $('#gol_pre').val("");
                $('#gol_pos').val("");
                $('#gol_liq').val("");
            }

        },
        error: function (response) {
            console.log(response);
        },
        beforeSend: function () {
            $("#load").show();
        },
        error: function (response) {
            console.log(response);
            alert('error');
            $("#load").hide();
        },
        complete: function () {
            $("#load").hide();
        }
    })
});
                /*-------------------END-----------------*/
                
                /*-----------------------Validation-----------------*/
                
     function validateFloatKeyPress(el, evt) {
        var charCode = (evt.which) ? evt.which : event.keyCode;
        var number = el.value.split('.');
        if (charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) {
            return false;
        }

        if (number.length > 1 && charCode == 46) {
            return false;
        }

        var caratPos = getSelectionStart(el);
        var dotPos = el.value.indexOf(".");
        if (caratPos > dotPos && dotPos > -1 && (number[1].length > 1)) {
            if (charCode == 8)
                return true;
            else
                return false;
        }
        return true;
    }

    //thanks: http://javascript.nwbox.com/cursor_position/
    function getSelectionStart(o) {
        if (o.createTextRange) {
            var r = document.selection.createRange().duplicate()
            r.moveEnd('character', o.value.length)
            if (r.text == '') return o.value.length
            return o.value.lastIndexOf(r.text)
        } else return o.selectionStart
    }
					/*-------------------------end--------------------*/
					
					
					/*---------------------modal call------------------*/
					
				function editbank(id){
				$("#edit_bank").modal('show');	
				$.ajax({
            type: 'POST',
            url: '/view-full-bank-asset-tool/',
            data: {'id': id},
            success: function (response) {
                if (response.success == 'true') {
                	
                	$('#id_bank').val(response.bank_id);
                    $('#mod_ba_bank').val(response.asset_name);
                    $('#mod_ba_acc').select2("val", response.account_type);
                    $('#mod_ba_bal').val(response.balance);
                    $('#mod_ba_du').val(response.duration);
                    $('#mod_ba_pre').val(response.pretax);
                    $('#mod_ba_po').val(response.posttax);
                    $('#mod_ba_li').val(response.liquidity);
                }
                else {
                    alert('ERRORS ' + response.error_message);
                }
            },
            error: function (response) {
                alert(response.error_message);
            },
        });	
				
		}
					
					/*-------------------------end-----------------------*/

					/*---------------------modal call------------------*/
					function editproduct(id){
						$("#edit_product").modal('show');	
						  $.ajax({
            		type: 'POST',
            		url: '/view-full-asset-tool/',
            		data: {'id': id},
           			success: function (response) {
                if (response.success == 'true') {
               	 $('#product_id').val(response.asset_id);	
                		$('#mod_name').val(response.asset_name);
                    $('#mod_bal').val(response.balance);
                    $('#mod_dur').val(response.duration);
                    $('#mod_tax').val(response.pretax);
                    $('#mod_pos').val(response.posttax);
                    $('#mod_liq').val(response.liquidity);
                        }
                else {
                    alert('ERRORS ' + response.error_message);
                }
            },
            error: function (response) {
                alert(response.error_message);
            },
        });
					
		}
					
					/*-------------------------end-----------------------*/
					
					/*------------------------Updation--------------*/
					
		$("#update_product").click(function () {
			
		if ($('#mod_name').val() == "" || $('#gol_na').val() == null) {
        $('#lbl_modpn').css("color", "red");
    } else {
        $('#lbl_modpn').css("color", "#6A6C6F");
    }
    
    if ($('#mod_bal').val() == "" || $('#gol_ba').val() == null) {
        $('#lbl_modpb').css("color", "red");
    } else {
        $('#lbl_modpb').css("color", "#6A6C6F");
    }

    if ($('#mod_dur').val() == "" || $('#gol_dur').val() == null) {
        $('#lbl_modpd').css("color", "red");
    } else {
        $('#lbl_modpd').css("color", "#6A6C6F");
    }
    
    if ($('#mod_tax').val() == "" || $('#gol_pre').val() == null) {
        $('#lbl_modpt').css("color", "red");
    } else {
        $('#lbl_modpt').css("color", "#6A6C6F");
    }
    
     if($('#mod_tax').val()>100){
     alert(" % Less than 100");
     return false;
		}
    
    if ($('#mod_pos').val() == "" || $('#gol_pos').val() == null) {
        $('#lbl_modpost').css("color", "red");
    } else {
        $('#lbl_modpost').css("color", "#6A6C6F");
    }
    
    if($('#mod_pos').val()>100){
     alert(" % Less than 100");
     return false;
		}
    
    if ($('#mod_liq').val() == "" || $('#gol_liq').val() == null) {
        $('#lbl_modliq').css("color", "red");
    } else {
        $('#lbl_modliq').css("color", "#6A6C6F");
    }

    if ($('#mod_name').val() == "" || $('#mod_bal').val() == "" ||  $('#mod_dur').val() == "" ||
         $('#mod_tax').val() == "" ||  $('#mod_pos').val() == "" ||$('#mod_liq').val() == "" 
        ) {
        return false;
    }

		    $.ajax({
		        type: 'POST',
		        url: '/update-full-asset-tool/',
		        data: $('#edit_product_form').serialize(),
		        success: function (response) {
		            console.log(response);
		            if (response.success == "true") {
		            	toastr.success('Updated sucessfully.');
		                load_asset_data();
		            }
		
		        },
		        error: function (response) {
		            console.log(response);
		        },
		        beforeSend: function () {
		            $("#load").show();
		        },
		        error: function (response) {
		            console.log(response);
		            alert('error');
		            $("#load").hide();
		        },
		        complete: function () {
		            $("#load").hide();
		        }
		    })
});					
					
					
$("#update_bank").click(function () {
	
	if ($('#mod_ba_bank').val() == "" || $('#mod_ba_bank').val() == null) {
        $('#lbl_ebank').css("color", "red");
    } else {
        $('#lbl_ebank').css("color", "#6A6C6F");
    }

    if ($('#mod_ba_acc option:selected').val() == "" || $('#mod_ba_acc option:selected').val() == null) {
        $('#lbl_ebanka').css("color", "red");
    } else {
        $('#lbl_ebanka').css("color", "#6A6C6F");
    }
    
    if ($('#mod_ba_bal').val() == "" || $('#mod_ba_bal').val() == null) {
        $('#lbl_ebankb').css("color", "red");
    } else {
        $('#lbl_ebankb').css("color", "#6A6C6F");
    }

    if ($('#mod_ba_du').val() == "" || $('#mod_ba_du').val() == null) {
        $('#lbl_ebankd').css("color", "red");
    } else {
        $('#lbl_ebankd').css("color", "#6A6C6F");
    }
    
    if ($('#mod_ba_pre').val() == "" || $('#mod_ba_pre').val() == null) {
        $('#lbl_ebankpr').css("color", "red");
    } else {
        $('#lbl_ebankpr').css("color", "#6A6C6F");
    }
    
     if($('#mod_ba_pre').val()>100){
     alert(" % Less than 100");
     return false;
	}
		
    
    if ($('#mod_ba_po').val() == "" || $('#mod_ba_po').val() == null) {
        $('#lbl_ebankpo').css("color", "red");
    } else {
        $('#lbl_ebankpo').css("color", "#6A6C6F");
    }
    
     if($('#mod_ba_po').val()>100){
     alert("% Less than 100");
     return false;
	}
    
    if ($('#mod_ba_li').val() == "" || $('#mod_ba_li').val() == null) {
        $('#lbl_ebankli').css("color", "red");
    } else {
        $('#lbl_ebankli').css("color", "#6A6C6F");
    }


    if ($('#mod_ba_bank').val() == "" || $('#mod_ba_acc option:selected').val() == "" || $('#mod_ba_acc option:selected').val() == null ||
        $('#mod_ba_bal').val() == "" ||  $('#mod_ba_du').val() == "" || $('#mod_ba_pre').val() == "" ||  $('#mod_ba_po').val() == "" ||$('#mod_ba_li').val() == "" 
        ) {
        return false;
    }			

    $.ajax({
        type: 'POST',
        url: '/update-full-asset-tool/',
        data: $('#edit_bank_form').serialize(),
        success: function (response) {
            console.log(response);
            if (response.success == "true") {
            	toastr.success('Updated sucessfully.');
                load_asset_data();
            }

        },
        error: function (response) {
            console.log(response);
        },
        beforeSend: function () {
            $("#load").show();
        },
        error: function (response) {
            console.log(response);
            alert('error');
            $("#load").hide();
        },
        complete: function () {
            $("#load").hide();
        }
    })
});

/*--------------------------end----------------*/
         
                
   function load_asset_data() {
    var dataTable = $('#asset_table').dataTable({
        'destroy': true,
        "ajax": "/get-full-asset-tool-list/",
        "columns": [
        		{"data":"product"},
            {"data": "asset_name"},
            {"data": "balance"},
            {"data": "duration"},
            {"data": "pretax"},
            {"data": "posttax"},
            {"data": "liquidity"},
            {"data":"edit"},
            {"data":"delete"}

        ],
          "columnDefs": [
                {"targets": 7, "orderable": false},
                {"targets": 8, "orderable": false}
            ],
        drawCallback: function () {
            var page_min = 10;
            var $api = this.api();
            var pages = $api.page.info().pages;
            var rows = $api.data().length;
            var page = $api.page.info().page;

            if (pages === 1) {
                $('#asset_table_paginate').css('display', 'none').next('.dataTables_paginate').css('display', 'none');
                $('#asset_table_next').css('display', 'none').next('.dataTables_paginate').css('display', 'none');
                $('#asset_table_previous').css('display', 'none').next('.dataTables_paginate').css('display', 'none');
            } else if (page === 0) {
                $('#asset_table_previous').css('display', 'none').next('.dataTables_paginate').css('display', 'none');
            }
        },
    });
}
             
             
     function delete_product(id) {
        console.log(id);
        swal({
                    title: "Are you sure you want to delete this record ?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "Yes",
                    cancelButtonText: "No",
                    closeOnConfirm: true,
                    closeOnCancel: true
                },
                function (isConfirm) {
                    if (isConfirm) {
                        swal("Deleted!");
                        $.ajax({
                            type: 'POST',
                            url: '/delete-product/',
                            data: {'id': id},
                            success: function (response) {
                                if (response.success == 'true') {
                                    load_asset_data();
                                }
                                else {
                                    alert('ERRORS ' + response.error_message);
                                }
                            },
                            error: function (response) {
                                alert(response.error_message);
                            },
                        });

                    }
                });
    }              
               
               /*----------------------------------END FULL ASSET TOOL------------------------------*/
               
               
                /*----------------------------------GOAL SETTING PARAMETER------------------------------*/
                
   $("#add_goal_par").click(function () {



    if ($('#goal_pr_yr').val() == "" || $('#goal_pr_yr').val() == null) {
        $('#lbl_pryr').css("color", "red");
    } else {
        
        $('#lbl_pryr').css("color", "#6A6C6F");
    }

    if ($('#parameter').val() == "" || $('#parameter').val() == null) {
        $('#lbl_para').css("color", "red");
    } else {
        $('#lbl_para').css("color", "#6A6C6F");
    }

    if ($('#goal_per').val() == "" || $('#goal_per').val() == null) {
        $('#lbl_gol_per').css("color", "red");
    } else {
        $('#lbl_gol_per').css("color", "#6A6C6F");
    }
    
      if($('#goal_per').val()>100){
     $('#lbl_gol_per_ale').html('&nbsp % Less than 100');
     $('#lbl_gol_per_ale').css("color", "red");
     return false;
		}else{
		$("#lbl_gol_per_aler").html("");
      $('#lbl_gol_per_ale').css("color", "white");	
		}


    if ($('#goal_per').val() == "" || $('#goal_per').val() == null || $('#parameter').val() == "" || $('#parameter').val() == null||$('#goal_pr_yr').val() == "" || $('#goal_pr_yr').val() == null) {
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/save-goal-parameter/',
        data: $('#goal_parameter').serialize(),
        success: function (response) {
            console.log(response);
            if (response.success == "true") {
                load_parameter_data();
                toastr.success('Parameter added sucessfully.');
                $('#goal_pr_yr').select2().select2("val", '');
                $('#goal_per').val("");
                $('#parameter').val("");
            }

        },
        error: function (response) {
            console.log(response);
        },
        beforeSend: function () {
            $("#load").show();
        },
        error: function (response) {
            console.log(response);
            alert('error');
            $("#load").hide();
        },
        complete: function () {
            $("#load").hide();
        }
    })
});

   function load_parameter_data() {
    var dataTable = $('#goal_parameter_table').dataTable({
        'destroy': true,
        "ajax": "/get-goal-setting-parameter/",
        "columns": [
        		{"data":"year"},
            {"data": "parameter"},
            {"data": "percentage"},
            {"data": "edit"},

        ],
          "columnDefs": [
                {"targets": 3, "orderable": false},
            ],
        drawCallback: function () {
            var page_min = 10;
            var $api = this.api();
            var pages = $api.page.info().pages;
            var rows = $api.data().length;
            var page = $api.page.info().page;

            if (pages === 1) {
                $('#goal_parameter_table_paginate').css('display', 'none').next('.dataTables_paginate').css('display', 'none');
                $('#goal_parameter_table_next').css('display', 'none').next('.dataTables_paginate').css('display', 'none');
                $('#goal_parameter_table_previous').css('display', 'none').next('.dataTables_paginate').css('display', 'none');
            } else if (page === 0) {
                $('#goal_parameter_table_previous').css('display', 'none').next('.dataTables_paginate').css('display', 'none');
            }
        },
    });
}

/*---------------------modal call------------------*/
					function editgoalparameter(id){
						$("#edit_goal_par").modal('show');	
						  $.ajax({
            		type: 'POST',
            		url: '/view-goal-parameter/',
            		data: {'id': id},
           			success: function (response) {
                if (response.success == 'true') {
               	 $('#goal_parameter_id').val(response.goal_setting_parameter_id);
                		$('#mod_goal_pr_yr').select2("val", response.goal_parameter_year_id);	
                    $('#mod_goal_par').val(response.goal_setting_parameter);
                    $('#mod_goal_per').val(response.goal_setting_parameter_per);

                        }
                else {
                    alert('ERRORS ' + response.error_message);
                }
            },
            error: function (response) {
                alert(response.error_message);
            },
        });
					
		}
					
					/*-------------------------end-----------------------*/
					
$("#update_goal_param_btn").click(function () {


    if ($('#mod_goal_pr_yr').val() == "" || $('#mod_goal_pr_yr').val() == null) {
        $('#lbl_par_yr').css("color", "red");
    } else {
        $('#lbl_par_yr').css("color", "6A6C6F");
    }

    if ($('#mod_goal_par').val() == "" || $('#mod_goal_par').val() == null) {
        $('#lbl_gol_par_edit').css("color", "red");
    } else {
        $('#lbl_gol_par_edit').css("color", "#6A6C6F");
    }
    
    if ($('#mod_goal_per').val() == "" || $('#mod_goal_per').val() == null) {
        $('#lbl_gol_per_edit').css("color", "red");
    } else {
        $('#lbl_gol_per_edit').css("color", "#6A6C6F");
    }
    
    if($('#mod_goal_per').val()>100){
     $('#lbl_edi_gol_per').html('&nbsp % Less than 100');
     $('#lbl_edi_gol_per').css("color", "red");
     return false;
		}else{
		$("#lbl_edi_gol_per").html("");
      $('#lbl_edi_gol_per').css("color", "#6A6C6F");	
		}


    if ($('#mod_goal_pr_yr').val() == "" || $('#mod_goal_pr_yr').val() == null || $('#mod_goal_par').val() == "" || $('#mod_goal_per').val() == "") {
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/edit-goal-parameter/',
        data: $('#edit_goal_par_frm').serialize(),
        success: function (response) {
            console.log(response);
            if (response.success == "true") {
                load_parameter_data();
                toastr.success('Updated sucessfully.');

            }

        },
        error: function (response) {
            console.log(response);
        },
        beforeSend: function () {
            $("#load").show();
        },
        error: function (response) {
            console.log(response);
            alert('error');
            $("#load").hide();
        },
        complete: function () {
            $("#load").hide();
        }
    })
});

    function isNumberKey(evt) {
        var charCode = (evt.which) ? evt.which : event.keyCode
        if (charCode > 31 && (charCode < 48 || charCode > 57 || charCode == 43 || charCode == 45 ))
            return false;
        return true;
    }
                
                 /*----------------------------------END GOAL SETTING PARAMETER------------------------------*/


$("#add_variable").click(function () {
    console.log($('#txt_percentage').val());
    console.log($('#txt_variable').val());


    if ($('#selectVariableType').val() == "" || $('#selectVariableType').val() == null) {
        console.log('==================>>');
        $('#lbl_variableType').css("color", "red");
    } else {
        console.log('===============vkmcha de===>>');
        $('#lbl_variableType').css("color", "#6A6C6F");
    }

    if ($('#txt_variable').val() == "" || $('#txt_variable').val() == null) {
        $('#lbl_variable').css("color", "red");
    } else {
        $('#lbl_variable').css("color", "#6A6C6F");
    }

    if ($('#txt_percentage').val() == "" || $('#txt_percentage').val() == null) {
        $('#lbl_percentage').css("color", "red");
    } else {
        $('#lbl_percentage').css("color", "#6A6C6F");
    }
    
     if($('#txt_percentage').val()>100){
     $('#lbl_var_per').html('&nbsp % Less than 100');
     $('#lbl_var_per').css("color", "red");
     return false;
		}else{
		$("#lbl_var_per").html("");
      $('#lbl_var_per').css("color", "#6A6C6F");	
		}

    if ($('#txt_percentage').val() == "" || $('#txt_percentage').val() == null || $('#txt_variable').val() == "" || $('#txt_variable').val() == null||$('#selectVariableType').val() == "" || $('#selectVariableType').val() == null) {
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/save-variables/',
        data: $('#variable_frm').serialize(),
        success: function (response) {
            console.log(response);
            if (response.success == "true") {
                load_data();
                $('#txt_percentage').val("");
                $('#txt_variable').val("");
            }

        },
        error: function (response) {
            console.log(response);
        },
        beforeSend: function () {
            $("#load").show();
        },
        error: function (response) {
            console.log(response);
            alert('error');
            $("#load").hide();
        },
        complete: function () {
            $("#load").hide();
        }
    })
});


$("#update_btn").click(function () {


    if ($('#txt_variable_edit').val() == "" || $('#txt_variable_edit').val() == null) {
        $('#lbl_variable_edit').css("color", "red");
    } else {
        $('#lbl_variable_edit').css("color", "6A6C6F");
    }

    if ($('#txt_percentage_edit').val() == "" || $('#txt_percentage_edit').val() == null) {
        $('#lbl_percentage_edit').css("color", "red");
    } else {
        $('#lbl_percentage_edit').css("color", "#6A6C6F");
    }


    if ($('#txt_percentage_edit').val() == "" || $('#txt_percentage_edit').val() == null || $('#txt_variable_edit').val() == "" || $('#txt_variable_edit').val() == null) {
        return false;
    }

    console.log('===============fgfdgf========================');
    $.ajax({
        type: 'POST',
        url: '/edit-variables/',
        data: $('#edit_variable_frm').serialize(),
        success: function (response) {
            console.log(response);
            if (response.success == "true") {
                load_data();
                $('#txt_percentage_edit').val("");
                $('#txt_variable').val("");
            }

        },
        error: function (response) {
            console.log(response);
        },
        beforeSend: function () {
            $("#load").show();
        },
        error: function (response) {
            console.log(response);
            alert('error');
            $("#load").hide();
        },
        complete: function () {
            $("#load").hide();
        }
    })
});


function load_data() {
    var dataTable = $('#goal_table').dataTable({
        'destroy': true,
        "ajax": "/get-variables-list/",
        "columns": [
            {"data": "sr_no"},
            {"data": "type"},
            {"data": "variable"},
            {"data": "percentage"},
            {"data": "edit"},
            {"data": "delete"},

        ],
          "columnDefs": [
                {"targets": 4, "orderable": false},
                {"targets": 5, "orderable": false}
            ],
        drawCallback: function () {
            var page_min = 10;
            var $api = this.api();
            var pages = $api.page.info().pages;
            var rows = $api.data().length;
            var page = $api.page.info().page;

            if (pages === 1) {
                $('#goal_table_paginate').css('display', 'none').next('.dataTables_paginate').css('display', 'none');
                $('#goal_table_next').css('display', 'none').next('.dataTables_paginate').css('display', 'none');
                $('#goal_table_previous').css('display', 'none').next('.dataTables_paginate').css('display', 'none');
            } else if (page === 0) {
                $('#goal_table_previous').css('display', 'none').next('.dataTables_paginate').css('display', 'none');
            }
        },
    });
}


function validateFloatKeyPress(el, evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode;
    var number = el.value.split('.');
    if (charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }

    if (number.length > 1 && charCode == 46) {
        return false;
    }

    var caratPos = getSelectionStart(el);
    var dotPos = el.value.indexOf(".");
    if (caratPos > dotPos && dotPos > -1 && (number[1].length > 1)) {
        if (charCode == 8)
            return true;
        else
            return false;
    }
    return true;
}

//thanks: http://javascript.nwbox.com/cursor_position/
function getSelectionStart(o) {
    if (o.createTextRange) {
        var r = document.selection.createRange().duplicate()
        r.moveEnd('character', o.value.length)
        if (r.text == '') return o.value.length
        return o.value.lastIndexOf(r.text)
    } else return o.selectionStart
}


function edit_varialbe(id) {
        $.ajax({
            type: 'POST',
            url: '/get-variable-data/',
            data: {'id': id},
            success: function (response) {
                if (response.success == 'true') {
                    $('#id_edit').val(response.id);
                    $('#txt_variable_edit').val(response.variable);
                    $('#txt_percentage_edit').val(response.percentage);
                     $('#edit_variable').modal('show');
                }
                else {
                    alert('ERRORS ' + response.error_message);
                }
            },
            error: function (response) {
                alert(response.error_message);
            },
        });
    }

    function delete_variable(id) {
        console.log(id);
        swal({
                    title: "Are you sure you want to delete this record ?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "Yes",
                    cancelButtonText: "No",
                    closeOnConfirm: true,
                    closeOnCancel: true
                },
                function (isConfirm) {
                    if (isConfirm) {
                        swal("Deleted!");
                        $.ajax({
                            type: 'POST',
                            url: '/delete-variable/',
                            data: {'id': id},
                            success: function (response) {
                                if (response.success == 'true') {
                                    load_data();
                                }
                                else {
                                    alert('ERRORS ' + response.error_message);
                                }
                            },
                            error: function (response) {
                                alert(response.error_message);
                            },
                        });

                    }
                });
    }