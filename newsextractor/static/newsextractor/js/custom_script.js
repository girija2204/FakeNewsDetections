console.log('Hey this is girija')

$(document).on('change','#id_job_types',function() {
    if($("#id_job_types option:selected").text()=='DAILY_TRAINING'){
      $('#tempId').show();
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

$('.fake_real').on('click',function(){
    console.log($(this).text());
    if($(this).text() == 'All Articles'){
        $("#news_articles .article .fake_status").filter(function() {
            $(this).parent().parent().show();
            $('#all').addClass('active');
            $('#fake').removeClass('active');
            $('#real').removeClass('active');
        })
    }
    if($(this).text() == 'Real Articles'){
        var value = "true"
        $("#news_articles .article .fake_status").filter(function() {
            $(this).parent().parent().toggle($(this).text().toLowerCase().indexOf(value) > -1);
            $('#all').removeClass('active');
            $('#fake').removeClass('active');
            $('#real').addClass('active');
        })
    }
    if($(this).text() == 'Fake Articles'){
        var value = "false"
        $("#news_articles .article .fake_status").filter(function() {
            $(this).parent().parent().toggle($(this).text().toLowerCase().indexOf(value) > -1);
            $('#all').removeClass('active');
            $('#fake').addClass('active');
            $('#real').removeClass('active');
        })
    }
});