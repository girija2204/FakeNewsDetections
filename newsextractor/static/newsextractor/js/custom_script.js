console.log('Hey this is girija')

$(document).on('change','#id_job_types',function() {
    if($("#id_job_types option:selected").text()=='DAILY_TRAINING'){
      $('#tempId').show();
//        $('#tempId').css('display', 'inline-flex');
    }else{
      $('#tempId').hide();
    }
});

$('#nav-minutes-tab').on('click',function(){
    $('.hour_choices').val('--');
    $('.hour_start_choices').val('--');
    $('.minute_start_choices').val('--');
});
$('#nav-hour-tab').on('click',function(){
    $('.minutes_choices').val('--');
    $('.hour_start_choices').val('--');
    $('.minute_start_choices').val('--');
});
$('#nav-daily-tab').on('click',function(){
    $('.hour_choices').val('--');
    $('.minutes_choices').val('--');
});
$(document).ready(function() {
    $('.select').materialSelect();
});