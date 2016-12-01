 function company_validation(){

            if ($('#company_name').val() === "") {
                $('#lbl_cname').css("color", "red");
            } else {
                $('#lbl_cname').css("color", "#6a6c6f");
            }


            if ($('#txt_country_name option:selected').val() === "") {
                $('#lbl_cntry').css("color", "red");
            } else {
                $('#lbl_cntry').css("color", "#6a6c6f");
            }            
            
				if ($("#txt_currency_name :selected").val() === "") {
                $('#lbl_currency').css("color", "red");
            } else {
                $('#lbl_currency').css("color", "#6a6c6f");
            }            
            
            if ($('#txt_bloomberg_ticker').val() === "") {
                $('#lbl_bt').css("color", "red");
            } else {
                $('#lbl_bt').css("color", "#6a6c6f");
            }
            
       /*     if ($('#txt_source').val() === "") {
                $('#lbl_sour').css("color", "red");
            } else {
                $('#lbl_sour').css("color", "white");
            }  */

           if ($('#txt_mkt_cap').val() === ""||$('#txt_mkt_cap').val()==null) {
                $('#lbl_cap').css("color", "red");
            } 
            else{
                $('#lbl_cap').css("color", "#6a6c6f");
            }
            
            if ($('#txt_daily_turnover').val() === ""||$('#txt_daily_turnover').val()==null) {
                $('#lbl_dat').css("color", "red");
            } 
            else{
                $('#lbl_dat').css("color", "#6a6c6f");
            }
            
            if ($('#txt_cmp').val() === ""||$('#txt_cmp').val()==null) {
                $('#lbl_cmp').css("color", "red");
            } 
            else{
                $('#lbl_cmp').css("color", "#6a6c6f");
            }


            if ($('#company_name').val() === "" || $('#txt_country_name').val() === ""
                     || $('#txt_bloomberg_ticker').val() === "" ||
                  //  	$('#txt_source').val() === "" ||
                     $('#txt_mkt_cap').val() === "" ||
                    $('#txt_daily_turnover').val() === ""|| $('#txt_cmp').val() === ""  ) {
                return false;
            }

           
     return true;
        }
        
        
         function portfolio_company_validation(){

            if ($('#txt_company_name').val() === "") {
                $('#lbl_cname').css("color", "red");
            } else {
                $('#lbl_cname').css("color", "#6a6c6f");
            }


            if ($('#txt_country_name option:selected').val() === "") {
                $('#lbl_cntry').css("color", "red");
            } else {
                $('#lbl_cntry').css("color", "#6a6c6f");
            }
            
				if ($("#txt_currency_name :selected").val() === "") {
                $('#lbl_currency').css("color", "red");
            } else {
                $('#lbl_currency').css("color", "#6a6c6f");
            }             
            
            if ($('#txt_bloomberg_ticker').val() === "") {
                $('#lbl_bt').css("color", "red");
            } else {
                $('#lbl_bt').css("color", "#6a6c6f");
            }
            
            if ($('#txt_vt_price').val() === "" || $('#txt_vt_price').val()==null ) {
                $('#lbl_vt').css("color", "red");
            } else {
                $('#lbl_vt').css("color", "#6a6c6f");
            }


            if ($('#txt_cmp').val() === ""||$('#txt_cmp').val()==null) {
                $('#lbl_cmp').css("color", "red");
            } 
            else{
                $('#lbl_cmp').css("color", "#6a6c6f");
            }
            
            if ($('#txt_updn').val() === ""||$('#txt_updn').val()==null) {
                $('#lbl_ud').css("color", "red");
            } 
            else{
                $('#lbl_ud').css("color", "#6a6c6f");
            }
            
            if ($('#model_file').val() == "") {
            $('#lbl_mod').css("color", "red");
            }
            else{
                $('#lbl_mod').css("color", "#6a6c6f");
            }

            if ($('#invst_file').val() == "") {
            $('#lbl_inv').css("color", "red");
            }
            else{
                $('#lbl_inv').css("color", "#6a6c6f");
            }


            if ($('#txt_company_name').val() === "" || $('#txt_country_name').val() === ""
                     || $('#txt_bloomberg_ticker').val() === "" ||
                    $('#txt_vt_price').val() === "" || $('#txt_cmp').val() === "" ||
                    $('#model_file').val() == "" || $('#invst_file').val() == "" ||
                    $('#txt_updn').val() === ""   ) {
                return false;
            }

           
     return true;
        }


  function portfolio_edit_company_validation(){

            if ($('#txt_company_name').val() === "") {
                $('#lbl_cname').css("color", "red");
            } else {
                $('#lbl_cname').css("color", "#6a6c6f");
            }


            if ($('#txt_country_name option:selected').val() === "") {
                $('#lbl_cntry').css("color", "red");
            } else {
                $('#lbl_cntry').css("color", "#6a6c6f");
            }
            
            if ($("#txt_currency_name :selected").val() === "") {
                $('#lbl_currency').css("color", "red");
            } else {
                $('#lbl_currency').css("color", "#6a6c6f");
            } 

            if ($('#txt_bloomberg_ticker').val() === "") {
                $('#lbl_bt').css("color", "red");
            } else {
                $('#lbl_bt').css("color", "#6a6c6f");
            }

            if ($('#txt_vt_price').val() === "" || $('#txt_vt_price').val()==null ) {
                $('#lbl_vt').css("color", "red");
            } else {
                $('#lbl_vt').css("color", "#6a6c6f");
            }


            if ($('#txt_cmp').val() === ""||$('#txt_cmp').val()==null) {
                $('#lbl_cmp').css("color", "red");
            }
            else{
                $('#lbl_cmp').css("color", "#6a6c6f");
            }

            if ($('#txt_updn').val() === ""||$('#txt_updn').val()==null) {
                $('#lbl_ud').css("color", "red");
            }
            else{
                $('#lbl_ud').css("color", "#6a6c6f");
            }




            if ($('#txt_company_name').val() === "" || $('#txt_country_name').val() === ""
                     || $('#txt_bloomberg_ticker').val() === "" ||
                    $('#txt_vt_price').val() === "" || $('#txt_cmp').val() === "" ||
                    $('#txt_updn').val() === ""   ) {
                return false;
            }


     return true;
        }
        
        

        
         /*---------------------------------------Add Communication-------------------------------*/

       function add_log(){

            if ($('#cdate').val() === "") {
                $('#lbl_cdate').css("color", "red");
            }else{
                $('#lbl_cdate').css("color", "#6a6c6f");
            } 


            if ( $('#cdate').val() === "" 
                     
            ) {
				
                return false;
            }
            

					return true;
        }
        
        function add_active_log(){

            if ($('#ac_cdate').val() === "") {
                $('#ac_lbl_cdate').css("color", "red");
            }else{
                $('#ac_lbl_cdate').css("color", "#6a6c6f");
            } 



            if ( $('#ac_cdate').val() === "" 
            ) {

                return false;
            }

					return true;
        }
         
         function add_port_log(){

            if ($('#port_cdate').val() === "") {
                $('#port_lbl_cdate').css("color", "red");
            }else{
                $('#port_lbl_cdate').css("color", "#6a6c6f");
            }  


            if ( $('#port_cdate').val() === "" 
            ) {

                return false;
            }

					return true;
        }
        
        /*--------------FOR ADD NEW LOG---------------*/
			
				$("#addDiv1").hide();
    			$("#addDiv2").hide();
    
    			$('#add_select_contact_type').on('change', function() {
      		if ( $('#add_select_contact_type option:selected').text() == "Management")
     			 {  
        			$("#addDiv1").show();

      		}else{
					$("#addDiv1").hide();      
      		}
      		if ( $('#add_select_contact_type option:selected').text() == "Analyst")
      		{  
        			$("#addDiv2").show();
      		}else{
					$("#addDiv2").hide();      
      		}
    		});
		
        
        /*------------END----------------------------*/

			/* For Add log in Focus to show the div  */        
        
           	$("#fanalyst").hide();
    			$("#fcompany_personnel").hide();
    
    			$('#select_contact_type').on('change', function() {
      		if ( $('#select_contact_type option:selected').text() == "Management")
     			 {  
        			$("#fcompany_personnel").show();

      		}else{
					$("#fcompany_personnel").hide();      
      		}
      		if ( $('#select_contact_type option:selected').text() == "Analyst")
      		{  
        			$("#fanalyst").show();
      		}else{
					$("#fanalyst").hide();      
      		}
    		}); 
    		
    		
    		/* For Add log in Active to show the div  */        
        
           	$("#aanalyst").hide();
    			$("#acompany_personnel").hide();
    
    			$('#ac_select_contact_type').on('change', function() {
      		if ( $('#ac_select_contact_type option:selected').text() == "Management")
     			 {  
        			$("#acompany_personnel").show();

      		}else{
					$("#acompany_personnel").hide();      
      		}
      		if ( $('#ac_select_contact_type option:selected').text() == "Analyst")
      		{  
        			$("#aanalyst").show();
      		}else{
					$("#aanalyst").hide();      
      		}
    		}); 
    		
    		
    		/* For Add log in Portfolio to show the div  */        
        
           	$("#panalyst").hide();
    			$("#pcompany_personnel").hide();
    
    			$('#port_select_contact_type').on('change', function() {
      		if ( $('#port_select_contact_type option:selected').text() == "Management")
     			 {  
        			$("#pcompany_personnel").show();

      		}else{
					$("#pcompany_personnel").hide();      
      		}
      		if ( $('#port_select_contact_type option:selected').text() == "Analyst")
      		{  
        			$("#panalyst").show();
      		}else{
					$("#panalyst").hide();      
      		}
    		});    
    		
