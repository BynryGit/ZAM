$(function () {
    $('#analysis_log_tbl').dataTable({
        "dom": 'T<"clear">lfrtip',
        tableTools: {
            "sSwfPath": "{% static 'swf/copy_csv_xls_pdf.swf' %}",
            "aButtons": [{
                "sExtends": "xls",
                "sButtonText": "Export to Excel",
                "oSelectorOpts": {filter: 'applied', order: 'current'},
            }],
        },
        "ajax": '/get-securityanalysis-list/?security_id=' + $('#txtSecurity_id').val(),
        "columns": [
            {"data": "date"},
            {"data": "view"},
            {"data": "desc"},
            {"data": "readmore"},
        ],
        "columnDefs": [{"targets": 3, "orderable": false}],
    });

    /* $("#security_form input").prop("disabled", true);
     $("#security_form select").prop("disabled", true);  */

    $(".js-source-states").select2();
    $(".js-source-states-2").select2();
    $.fn.datepicker.defaults.format = "dd/mm/yyyy";

    $('.input-group.date').datepicker({}).on('changeDate', function (e) {
        $(this).datepicker('hide');
        $(this).datepicker({maxDate: 0});

    });

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


$("#edit_button").click(function () {
    // alert(check_edit_flag);
    //if (check_edit_flag == 0 && $('#check_lag').val()=="view") {
    if (check_edit_flag == 0) {
        check_edit_flag = 1;
        //alert('vkm');
        $("#security_form input").prop("disabled", false);
        $("#security_form select").prop("disabled", false);
        $('#edit_button').text('Save');
        //$('#edit_button').attr('id', 'save_button');
    }
    else {
        //alert('vkm else');
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
        else {
            $('#lbl_beta').html('&nbsp ');
            $('#lbl_beta').css("color", "white");
        }

        if ($('#txtSecurity').val() === "" || $('#selectAssetClass').val() === "" ||
            $('#selectAssetSubClass').val() === "" || $('#selectType').val() === "" ||
            $('#selectBenchmarkIndex').val() === "" || $('#selectCountry').val() === "" === "" || $('#txtbloombergticker').val() === "" ||
            $('#selectCurrency').val() === "" || $('#txtSecurity').val() === null || $('#selectAssetClass').val() === null ||
            $('#selectAssetSubClass').val() === null || $('#selectType').val() === null || $('#txtbloombergticker').val() === null ||
            $('#selectBenchmarkIndex').val() === null || $('#selectCountry').val() === null === null ||
            $('#selectCurrency').val() === null || $('#selectSecurityState').val() == "" || $('#selectSecurityState').val() === null || $('#txtLotSize').val() === "" || $('#txtLotSize').val() === null

        ) {
            return false;
        }

        if ($('#txtCouponRate').val() == "" || $('#txtCouponRate').val() == null)
            $('#txtCouponRate').val(0)

        if ($('#txtBeta').val() == "" || $('#txtBeta').val() == null)
            $('#txtBeta').val(0)

        $.ajax({
            type: 'POST',
            url: '/update-security-details/',
            data: $('#security_form').serialize(),
            success: function (response) {
                if (response.success == "true")
                    location.href = "/open-security-page/"
                else if (response.success == "ticker_available")
                    $('#lbl_error_ticker').css('color', 'red');
                $('#lbl_error_ticker').css('visibility', 'visible');
            },
            error: function (response) {
                alert('cant save');
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
    }
});

/*-----------------------------save modal data----------------------------------*/

$('#btn_save').click(function () {
    if ($('#select_view').val() == "" || $('#select_view').val() == null) {
        $('#lbl_select_view').css("color", "red");
        $('#lbl_select_view').html('&nbsp Please Select')
    } else {
        $('#lbl_select_view').css("color", "white");
    }

    if ($('#analysis_date').val() == "" || $('#select_view').val() == null) {
        $('#lbl_analysis_date').css("color", "red");
        $('#lbl_analysis_date').html('&nbsp Please Select')
    } else {
        $('#lbl_analysis_date').css("color", "white");
    }

    if ($('#area_desc').val() == "" || $('#area_desc').val() == null) {
        $('#lbl_area_desc').css("color", "red");
        $('#lbl_area_desc').html('&nbsp Please fill out')
    } else {
        $('#lbl_area_desc').css("color", "white");
    }
    if ($('#select_view').val() == "" || $('#select_view').val() == null || $('#analysis_date').val() == "" || $('#select_view').val() == null || $('#area_desc').val() == "" || $('#area_desc').val() == null)
        return false;

    $.ajax({
        type: 'GET',
        url: '/save-analysis/',
        data: $('#analysis_frm').serialize(),
        success: function (response) {
            console.log(response);
            if (response.success === 'true') {
                var table = $('#analysis_log_tbl').DataTable();
                table.clear().draw();
                $('#add_analysis_modal').modal('hide');
                $.each(response.data, function (index, item) {
                    table.row.add([
                        "A", "B", "C", "D", "E"
                    ]).draw(false);
                });

            } else {
                alert('ERRORS ' + response.error_message);
            }
        },
        error: function (response) {
            alert(response.error_message);
        },

    });

});

//==================================================================================
$("#add_analysis").click(function () {
            $('#add_analysis_modal').modal('show');
        });


    $("#selectAssetClass").change(function () {
        add_relevent_value('/add-subassetclass-security/', "#selectAssetSubClass", $('#selectAssetClass :selected').val());
    });

    $("#selectCountry").change(function () {
        select_relevent_currency('/add-currency-security/', "#selectCurrency", $('#selectCountry :selected').val());
    });

    function add_relevent_value(url, dropdown, id) {
        $(dropdown).empty();
        $(dropdown).select2("val", "");
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
    function isNumberKey(evt) {
        var charCode = (evt.which) ? evt.which : event.keyCode
        if (charCode > 31 && (charCode < 48 || charCode > 57 || charCode == 43 || charCode == 45 ))
            return false;
        return true;
    }