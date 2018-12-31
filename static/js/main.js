

$("#gender").on('input propertychange paste', function() {
    value = $(this).val();
    value = value.slice(0,1).toUpperCase();
    if (value == 'M' || value == 'F'){
        $(this).val(value);
    }
    else{
        $(this).val('');
    }
});

$("#first_name").on('input propertychange paste', function() {
    value = $(this).val();
    $(this).val(value.slice(0,45));
});

$("#last_name").on('input propertychange paste', function() {
    value = $(this).val();
    $(this).val(value.slice(0,45));
});

$("#email_name").on('input propertychange paste', function() {
    value = $(this).val();
    $(this).val(value.slice(0,45));
});

$("tr").click(function(){
  window.location = "#";
});
