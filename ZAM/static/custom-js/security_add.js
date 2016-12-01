$(function () {
        $(".js-source-states").select2();

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
    });


    $("#btn_save").click(function () {

      if ($('#txtLotSize').val() === "" || $('#txtLotSize').val() === null) {
            $('#lbl_lotsize').css("color", "red");
        } else {
            $('#lbl_lotsize').css("color", "#6A6C6F");
        }

        if ($('#txtSecurity').val() === "" || $('#txtSecurity').val() === null) {
            $('#lbl_name').css("color", "red");
        } else {
            $('#lbl_name').css("color", "#6A6C6F");
        }


        if ($('#selectAssetClass').val() === "" || $('#selectAssetClass').val() == null) {
            $('#lbl_asset').css("color", "red");
        } else {
            $('#lbl_asset').css("color", "#6A6C6F");
        }

        if ($('#selectAssetSubClass').val() === "" || $('#selectAssetSubClass').val() == null) {
            $('#lbl_sub').css("color", "red");
        } else {
            $('#lbl_sub').css("color", "#6A6C6F");
        }


         if ($('#selectSector').val() === "" || $('#selectSector').val() == null) {
            $('#lbl_sector').css("color", "red");
        } else {
            $('#lbl_sector').css("color", "#6A6C6F");
        }

        if ($('#selectType').val() === "" || $('#selectType').val() == null) {
            $('#lbl_type').css("color", "red");
        } else {
            $('#lbl_type').css("color", "#6A6C6F");
        }


        if ($('#selectBenchmarkIndex').val() === "" || $('#selectBenchmarkIndex').val() === null) {
            $('#lbl_bi').css("color", "red");
        } else {
            $('#lbl_bi').css("color", "#6A6C6F");
        }

        if ($('#txtbloombergticker').val() === "" || $('#txtbloombergticker').val() === null) {
            $('#lbl_bt').css("color", "red");
        } else {
            $('#lbl_bt').css("color", "#6A6C6F");
        }


        if ($('#selectCountry').val() === "" || $('#selectCountry').val() == null) {
            $('#lbl_cntry').css("color", "red");
        } else {
            $('#lbl_cntry').css("color", "#6A6C6F");
        }

        if ($('#selectCurrency').val() === "" || $('#selectCurrency').val() === null) {
            $('#lbl_curr').css("color", "red");
        } else {
            $('#lbl_curr').css("color", "#6A6C6F");
        }

        if ($('#selectSecurityState').val() == "" || $('#selectSecurityState').val() === null) {
            $('#lbl_selectSecurityState').css("color", "red");
        } else {
            $('#lbl_selectSecurityState').css("color", "#6A6C6F");
        }


        var beta = $('#txtBeta').val();
        if (beta < 0) {
        		$('#lbl_beta').html('&nbsp Should be greater than -1');
        		$('#lbl_beta').css("color", "red");
        		return false;
        }
        else if (beta > 10) {
				$('#lbl_beta').html('&nbsp Should be less than 10');
        		$('#lbl_beta').css("color", "red");
        		return false;
        }
        else{
            $('#lbl_beta').html('&nbsp ');
            $('#lbl_beta').css("color", "white");
        }

     /*   if (beta == "" || beta == null) {
            $('#txtBeta').val(0)
        }*/


        if ($('#txtSecurity').val() === "" || $('#selectAssetClass').val() === "" ||
                $('#selectAssetSubClass').val() === "" || $('#selectType').val() === "" ||
                $('#selectBenchmarkIndex').val() === "" || $('#selectCountry').val() === "" === "" || $('#txtbloombergticker').val() === "" ||
                $('#selectCurrency').val() === "" || $('#txtSecurity').val() === null || $('#selectAssetClass').val() === null ||
                $('#selectAssetSubClass').val() === null || $('#selectType').val() === null || $('#txtbloombergticker').val() === null ||
                $('#selectBenchmarkIndex').val() === null || $('#selectCountry').val() === null === null ||
                $('#selectCurrency').val() === null || $('#selectSecurityState').val() == "" || $('#selectSecurityState').val() === null ||
                $('#selectSector').val() === "" || $('#selectSector').val() == null ||$('#txtLotSize').val() === "" || $('#txtLotSize').val() === null

        ) {
            return false;
        }

        $.ajax({
            type: "POST",
            url: '/save-security-details/',
            data: $('#security_form').serialize(),
            success: function (response) {
                if (response.success == "true")
                    location.href = "/open-security-page/"
                else if(response.success == "ticker_available")
                    $('#lbl_error_ticker').css('color','red');
                    $('#lbl_error_ticker').css('visibility','visible');
            },
            error: function (response) {
                alert('cant save');
                location.href = "/open-security-page/"
                console.log(response);
            },
            beforeSend: function () {
                $("#load").show();
            },
            	error : function(response){
                console.log(response);
                alert('error');
                $("#load").hide();
            },
            		complete: function () {
                $("#load").hide();
            }

        });
    });


    $("#selectAssetClass").change(function () {
        add_relevent_value('/add-subassetclass-security/', "#selectAssetSubClass", $('#selectAssetClass :selected').val());
    });

    $("#selectCountry").change(function () {
        select_relevent_currency('/add-currency-security/', "#selectCurrency", $('#selectCountry :selected').val());
    });

    function add_relevent_value(url, dropdown, id) {
        $(dropdown).empty();
        $(dropdown).text('');
        $.ajax({
            type: "GET",
            url: url,
            data: {'id': id},
            success: function (response) {
                if (response.success == "true") {
                    $.each(response.result, function (index, item) {
                        $(dropdown).append('<option value="' + item.id + '">' + item.name + '</option>');
                    });
                    var i = $(dropdown).first().val()
                    $(dropdown).select2().select2("val", i);
                }
            },
            error: function (response) {
                console.log(response);
            },
        });
    }

    function select_relevent_currency(url, dropdown, id) {
        $.ajax({
            type: "GET",
            url: url,
            data: {'id': id},
            success: function (response) {
                if (response.success == "true") {
                    $.each(response.result, function (index, item) {
                    		$(dropdown).select2().select2("val", item.id );
                    });
                }
            },
            error: function (response) {
                console.log(response);
            },
        });
    }

    //------------------------------validation for float field for Client IP-------------------//

     function isNumberKey(evt) {
        var charCode = (evt.which) ? evt.which : event.keyCode
        if (charCode > 31 && (charCode < 48 || charCode > 57 || charCode == 43 || charCode == 45 ))
            return false;
        return true;
    }

    function validateFloatKeyPress(el, evt) {
        var charCode = (evt.which) ? evt.which : event.keyCode;
        var number = el.value.split('.');
        if (charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) {
            return false;
        }
        //just one dot
        if (number.length > 1 && charCode == 46) {
            return false;
        }
        //get the carat position
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


    function getSelectionStart(o) {
        if (o.createTextRange) {
            var r = document.selection.createRange().duplicate()
            r.moveEnd('character', o.value.length)
            if (r.text == '') return o.value.length
            return o.value.lastIndexOf(r.text)
        } else return o.selectionStart
    }
    //-----------------------------------end-------------------------//