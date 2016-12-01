    var check_error = 0;
    var row_list = []	
	
	toastr.options = {
        "debug": false,
        "newestOnTop": false,
        "positionClass": "toast-top-center",
        "closeButton": true,
        "debug": false,
        "toastClass": "animated fadeInDown",
    };

    $(function () {
        $('#example1').dataTable({
            "iDisplayLength": 100,
            "dom": 'T<"clear">lfrtip',
            "bPaginate": false,
            tableTools: {
                "sSwfPath": "{% static 'swf/copy_csv_xls_pdf.swf' %}",
                "aButtons": [{
                    "sExtends": "csv",
                    "sButtonText": "Export to CSV",
                    "sFileName": "bulkTrade.csv",
                    "oSelectorOpts": {filter: 'applied', order: 'current'},
                    "mColumns": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                }],
            }
        });
        $(".js-source-states").select2();
        $(".js-source-states-2").select2();
        $('.input-group.date').datepicker({});
    });
    
	var openFile = function (event) {
        row_list = []
        $('#save').attr("disabled", false);
        var table = $('#example1').DataTable();
        $('#save').attr("disabled", false);
        $('#save').addClass("btn-outline");
        var input = event.target;
        var reader = new FileReader();
        table.clear().draw();
        if (!$('#file').hasExtension(['.csv'])) {
            toastr.error('Please upload file in .csv format');
            $("#file").val('');
            return false;
        }
        reader.onload = function (e) {
            var chars = new Uint8Array(e.target.result);
            var CHUNK_SIZE = 0x8000;
            var index = 0;
            var length = chars.length;
            var result = '';
            var slice;
            while (index < length) {
                slice = chars.subarray(index, Math.min(index + CHUNK_SIZE, length));
                result += String.fromCharCode.apply(null, slice);
                index += CHUNK_SIZE;
            }
            var row = result.split("\n");
            if (row.length > 102) {
                toastr.error('Please upload file containing upto 100 rows only !!!');
                $("#file").val('');
                return false;
            }
            $.each(row, function (index, item) {
                if (index == 0) {
                    var cols = item.split(",");
                     if (cols.length != 12){
                         toastr.error('Please upload a valid file with specified columns !!!');
                         $("#file").val('');
                         return false;
                     }
                    date = cols[0].replace(/["*]/g, "");
                    security = cols[1].replace(/["*]/g, "");
                    b_ticker = cols[2].replace(/["*]/g, "");
                    as_cls = cols[3].replace(/["*]/g, "");
                    as_sub_cls = cols[4].replace(/["*]/g, "");
                    td_type = cols[5].replace(/["*]/g, "");
                    quantity = cols[6].replace(/["*]/g, "");
                    td_price = cols[7].replace(/["*]/g, "");
                    fx_price = cols[8].replace(/["*]/g, "");
                    lot_size = cols[9].replace(/["*]/g, "");
                    td_amt = cols[10].replace(/["*]/g, "");
                    broker = cols[11].replace(/["*]/g, "");
                    if (date == "Date" && b_ticker == "Bloomberg Ticker" && security == "Security" && as_cls == "Asset Class" && as_sub_cls == "Asset Sub Class" && td_type == "Trade Type" &&
                            quantity == "Quantity" && td_price == "Trade Price" && fx_price == "FX Price" && lot_size == "Lot Size" && td_amt == "Total Amount" && broker == "Broker") {
                        return true;
                    } else {
                        toastr.error("File headers should be in the following sequence: Date, Security, Bloomberg Ticker, Asset Class, Asset Sub Class, " +
                                "Trade Type, Quantity, Trade Price, FX Price, Lot Size, Total Amount, Broker");
                        return false;
                    }
                } else {
                    if (item == "") {
                        return false;
                    } else {
                        row_status = "";
                        check_error = 0;
                        var cols = item.split(",");
                        date = cols[0].replace(/["]/g, "");
                        security = cols[1].replace(/["]/g, "");
                        b_ticker = cols[2].replace(/["*]/g, "");
                        as_cls = cols[3].replace(/["]/g, "");
                        as_sub_cls = cols[4].replace(/["]/g, "");
                        td_type = cols[5].replace(/["]/g, "");
                        quantity = cols[6].replace(/["]/g, "");
                        trd_price = cols[7].replace(/["]/g, "");
                        fx_price = cols[8].replace(/["]/g, "");
                        lot_size = cols[9].replace(/["]/g, "");
                        td_amt = cols[10].replace(/["]/g, "");
                        broker = cols[11].replace(/["]/g, "");
                        table = $('#example1').DataTable();

                        date = check_date(date, index)
                        security = check_security(security, index)
                        b_ticker = check_security(b_ticker, index)
                        as_cls = check_security(as_cls, index)
                        as_sub_cls = check_security(as_sub_cls, index)
                        td_type = check_td_type(td_type, index)
                        quantity = check_quantity(quantity, index)
                        td_amt = check_number(td_amt, index)
                        lot_size = check_number(lot_size, index)
                        trd_price = check_price_value(trd_price, index)
                        fx_price = check_price_value(fx_price, index)

                        if (check_error == 0)
                            row_status = '<td class="text-center "><span class="label label-success ">Valid Data</span></td>'
                        else
                            row_status = '<td class="text-center "><span class="label label-danger ">Invalid Data</span></td>'

                        table.row.add([
                            date, security, b_ticker, as_cls, as_sub_cls, td_type,
                            quantity, trd_price, fx_price, lot_size, td_amt, broker, row_status
                        ]).draw(false);
                        return true;
                    }
                }
            });
        };
        reader.readAsArrayBuffer(input.files[0]);
    };

    function check_security(security, index) {
        if (security == null || security == "" || !security.trim()) {
            row_list.push(index);
            check_error = 1
            security = '      '
            return '<td class="text-center"><span class="label label-danger ">' + security + '</span></td>';
        }
        else if ($.isNumeric(security.trim())) {
            row_list.push(index);
            check_error = 1
            return '<td class="text-center"><span class="label label-danger ">' + security + '</span></td>';
        }
        else {
            return security
        }
    }

    function check_date(date, index) {
        var pattern = /^([0-9]{2})[\/]([0-9]{2})[\/]([0-9]{4})$/;
        if (date == "") {
            row_list.push(index);
            check_error = 1
            date = '      '
            return '<td class="text-center"><span class="label label-danger ">' + date + '</span></td>';
        }
        else if (!pattern.test(date)) {
            row_list.push(index);
            check_error = 1
            return '<td class="text-center"><span class="label label-danger ">' + date + '</span></td>';
        }
        else {
            var check_date = isFutureDate(date)
            //alert(check_date);
            if (check_date == true){
                return date;
            }
            else{
                row_list.push(index);
                check_error = 1
                return '<td class="text-center"><span class="label label-danger ">' + date + '</span></td>';
            }
        }
    }

    function isFutureDate(dateText) {
        var arrDate = dateText.split("/");
        var today = new Date();
        useDate = new Date(arrDate[2], arrDate[1] - 1, arrDate[0]);
        if (useDate < today) {
            return true;
        } else return false;
    }

    function check_fxprice_value(price, index) {
        if (price == "") {
            return price
        }
        else if (!$.isNumeric(price.trim())) {
            row_list.push(index);
            check_error = 1
            return '<td class="text-center"><span class="label label-danger ">' + price + '</span></td>';
        }
        else {
            return parseFloat(price).toFixed(2);
        }
    }

    function check_price_value(price, index) {
        if (price == "") {
            row_list.push(index);
            check_error = 1
            price = '      '
            return '<td class="text-center"><span class="label label-danger ">' + price + '</span></td>';
        }
        else if (!$.isNumeric(price.trim())) {
            row_list.push(index);
            check_error = 1
            return '<td class="text-center"><span class="label label-danger ">' + price + '</span></td>';
        }
        else {
            return parseFloat(price).toFixed(2);
        }
    }

    function check_td_type(td_type, index) {
        if (td_type == "") {
            row_list.push(index);
            check_error = 1
            td_type = '      '
            return '<td class="text-center"><span class="label label-danger ">' + td_type + '</span></td>';
        }
        else if (td_type != "Buy" && td_type != "Sell" && td_type != "Sell Short" && td_type != "Cover Short") {
            row_list.push(index);
            check_error = 1
            return '<td class="text-center"><span class="label label-danger ">' + td_type + '</span></td>';
        }
        else {
            return td_type;
        }
    }

    function check_quantity(quantity, index) {
        if (quantity == "") {
            row_list.push(index);
            check_error = 1
            quantity = '      '
            return '<td class="text-center"><span class="label label-danger ">' + quantity + '</span></td>';
        }
        else if (!$.isNumeric(quantity.trim()) || quantity % 1 !== 0) {
            row_list.push(index);
            check_error = 1
            return '<td class="text-center"><span class="label label-danger ">' + quantity + '</span></td>';
        }
        else {
            return quantity;
        }
    }

    function check_number(quantity, index) {
        if (!$.isNumeric(quantity.trim()) || quantity % 1 !== 0) {
            row_list.push(index);
            check_error = 1
            return '<td class="text-center"><span class="label label-danger ">' + quantity + '</span></td>';
        }
        else {
            return quantity;
        }
    }


    function remove_duplicates(arr) {
        var obj = {};
        var arr2 = [];
        for (var i = 0; i < arr.length; i++) {
            if (!(arr[i] in obj)) {
                arr2.push(arr[i]);
                obj[arr[i]] = true;
            }
        }
        return arr2;
    }
    
    function save_trade() {
        var table = $('#example1').tableToJSON();
        var tot_data = (JSON.stringify(table));
        $('#totalData').val(tot_data);
        if (row_list != "") {
            err_row = remove_duplicates(row_list);
            $("#file").val('');
            toastr.error("Please check row number: " + err_row + " and upload file again !!!");
            return false;
        }
        $.ajax({
            type: 'POST',
            url: '/add-bulk-trade/',
            data: {
                'totalData': $('#totalData').val()
            },
            success: function (response) {
                if (response.success == 'true') {
                    $("#file").val('');
                    toastr.success('Data is saved successfully');
                    var table = $('#example1').DataTable();
                    table
                            .clear()
                            .draw();
                    $('#save').attr("disabled", true);
                    //location.href="/open-trade/";
                } else if (response.success == 'false') {
                    $("#file").val('');
                    var table = $('#example1').DataTable();
                    $('#save').attr("disabled", true);
                    table
                            .clear()
                            .draw();
                    $.each(response.data_list, function (index, item) {
                        table = $('#example1').DataTable();
                        table.row.add([
                            item.date,
                            item.security,
                            item.b_ticker,
                            item.as_cls,
                            item.as_sub_cls,
                            item.trade_type,
                            item.quantity,
                            item.trade_price,
                            item.fx_price,
                            item.lot_size,
                            item.total_amount,
                            item.broker,
                            item.status,
                        ]).draw(false);
                    });
                }

            },

        });
        return true;
    }